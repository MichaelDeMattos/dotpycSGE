#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class ModelsEntidade(object):
    def __init__(self, *args, **kwargs):
        super(ModelsEntidade, self).__init__(*args, **kwargs)
    
    def nova_entidade(self, cursor, conexao, nome, sobrenome, rg,
                      celular, email, tipo_morador, cod_usuario):
    
        sql_nova_entidade = (" insert into entidade"
                             " (nome, sobrenome, rg, celular,"
                             "  email, tipo_morador, cod_usuario_registro)"
                             " values (?,?,?,?,?,?,?)")
        sql_args = ([nome, sobrenome, rg, celular, email,
                     tipo_morador, cod_usuario])
        cursor.execute(sql_nova_entidade, sql_args)
        conexao.commit()               
    
    def busca_entidade(self, cursor, campo, filtro, status='A'):
        sql_busca_entidade = (" select cod_entidade,"
                              " nome, sobrenome, rg,"
                              " celular, email, tipo_morador"
                              " from entidade"
                              " where {} like"
                              " '%{}%' and status in ('{}')".format(campo, filtro, status))
        
        cursor.execute(sql_busca_entidade)
        return cursor.fetchall()
        
    
    def busca_entidade_codigo(self, cursor, cod_entidade):
        sql_busca_entidade_codigo = (" select nome, sobrenome,"
                                     " rg, celular, email,"
                                     " tipo_morador"
                                     " from entidade"
                                     " where cod_entidade = ?")
        sql_args = ([cod_entidade])
        cursor.execute(sql_busca_entidade_codigo, sql_args)
        return cursor.fetchall()
                                        
    
    def deletar_entidade(self, cursor, conexao, cod_entidade):
        sql_deletar_entidade = (" delete from entidade"
                                " where cod_entidade = ?")
        sql_args = ([cod_entidade])
        cursor.execute(sql_deletar_entidade, sql_args)
        conexao.commit()
    
    def atualizar_entidade(self, cursor, conexao, cod_entidade, nome,
                           sobrenome, rg, celular, email,
                           tipo_morador, cod_usuario):
                               
        sql_atualizar_entidade = (" update entidade"
                                  " set nome = ?,"
                                  " sobrenome = ?,"
                                  " rg = ?,"
                                  " celular = ?,"
                                  " email = ?,"
                                  " tipo_morador = ?,"
                                  " cod_usuario_registro = ?"
                                  " where cod_entidade = ?") 
        
        sql_args = ([nome, sobrenome, rg, celular, email, tipo_morador,
                     cod_usuario, cod_entidade])
        
        cursor.execute(sql_atualizar_entidade, sql_args)
        conexao.commit()
