#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Filename     : nagini_common.py
# Author       : James Dunne <james.dunne1@gmail.com>
# License      : LGPL-3.0-only
# Comment      : This file is part of Nagini.
# ----------------------------------------------------------------------------

""" Common functions for GUI. """

# Import python core modules.
import threading
import PySimpleGUI as sg

from core.nagini_datac import prn_data_col
from core.nagini_connc import prn_conn_chk
from core.nagini_snmpc import prn_snmp_chk

from functions.nagini_config import config_file
from icons.nagini_icons import warning

# Define Icon base64 strings.
warning_base64 = warning

def popup_warning(function, input, passwd, vendor):
    
    """
    Warning popup and ini file check function.
    """
    
    ini_file = 'conf/config.ini'
    
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
                        keep_on_top='True', icon=warning_base64, relative_location=(0,0))
    
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