#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
import traceback
import email.message
import base64


class SendEmail(object):
    def __init__(self, *args, **kwargs):
        super(SendEmail, self).__init__(*args, **kwargs)
        
    #Função para o envio do e-mail
    def enviar_email(self, servidor, porta=None, tipo_conexao=None, senha=None, 
                     origem=None, destino=None, mensagem=None, assunto=None,
                     nome=None, anexo=None):
	
        if servidor == 'smtp.gmail.com':
            _origem = origem
            _destino = destino
            _senha = senha
            _assunto = assunto
            _mensagem = mensagem
            _nome = nome
            
            msg = email.message.Message()
            msg['Subject'] = _assunto
            msg['From'] = _origem
            msg['To'] = _destino
            msg.add_header('Content-Type', 'text/html')
            msg.set_payload(_mensagem, charset='utf-8')
            
            servidor_smtp = smtplib.SMTP_SSL(servidor, porta)
            
            # Login Credentials for sending the mail
            servidor_smtp.login(msg['From'], _senha)
    
            servidor_smtp.sendmail(msg['From'], [msg['To']], msg.as_string())
                                                            
            #encera a conexão
            servidor_smtp.quit()

    def menssagem_layout(self, bloco, ap, andar, destinatario, remetente,
                         entregador, obs, data_registro,
                         prazo_retirada):
        
        tag_estilo = (" h3 {color: red;}"
                      " h3 {font-family: 'Times New Roman', Times, serif;}"
                      " h4 {font-size: 12px}"
                      " #sub {font-family: 'Times New Roman', Times, serif; bold;")
        
        texto = (
                "<!DOCTYPE html>"
                "<html lang='pt-br'>"
                "    <head>"
                "        <meta charset='utf-8'>"        
                "        <style>"
                "          {}   "
                "        </style>"
                "    </head>"
                "    <body>"
                "        <h3>Registro de entrega de encomenda</h3>"
                "        <blockquote>"
                "        <h4>Condomínio: Recanto Lagoinha</h4>"
                "        <h4>Telefone: +55 17 99174-00025</h4>"
                "        <h4>E-mail: chelmto3000@gmail.com</h4>"
                "        </blockquote>"
                "        </br>"
                "<p id='sub'>---------------------------------------------------------------------</p>"
                "        <h3>Dados do destinário</h3>"
                "<p id='sub'>---------------------------------------------------------------------</p>"
                "        <p>Bloco: {} </p>"
                "        <p>Apartamento: {} </p>"
                "        <p>Andar: {} </p>"
                "        <p>Destinatário: {} </p>"
                "<p id='sub'>---------------------------------------------------------------------</p>"
                "        <h3>Dados da sua encomenda</h3>"
                "<p id='sub'>---------------------------------------------------------------------</p>"
                "        <p>Remetente: {}</p>"
                "        <p>Entegador: {}</p>"
                "        <p>Dados adcionais: {}</p>"
                "        <p>Data recebimento: {}</p>"
                "        <p>Prazo para retirada: {}</p>"
                "<p id='sub'>---------------------------------------------------------------------</p>"
                "</html>").format(tag_estilo,
                                  bloco,
                                  ap,
                                  andar,
                                  destinatario,
                                  remetente,
                                  entregador,
                                  obs,
                                  data_registro,
                                  prazo_retirada)
        
        return texto.encode('utf-8')
        
    def layout_entrega(self, bloco, ap, andar, destinatario, remetente,
                       obs, data_retirada):
        
        tag_estilo = (" h3 {color: red;}"
                      " h3 {font-family: 'Times New Roman', Times, serif;}"
                      " h4 {font-size: 12px}"
                      " #sub {font-family: 'Times New Roman', Times, serif; bold;")
        
        texto = (
                "<!DOCTYPE html>"
                "<html lang='pt-br'>"
                "    <head>"
                "        <meta charset='utf-8'>"        
                "        <style>"
                "          {}   "
                "        </style>"
                "    </head>"
                "    <body>"
                "        <h3>Registro de retirada de encomenda</h3>"
                "        <blockquote>"
                "        <h4>Condomínio: Recanto Lagoinha</h4>"
                "        <h4>Telefone: +55 17 99174-00025</h4>"
                "        <h4>E-mail: chelmto3000@gmail.com</h4>"
                "        </blockquote>"
                "        </br>"
                "<p id='sub'>---------------------------------------------------------------------</p>"
                "        <h3>Dados do destinário</h3>"
                "<p id='sub'>---------------------------------------------------------------------</p>"
                "        <p>Bloco: {} </p>"
                "        <p>Apartamento: {} </p>"
                "        <p>Andar: {} </p>"
                "        <p>Destinatário: {} </p>"
                "<p id='sub'>---------------------------------------------------------------------</p>"
                "        <h3>Dados da sua encomenda</h3>"
                "<p id='sub'>---------------------------------------------------------------------</p>"
                "        <p>Remetente: {}</p>"
                "        <p>Observação de retirada: {}</p>"
                "        <p>Data da retirada: {}</p>"
                "<p id='sub'>---------------------------------------------------------------------</p>"
                "</html>").format(tag_estilo,
                                  bloco,
                                  ap,
                                  andar,
                                  destinatario,
                                  remetente,
                                  obs,
                                  data_retirada)
        
        return texto.encode('utf-8')
