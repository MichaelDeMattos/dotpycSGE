#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class ModelsLogin(object):
    def __init__(self, *args, **kwargs):
        super(ModelsLogin, self).__init__(*args, **kwargs)
    
    def verifica_login(self, cursor, chave, usuario):
        sql_login = (" select log.cod_login, log.usuario, log.senha,"
                     " emp.razao_social, emp.cpf_cnpj,"
                     " emp.chave, emp.situacao"
                     " from login log"
                     " join empresa emp"
                     " on emp.cod_empresa = log.cod_empresa"
                     " where emp.chave = '{}'"
                     " and log.usuario = '{}'".format(chave, usuario))
        cursor.execute(sql_login)
        return cursor.fetchall()
    
    def resetar_config_servidor(self, cursor, conexao):
        sql_resetar_config_servidor = "delete from config_servidor"
        self.cursor.execute(sql_resetar_config_servidor)
        self.conexao.commit()
    
    def nova_config_servidor(self, servidor, email, tipo, porta, senha,
                             cod_usuario, cursor, conexao):
        sql_novo_config_servidor = (" insert into config_servidor"
                                    " (servidor, email, tipo, porta,"
                                    "  senha, cod_usuario_registro)"
                                    " values (?,?,?,?,?,?)")
        sql_args = ([servidor, email, tipo, porta, senha, cod_usuario])
        cursor.execute(sql_novo_config_servidor, sql_args)
        conexao.commit()
    
    def busca_config_servidor(self, cursor):
        sql_buscar_config_servidor = (" select * from config_servidor")
        cursor.execute(sql_buscar_config_servidor)
        return cursor.fetchall()
                        
        
    
