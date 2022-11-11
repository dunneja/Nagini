#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Filename     : nagini_csv.py
# Author       : James Dunne <james.dunne1@gmail.com>
# License      : GPL-3.0
# Comment      : This file is part of Nagini.
# ----------------------------------------------------------------------------

""" CSV Importer and File checker. Will import/export CSV file into a dictionary. """

# Import modules
import csv
import os
import os.path
from datetime import datetime
from functions import nagini_log

def csv_chk(csv_file):
    """
    Check Printers.csv Configuration File Exists in OS.
    """
    # Check if the csv file exists.
    if (os.path.isfile(csv_file)):
        print(f' * File {csv_file} exists!')
        return (0)
    # If the csv file does not exist then print a message.
    elif (os.path.isfile(csv_file)) == False:
        print(
            f'\n * File {csv_file} does not exist! Unable to read file {csv_file} ...\n')
        emsg = f'File {csv_file} does not exist! Unable to read file {csv_file}'
        nagini_log.logw('syslog', emsg)
        os._exit(0)

def create_prn_csv(input_value):
    """
    Create the Printers.csv input csv file.
    """
    csv_filename = input_value
    try:
        if (os.path.isfile(csv_filename)):
            return (1)
        else:
            with open(csv_filename, 'w') as csv:
                csv.write('Trigram,PrinterIP,SNMPGet')
                csv.close()
    except FileNotFoundError:
        return ("Input File Value Not Found!")

def create_passwd_csv(input_value):
    """
    Create the Passwords.csv input csv file.
    """
    csv_filename = input_value
    try:
        if (os.path.isfile(csv_filename)):
            return (1)
        else:
            with open(csv_filename, 'w') as csv:
                csv.write('Trigram,SNMPGet')
                csv.close()
    except FileNotFoundError:
        return ("Input File Value Not Found!")

def csv_import(csv_input):
    """
    builds a dictionary from the csv specified
    and stores this in a list
    """
    # csv_input is assigned to the csv_filename variable.
    csv_filename = csv_input
    try:
        with open(csv_filename, 'r') as csv_file:
            csv_dict = csv.DictReader(csv_file)
            csv_import = list(csv_dict)
        return csv_import
    except FileNotFoundError:
        msg = f' * Error: Filename {csv_filename} Not Found.'
        print(msg)
        emsg = f'Error: Filename {csv_filename} Not Found.'
        nagini_log.logw('syslog', emsg)

def csv_header(output_dir, csv_name, csv_format, header):
    """
    Write csv headers to a csv output file.
    """
    if header == 'prn_connc':
        header = ['TRIGRAM', 'IP Address', 'HTTPS Check',
                  'Ping Check', 'DNS Resolution', 'Model']
    elif header == 'prn_snmpc':
        header = ['TRIGRAM', 'IP Address', 'SNMPGet', 'Serial']
    else:
        header = ['TRIGRAM', 'Description', 'IP Address', 'MAC Address', 'Hostname',
                  'Location', 'Monocount', 'Colorcount', 'Totalcount', 'Serial',
                  'SNMPGet', 'Firmware']
    # defines the day, month, year.
    file_date = datetime.now().strftime("%d-%m-%Y")
    # concatenate the longfilename.
    file_lfn = csv_name + '_' + file_date + csv_format
    csvoutpath = os.path.join(output_dir, file_lfn)
    # Open csv file and append contents of list/dict as a new line.
    with open(csvoutpath, 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()

def prn_datac_csv_output(outputs, output_dir, csv_name, csv_format):
    """ 
    Writes a list/dict to a csv file.
    """
    header = ['TRIGRAM', 'Description', 'IP Address', 'MAC Address', 'Hostname',
              'Location', 'Monocount', 'Colorcount', 'Totalcount', 'Serial',
              'SNMPGet', 'Firmware']
    # defines the day, month, year.
    file_date = datetime.now().strftime("%d-%m-%Y")
    # concatenate the longfilename.
    file_lfn = csv_name + '_' + file_date + csv_format
    csvoutpath = os.path.join(output_dir, file_lfn)
    prnoutput = outputs  # prndatac output
    # Open csv file and append contents of list/dict as a new line.
    with open(csvoutpath, 'a', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writerows(prnoutput)

def prn_connchk_csv_output(outputs, output_dir, csv_name, csv_format):
    """ 
    Writes a list/dict to a csv file.
    """
    # Define headers for the ouput csv file.
    header = ['TRIGRAM', 'IP Address', 'HTTPS Check',
              'Ping Check', 'DNS Resolution', 'Model']
    # defines the day, month, year.
    file_date = datetime.now().strftime("%d-%m-%Y")
    # concatenate the longfilename.
    file_lfn = csv_name + '_' + file_date + csv_format
    csvoutpath = os.path.join(output_dir, file_lfn)
    prnoutput = outputs  # prndatac output
    # Open csv file and append contents of list/dict as a new line.
    with open(csvoutpath, 'a', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writerows(prnoutput)

def prn_snmpchk_csv_output(outputs, output_dir, csv_name, csv_format):
    """ 
    Writes a list/dict to a csv file.
    """
    # Define headers for the ouput csv file.
    header = ['TRIGRAM', 'IP Address', 'SNMPGet', 'Serial']
    # defines the day, month, year.
    file_date = datetime.now().strftime("%d-%m-%Y")
    # concatenate the longfilename.
    file_lfn = csv_name + '_' + file_date + csv_format
    csvoutpath = os.path.join(output_dir, file_lfn)
    prnoutput = outputs  # prndatac output
    # Open csv file and append contents of list/dict as a new line.
    with open(csvoutpath, 'a', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writerows(prnoutput)