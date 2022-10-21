#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Filename     : guifunc.py
# version      : 1.0
# Created By   : James Dunne (HP UK&I Technology Consultant)
# Created Date : 16/05/2022
# ----------------------------------------------------------------------------
# Import python core modules.
import PySimpleGUI as sg
from core.prn_datac import prn_data_col
from core.prn_connc import prn_conn_chk
from core.prn_snmpc import prn_snmp_chk
from functions.cfg_func import config_file
import threading

def popup_warning(function, input, passwd, vendor):
    
    """
    Warning popup and ini file check function.
    """
    
    ini_file = 'config.ini'
    
    # Pass ini file variable to config_file class.
    conf = config_file(ini_file)
    
    prn_op = function 
    
    value = input
    
    snmp_passwd_file = passwd
    
    prn_conn_c = 'prn_conn_chk'
    
    prn_snmp_c = 'prn_snmp_chk'
    
    prn_data_c = 'prn_data_col'
    
    # Popup to warn user prior to execution. Quit possible.
    popup = sg.PopupYesNo('Are you sure you want to execute?',
                        'This will contact printers directly!', title='Warning!',
                        keep_on_top='True', icon=r'icons/warning.ico', relative_location=(0,0))
    
    if popup == 'Yes':
        
        print('---------------------------------------------------------------' +
              '-------------------------------------------------------')
        
        print(f' Checking {ini_file} exists before starting the tool.')
        
        print('---------------------------------------------------------------' +
              '-------------------------------------------------------')
        
        # Check config file exists and if not create with defaults.
        config_file.check_conf(conf)
        
        if prn_op == prn_conn_c:
            
            #prn_conn_chk(value, ini_file)
            threading.Thread(target=prn_conn_chk, args=(value, ini_file), daemon=True).start()
            
        elif prn_op == prn_snmp_c:
            
            #prn_snmp_chk(value, snmp_passwd_file)
            threading.Thread(target=prn_snmp_chk, args=(value, snmp_passwd_file), daemon=True).start()
            
        elif prn_op == prn_data_c:
            
            #prn_data_col(value, ini_file, vendor)
            threading.Thread(target=prn_data_col, args=(value, ini_file, vendor), daemon=True).start()
            
        else:
            
            print(f'No Operational function provided!\n')
            
    else:
        
        print(f'\nPrinter Connection Checker Operation Aborted!\n')
