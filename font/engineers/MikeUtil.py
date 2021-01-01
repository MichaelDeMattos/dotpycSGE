#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
import os
import re
import datetime
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class MikeGtk(object):
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # >> Simples MessageBox/MessageDialog
    def simple_msg_box(self, component, title, text, icon=None, *args):
        component.props.text = (title)
        component.props.secondary_text = (text)
        component.props.icon_name = (icon)
        component.show_all()
        component.run()
        component.hide()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # >> Estilos e Persolalização
    def style_app(self, style_path, set_screen, *args):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(style_path)
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(set_screen.get_default(),
                                              css_provider,
                                              Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # >> Retorna a data atual em formato pt-br
    def format_current_date(self, *args):
        date_today = datetime.date.today()
        date_today_format = ("{}/{}/{}").format("0" + str(date_today.day) if int(date_today.day) < 10 else str(date_today.day),
                                                "0" + str(date_today.month) if int(date_today.month) < 10 else str(date_today.month),
                                                date_today.year)
        return str(date_today_format)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # >> Retorna uma string formatada sem espaços duplicados
    def format_str_not_space(self, string, upper=False):
        text_format = re.sub(r"^\s+|\s+$", "", string)
        text_format = " ".join(text_format.split())
        if upper == False:
            return text_format
        else:
            return text_format.upper()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # >> Retorna o RG formatado
    def format_rg(self, rg):
        # LAYOUT => xx.xxx.xxx-x
        replace_dot = rg.replace(".", "")
        replace_digit = replace_dot.replace("-", "")
        
        rg_rough = replace_digit
        
        xx = None # xx
        xxx1 = None # xxx
        xxx2 = None # xxx
        x = None # x
        
        count_str = len(rg_rough)
        if count_str < 9:
            return 0
            
        else:
            xx = int(rg_rough[0:2])
            xxx1 = int(rg_rough[2:5])
            xxx2 = int(rg_rough[5:8])
            x = rg_rough[8]
            rg_format = str(xx) + "." + str(xxx1) + "." + str(xxx2) + "-" + x
            
            return rg_format
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # >> formata N° de Celular
    def format_cellfone(self, codeCountry, numberCellFone):
        # layout = +xx (xxx) x xxxx-xxxx
        pass
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # >> formata N° de Telefone
    def format_fone(self, codeCountry, numberFone):
        # layout = +xx (xxx) xxxx-xxxx
        pass
