#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Filename     : csvtable.py
# version      : 1.0
# Created By   : James Dunne (HP UK&I Technology Consultant)
# Created Date : 14/03/2022
# ----------------------------------------------------------------------------
import PySimpleGUI as sg
import csv

def csv_viewer():

    # Show CSV data in Table
    sg.theme('Reddit')

    filename = sg.popup_get_file('filename to open', no_window=True, icon=r'icons/printer64.ico', file_types=(("CSV Files","*.csv"),))

    # --- populate table with file contents --- #
    if filename == '':

        return

    data = []

    header_list = []

    button = sg.popup_yes_no('Does this file have column names already?', icon=r'icons/warning.ico')

    if filename is not None:

        with open(filename, "r") as infile:

            reader = csv.reader(infile)

            if button == 'Yes':

                header_list = next(reader)

            try:

                data = list(reader)  # read everything else into a list of rows

                if button == 'No':

                    header_list = ['column' + str(x) for x in range(len(data[0]))]

            except:

                sg.popup_error('Error reading file', icon=r'icons/warning.ico')

                return

    sg.set_options(element_padding=(0, 0))

    layout = [[sg.Table(values=data,
                            headings=header_list,
                            max_col_width=25,
                            auto_size_columns=True,
                            justification='right',
                            alternating_row_color='lightblue',
                            num_rows=min(len(data), 20))]]

    window = sg.Window('CSV Viewer', layout, grab_anywhere=False, keep_on_top='True', icon=r'icons/printer64.ico', relative_location=(0,0))

    event, values = window.read()
    
    window.close()