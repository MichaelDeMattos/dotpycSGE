#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import gi
import traceback, sys
from engineers.MikeUtil import MikeGtk
from model.ModelApartamento import ModelsApartamento
from widgets.WidgetsModApartamento import WidgetsApartamento
gi.require_version('Gtk', '3.0')
import glib
from gi.repository import Gtk, Gdk

DEBUG=True

#janela_login = (zlib.decompress(base64.b64decode())).decode("utf-8") <-- user somente em produção
#self.builderadd_objects_from_string(janela_login, ["janela_login"]) <-- user somente em produção

"""
Depêndencias: python3-fdb, python3-gi, python3-gi-cairo, gir1.2-gtk-3.0

Copyright (C) 
Copying and distribution of this file, with or without modification,
are permitted in any medium without royalty provided the copyright
notice and this notice are preserved.  This file is offered as-is,
without any warranty.

Author: Michael de Mattos
"""

class ModuloApartamento(MikeGtk, ModelsApartamento, WidgetsApartamento):
    
    def __init__(self, builder, conexao, cursor, cod_usuario, *args, **kwargs):
        super(ModuloApartamento, self).__init__(*args, **kwargs)
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
        self.builder.add_from_file("interface/Apartamento.ui")
        self.builder.connect_signals(self)
        
        # -- Inicia os widgets
        self.start_widgets(self.builder)
        
        # -- Global
        self.cod_ap_selecionado = None
        self.cod_vinculo_endereco = {"codigo": []}
        self.cod_entidade_ativa = {"codigo": []}
        self.cod_entidade_inativa = {"codigo": []}
        
    # --> Encerra a execução da janela principal
    def on_janela_apartamento_destroy(self, *args):
        window = self.janela_apartamento
        window.destroy()
    
    # --> Realiza a busca dos apartamentos cadastrados
    def on_bt_pesquisar_apartamento_clicked(self, *args):
        try:
            # --> reseta lista da grade
            self.lst_gr_apartamento.clear()
            self.on_bt_limpar_clicked(*args)
            
            linha_combo = self.cmb_tipo_pesquisa_ap.get_active()
            campo = self.cmb_tipo_pesquisa_ap.get_model()[linha_combo][1]
            filtro = self.entry_tipo_pesquisa.get_text()
            busca = self.buscar_apartamento(self.cursor, campo, filtro)
            
            for i in busca:
                selecao_ap = False
                cod_ap = i[0]
                bloco = i[1]
                andar = str(i[2])
                numero = int(i[3])
                
                # --> Dados da grade apartamento
                lst_ap = (selecao_ap, cod_ap, bloco, andar, numero)
                self.lst_gr_apartamento.append(lst_ap)
                
        except Exception as ex:
            self.simple_msg_box(self.msg_dialog,title="Erro",
                                text="Erro: " + str(ex))
    
    # --> Chama a nova janela para realizar o cadastro do apartamento
    def on_bt_novo_apartamento_clicked(self, *args):
        try:
            self.new_window_main(self.janela_cadastrar_apartamento,
                                 self.janela_apartamento,
                                 True)
        except Exception as ex:
            print(str(ex))
            self.simple_msg_box(self.msg_dialog,title="Erro",
                                text="Erro: " + str(ex))
    
    # --> Inativar endereco de uma entidade ativa
    def on_btInativarEntidade_clicked(self, *args):
        try:
            self.inativar_entidade(self.cursor, self.conexao,
                                   self.cod_entidade_ativa["codigo"],
                                   self.cod_usuario_logado)
            self.on_bt_pesquisar_apartamento_clicked(*args)
            
        except Exception as ex:
            erro = traceback.print_exc(file=sys.stdout)
            print(str(erro))
            self.simple_msg_box(self.msg_dialog,title="Erro",
                                text="Erro: " + str(ex))
    
    # --> Ao ativar endereco de uma entidade inativa
    def on_btAtivarEntidade_clicked(self, *args):
        try:
            self.ativar_entidade(self.cursor, self.conexao,
                                 self.cod_entidade_inativa["codigo"],
                                 self.cod_usuario_logado)
            self.on_bt_pesquisar_apartamento_clicked(*args)
            
        except Exception as ex:
            erro = traceback.print_exc(file=sys.stdout)
            print(str(erro))
            self.simple_msg_box(self.msg_dialog,title="Erro",
                                text="Erro: " + str(ex))
    
    # --> Excluir apartamento cadastrado
    def on_bt_excluir_apartamento_clicked(self, *args):
        try:
            if self.cod_ap_selecionado == None:
                return
            
            else:
                self.excluir_apartamento(self.cursor, self.conexao,
                                         self.cod_ap_selecionado)
                self.lst_gr_apartamento.clear()
                self.grade_apartamento.set_sensitive(True)
                self.grade_vincular_entidade.set_sensitive(True)
                
                self.simple_msg_box(self.msg_dialog,title="Suesso!",
                                text="Registro exclído com sucesso!")
        except Exception as ex:
            self.simple_msg_box(self.msg_dialog,title="Erro",
                                text="Erro: " + str(ex))
    
    # --> Limpar os registros selecionados e variáveis globais
    def on_bt_limpar_clicked(self, *args):
        try:
            # --> Reseta lista da grade e variáveis globais
            self.lst_gr_apartamento.clear()
            self.cod_vinculo_endereco = {"codigo": []}
            self.cod_entidade_inativa = {"codigo": []}
            self.cod_entidade_ativa = {"codigo": []}
            self.grade_apartamento.set_sensitive(True)
            self.grade_vincular_entidade.set_sensitive(True)
            self.lst_vinculo_apartamento.clear()
            self.lstEntidadeInativa.clear()
            self.cod_ap_selecionado = None
            
        except Exception as ex:
            self.simple_msg_box(self.msg_dialog,title="Erro",
                                text="Erro: " + str(ex))
    
    # -- Vincular nova entidade ao apartamento
    def on_bt_vincular_entidade_clicked(self, *args):
        try:
            if self.cod_ap_selecionado == None:
                self.simple_msg_box(self.msg_dialog,title="Atenção!!!",
                                text="Selecione um apartamento para vincular uma entidade")
            
            else:
                self.new_window_main(self.janela_entidade_vinculo,
                                     self.janela_apartamento,
                                     True)
                self.janela_entidade_vinculo.maximize()
                
        except Exception as ex:
            self.simple_msg_box(self.msg_dialog,title="Erro",
                                text="Erro: " + str(ex))
    
    
    # --> Encera a execução da janela de vinculo da entidade
    def on_janela_entidade_vinculo_delete_event(self, *args):
        window = self.janela_entidade_vinculo
        window.hide()
        return True
    
    # --> Excluir entidade vinculada ao apartamento
    def on_btExcluirVinculo_clicked(self, *args):
        try:
            codigo = self.cod_vinculo_endereco["codigo"]
            self.deletar_vinculo_endereco(self.cursor, self.conexao, codigo)
            
            self.simple_msg_box(self.msg_dialog,title="Sucesso!",
                                text="Registro excluído com sucesso!")
            
        except Exception as ex:
            self.simple_msg_box(self.msg_dialog,title="Erro",
                                text="Erro: " + str(ex))
    
    # --> Pesquisar entidades cadastradas para vinculo
    def on_bt_pesquisar_entidade_clicked(self, *args):
        try:
            # --> Reseta grade 
            self.lst_vinculo_entidade.clear()
            
            id_cmb_filtro = self.cmb_tipo_pesquisa_vinculo.get_active()
            campo = self.cmb_tipo_pesquisa_vinculo.get_model()[id_cmb_filtro][1]
            filtro = self.entry_tipo_pesquisa_entidade.get_text()
            
            vetor = self.busca_entidade(self.cursor, campo, filtro, self.cod_ap_selecionado)
          
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
                self.lst_vinculo_entidade.append(lst)
                
        except Exception as ex:
            self.simple_msg_box(self.msg_dialog,title="Erro",
                                text="Erro: " + str(ex))
                                
    # --> Ao clicar em salvar novo apartamento
    def on_bt_salvar_apartamento_clicked(self, *args):
        try:
            bloco = self.entry_bloco.get_text()
            andar = self.entry_andar.get_text()
            numero = self.entry_numero.get_text()
            
            self.novo_apartamento(self.cursor, self.conexao, bloco, 
                                  andar, numero, self.cod_usuario_logado)
            
            self.simple_msg_box(self.msg_dialog,title="Sucesso!!",
							    text="Apartamento cadastrado com sucesso!!\n")
                                
        except Exception as ex:
            self.simple_msg_box(self.msg_dialog,title="Erro",
                                text="Erro: " + str(ex))
    
    # --> Ao clicar voltar da janela cadastrar apartamento
    def on_bt_voltar_janela_apartamento_clicked(self, *args):
        window = self.janela_cadastrar_apartamento
        window.hide()
        return True
    
    # --> Ao selecionar entidade para vincular ao endereço
    def on_render_selecao_entidade_toggled(self, *args):
        try:
            # --> Reseta as listas das grade
            self.lst_vinculo_apartamento.clear()
            
            linha = args[1]
            grade = self.grade_entidade
            valor_default = False
            novo_valor = True
            valor_atual = grade.get_model()[linha][0]
            
            if valor_atual == valor_default:
                grade.get_model()[linha][0] = novo_valor
                cod_entidade = grade.get_model()[linha][1]
                self.vincular_entidade_apartamento(self.cursor,
                                                   self.conexao,
                                                   cod_entidade,
                                                   self.cod_ap_selecionado,
                                                   self.cod_usuario_logado)
                
                # --> Trata a seleção das entidades
                vetor_entidade = self.busca_entidade_apartamento(self.cursor, self.cod_ap_selecionado)
                
                for i in vetor_entidade:
                    selecao = False
                    cod = i[0]
                    cod_entidade = i[1]
                    nome = i[2]
                    celular = i[3]
                    rg = i[4]
                    
                    lst_entidade = (selecao, cod, cod_entidade, nome, celular, rg)
                    self.lst_vinculo_apartamento.append(lst_entidade)
                
                self.lst_vinculo_entidade.clear()
                window = self.janela_entidade_vinculo
                window.hide()
                return True
                
            else:
                grade.get_model()[linha][0] = valor_default
        
        except Exception as ex:
            erro = traceback.print_exc(file=sys.stdout)
            print(str(erro))
            self.simple_msg_box(self.msg_dialog,title="Erro",
                                text="Erro: " + str(ex))
    
    # --> Ao selecionar entidade já selecionada
    def on_render_selecao_entidade_vinculada_toggled(self, *args):
        try:
            linha = args[1]
            grade = self.grade_vincular_entidade
            valor_default = False
            novo_valor = True
            valor_atual = grade.get_model()[linha][0]
            cod_endereco = grade.get_model()[linha][1]
            cod_entidade = grade.get_model()[linha][2]
            
            if valor_atual == False:
                grade.get_model()[linha][0] = novo_valor
                self.cod_vinculo_endereco["codigo"].append(cod_endereco)
                self.cod_entidade_ativa["codigo"].append(cod_entidade)
            
            else:
                self.cod_vinculo_endereco["codigo"].remove(cod_endereco)
                self.cod_entidade_ativa["codigo"].remove(cod_entidade)
                grade.get_model()[linha][0] = valor_default
                
        except Exception as ex:
            erro = traceback.print_exc(file=sys.stdout)
            print(str(erro))
            self.simple_msg_box(self.msg_dialog,title="Erro",
                                text="Erro: " + str(ex))
    
    # --> Ao selecionar entidade inativa
    def on_renderSelecaoEntidadeInativa_toggled(self, *args):
        try:
            linha = args[1]
            grade = self.gradeEntidadeInativa
            valor_default = False
            novo_valor = True
            valor_atual = grade.get_model()[linha][0]
            cod_entidade = grade.get_model()[linha][2]
            
            if valor_atual == False:
                grade.get_model()[linha][0] = novo_valor
                self.cod_entidade_inativa["codigo"].append(cod_entidade)
            
            else:
                self.cod_entidade_inativa["codigo"].remove(cod_entidade)
                grade.get_model()[linha][0] = valor_default
            
        except Exception as ex:
            self.simple_msg_box(self.msg_dialog,title="Erro",
                                text="Erro: " + str(ex))
    
    # --> Ao selecionar apartamento 
    def on_render_selecao_apartamento_toggled(self, *args):
        try:
            # --> reseta a seleção da entidade
            self.lst_vinculo_apartamento.clear()
            self.lstEntidadeInativa.clear() 
            
            linha = args[1]
            grade = self.grade_apartamento
            valor_default = False
            novo_valor = True
            valor_atual = grade.get_model()[linha][0]
            
            if valor_atual == valor_default:
                # --> Trata a seleção do apartamento
                grade.get_model()[linha][0] = novo_valor
                cod_apartamento = grade.get_model()[linha][1]
                self.cod_ap_selecionado = cod_apartamento
                self.grade_apartamento.set_sensitive(False)
                
                # --> Trata a seleção das entidades ativa
                vetor_entidade_ativa = self.busca_entidade_apartamento_ativa(self.cursor, cod_apartamento)
                
                for i in vetor_entidade_ativa:
                    selecao = False
                    cod = i[0]
                    cod_entidade = i[1]
                    nome = i[2]
                    celular = i[3]
                    rg = i[4]
                    
                    lst_entidade = (selecao, cod, cod_entidade, nome, celular, rg)
                    self.lst_vinculo_apartamento.append(lst_entidade)
                
                # --> Trata a seleção das entidades inativas
                vetor_entidade_inativa = self.busca_entidade_apartamento_inativo(self.cursor, cod_apartamento)
                
                for i in vetor_entidade_inativa:
                    selecao = False
                    cod = i[0]
                    cod_entidade = i[1]
                    nome = i[2]
                    celular = i[3]
                    rg = i[4]
                    
                    lst_entidade = (selecao, cod, cod_entidade, nome, celular, rg)
                    self.lstEntidadeInativa.append(lst_entidade)
            
            else:
                grade.get_model()[linha][0] = valor_default
                elf.grade_apartamento.set_sensitive(True)
                self.cod_ap_selecionado = None
            
        except Exception as ex:
             self.simple_msg_box(self.msg_dialog,title="Erro",
                                text="Erro: " + str(ex))
    
    # --> Chamar uma nova Janela no mesmo arquivo glade
    def new_window_main(self, new_window, now_window,  modal=False, 
						destroy_parent=False, maximize=False):
        new_window.set_transient_for(now_window)
        new_window.set_modal(modal)
        new_window.set_destroy_with_parent(destroy_parent)
        new_window.show_all()
        if maximize == True:
            new_window.maximize()
