#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Filename     : prnsnmpc.py
# version      : 1.0
# Created By   : James Dunne (HP UK&I Technology Consultant)
# Created Date : 09/05/2022
# ----------------------------------------------------------------------------
# import modules
from functions import nagini_snmp as nagini_snmp
from functions import nagini_csv as nagini_csv
from functions import nagini_log as nagini_log
from functions import nagini_dir as nagini_dir
from pysnmp import hlapi  # Import Standard Python Modules.
def prn_snmp_chk(prn_file, snmp_file):

    """
    Function to match and test snmp passwords from csv files.
    Function will test matched passwds against printers.
    """
    
    prn_info = {}  # Blank dict for storing printer info.

    snmp_passwd = {}  # Blanks dict for storing snmp info.

    prn_output = []  # Blank list to store the dicts for fileout.

    prn_csv = nagini_csv.csv_import(prn_file)  # Define Printer CSV Input File.

    snmp_csv = nagini_csv.csv_import(snmp_file)  # Define SNMP CSV Input File.

    serial_oid = '1.3.6.1.2.1.43.5.1.1.17.1'

    env_chk(prn_file, snmp_file)  # Check Printer and SNMP input files exist.

    prn_count = 1  # Set the Printer count to 1.

    prn_qty = len(prn_csv)  # Count total printers.

    for line in snmp_csv:

        site_tri = line['Trigram']  # Define Site Trigram

        snmpg_cs = line['SNMPGet']  # Define Site SNMPGet Password.

        # Add site tri as key and SNMP Password as value to dict.
        snmp_passwd[site_tri] = snmpg_cs

    for printer in prn_csv:  # start looping through all class methods per printer.

        prn_tri = printer['Trigram']  # Define printer trigram.

        prn_ip = printer['PrinterIP']  # Define Printer IP Address.

        prn_snmpg = printer['SNMPGet']  # Define Printer SNMPGet Password.

        print('---------------------------------------------------------------' +
              '-------------------------------------------------------')

        print(f' Printer {prn_count} of {prn_qty}')

        prn_count += 1  # Increase Printer Count by 1.

        # Loop through dict and find prn tri in snmp_passwd dict.
        if prn_tri in snmp_passwd.keys():

            print(f' SNMP Community String Found for Site Printer Is Located On!')

        else:  # If no SNMP Password is matched in the snmp_passwd dict, use default passwd.
            # Default password is taken from printer input csv SNMPGet Password field.

            print(f' * Printer IP: {prn_ip}')

            print(f' * No Valid SNMP Community String Matched To Printer + Location!')

            print(
                f' * Using Printer Default SNMP Community String: {prn_snmpg}')

            print('---------------------------------------------------------------' +
                  '-------------------------------------------------------')

            print(f' Starting Printer SNMP interrogation on IP: {str(prn_ip)}')

            print('---------------------------------------------------------------' +
                  '-------------------------------------------------------')

            # Use the MAC Address SNMP OID to test passwd.
            #prn_mac = snmp_func.snmpmac(prn_ip, prn_snmpg)
            #print(f' * Printer MAC Address: {str(prn_mac)}')
            try:
                  # Using SNMPv2c, we retrieve the serial of the remote device.
                  prn_sn = nagini_snmp.get(
                  prn_ip, [serial_oid], hlapi.CommunityData(prn_snmpg))
                  print(f' * Printer Serial: {str(prn_sn[serial_oid])}')
            except RuntimeError:
                  return error_msg()
            prn_info['TRIGRAM'] = prn_tri  # Add TRI to prn_info dict.

            # Add device ip to prn_info dict.
            prn_info['IP Address'] = str(prn_ip)

            # Add SNMP GET Community String (Password) to dict.
            prn_info['SNMPGet'] = str(prn_snmpg)

            prn_info['Serial'] = str(prn_sn[serial_oid])  # Add SNMP Result to dict.

            # Append populated prn_info dictionary to list.
            prn_output.append(prn_info)

            # Write prnolutput list/dict to csv file.
            # Usage: <function>(output_dir, filename, fileformat)
            nagini_csv.prn_snmpchk_csv_output(
                prn_output, 'output', 'prn_snmpchk_output', '.csv')

            prn_info.clear()  # Clear prn_info dict.

            prn_output.clear()  # Clear prn_output list.

        # Loop through site snmp_passwd dict.
        for site_tri, site_passwd in snmp_passwd.items():

            # If prn_tri matches site_tri then set snmp_get to site passwd.
            if prn_tri == site_tri:  

                snmp_get = site_passwd  # Set snmp_get to site password value.

                print(f' Using Printer SNMP Community String: {snmp_get}')

                print(
                    f' Starting Printer SNMP interrogation on IP: {str(prn_ip)}')

                print('---------------------------------------------------------------' +
                      '-------------------------------------------------------')
                try:
                  # Using SNMPv2c, we retrieve the serial of the remote device.
                  prn_sn = nagini_snmp.get(
                  prn_ip, [serial_oid], hlapi.CommunityData(snmp_get))
                  print(f' * Printer Serial: {str(prn_sn[serial_oid])}')
                except RuntimeError:
                  return error_msg()
                # Add TRI to prninfo dict.
                prn_info['TRIGRAM'] = prn_tri

                # Add device ip to prninfo dict.
                prn_info['IP Address'] = str(prn_ip)

                # Add SNMP GET Community String (Password) to dict.
                prn_info['SNMPGet'] = str(snmp_get)

                # Add SNMP Result to dict.
                prn_info['Serial'] = str(prn_sn[serial_oid])

                # Append populated prninfo dictionary to list.
                prn_output.append(prn_info)

                # Write prnoutput list/dict to csv file.
                # Usage: <function>(contents, output_dir, filename, fileformat)
                nagini_csv.prn_snmpchk_csv_output(
                    prn_output, 'output', 'prn_snmpchk_output', '.csv')

                # Clear prninfo dict.
                prn_info.clear()

                # Clear prnoutput list.
                prn_output.clear()
    end_msg()

