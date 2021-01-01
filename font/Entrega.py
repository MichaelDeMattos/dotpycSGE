#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import json
import datetime
import threading
import gi
import traceback, sys
from engineers.MikeUtil import MikeGtk
from engineers.MikeEmail import SendEmail
from model.ModelEntrega import ModelsEntrega
from widgets.WidgetsModEntrega import WidgetsEntrega
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

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

class ModuloEntrega(MikeGtk, ModelsEntrega, SendEmail, WidgetsEntrega):
    
    def __init__(self, builder, conexao, cursor, cod_usuario, *args, **kwargs):
        super(ModuloEntrega, self).__init__(*args, **kwargs)
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # -- Estilo app,
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
        self.builder.add_from_file("interface/Entrega.ui")
        self.builder.connect_signals(self)
        
        # -- Inicia os Widgets da Janela
        self.start_widgets(self.builder)
        
        # >> Global
        self.nova_entrega = {"cod_ap": None,
                             "bloco": None,
                             "numero": None,
                             "andar": None,
                             "cod_ent": None,
                             "destinatario": None,
                             "email": None,
                             "remetente": None,
                             "obs": None,
                             "entregador": None,
                             "prazo_retirada": None,
                             "enviar_email": False,
                             "enviar_sms": False,
                             "data_entrega": self.format_current_date()}
        
        self.finalizar_entrega = {"cod_entrega": None,
                                  "bloco": None,
                                  "numero": None,
                                  "andar": None,
                                  "cod_ent": None,
                                  "destinatario": None,
                                  "email": None,
                                  "remetente": None,
                                  "obs": None,
                                  "entregador": None,
                                  "prazo_retirada": None,
                                  "data_recebimento": None,
                                  "enviar_email": False,
                                  "enviar_sms": False}
        
    # --> Fecha a janela de entrega
    def on_janela_entrega_delete_event(self, *args):
        window = self.janela_entrega
        window.destroy()
    
    # --> Pesquisar apartamento para registrar entrega
    def on_bt_pesquisar_apartamento_entrega_clicked(self, *args):
        try:
            # --> reseta lista da grade
            self.lst_gr_apartamento.clear()
            self.lst_vinculo_apartamento.clear()
            self.grade_vincular_entidade.set_sensitive(True)
            self.grade_apartamento.set_sensitive(True)
            
            # --> reseta variáveis globais
            self.nova_entrega["cod_ap"] = None
            self.nova_entrega["cod_ent"] = None
            
            linha_combo = self.cmb_tipo_pesquisa_ap.get_active()
            campo = self.cmb_tipo_pesquisa_ap.get_model()[linha_combo][1]
            digitado = self.entry_tipo_pesquisa.get_text()
            filtro = digitado[1] if int(digitado) < 10 and len(digitado) > 1 else digitado
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
            erro = traceback.print_exc(file=sys.stdout)
            print(str(erro))
            self.simple_msg_box(self.msg_dialog,title="Erro",
                                text="Erro: " + str(ex))
                                
    # --> Ao selecionar apartamento
    def on_render_selecao_apartamento_toggled(self, *args):
        try:
             # --> reseta a seleção da entidade
            self.lst_vinculo_apartamento.clear() 
            
            linha = args[1]
            grade = self.grade_apartamento
            valor_default = False
            novo_valor = True
            valor_atual = grade.get_model()[linha][0]
            
            if valor_atual == valor_default:
                # --> Trata a seleção do apartamento
                grade.get_model()[linha][0] = novo_valor
                cod_ap = grade.get_model()[linha][1]
                bloco = grade.get_model()[linha][2]
                andar = grade.get_model()[linha][3]
                numero = grade.get_model()[linha][4]
                self.nova_entrega["cod_ap"] = cod_ap
                self.nova_entrega["bloco"] = bloco
                self.nova_entrega["andar"] = andar
                self.nova_entrega["numero"] = numero
                self.grade_apartamento.set_sensitive(False)
                                
                # --> Trata a seleção das entidades
                vetor_entidade = self.busca_entidade_apartamento(self.cursor, cod_ap)
                
                for i in vetor_entidade:
                    selecao = False
                    cod = i[0]
                    cod_entidade = i[1]
                    nome = i[2]
                    celular = i[3]
                    rg = i[4]
                    email = i[5]
                    
                    lst_entidade = (selecao, cod, cod_entidade, nome, celular, rg, email)
                    self.lst_vinculo_apartamento.append(lst_entidade)
            
            else:
                grade.get_model()[linha][0] = valor_default
                elf.grade_apartamento.set_sensitive(True)
                self.cod_ap_selecionado = None
            
        except Exception as ex:
            erro = traceback.print_exc(file=sys.stdout)
            print(str(erro))
            self.simple_msg_box(self.msg_dialog,title="Erro!",
							    text="Detalhes: %s" % (str(ex)))
    
    # --> Ao selecionar entidade
    def on_render_selecao_entidade_vinculada_toggled(self, *args):
        try:
            linha = args[1]
            grade = self.grade_vincular_entidade
            valor_default = False
            novo_valor = True
            valor_atual = grade.get_model()[linha][0]
            cod_entidade = grade.get_model()[linha][2]
            destinatario = grade.get_model()[linha][3]
            email = grade.get_model()[linha][6]
            
            if valor_atual == False:
                grade.get_model()[linha][0] = novo_valor
                self.nova_entrega["cod_ent"] = cod_entidade
                self.nova_entrega["destinatario"] = destinatario
                self.nova_entrega["email"] = email.lower()
                self.grade_vincular_entidade.set_sensitive(False)
            
            else:
                self.nova_entrega["cod_ent"] = None
                grade.get_model()[linha][0] = valor_default
        
        except Exception as ex:
            erro = traceback.print_exc(file=sys.stdout)
            print(str(erro))
            self.simple_msg_box(self.msg_dialog,title="Erro!",
							    text="Detalhes: %s" % (str(ex)))
    
    # --> Ao definir notificar via e-mail
    def on_chk_email_toggled(self, *args):
        try:
            if self.chk_email.get_active() == True:
                self.nova_entrega["enviar_email"] = True
                
            else:
                self.nova_entrega["enviar_email"] = False
        
        except Exception as ex:
            erro = traceback.print_exc(file=sys.stdout)
            print(str(erro))
            self.simple_msg_box(self.msg_dialog,title="Erro!",
							    text="Detalhes: %s" % (str(ex)))
                                
    # --> Ao definir notificar via sms
    def on_chk_sms_toggled(self, *args):
        try:
            if self.chk_sms.get_active() == True:
                self.nova_entrega["enviar_sms"] = True

            else:
                 self.nova_entrega["enviar_sms"] = True
            
        except Exception as ex:
            erro = traceback.print_exc(file=sys.stdout)
            print(str(erro))
            self.simple_msg_box(self.msg_dialog,title="Erro!",
							    text="Detalhes: %s" % (str(ex)))
    
    # --> Ao clicar registrar entrega
    def on_bt_registrar_entrega_clicked(self, *args):
        try:
            self.nova_entrega["remetente"] = self.entry_remetente.get_text().upper()
            self.nova_entrega["obs"] = self.entry_obs.get_text().upper()
            self.nova_entrega["prazo_retirada"] = self.entry_prazo_retirada.get_text().upper()
            self.nova_entrega["entregador"] = self.entry_entregador.get_text().upper()
            
            vetor = []
            for i in self.nova_entrega.values():
                vetor.append(i)
            
            # >> Verifica se existe campos em branco no form
            if '' in vetor:
                self.simple_msg_box(self.msg_dialog,title="Atenção!",
                                    text="É necessário realizar o preenchimento de todas informações")
                return
            
            else:
                self.new_window_main(self.janela_confirmar,
                                     self.janela_entrega, True)
                
                self.lb_titulo.set_text("Confirmar Registro de nova entrega")
                self.janela_confirmar.set_title("Registro de nova entrega")
                
        except Exception as ex:
            erro = traceback.print_exc(file=sys.stdout)
            print(str(erro))
            self.simple_msg_box(self.msg_dialog,title="Erro!",
							    text="Detalhes: %s" % (str(ex)))
    
    # --> Ao cancelar registro de nova entrega
    def on_bt_cancelar_clicked(self, *args):
        window = self.janela_confirmar
        window.hide()
        return True
    
    # --> Ao fechar Janela vincular OBS
    def on_janela_vincular_obs_delete_event(self, *args):
        window = self.janela_vincular_obs
        window.hide()
        return True
    
    # -- Ao clicar finalizar entrega 
    def on_bt_finalizar_entrega_clicked(self, *args):
        try:
            if self.finalizar_entrega["cod_entrega"] == None:
                return
            
            else:
                self.new_window_main(self.janela_vincular_obs,
                                     self.janela_entrega,
                                     True,
                                     True)
        
        except Exception as ex:
            erro = traceback.print_exc(file=sys.stdout)
            print(str(erro))
            self.simple_msg_box(self.msg_dialog,title="Erro!",
							    text="Detalhes: %s" % (str(ex)))
    
    # --> Ao clicar salvar observação entrega
    def on_bt_salvar_obs_entrega_clicked(self, *args):
        try:
            obs = self.tx_observacao_entrega.props.text
            id = self.cmb_status_entrega.get_active()
            status_entrega = self.cmb_status_entrega.get_model()[id][0]
            usuario = self.cod_usuario_logado
            
            if obs == '':
                self.simple_msg_box(self.msg_dialog,title="Atenção",
                                    text="Informe a observação de retirada")
                return
            
            else:
                self.encerrar_entrega(cursor = self.cursor,
                                      conexao = self.conexao,
                                      cod_entrega = self.finalizar_entrega["cod_entrega"],
                                      status = status_entrega,
                                      obs_final = obs,
                                      cod_usuario_final = usuario)
                
                self.simple_msg_box(self.msg_dialog,title="Sucesso!",
                                    text="Encomenda finalizada com sucesso!")
                                    
                layout = self.layout_entrega(self.finalizar_entrega["bloco"],
                                             self.finalizar_entrega["numero"],
                                             self.finalizar_entrega["andar"],
                                             self.finalizar_entrega["destinatario"],
                                             self.finalizar_entrega["remetente"],
                                             obs,
                                             self.format_current_date())
                
                # >> var local
                _senha = None
                _origem = None
                
                with open("engineers/.password/passwd.json", "rb") as config:
                    bytecode = config.read()
                    string_json = json.loads(bytecode)
                    _senha = string_json["senha"]
                    _origem = string_json["origem"]
                
                self.enviar_email(servidor='smtp.gmail.com',
                                  porta =465,
                                  senha = _senha,
                                  origem = _origem,
                                  destino = self.finalizar_entrega["email"],
                                  assunto = 'Retirada de encomenda registrada!',
                                  mensagem=layout,
                                  nome='Michael de Mattos')
                
                window = self.janela_vincular_obs
                window.hide()
                return True
                
        except Exception as ex:
            erro = traceback.print_exc(file=sys.stdout)
            print(str(erro))
            self.simple_msg_box(self.msg_dialog,title="Erro!",
							    text="Detalhes: %s" % (str(ex)))
    
    # --> Ao selecionar a entrega
    def on_render_selecao_entrega_toggled(self, *args):
        try:
            linha = args[1]
            grade = self.grade_entrega
            valor_default = False
            novo_valor = True
            valor_atual = grade.get_model()[linha][0]
            
            if valor_atual == valor_default:
                grade.get_model()[linha][0] = novo_valor
                self.finalizar_entrega["bloco"] = grade.get_model()[linha][2]
                self.finalizar_entrega["andar"] = grade.get_model()[linha][3]
                self.finalizar_entrega["numero"] = grade.get_model()[linha][4]
                self.finalizar_entrega["destinatario"] = grade.get_model()[linha][6]
                self.finalizar_entrega["data_recebimento"] = grade.get_model()[linha][13].split(" ")[0]
                self.finalizar_entrega["cod_entrega"] = grade.get_model()[linha][9]
                self.finalizar_entrega["remetente"] = grade.get_model()[linha][12]
                self.finalizar_entrega["entregador"] = grade.get_model()[linha][11]
                self.finalizar_entrega["email"] = grade.get_model()[linha][15]
                grade.set_sensitive(False)
                
            else:
                grade.get_model()[linha][0] = valor_default
        
        except Exception as ex:
            erro = traceback.print_exc(file=sys.stdout)
            print(str(erro))
            self.simple_msg_box(self.msg_dialog,title="Erro!",
							    text="Detalhes: %s" % (str(ex)))
            
    
    # --> Ao clicar pesquisar entrega
    def on_bt_pesquisar_entrega_clicked(self, *args):
        try:
            # --> reseta lista da grade
            self.lst_grade_entrega.clear()
            self.grade_entrega.set_sensitive(True)
            
            # --> reseta variáveis globais
            self.finalizar_entrega = {"cod_entrega": None,
                                      "bloco": None,
                                      "numero": None,
                                      "andar": None,
                                      "cod_ent": None,
                                      "destinatario": None,
                                      "email": None,
                                      "remetente": None,
                                      "obs": None,
                                      "entregador": None,
                                      "prazo_retirada": None,
                                      "data_recebimento": None,
                                      "enviar_email": False,
                                      "enviar_sms": False}

            linha_combo = self.cmb_tipo_pesquisa_entrega.get_active()
            campo = self.cmb_tipo_pesquisa_entrega.get_model()[linha_combo][1]
            filtro = self.entry_pesquisa_entrega.get_text().upper()
            busca = self.buscar_entrega(self.cursor, campo, filtro)
            for i in busca:
                selecao_entrega = False
                cod_ap = int(i[0])
                bloco = i[1]
                andar = i[2]
                numero = str(i[3])
                cod_entidade = int(i[4])
                nome = i[5]
                sobrenome = i[6]
                rg = i[7]
                cod_entrega = int(i[8])
                status = i[9]
                entregador = i[10]
                remetente = i[11]
                data_recebimento = str(i[12])
                obs = i[13]
                email = i[14]
                
                # --> Dados da grade apartamento
                lst_entrega = (selecao_entrega, cod_ap, bloco, andar,
                               numero, cod_entidade, nome, sobrenome,
                               rg, cod_entrega, status, entregador,
                               remetente, data_recebimento, obs, email)
                self.lst_grade_entrega.append(lst_entrega)
        
        except Exception as ex:
            erro = traceback.print_exc(file=sys.stdout)
            print(str(erro))
            self.simple_msg_box(self.msg_dialog,title="Erro!",
							    text="Detalhes: %s" % (str(ex)))
        
    
    # --> Pesquisar entregas finalizadas
    def on_bt_pesquisar_entrega_finalizada_clicked(self, *args):
        try:
             # --> reseta lista da grade
            self.lst_grade_entrega_finalizada.clear()
            self.grade_entrega.set_sensitive(True)
            
            linha_combo = self.cmb_filtro_entrega_finalizada.get_active()
            campo = self.cmb_filtro_entrega_finalizada.get_model()[linha_combo][1]
            filtro = self.entry_pesquisa_entrega_finalizada.get_text().upper()
            busca = self.buscar_entrega_finalizada(self.cursor, campo, filtro)
            for i in busca:
                cod_ap = int(i[0])
                bloco = i[1]
                andar = i[2]
                numero = str(i[3])
                cod_entidade = int(i[4])
                nome = i[5]
                sobrenome = i[6]
                rg = i[7]
                cod_entrega = int(i[8])
                status = i[9]
                entregador = i[10]
                remetente = i[11]
                data_recebimento = str(i[12])
                obs = i[13]
                email = i[14]
                login = i[15]
                
                # --> Dados da grade apartamento
                lst_entrega = (cod_ap, bloco, andar, numero,
                               cod_entidade, nome, sobrenome, rg,
                               cod_entrega, status, entregador,
                               remetente, data_recebimento, obs, email,
                               login)
                self.lst_grade_entrega_finalizada.append(lst_entrega)
        
        except Exception as ex:
            erro = traceback.print_exc(file=sys.stdout)
            print(str(erro))
            self.simple_msg_box(self.msg_dialog,title="Erro!",
							    text="Detalhes: %s" % (str(ex)))
    
    # --> Ao finalizar registro de nova entidade
    def on_bt_confirmar_clicked(self, *args):
        try:
            self.on_bt_pesquisar_entrega_clicked(*args)
            opcao = ["Confirmar Registro de nova entrega"]
            operacao = self.lb_titulo.get_text()
            
            # >> Registra nova entrega
            if opcao[0] == operacao:
                self.salvar_entrega(self.cursor, self.conexao,
                                    self.nova_entrega["cod_ap"],
                                    self.nova_entrega["cod_ent"],
                                    self.nova_entrega["remetente"],
                                    self.nova_entrega["entregador"],
                                    self.nova_entrega["prazo_retirada"],
                                    self.nova_entrega["obs"],
                                    self.cod_usuario_logado)
                
                self.simple_msg_box(self.msg_dialog,title="Sucesso!",
                                    text="Entrega cadastrada com sucesso!")
                
                if self.nova_entrega["enviar_email"] == True:
                    # >> var local
                    _senha = None
                    _origem = None
                
                    with open("engineers/.password/passwd.json", "rb") as config:
                        bytecode = config.read()
                        string_json = json.loads(bytecode)
                        _senha = string_json["senha"]
                        _origem = string_json["origem"]
                    
                        layout = self.menssagem_layout(bloco=self.nova_entrega["bloco"],
                                                        ap=self.nova_entrega["numero"],
                                                        andar=self.nova_entrega["andar"],
                                                        destinatario=self.nova_entrega["destinatario"],
                                                        remetente=self.nova_entrega["remetente"],
                                                        entregador=self.nova_entrega["entregador"],
                                                        obs=self.nova_entrega["obs"],
                                                        data_registro=self.nova_entrega["data_entrega"],
                                                        prazo_retirada=self.nova_entrega["prazo_retirada"])
                        
                        thread = threading.Thread(target=self.enviar_email(servidor='smtp.gmail.com',
                                                  porta =465,
                                                  senha = _senha,
                                                  origem = _origem,
                                                  destino=self.nova_entrega["email"],
                                                  assunto='Entrada de encomenda registrada com sucesso!',
                                                  mensagem=layout,
                                                  nome='Michael de Mattos'))
                        thread.daemon = True
                        thread.start()
                        
                        # >> Fecha a janela de confirmação
                        window = self.janela_confirmar
                        window.hide()
                        return True
                        
        except Exception as ex:
            erro = traceback.print_exc(file=sys.stdout)
            print(str(erro))
            self.simple_msg_box(self.msg_dialog,title="Erro!",
							    text="Detalhes: %s" % (str(ex)))
    
    # --> Chamar uma nova Janela no mesmo arquivo glade
    def new_window_main(self, new_window, now_window,  modal=False, 
						destroy_parent=False, maximize=False):
        new_window.set_transient_for(now_window)
        new_window.set_modal(modal)
        new_window.set_destroy_with_parent(destroy_parent)
        new_window.show_all()
        if maximize == True:
            new_window.maximize()
