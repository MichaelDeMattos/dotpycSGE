#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class ModelsApartamento(object):
    def __init__(self, *args, **kwargs):
        super(ModelsApartamento, self).__init__(*args, **kwargs)
    
    
    def novo_apartamento(self, cursor, conexao, bloco, andar, numero,
                         cod_usuario):
        sql_novo_apartamento = (" insert into apartamento"
                                " (bloco, andar, numero,"
                                " cod_usuario_registro)"
                                " values (?,?,?,?)")
        
        sql_args = ([bloco, andar, numero, cod_usuario])
        cursor.execute(sql_novo_apartamento, sql_args)
        conexao.commit()
    
    def buscar_apartamento(self, cursor, campo, filtro):
        if campo != "NUMERO":
            sql_query = (" select ap.cod_apartamento,"
                         " ap.bloco,"
                         " ap.andar," 
                         " ap.numero"
                         " from apartamento ap"
                         " where ap.{} = '{}'".format(campo, filtro))
            print(sql_query)
            cursor.execute(sql_query)
            return cursor.fetchall()
            
        else:
            sql_query = (" select ap.cod_apartamento,"
                         " ap.bloco,"
                         " ap.andar," 
                         " ap.numero"
                         " from apartamento ap"
                         " where ap.{} in ({})".format(campo, 1 if filtro == "" else filtro))
            print(sql_query)
            cursor.execute(sql_query)
            return cursor.fetchall()
    
    def excluir_apartamento(self, cursor, conexao, cod_apartamento):
        sql_query = (" delete from apartamento"
                     " where cod_apartamento = ?")
        
        sql_args = ([cod_apartamento])
        cursor.execute(sql_query, sql_args)
        conexao.commit()
    
    def busca_entidade(self, cursor, campo, filtro, cod_apartamento):
        sql_busca_entidade = (" select ent.cod_entidade,"
                              " ent.nome,"
                              " ent.sobrenome,"
                              " ent.rg,"
                              " ent.celular,"
                              " ent.email,"
                              " ent.tipo_morador"
                              " from entidade ent"
                              " where ent.{} like '%{}%'"
                              " and ent.cod_entidade"
                              " not in (select ende.cod_entidade"
                              "         from endereco ende"
                              "         where ende.cod_apartamento = {})".format(campo, filtro, cod_apartamento))
        
        print(sql_busca_entidade)
        cursor.execute(sql_busca_entidade)
        return cursor.fetchall()
    
    def busca_entidade_apartamento_ativa(self, cursor, cod_apartamento):
        sql_query = (" select ende.cod_endereco,"
                     " ende.cod_entidade,"
                     " ent.nome,"
                     " ent.celular,"
                     " ent.rg"
                     " from endereco ende"
                     " join entidade ent"
                     " on ent.cod_entidade = ende.cod_entidade"
                     " where ende.cod_apartamento = {}"
                     " and status = 'A'".format(cod_apartamento))
        
        cursor.execute(sql_query)
        return cursor.fetchall()
    
    def busca_entidade_apartamento_inativo(self, cursor, cod_apartamento):
        sql_query = (" select ende.cod_endereco,"
                     " ende.cod_entidade,"
                     " ent.nome,"
                     " ent.celular,"
                     " ent.rg"
                     " from endereco ende"
                     " join entidade ent"
                     " on ent.cod_entidade = ende.cod_entidade"
                     " where ende.cod_apartamento = {}"
                     " and status = 'I'".format(cod_apartamento))
        
        cursor.execute(sql_query)
        return cursor.fetchall()
        
    def vincular_entidade_apartamento(self, cursor, conexao, cod_entidade, cod_apartamento, cod_usuario_registro):
        sql_query = (" insert into endereco"
                     " (cod_entidade,"
                     " cod_apartamento,"
                     " cod_usuario_registro)"
                     " values (?,?,?)")
        
        sql_args = ([cod_entidade, cod_apartamento, cod_usuario_registro])
        cursor.execute(sql_query, sql_args)
        conexao.commit()
    
    def deletar_vinculo_endereco(self, cursor, conexao, cod_endereco):
        for i in cod_endereco:
            sql_query = (" delete from endereco"
                         " where cod_endereco = ?")
        
            sql_args = ([i])
            cursor.execute(sql_query, sql_args)
            conexao.commit()
    
    def inativar_entidade(self, cursor, conexao, cod_entidade, cod_usuario_registro):
        for i in cod_entidade:
            sqlquery = (" update entidade set status = ?,"
                        " cod_usuario_registro = ?"
                        " where cod_entidade = ?")
        
            sqlargs = (['I', cod_usuario_registro, i])
            cursor.execute(sqlquery, sqlargs)
            conexao.commit()
            
    def ativar_entidade(self, cursor, conexao, cod_entidade, cod_usuario_registro):
        for i in cod_entidade:
            sqlquery = (" update entidade set status = ?,"
                        " cod_usuario_registro = ?"
                        " where cod_entidade = ?")
        
            sqlargs = (['A', cod_usuario_registro, i])
            cursor.execute(sqlquery, sqlargs)
            conexao.commit()
