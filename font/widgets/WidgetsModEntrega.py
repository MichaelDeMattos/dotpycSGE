class WidgetsEntrega():
    def start_widgets(self, builder):
        # --> Janela principal
        self.janela_entrega = self.builder.get_object("janela_entrega")
        self.janela_entrega.show_all()
        self.janela_entrega.maximize()
        
        # >> widgets janela principal
        self.cmb_tipo_pesquisa_ap = self.builder.get_object("cmb_tipo_pesquisa_ap")
        self.lst_cmb_tipo_pesquisa = self.builder.get_object("lst_cmb_tipo_pesquisa")
        
        # >> Opções de filtro de pesquisa
        op_filtro_pesquisa_ap = ([1, "BLOCO"], [2, "NUMERO"], [3, "ANDAR"])
        for i in op_filtro_pesquisa_ap:
            self.lst_cmb_tipo_pesquisa.append(i)
        self.cmb_tipo_pesquisa_ap.set_active(0)
        
        self.lst_cmb_tipo_pesquisa = self.builder.get_object("lst_cmb_tipo_pesquisa")
        self.entry_tipo_pesquisa = self.builder.get_object("entry_tipo_pesquisa")
        self.entry_remetente = self.builder.get_object("entry_remetente")
        self.entry_prazo_retirada = self.builder.get_object("entry_prazo_retirada")
        self.entry_prazo_retirada.set_text("120 DIAS")
        self.entry_obs = self.builder.get_object("entry_obs")
        self.entry_obs.set_text("RETIRAR NO PRAZO INFORMADO")
        self.entry_entregador = self.builder.get_object("entry_entregador")
        self.entry_entregador.set_text("CORREIOS")
        self.chk_email = self.builder.get_object("chk_email")
        self.chk_sms = self.builder.get_object("chk_sms")
        self.grade_apartamento = self.builder.get_object("grade_apartamento")
        self.lst_gr_apartamento = self.builder.get_object("lst_gr_apartamento")
        self.grade_vincular_entidade = self.builder.get_object("grade_vincular_entidade")
        self.lst_vinculo_apartamento = self.builder.get_object("lst_vinculo_apartamento")
        
        self.cmb_tipo_pesquisa_entrega = self.builder.get_object("cmb_tipo_pesquisa_entrega")
        self.lst_cmb_tipo_pesquisa_entrega = self.builder.get_object("lst_cmb_tipo_pesquisa_entrega")
        op_filtro_pesquisa_entrega = [1, "NOME"]
        self.lst_cmb_tipo_pesquisa_entrega.append(op_filtro_pesquisa_entrega)
        self.cmb_tipo_pesquisa_entrega.set_active(0)
        self.entry_pesquisa_entrega = self.builder.get_object("entry_pesquisa_entrega")
        self.grade_entrega = self.builder.get_object("grade_entrega")
        self.lst_grade_entrega = self.builder.get_object("lst_grade_entrega")
        self.cmb_status_entrega = self.builder.get_object("cmb_status_entrega")
        self.cmb_status_entrega.set_active(0)
        self.lst_cmb_status_entrega = self.builder.get_object("lst_cmb_status_entrega")
        self.grade_entrega_finalizada = self.builder.get_object("grade_entrega_finalizada")
        self.entry_pesquisa_entrega_finalizada = self.builder.get_object("entry_pesquisa_entrega_finalizada")
        self.lst_grade_entrega_finalizada = self.builder.get_object("lst_grade_entrega_finalizada")
        self.lst_cmb_entrega_finalizada = self.builder.get_object("lst_cmb_entrega_finalizada")
        self.cmb_filtro_entrega_finalizada = self.builder.get_object("cmb_filtro_entrega_finalizada")
        op_filtro_entrega_finalizada = [1, "NOME"]
        self.lst_cmb_entrega_finalizada.append(op_filtro_entrega_finalizada)
        self.cmb_filtro_entrega_finalizada.set_active(0)
        
    
        # >> Utilidades
        self.msg_dialog = self.builder.get_object("msg_dialog")
        self.janela_confirmar = self.builder.get_object("janela_confirmar")
        self.lb_titulo = self.builder.get_object("lb_titulo")
        self.janela_vincular_obs = self.builder.get_object("janela_vincular_obs")
        self.tx_observacao_entrega = self.builder.get_object("tx_observacao_entrega")
        
        
        
