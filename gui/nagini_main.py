#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Filename     : nagini_main.py
# Author       : James Dunne <james.dunne1@gmail.com>
# License      : LGPL-3.0-only
# Comment      : This file is part of Nagini.
# ----------------------------------------------------------------------------

""" Main Nagini GUI module. """

# Import python core modules.
import os
import clipboard
import PySimpleGUI as sg

# Import classes, methods and functions.
from functions.nagini_csv import create_prn_csv, create_passwd_csv
from functions.nagini_config import config_file

from gui.nagini_csv_view import csv_viewer
from gui.nagini_help import about, github, usage, notice
from gui.nagini_common import popup_warning

from icons.nagini_icons import printer
from icons.nagini_icons import warning

# Define config file variable.
ini_file = 'config.ini'

# Pass ini file variable to config_file class.
conf = config_file(ini_file)

def prn_tool_gui():
    
    """
    Nagini Main GUI Interface
    """
    
    # Define the theme to be used.
    sg.theme('Reddit')
    
    # Define the window top menus.
    menu_def = [['File', ['Generate CSV', ['Printers CSV','Passwords CSV'], 'Quit']],
                ['Edit', ['Paste']],
                ['Help', ['Notice', 'Usage', 'About', 'Github']],]
    
    # Define the window main layout.
    layout = [[sg.Menu(menu_def, tearoff=False)],
            [sg.Text('Select a CSV file containing printer information.')],
            [sg.Text('Printer CSV:', size=(11, 1)), sg.Input(size=(49, 1), default_text='Printers.csv', key='_INPUT_'), sg.FileBrowse(file_types=(("CSV Files", "*.csv"),),)],
            [sg.Text('Password CSV:', size=(11, 1), key='_CSVPTXT_', visible=False), sg.Input(size=(49, 1), default_text='Passwords.csv', key='_CSVPASSWD_', visible=False), sg.FileBrowse(file_types=(("CSV Files", "*.csv"),),visible=False, key='_CSVPFB_')],
            [sg.Radio('Printer Connection Checker', 'Radio1', default='True', key='_PRNCONNCHK_', enable_events=True), sg.Radio('SNMP Passwd Checker', 'Radio1', enable_events=True, key='_PRNSNMPCHK_'), sg.Radio('SNMP Data Collector', 'Radio1', key='_PRNDATACOL_', enable_events=True),],
            [sg.Output(size=(80, 20), key='_OUTPUT_')],
            [sg.Submit(button_text='Start'), sg.Button(button_text='Clear'), sg.Cancel(button_text='Quit'), sg.Text('Vendor Selection:', visible=False, key='_VENDOR_TXT_'), sg.Combo(['Xerox','HP'], default_value='Xerox', size=(20,5), key='_VENDOR_', visible=False), sg.Push(), sg.Button(button_text='View CSV File')], ]
    
    # Icons
    printer_base64 = printer
    warning_base64 = warning

    # Define the main window.
    window = sg.Window('Nagini - Printer Information Collection Tool',
                   layout, icon=printer_base64, relative_location=(0,0), finalize='True')
    
    # Window Event Loops
    while True:
        
        event, values = window.read(timeout=500)
        
        vendor = values['_VENDOR_']
        
        if event == sg.WIN_CLOSED or event == 'Quit':
            
            break
            
        if event == 'View CSV File':
            
            csv_viewer()
            
        if event == 'Start' and values['_PRNCONNCHK_'] == True:
            
            window['_OUTPUT_']('')
            
            prn_conn_chk_input = values['_INPUT_'] 
            
            popup_warning('prn_conn_chk', prn_conn_chk_input,os.devnull, vendor)
            
        if event == 'Start' and values['_PRNDATACOL_'] == True:
            
            window['_OUTPUT_']('')
            
            prn_data_col_input = values['_INPUT_']
            
            popup_warning('prn_data_col', prn_data_col_input,os.devnull, vendor)
            
        if event == 'Start' and values['_PRNSNMPCHK_'] == True:
            
            window['_OUTPUT_']('')
            
            prn_snmp_chk_prn_input = values['_INPUT_']
            
            prn_snmp_chk_passwd_input = values['_CSVPASSWD_']
            
            popup_warning('prn_snmp_chk', prn_snmp_chk_prn_input, prn_snmp_chk_passwd_input, vendor)
            
        if event == 'Clear':
            
            window['_OUTPUT_']('')
            
        if event == "Paste":
            
            text = clipboard.paste()
            
            window['_INPUT_'].Widget.insert("insert", text)
            
        if event == 'About':
            
            about()
            
        if event == 'Usage':
            
            usage()
            
        if event == 'Notice':
            
            notice()
            
        if event == 'Github':
            
            github()
            
        if event == 'Printers CSV':
            
            if create_prn_csv('Printers.csv') == 1:
                
                popup = sg.PopupOK('Printers CSV File Already Exists!',
                        title='Warning!', keep_on_top='True', icon=warning_base64, relative_location=(0,0))
                
            else: 
                
                window['_INPUT_']('Printers.csv')
                
                popup = sg.PopupOK('CSV File Generated!',
                        'Check README for CSV Config options.',
                        title='CSV Template', keep_on_top='True', icon=warning_base64, relative_location=(0,0))
                
        if event == 'Passwords CSV':
            
            if create_passwd_csv('Passwords.csv') == 1:
                
                popup = sg.PopupOK('Passwords CSV File Already Exists!',
                     title='Warning!', keep_on_top='True', icon=warning_base64, relative_location=(0,0))
                
            else:
                window['_CSVPTXT_']('Passwords.csv')
                window['_OUTPUT_']('')
                popup = sg.PopupOK('CSV File Generated!',
                        'Check README for CSV Config options.',
                        title='CSV Template', keep_on_top='True', icon=warning_base64, relative_location=(0,0))
        # When PRNSNMPCHK program is selected - csvfile txt, csv file path and csv file browse button shown.
        if event == '_PRNSNMPCHK_':
            
            window['_CSVPTXT_'].update(visible=True)
            
            window['_CSVPASSWD_'].update(visible=True)
            
            window['_CSVPFB_'].update(visible=True)
            
            window['_VENDOR_TXT_'].update(visible=False)
            
            window['_VENDOR_'].update(visible=False)
            
        # When PRNCONNCHK program is selected, PRNSNMPCHK elements are hidden.
        if event == '_PRNCONNCHK_':
            
            window['_CSVPTXT_'].update(visible=False)
            
            window['_CSVPASSWD_'].update(visible=False)
            
            window['_CSVPFB_'].update(visible=False)
            
            window['_VENDOR_TXT_'].update(visible=False)
            
            window['_VENDOR_'].update(visible=False)
            
        # When PRNDATACOL program is selected, PRNSNMPCHK elements are hidden.
        if event == '_PRNDATACOL_':
            
            window['_CSVPTXT_'].update(visible=False)
            
            window['_CSVPASSWD_'].update(visible=False)
            
            window['_CSVPFB_'].update(visible=False)
            
            window['_VENDOR_TXT_'].update(visible=True)
            
            window['_VENDOR_'].update(visible=True)
            
    window.close()