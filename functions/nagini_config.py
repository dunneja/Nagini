#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Filename     : nagini_config.py
# Author       : James Dunne <james.dunne1@gmail.com>
# License      : LGPL-3.0-only
# Comment      : This file is part of Nagini.
# ----------------------------------------------------------------------------

""" Config file class. """

# Import python core modules.
import os.path
from configparser import ConfigParser

class config_file():
    """
    A Class to represent a config file
    """
    def __init__(self, config_file):
        """
        Initialisation
        Define a config file variable.
        """
        self.config_file = config_file

    def check_conf(self):
        """
        Create a conf / ini file if one does not exist
        """
        # Check if the config_file exists.
        if (os.path.isfile(self.config_file)):
            print(f' * File {self.config_file} exists!')
        # If the config_file does not exist then create a template.
        elif (os.path.isfile(self.config_file)) == False:
            print(f'\nFile {self.config_file} does not exist!\n')
            # Create a config layout.
            config = ConfigParser()
            # Read the config file
            config.read(self.config_file)
            # Set the main section variables
            config.add_section('main')
            config.set('main', 'log_dir', 'logs')
            config.set('main', 'output_dir', 'output')
            config.set('main', 'default_snmp_get', 'public')
            # Create Xerox config layout.
            config.add_section('Xerox')
            config.set('Xerox', 'snmp_hostname_oid', '1.3.6.1.2.1.1.5.0') # Hostname.
            config.set('Xerox', 'sys_location_oid', '1.3.6.1.2.1.1.6.0') # Sysloc.
            config.set('Xerox', 'mac_addr_oid', '1.3.6.1.2.1.2.2.1.6.1') # Mac Address.
            config.set('Xerox', 'mono_oid', '1.3.6.1.4.1.253.8.53.13.2.1.6.1.20.34') # Mono.
            config.set('Xerox', 'color_oid', '1.3.6.1.4.1.253.8.53.13.2.1.6.1.20.33') # Color.
            config.set('Xerox', 'total_oid', '1.3.6.1.4.1.253.8.53.13.2.1.6.1.20.1') # Total counts.
            config.set('Xerox', 'hr_Device_Descr_oid', '1.3.6.1.2.1.25.3.2.1.3.1') # Device desc oid.
            config.set('Xerox', 'sys_Descr_oid', '1.3.6.1.2.1.1.1.0') # Sys firmware oid.
            config.set('Xerox', 'serial_oid', '1.3.6.1.2.1.43.5.1.1.17.1') # Serialnumber oid.
            # Create HP config layout.
            config.add_section('HP')
            config.set('HP', 'snmp_hostname_oid', '1.3.6.1.4.1.11.2.3.9.4.2.1.1.3.10.0') # Hostname.
            config.set('HP', 'sys_location_oid', '1.3.6.1.2.1.1.6.0') # Sysloc.
            config.set('HP', 'mac_addr_oid', '1.3.6.1.2.1.2.2.1.6.1') # Mac Address.
            config.set('HP', 'mono_oid', '1.3.6.1.4.1.11.2.3.9.4.2.1.4.1.2.6.0') # Mono.
            config.set('HP', 'color_oid', '1.3.6.1.4.1.11.2.3.9.4.2.1.4.1.2.7.0') # Color.
            config.set('HP', 'total_oid', '1.3.6.1.2.1.43.10.2.1.4.1.1') # Total counts.
            config.set('HP', 'hr_Device_Descr_oid', '1.3.6.1.2.1.25.3.2.1.3.1') # Device desc oid.
            config.set('HP', 'sys_Descr_oid', '1.3.6.1.2.1.1.1.0') # Sys firmware oid.
            config.set('HP', 'serial_oid', '1.3.6.1.2.1.43.5.1.1.17.1') # Serialnumber oid.
            # Write the config layout to an ini file.
            with open('config.ini', 'w') as f:
                config.write(f)
                print(f'Creating file {self.config_file} ...\n')