#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import gi
import traceback, sys
from engineers.MikeUtil import MikeGtk
from model.ModelEntidade import ModelsEntidade
from widgets.WidgetsModEntidade import WidgetsEntidade
gi.require_version('Gtk', '3.0')
import glib
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

class ModuloEntidade(MikeGtk, ModelsEntidade, WidgetsEntidade):
    
    def __init__(self, builder, conexao, cursor, cod_usuario, *args, **kwargs):
        super(ModuloEntidade, self).__init__(*args, **kwargs)
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # -- Estilo app
        estlo = None        
        if DEBUG == True:
            estilo = "../static/style.css"
        screen = Gdk.Screen()
        self.style_app(style_path=estilo, set_screen=screen)
        
        # --> Usuário logado no sistema
        self.cod_usuario_logado = cod_usuario
        
        # -- Conexao com o banco de dados
        self.conexao = conexao
        self.cursor = cursor
        
        # --> Construtor
        self.builder = builder
        self.builder.add_from_file("interface/Entidade.ui")
        self.builder.connect_signals(self)
        
        # --> Inicia os widgets
        self.start_widgets(self.builder)
        
    # --> Fecha a janela buscar entidade
    def on_janela_entidade_delete_event(self, *args):
        window =  self.janela_entidade
        window.destroy()
    
    # --> Realiza a busca de entidades cadastradas
    def on_bt_pesquisar_entidade_clicked(self, *args):
        try:
            self.on_bt_limpar_clicked(*args)
            id_cmb_filtro = self.cmb_tipo_pesquisa.get_active()
            campo = self.cmb_tipo_pesquisa.get_model()[id_cmb_filtro][1]
            filtro = self.entry_tipo_pesquisa.get_text().upper()
            
            vetor = self.busca_entidade(self.cursor, campo, filtro)
          
            for i in vetor:
                selecao = False
                cod_entidade = i[0]
                nome = i[1]
                sobrenome = i[2]
                rg = i[3]
                celular = i[4]
                email = i[5]
                tipo = "Proprietário" if i[6] == "P" else "Inquílino"
                
                lst = (selecao, cod_entidade, nome, sobrenome, rg,
                       celular, email, tipo)
                self.lst_gr_entidade.append(lst)
                
        except Exception as ex:
            self.simple_msg_box(self.msg_dialog,title="Erro!",
							    text="Error carregar registros!\n"
								"Detalhes: %s" % (str(ex)))
            erro = traceback.print_exc(file=sys.stdout)
            print(str(erro))
    
    # -- Limpa e reativa a grade de pesquisa da entidade
    def on_bt_limpar_clicked(self, *args):
        self.lst_gr_entidade.clear()
        self.grade_entidade.set_sensitive(True)
    
    # -- Ao ativar uma entidade
    def on_btAtivarEntidade_clicked(self, *args):
        try:
            pass
        
        except Exception as ex:
            pass
            
    # --> Tras a janela de cadastrar entidade
    def on_bt_novo_entidade_clicked(self, *args):
        try:
            self.new_window_main(self.janela_cadastrar_entidade,
                                 self.janela_entidade, True)
        
        except Exception as ex:
            self.simple_msg_box(self.msg_dialog,title="Erro!",
							    text="Error carregar môdulo!\n"
								"Detalhes: %s" % (str(ex)))
    
    def on_render_selecao_entidade_toggled(self, *args):
        try:
            linha = args[1]
            valor_default = False
            novo_valor = True
            grade = self.grade_entidade
            valor_atual = grade.get_model()[linha][0]
            
            if valor_atual == valor_default:
                grade.get_model()[linha][0] = novo_valor
                self.grade_entidade.set_sensitive(False)
                self.bt_limpar.set_visible(True)
                self.cod_entidade_selecionada = grade.get_model()[linha][1]
                
            else:
                grade.get_model()[linha][0] = valor_default
                
        except Exception as ex:
            self.simple_msg_box(self.msg_dialog,title="Erro!",
							    text="Error marcar registro!\n"
								"Detalhes: %s" % (str(ex)))
    
    # --> Ao clicar em alterar uma entidade cadastrada
    def on_bt_alterar_entidade_clicked(self, *args):
        try:
            vetor = self.busca_entidade_codigo(self.cursor,
                                               self.cod_entidade_selecionada)
            
            for i in vetor:
                self.entry_nome.set_text(i[0])
                self.entry_sobrenome.set_text(i[1])
                self.entry_rg.set_text(i[2])
                self.entry_celular.set_text(i[3])
                self.entry_email.set_text(i[4])
                self.cmb_tipo_morador.set_active(0) if i[5] == "P" else self.cmb_tipo_morador.set_active(1)
            
            self.bt_salvar_entidade.set_label("Atualizar")
            self.new_window_main(self.janela_cadastrar_entidade,
                                 self.janela_entidade, True)
        
        except Exception as ex:
            self.simple_msg_box(self.msg_dialog,title="Erro!",
							    text="Error carregar registro!\n"
								"Detalhes: %s" % (str(ex)))
    
    # --> Ao clicar em excluir uma entidade cadastrada
    def on_bt_excluir_entidade_clicked(self, *args):
        try:
            if self.cod_entidade_selecionada == None:
                return
            
            else:
                self.deletar_entidade(self.cursor, self.conexao, 
                                      self.cod_entidade_selecionada)
            
                self.simple_msg_box(self.msg_dialog,title="Sucesso!",
                                    text="Registro excluído com sucesso!")
                                    
                self.on_bt_limpar_clicked(*args)
                self.on_bt_pesquisar_entidade_clicked(*args)
                
        except Exception as ex:
            self.simple_msg_box(self.msg_dialog,title="Erro!",
							    text="Error excluir registro!\n"
								"Detalhes: %s" % (str(ex)))
                                
    # --> Ao clicar em salvar/atualizar nova entidade
    def on_bt_salvar_entidade_clicked(self, *args):
        try:
            nome_digitado = self.entry_nome.get_text()
            nome = self.format_str_not_space(nome_digitado, True)
            sobrenome_digitado = self.entry_sobrenome.get_text()
            sobrenome = self.format_str_not_space(sobrenome_digitado, True)
            rg_digitado = self.entry_rg.get_text()
            rg = self.format_rg(rg_digitado) 
            celular = self.entry_celular.get_text()
            email_digitado = self.entry_email.get_text()
            email = self.format_str_not_space(email_digitado, True)
            
            # -- Validação do RG
            if rg == 0:
                self.simple_msg_box(self.msg_dialog, "Erro", "RG INVÀLIDO")
                return
                
            # -- Seleção GtkComboBox 
            id_cmb_tipo = self.cmb_tipo_morador.get_active()
            tipo_morador = self.cmb_tipo_morador.get_model()[id_cmb_tipo][1]
            if tipo_morador == "Proprietário":
                tipo_morador = "P"
            else:
                tipo_morador = "I"
            
            if self.bt_salvar_entidade.get_label() == "Salvar":
                self.nova_entidade(self.cursor, self.conexao, nome, sobrenome,
                                   rg, celular, email, tipo_morador,
                                   self.cod_usuario_logado)
                                   
                self.simple_msg_box(self.msg_dialog,title="Sucesso!",
							    text="Sucesso ao gravar o registro!")
            
            else:
                self.atualizar_entidade(self.cursor, self.conexao, nome,
                                        sobrenome, rg, celular,
                                        email, tipo_morador,
                                        self.cod_usuario_logado,
                                        self.cod_entidade_selecionada)
                
                self.simple_msg_box(self.msg_dialog,title="Sucesso!",
							    text="Sucesso ao gravar o registro!")
                
                self.bt_salvar_entidade.set_label("Salvar")
        except Exception as ex:
            self.simple_msg_box(self.msg_dialog,title="Erro!",
							    text="Error salvar registro!\n"
								"Detalhes: %s" % (str(ex)))
    
    # --> Ao clicar em sair ou voltar da janela cadastrar entidade
    def on_bt_voltar_janela_entidade_clicked(self, *args):
        window = self.janela_cadastrar_entidade
        window.hide()
        return True
        
    # --> Chamar uma nova Janela no mesmo arquivo glade
    def new_window_main(self, new_window, now_window,  modal=False, 
						destroy_parent=False, maximize=False):
        new_window.set_transient_for(now_window)
        new_window.set_modal(modal)
        new_window.set_destroy_with_parent(destroy_parent)
        new_window.show_all()
        if maximize == True:
            new_window.maximize()
            
