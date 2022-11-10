#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Filename     : nagini_csv_view.py
# Author       : James Dunne <james.dunne1@gmail.com>
# License      : LGPL-3.0-only
# Comment      : This file is part of Nagini.
# ----------------------------------------------------------------------------

""" Pysimplegui CSV viewer program """

import PySimpleGUI as sg
import csv

from icons.nagini_icons import warning
from icons.nagini_icons import printer

# Define Icon base64 strings.
warning_base64 = warning
printer_base64 = printer

def csv_viewer():

    # Show CSV data in Table
    sg.theme('Reddit')

    filename = sg.popup_get_file('filename to open', no_window=True, icon=warning_base64, file_types=(("CSV Files","*.csv"),))

    # --- populate table with file contents --- #
    if filename == '':

        return

    data = []

    header_list = []

    button = sg.popup_yes_no('Does this file have column names already?', icon=warning_base64)

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

                sg.popup_error('Error reading file', icon=warning_base64)

                return

    sg.set_options(element_padding=(0, 0))

    layout = [[sg.Table(values=data,
                            headings=header_list,
                            max_col_width=25,
                            auto_size_columns=True,
                            justification='right',
                            alternating_row_color='lightblue',
                            num_rows=min(len(data), 20))]]

    window = sg.Window('CSV Viewer', layout, grab_anywhere=False, keep_on_top='True', icon=printer_base64, relative_location=(0,0))

    event, values = window.read()
    
    window.close()