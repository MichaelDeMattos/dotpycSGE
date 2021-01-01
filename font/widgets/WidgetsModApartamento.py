class WidgetsApartamento():
    def start_widgets(self, builder):
       # --> Janela Principal
        self.janela_apartamento = self.builder.get_object("janela_apartamento")
        self.janela_apartamento.show_all()
        self.janela_apartamento.maximize()
        self.entry_tipo_pesquisa = self.builder.get_object("entry_tipo_pesquisa")
        self.cmb_tipo_pesquisa_ap = self.builder.get_object("cmb_tipo_pesquisa_ap")
        self.lst_cmb_tipo_pesquisa = self.builder.get_object("lst_cmb_tipo_pesquisa")
        self.lst_cmb_tipo_pesquisa.clear()
        op_filtro_pesquisa_ap = ([1, "BLOCO"], [2, "NUMERO"], [3, "ANDAR"])
        for i in op_filtro_pesquisa_ap:
            self.lst_cmb_tipo_pesquisa.append(i)
        self.cmb_tipo_pesquisa_ap.set_active(0)
        self.lst_vinculo_apartamento = self.builder.get_object("lst_vinculo_apartamento")
        self.lst_gr_apartamento = self.builder.get_object("lst_gr_apartamento")
        self.grade_apartamento = self.builder.get_object("grade_apartamento")
        self.grade_vincular_entidade = self.builder.get_object("grade_vincular_entidade")
        
        # -- Janela vinculo entidade
        self.janela_entidade_vinculo = self.builder.get_object("janela_entidade_vinculo")
        self.cmb_tipo_pesquisa_vinculo = self.builder.get_object("cmb_tipo_pesquisa_vinculo")
        self.lst_cmb_tipo_pesquisa = self.builder.get_object("lst_cmb_tipo_pesquisa")
        self.entry_tipo_pesquisa_entidade = self.builder.get_object("entry_tipo_pesquisa_entidade")
        self.grade_entidade = self.builder.get_object("grade_entidade")
        self.lst_vinculo_entidade = self.builder.get_object("lst_vinculo_entidade")
        self.lst_cmb_tipo_pesquisa_entidade = self.builder.get_object("lst_cmb_tipo_pesquisa_entidade")
        self.lst_cmb_tipo_pesquisa_entidade.clear()
        op_filtro_entidade = ([1, "NOME"], [2, "RG"])
        for i in op_filtro_entidade:
            self.lst_cmb_tipo_pesquisa_entidade.append(i)
        self.cmb_tipo_pesquisa_vinculo.set_active(0)
        self.lstEntidadeInativa = self.builder.get_object("lstEntidadeInativa")
        self.gradeEntidadeInativa = self.builder.get_object("gradeEntidadeInativa")
        
        # --> Janela cadastrar apartamento
        self.janela_cadastrar_apartamento = self.builder.get_object("janela_cadastrar_apartamento")
        self.entry_bloco = self.builder.get_object("entry_bloco")
        self.entry_andar = self.builder.get_object("entry_andar")
        self.entry_numero = self.builder.get_object("entry_numero")
        
        # --> Utilidades 
        self.msg_dialog = self.builder.get_object("msg_dialog")
