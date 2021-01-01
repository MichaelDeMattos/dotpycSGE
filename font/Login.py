#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
import os
import fdb
import json
import zlib 
import base64
import traceback, sys

from engineers.MikeUtil import MikeGtk
from model.ModelLogin import ModelsLogin
from widgets.WidgetsModLogin import WidgetsLogin
from Entidade import ModuloEntidade
from Apartamento import ModuloApartamento
from Entrega import ModuloEntrega
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

DEBUG=True

#janela_login = (zlib.decompress(base64.b64decode())).decode("utf-8") <-- user somente em produção
#builder.add_objects_from_string(janela_login, ["janela_login"]) <-- user somente em produção

"""
Depêndencias: python3-fdb, python3-gi, python3-gi-cairo, gir1.2-gtk-3.0

Copyright (C) 
Copying and distribution of this file, with or without modification,
are permitted in any medium without royalty provided the copyright
notice and this notice are preserved.  This file is offered as-is,
without any warranty.

Author: Michael de Mattos
"""

builder = Gtk.Builder()

class Handler(MikeGtk, ModelsLogin, WidgetsLogin):
    
    def __init__(self, *args, **kwargs):
        super(Handler, self).__init__(*args, **kwargs)
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        builder.add_from_file("interface/Login.ui")

        # -- Estilo app
        estlo = None        
        if DEBUG == True:
            estilo = "../static/style.css"
        screen = Gdk.Screen()
        self.style_app(style_path=estilo, set_screen=screen)
        
        # Inicia os widgets 
        self.start_widgets(builder)
        
        # -- Conexao com o banco de dados
        try:
            if DEBUG == True:
                with open("../config.json", "rb") as arquivo:
                    bytecode = arquivo.read()
                    string_json = json.loads(bytecode)
                    self.servidor = string_json["servidor"]
                    self.usuario = base64.b64decode(string_json["usuario"]).decode("UTF-8")
                    self.senha = base64.b64decode(string_json["senha"]).decode("UTF-8")
                    self.porta = base64.b64decode(string_json["porta"]).decode("UTF-8")
                    self.aliases = base64.b64decode(string_json["aliases"]).decode("UTF-8")
                    self.chave = string_json["chave"]                    
                    
                    self.conexao = fdb.connect(host=self.servidor, 
                                               port=int(self.porta), 
                                               database=self.aliases,
                                               user=self.usuario,
                                               password=self.senha,
                                               charset='UTF8')
                    
                    self.cursor = self.conexao.cursor()
                    
        except Exception as ex:
            self.simple_msg_box(self.msg_dialog,title="Erro",
                                text="Erro: " + str(ex))
    
    #--> Destroy a aplicação
    def ao_clicar_sair(self, *args):
        Gtk.main_quit()
        
	#--> Ao clicar no botão login
    def on_bt_login_clicked(self, *args):
        try:
            # -- Executa a função de login
            self.check_login()
            
        # -- Caso ocorra algum erro inesperado
        except Exception as e:
            self.simple_msg_box(self.msg_dialog,title="Erro",
                                text="Erro: " + str(e))
			
	# -- Regra para login
    def check_login(self, *args):
		# -- Executa a busca da empresa atraver da chave
        empresa_selecionada = self.verifica_login(self.cursor,
                                                  self.chave,
                                                  usuario = self.entry_usuario.get_text().upper())
		
        print(empresa_selecionada)
        # -- Tipo de retorno vazio, 
		# -- significa que não existe licença ou a chave foi modificada
        retorno_nullo = [[]]
        if empresa_selecionada == retorno_nullo[0]:
            self.simple_msg_box(self.msg_dialog,title="Erro",
								text="Chave de acesso não encontrada\n"
								"Por favor contate o suporte!")
		
        else:						
            # -- Monta as variáveis para trabalhar com mais facilidade
            cod_usuario = empresa_selecionada[0][0]
            usuario = empresa_selecionada[0][1]
            senha =  empresa_selecionada[0][2]
            empresa = empresa_selecionada[0][3]
            cpf_cnpj = empresa_selecionada[0][4]
            chave = empresa_selecionada[0][5]
            situacao = empresa_selecionada[0][6]
            
            # -- Monta as variáveis com os usuário e senha informado
            usuario_informado = str(self.entry_usuario.get_text())
            senha_informada = str(self.entry_senha.get_text())
            
            # -- Verifica se a empresa está com a licença em dia
            if situacao == 'B' or situacao == 'D':
                msg =  ("Estamos com problema para validar sua licença!\n"
                        "Por favor entre em contato com o suporte")
                self.simple_msg_box(self.msg_dialog,title="Ops!",
                                    text=msg,
                                    icon=None)
			
			# -- Caso usuário e senha estejam corretos
            elif usuario_informado.upper() == usuario and senha_informada == senha:
                self.simple_msg_box(self.msg_dialog,title="Sucesso",
                                    text="Usuário logado com sucesso!\n",
                                    icon=None)
                
                # --> Janela login invisível
                self.janela_login.set_visible(False)
                
                # -- registra o usuario logado
                self.cod_usuario_logado = cod_usuario
                
                # -- Chama nova janela
                self.new_window_main(self.janela_modulos,
                                     self.janela_login, True, True)
                self.janela_modulos.maximize()
                
            # -- Caso usuário ou senha incorretos
            else:
                self.simple_msg_box(self.msg_dialog,title="Erro",
									text="Usuário ou senha incorretos",
									icon=None)
																				 
	#--> Indentifica empresa e número de acesso
    def identificar_empresa(self, *args):
        try:
            if DEBUG == True:
                path = "../../.config.json"
                with open(path, "rb") as file_json:
                    dados = file_json.read()
                    string_json = json.loads(dados)
                    chave = string_jason["chave"]
                    
                    return chave
                    
        except Exception as ex:
            self.simple_msg_box(self.msg_dialog,title="Erro!",
							    text="Empresa não encontrada\n"
								"Entre em contato com o suporte\n"
								"Detalhes: %s" % (str(ex)))
    
    # -- Defualt módulo cadastrar entidade
    def on_bt_modulo_entidade_clicked(self, *args):
        try:
            ModuloEntidade(builder=builder, conexao=self.conexao,
                           cursor=self.cursor, 
                           cod_usuario=self.cod_usuario_logado)
        
        except Exception as ex:
            self.simple_msg_box(self.msg_dialog,title="Erro!",
							    text="Erro ao importar o módulo!\n"
								"Entre em contato com o suporte\n"
								"Detalhes: %s" % (str(ex)))
            erro = traceback.print_exc(file=sys.stdout)
            print(str(erro))
    
    # -- Defualt módulo registrar AP
    def on_bt_modulo_ap_clicked(self, *args):
        try:
            ModuloApartamento(builder=builder, conexao=self.conexao,
                              cursor=self.cursor, 
                              cod_usuario=self.cod_usuario_logado)
        
        except Exception as ex:
            self.simple_msg_box(self.msg_dialog,title="Erro!",
							    text="Erro ao importar o módulo!\n"
								"Entre em contato com o suporte\n"
								"Detalhes: %s" % (str(ex)))
            erro = traceback.print_exc(file=sys.stdout)
            print(str(erro))
    
    # -- Defualt módulo cadastrar Entrega
    def on_bt_modulo_entrega_clicked(self, *args):
        try:
            ModuloEntrega(builder=builder, conexao=self.conexao,
                          cursor=self.cursor,
                          cod_usuario=self.cod_usuario_logado)
        
        except Exception as ex:
            self.simple_msg_box(self.msg_dialog,title="Erro!",
							    text="Erro ao importar o módulo!\n"
								"Entre em contato com o suporte\n"
								"Detalhes: %s" % (str(ex)))
            erro = traceback.print_exc(file=sys.stdout)
            print(str(erro))
    
    # --> Fecha a exexução da janela configurar servidor
    def on_janela_config_delete_event(self, *args):
        window = self.janela_config_servidor
        window.hide()
        return True
    
    # --> Ai clicar em salvar configurações do servidor
    def on_bt_salvar_config_servidor_clicked(self, *args):
        try:
            servidor = self.entry_servidor.get_text()
            email = self.entry_email_servidor.get_text()
            tipo = self.cmb_tipo_conexao.get_model()[self.cmb_tipo_conexao.get_active()][1]
            porta = self.entry_porta_servidor.get_text()
            senha = self.entry_senha_email.get_text()
            cod_usuario = self.cod_usuario_logado
            
            # Reseta configuração existente
            self.resetar_config_servidor(self.cursor, self.conexao)
            
            # Define a nova configuração
            self.nova_config_servidor(servidor, email, tipo, porta,
                                      senha, cod_usuario, self.cursor,
                                      self.conexao)
                                      
            self.simple_msg_box(self.msg_dialog,title="Sucesso!",
                                text="Servidor configurado com sucesso!")
                                            
        except Exception as ex:
            erro = traceback.print_exc(file=sys.stdout)
            print(str(erro))
            self.simple_msg_box(self.msg_dialog,title="Erro!",
							    text="Error ao salvar modificações!\n"
								"Detalhes: %s" % (str(ex)))
    
    # --> Ao clicar em cancelar atualizar o servidor
    def on_bt_cancelar_config_servidor_clicked(self, *args):
        window = self.janela_config_servidor
        window.hide()
        return True
    
    # --> Traz a janela de configuração do servidor
    def ao_clicar_configurar_servidor(self, *args):
        try:
            self.lst_tipo_conexao_servidor.clear()
            
            # >> Opções default cmb_tipo_conexao
            tipos = ([1, "SSL"], [2, "SMTP"])
            for i in tipos:
                self.lst_tipo_conexao_servidor.append(i)
                    
            self.new_window_main(self.janela_config_servidor,
                                 self.janela_modulos, True)
            
            config = self.busca_config_servidor(self.cursor)
            
            self.entry_servidor.set_text(config[0][1])
            self.entry_email_servidor.set_text(config[0][2])
            if config[0][3] == 'SSL':
                self.cmb_tipo_conexao.set_active(0)
            
            self.entry_porta_servidor.set_text(str(config[0][4]))
            self.entry_senha_email.set_text(config[0][7])
            
        except Exception as ex:
            self.simple_msg_box(self.msg_dialog,title="Erro!",
							    text="Error carregar môdulo!\n"
								"Detalhes: %s" % (str(ex)))
    
    # --> Chamar uma nova Janela no mesmo arquivo glade
    def new_window_main(self, new_window, now_window,  modal=False, 
						destroy_parent=False, maximize=False):
        new_window.set_transient_for(now_window)
        new_window.set_modal(modal)
        new_window.set_destroy_with_parent(destroy_parent)
        new_window.show_all()
        if maximize == True:
            new_window.maximize()
            
if __name__ == '__main__':
    builder.connect_signals(Handler())
    Gtk.main()
	
