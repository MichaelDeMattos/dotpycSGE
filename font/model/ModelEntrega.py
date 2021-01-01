#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class ModelsEntrega(object):
    def __init__(self, *args, **kwargs):
        super(ModelsEntrega, self).__init__(*args, **kwargs)
    
    def buscar_apartamento(self, cursor, campo, filtro):
        if campo != "NUMERO":
            sql_query = (" select ap.cod_apartamento,"
                         " ap.bloco,"
                         " ap.andar," 
                         " ap.numero"
                         " from apartamento ap"
                         " where ap.{} = '{}'".format(campo, filtro))
                         
            cursor.execute(sql_query)
            return cursor.fetchall()
    
    def busca_entidade_apartamento(self, cursor, cod_apartamento):
        sql_query = (" select ende.cod_endereco,"
                     " ende.cod_entidade,"
                     " ent.nome,"
                     " ent.celular,"
                     " ent.rg,"
                     " ent.email"
                     " from endereco ende"
                     " join entidade ent"
                     " on ent.cod_entidade = ende.cod_entidade"
                     " where ende.cod_apartamento = {}"
                     " and status = 'A'".format(cod_apartamento))
        
        cursor.execute(sql_query)
        return cursor.fetchall()
    
    def salvar_entrega(self, cursor, conexao, cod_ap, cod_ent, remetente,
                     entregador, prazo_retirada, obs, cod_usuario):
            sql_query = (" insert into entrega"
                         " (cod_apartamento,"
                         " cod_entidade,"
                         " remetente,"
                         " entregador,"
                         " prazo_retirada,"
                         " obs,"
                         " cod_usuario_registro)"
                         " values (?,?,?,?,?,?,?)")
            
            sql_args = ([cod_ap, cod_ent, remetente, entregador,
                       prazo_retirada, obs, cod_usuario])
            
            cursor.execute(sql_query, sql_args)
            conexao.commit()

    def buscar_entrega(self, cursor, campo, filtro):
        sql_query =  (" select ap.cod_apartamento,"
                      " ap.bloco,"
                      " ap.andar,"
                      " ap.numero,"
                      " e.cod_entidade,"
                      " e.nome,"
                      " e.sobrenome,"
                      " e.rg,"
                      " ent.cod_entrega,"
                      " ent.status,"
                      " ent.entregador,"
                      " ent.remetente,"
                      " ent.data_registro,"
                      " ent.obs,"
                      " e.email"
                      " from apartamento ap"
                      " join entrega ent"
                      " on ap.cod_apartamento = ent.cod_apartamento"
                      " join entidade e"
                      " on e.cod_entidade = ent.cod_entidade"
                      " where e.{} like '%{}%'"
                      " and ent.status = 'A'".format(campo, filtro))
        
        cursor.execute(sql_query)
        return cursor.fetchall()
    
    def buscar_entrega_finalizada(self, cursor, campo, filtro):
        sql_query =  (" select ap.cod_apartamento,"
                      " ap.bloco,"
                      " ap.andar,"
                      " ap.numero,"
                      " e.cod_entidade,"
                      " e.nome,"
                      " e.sobrenome,"
                      " e.rg,"
                      " ent.cod_entrega,"
                      " ent.status,"
                      " ent.entregador,"
                      " ent.remetente,"
                      " ent.data_registro,"
                      " ent.obs,"
                      " e.email,"
                      " l.usuario"
                      " from apartamento ap"
                      " join entrega ent"
                      " on ap.cod_apartamento = ent.cod_apartamento"
                      " join entidade e"
                      " on e.cod_entidade = ent.cod_entidade"
                      " join login l"
                      " on l.cod_login = e.cod_usuario_registro"
                      " where e.{} like '%{}%'"
                      " and ent.status not in ('A')".format(campo, filtro))
        
        cursor.execute(sql_query)
        return cursor.fetchall()
    
    def encerrar_entrega(self, cursor, conexao, cod_entrega, status,
                          obs_final, cod_usuario_final):
        
        sql_query = (" update entrega"
                     " set status = ?,"
                     " data_final = current_timestamp,"
                     " obs_final = ?,"
                     " cod_usuario_final = ?"
                     " where cod_entrega = ?")
        sql_args = ([status, obs_final, cod_usuario_final, cod_entrega])
        
        cursor.execute(sql_query, sql_args)
        conexao.commit()
        
        