def env_chk(prn_file, snmp_file):

    """
    Function to check directories and files exist.
    """

    # Check files and directories in the environment.

    print('---------------------------------------------------------------' +
          '-------------------------------------------------------')

    print(f' Checking {prn_file} exists before starting the tool.')

    print('---------------------------------------------------------------' +
          '-------------------------------------------------------')

    nagini_csv.csv_chk(prn_file)  # Check csv file is present and available.

    # Check files and directories in the environment.

    print('---------------------------------------------------------------' +
          '-------------------------------------------------------')

    print(f' Checking {snmp_file} exists before starting the tool.')

    print('---------------------------------------------------------------' +
          '-------------------------------------------------------')

    nagini_csv.csv_chk(snmp_file)  # Check csv file is present and available.

    # Check if log directory exists and create if not.

    print('---------------------------------------------------------------' +
          '-------------------------------------------------------')

    print(f' Checking log folder exists before starting the tool.')

    print('---------------------------------------------------------------' +
          '-------------------------------------------------------')

    nagini_dir.chk_log_dir('logs')  # Specify logs directory

    # Check if output directory exists and create if not.

    print('---------------------------------------------------------------' +
          '-------------------------------------------------------')

    print(f' Checking ouput folder exists before starting the tool.')

    print('---------------------------------------------------------------' +
          '-------------------------------------------------------')

    nagini_dir.chk_output_dir('output')  # Specify output directory.

    # Write csv header fields to csv file in output directory.
    # Usage: <function>(output_dir, filename, fileformat, header type)
    nagini_csv.csv_header('output', 'prn_snmpchk_output', '.csv', 'prn_snmpc')

def error_msg():
      
      """
      Function to display error information.
      """

      error_msg = (f' * RuntimeError: Check IP Address and SNMP '

                        f'Community Name Are Correct!')

      print(" * RuntimeError: Most Likely No SNMP Response Received Before Timeout!")

      print(" * RuntimeError: Check IP Address and SNMP Community Name Are Correct!")

      nagini_log.logw('snmpc_log', error_msg)

def end_msg():

      """
      Function to display end of operation message.
      """

      print('---------------------------------------------------------------' +
                '-------------------------------------------------------')

      print(" The programmed operations completed! Check output & logs for results.")

      print('---------------------------------------------------------------' +
            '-------------------------------------------------------')

# ---------------------------------------------------------------------
#  Class Calls.
#  Class Usage: main()
# ---------------------------------------------------------------------
#prn_snmpc = prn_snmp_chk('printers.csv','passwords.csv' )