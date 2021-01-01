class WidgetsLogin():
    def start_widgets(self, builder, *args):
        # -- Janela Login
        self.janela_login = builder.get_object("janela_login")
        self.janela_login.show_all()
        self.cod_usuario_logado = None
        
         # -- Janela Modulos
        self.janela_modulos = builder.get_object("janela_modulos")
    
        # -- Janela Config Servidor
        self.janela_config_servidor = builder.get_object("janela_config_servidor")
        self.entry_servidor = builder.get_object("entry_servidor")
        self.entry_email_servidor = builder.get_object("entry_email_servidor")
        self.cmb_tipo_conexao = builder.get_object("cmb_tipo_conexao")
        self.lst_tipo_conexao_servidor = builder.get_object("lst_tipo_conexao_servidor")
        self.entry_porta_servidor = builder.get_object("entry_porta_servidor")
        self.entry_senha_email = builder.get_object("entry_senha_email")
        
        # -- Message Dialog
        self.msg_dialog = builder.get_object("msg_dialog")
        
        # -- Entry
        self.entry_usuario = builder.get_object("entry_usuario")
        self.entry_senha = builder.get_object("entry_senha")
        
        # -- Lista
        self.lst_empresa = builder.get_object("lst_empresa")	
        
        # -- ComboBox
        self.cmb_empresa = builder.get_object("cmb_empresa")
