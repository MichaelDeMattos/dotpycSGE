class WidgetsEntidade():
    def start_widgets(self, builder):
        # -- Janela busca Entidade 
        self.janela_entidade = self.builder.get_object("janela_entidade")
        self.janela_entidade.show_all()
        self.janela_entidade.maximize()
        self.cmb_tipo_pesquisa = self.builder.get_object("cmb_tipo_pesquisa")
        self.entry_tipo_pesquisa = self.builder.get_object("entry_tipo_pesquisa")
        self.grade_entidade = self.builder.get_object("grade_entidade")
        self.lst_gr_entidade = self.builder.get_object("lst_gr_entidade")
        self.bt_limpar = self.builder.get_object("bt_limpar")
        self.bt_limpar.set_visible(False)
    
        self.lst_cmb_tipo_pesquisa = self.builder.get_object("lst_cmb_tipo_pesquisa")
        self.lst_cmb_tipo_pesquisa.clear()
        filtros_combo = ([1, "Nome"], [2, "Sobrenome"])
        for i in filtros_combo:
            self.lst_cmb_tipo_pesquisa.append(i)
        self.cmb_tipo_pesquisa.set_active(0)
        
        # -- Janela cadastrar Entidade
        self.janela_cadastrar_entidade = self.builder.get_object("janela_cadastrar_entidade")
        self.bt_salvar_entidade = self.builder.get_object("bt_salvar_entidade")
        self.bt_voltar_janela_entidade = self.builder.get_object("bt_voltar_janela_entidade")
        self.cmb_tipo_morador = self.builder.get_object("cmb_tipo_morador")
        self.entry_nome = self.builder.get_object("entry_nome")
        self.entry_sobrenome = self.builder.get_object("entry_sobrenome")
        self.entry_rg = self.builder.get_object("entry_rg")
        self.entry_celular = self.builder.get_object("entry_celular")
        self.entry_email = self.builder.get_object("entry_email")
        
        # -- Utilidades
        self.msg_dialog = self.builder.get_object("msg_dialog")
        self.cod_entidade_selecionada = None
        self.janela_progresso = builder.get_object("janela_progresso")
        self.bt_parar_busca = builder.get_object("bt_parar_busca")
        self.barra_progresso = builder.get_object("barra_progresso")
