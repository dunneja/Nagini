#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Filename     : nagini_connc.py
# Author       : James Dunne <james.dunne1@gmail.com>
# License      : LGPL-3.0-only
# Comment      : This file is part of Nagini.
# ----------------------------------------------------------------------------

""" Printer PING, DNS and HTTPS Checker, Class Tests Printer Connectivity """

# Import modules.
import platform
import requests
import urllib3
import socket
from subprocess import PIPE, run

# Import self coded functions.
from functions import nagini_csv
from functions import nagini_log
from functions import nagini_global

class prn_conn_chk():
    """
    Class to check printer web service operation status.
    """
    def __init__(self, csv_file, config_file):
        self.config_file = config_file # Define config file.
        self.csv_file = csv_file # Define CSV file Variable.
        nagini_global.env_chk(self.config_file, self.csv_file)  # Check file and directories exist.
        self.results = {} # Dictionary for results to be stored.
        self.output = [] # List for Results Dictionary to be stored.
        self.printers = nagini_csv.csv_import(self.csv_file)  # Feed csv.
        prn_count = 1 # Set the Printer count to 1.
        prn_qty = len(self.printers) # Count total printers.
        # Write csv header fields to csv file in output directory.
        # Usage: <function>(output_dir, filename, fileformat, header type)
        nagini_csv.csv_header('output', 'prn_connchk_output', '.csv', 'prn_connc')
        for printer in self.printers:  # Loop through printers.
            self.trigram = printer['Trigram'] # Define Trigram.
            self.dev_ip = printer['PrinterIP'] # Define Printer IP.
            # start looping through all class methods per printer.
            print('---------------------------------------------------------------' +
            '-------------------------------------------------------')
            print(f' Printer {prn_count} of {prn_qty}')
            print(f' Starting Printer Connection Checks on Host: {str(self.dev_ip)}')
            #print('---------------------------------------------------------------')
            prn_count += 1 # Increase Printer Count by 1.
            self.results['IP Address'] = self.dev_ip # Append IP to Dict.
            self.results['TRIGRAM'] = self.trigram # Append TRI to Dict.
            self.prn_web_chk(self.dev_ip) # Call Webchk method.
            self.output.append(self.results) # Append results to Dict.
            # Write output to csv file.
            nagini_csv.prn_connchk_csv_output(self.output, 'output', 'prn_connchk_output', '.csv')
            # Clear results dict.
            self.results.clear()
            # Clear output list.
            self.output.clear()
        nagini_global.end_msg()

    def prn_web_chk(self, dev_ip):
        """
        Method to check printer connectivity via PING, DNS and HTTPS.
        """
        remote_device_url = 'https://' + dev_ip  # final string.
        # Vendor Description and response variables.
        xrx = 'Xerox'
        xrx_response = ' * Printer: Xerox Found!'
        hp = 'HP'
        hp_response = ' * Printer Vendor: HP Found!'
        # Disable SSL cert warnings via the urllib3 module.
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        # Used to set the default cipher, weak DH_KEY on remote servers cause issues.
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'
        try:
            self.ping_chk(self.dev_ip)
            print("---------------------------------------------------------------" +
            '-------------------------------------------------------')
            print(f' Starting HTTPS requests on URL: {str(remote_device_url)}')
            print("---------------------------------------------------------------"+
            '-------------------------------------------------------')
            #verify flag here forces the ignoring of self signed ssl certs.
            response = requests.get(
                remote_device_url, verify=False, timeout=60)
            if response.status_code == 200:  # Finds the OK response.
                print(" * Web Service Status: HTTPS Connection OK! HTTPS Running!")
                self.results['HTTPS Check'] = str('Online')
                if (str(response.content).find(xrx) != -1):
                    print(xrx_response)
                    self.results['Model'] = xrx
                elif (str(response.content).find(xrx.lower()) != -1):
                    print(xrx_response)
                    self.results['Model'] = xrx
                elif (str(response.content).find(xrx.upper()) != -1):
                    print(xrx_response)
                    self.results['Model'] = xrx
                elif (str(response.content).find(hp) != -1):
                    print(hp_response)
                    self.results['Model'] = hp
                elif (str(response.content).find(hp.lower()) != -1):
                    print(hp_response)
                    self.results['Model'] = hp
                elif (str(response.content).find(hp.upper()) != -1):
                    print(hp_response)
                    self.results['Model'] = hp
                else:
                    print(" * Other Device Using Active Web Service!")
                    self.results['Model'] = str('Other')
                    # print(response) #for troubleshooting only.
                    # print(response.content)
            elif response.status_code == 404:  # Finds the Error response.
                print(" * HTTP 404! Reboot Device.")
                self.results['HTTPS Check'] = str('HTTP 404')
                self.results['Model'] = 'None'
            else:
                print(" * HTTPS Not Running!")
                # print(response) #for troubleshooting only.
                self.results['HTTPS Check'] = str('Offline')
                self.results['Model'] = 'None'
        except requests.exceptions.ConnectionError:
            print(" * HTTPS Connection Error: Unable to Connect to remote device!")
            self.results['HTTPS Check'] = str('Offline')
            self.results['Model'] = 'None'
            emsg = (f'HTTPS Connection Error: Unable to Connect to remote device '
            f'{self.dev_ip}')
            nagini_log.logw('conn_log', emsg)

    def ping_chk(self, host):
        """
        Returns True if host (str) responds to a ping request.
        Remember that a host may not respond to a ping (ICMP) 
        request even if the host name is valid.
        """
        print("---------------------------------------------------------------" +
        '-------------------------------------------------------')
        print(f' Starting ICMP PING requests on Host: {str(host)}')
        print("---------------------------------------------------------------" +
        '-------------------------------------------------------')
        # Option for the number of packets as a function of
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        # Building the command. Ex: "ping -c 1 <dev_ip>"
        command = ['ping', param, '1', host]
        # running the results through stdout and strerr.
        result = run(command, stdout=PIPE, stderr=PIPE,
                     universal_newlines=True)
        #print(" * Ping Return Code: " + str(result.returncode))
        #print(str(result.stdout) + str(result.stderr))
        if result.returncode == 0:
            print(" * Printer Ping Result: Ping Successful!")
            self.results['Ping Check'] = str('Online')
            self.dns_lookup(host)
        else:    
            print(" * Printer Ping Result: No Response!")
            self.results['Ping Check'] = str('Offline')
            self.dns_lookup(host)

    def dns_lookup(self, dev_ip):
        """ 
        Use socket module to resolve ip address to hostname
        """
        try:
            print("---------------------------------------------------------------" +
            '-------------------------------------------------------')
            print(f' Starting DNS Lookup on Host: {dev_ip}')
            print("---------------------------------------------------------------" +
            '-------------------------------------------------------')
            self.dns = socket.gethostbyaddr(dev_ip)
            print(f' * DNS Hostname: {self.dns[0]}')
            self.results['DNS Resolution'] = str(self.dns[0])
        except socket.herror:
            print(f' * DNS Hostname: Unable to resolve DNS.')
            emsg = f'DNS Hostname: Unable to resolve DNS for {dev_ip}'
            nagini_log.logw('conn_log', emsg)
            csv_result = 'Unresolved'
            self.results['DNS Resolution'] = str(csv_result)