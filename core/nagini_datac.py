#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Filename     : prndatac.py
# version      : 1.0
# Created By   : James Dunne (HP UK&I Technology Consultant)
# Created Date : 14/03/2022
# ----------------------------------------------------------------------------
# Tested Models: Phaser / VersaLink / WorkCentre / DocuCentre / AperosPort-V
# ----------------------------------------------------------------------------
""" Printer SNMP Data Collector Class, Class Collects MIB/SNMP Readings """
# Import python modules.
import configparser  # Import Standard Python Modules.
from pysnmp import hlapi  # Import Standard Python Modules.

# Import functions.
from functions import nagini_csv as nagini_csv  # CSV functions.
from functions import nagini_dir as nagini_dir  # Directory I/O Functions.
from functions import nagini_log as nagini_log  # Logging Function.
from functions import nagini_snmp as nagini_snmp # SNMP functions.

class prn_data_col():
    
    """
    Printer SNMP Data Collector Tool, Collects Xerox MIB/SNMP Readings
    """
    
    def __init__(self, csv_file, config_file, vendor):
        
        # Define config file.
        self.config_file = config_file
        
        # Set csv filename.
        self.csv_file = csv_file  
        
        # Printer vendor name.
        self.vendor = vendor  
        
        # Read the config_file contents.
        config = configparser.ConfigParser()
        config.read(self.config_file)
        
        # '1.3.6.1.2.1.1.5.0' # Hostname.
        self.snmp_hostname_oid = config.get(self.vendor, 'snmp_hostname_oid')
        
        # Syslc.
        self.sys_location_oid = config.get(self.vendor, 'sys_location_oid')
        
        self.mac_addr_oid = config.get(self.vendor, 'mac_addr_oid')  # Mac Address.
        
        self.mono_oid = config.get(self.vendor, 'mono_oid')  # Mono.
        
        self.color_oid = config.get(self.vendor, 'color_oid')  # Color.
        
        self.total_oid = config.get(self.vendor, 'total_oid')  # Total counts.
        
        # Device desc oid.
        self.hr_Device_Descr_oid = config.get(self.vendor, 'hr_Device_Descr_oid')
        
        # Sys firmware oid.
        self.sys_Descr_oid = config.get(self.vendor, 'sys_Descr_oid')
        
        # Serialnumber oid.
        self.serial_oid = config.get(self.vendor, 'serial_oid')
        
        self.prn_info = {}  # Blank dictionary to store output k,v.
        
        self.prn_output = []  # Blank list to store the dicts for fileout.
        
        self.main()  # Call Main Method.

    def main(self):
        
        """
        Main Method to loop through printers and call all other methods!
        """
        
        self.env_chk()
        
        # Feed csv file into csv_import function.
        self.printers = nagini_csv.csv_import(self.csv_file)
        
        prn_count = 1  # Set the Printer count to 1.
        
        prn_qty = len(self.printers)  # Count total printers.
        
        # Loop through csv file and call methods from class.
        for printer in self.printers:
            
            self.trigram = printer['Trigram']
            
            self.dev_ip = printer['PrinterIP']
            
            self.snmp_cs = printer['SNMPGet']
            
            # start looping through all class methods per printer.
            print('---------------------------------------------------------------' +
            '-------------------------------------------------------')
            
            print(f' Printer {prn_count} of {prn_qty}')
            
            print(
                f' Starting Printer SNMP interrogation on IP: {str(self.dev_ip)}')
            
            print('---------------------------------------------------------------' +
            '-------------------------------------------------------')
            
            prn_count += 1  # Increase Printer Count by 1.
            
            # Call methods from the prndatacollector class.
            self.prn_desc()  # Retrieves Printer Description.
            
            self.snmp_hostname()  # Retrieves Printer local hostname.
            
            self.mac_addr()  # Retrieves Printer MAC address.
            
            self.prn_loc()  # Retrieves Printer Location Field.
            
            self.mono_c()  # Retrieves Printer Mono Count.
            
            self.color_c()  # Retrieves Printerc Color Count.
            
            self.total_c()  # Retrieves Printer Total Count.
            
            self.serial()  # Retrieves Printer Serial Number.
            
            # Retrieves Printer System Description / Firmware versions.
            self.sys_desc()
            
            # Add TRI to prninfo dict.
            self.prn_info['TRIGRAM'] = self.trigram
            
            # Add device ip to prninfo dict.
            self.prn_info['IP Address'] = str(self.dev_ip)
            
            # Add SNMP GET Community String (Password) to dict.
            self.prn_info['SNMPGet'] = str(self.snmp_cs)
            
            # append populated prninfo dictionary to list.
            self.prn_output.append(self.prn_info)
            
            # Write prnoutput list/dict to csv file.
            # Usage: <function>(output_dir, filename, fileformat)
            nagini_csv.prn_datac_csv_output(
                self.prn_output, 'output', 'prn_datacol_output', '.csv')
            
            # Clear prninfo dict.
            self.prn_info.clear()
            
            # Clear prnoutput list.
            self.prn_output.clear()
            
        self.end_msg()

    def env_chk(self):
        
        """
        Method to check directories and files exist.
        """
        
        # Check files and directories in the environment.
        print("---------------------------------------------------------------" +
        '-------------------------------------------------------')
        
        print(f' Checking {self.csv_file} exists before starting the tool.')
        
        print("---------------------------------------------------------------" +
        '-------------------------------------------------------')
        
        # Check csv file is present and available.
        nagini_csv.csv_chk(self.csv_file)
        
        # Check if log directory exists and create if not.
        print("---------------------------------------------------------------" +
        '-------------------------------------------------------')
        
        print(f' Checking log folder exists before starting the tool.')
        
        print("---------------------------------------------------------------" +
        '-------------------------------------------------------')
        
        nagini_dir.chk_log_dir('logs')  # Specify logs directory
        
        # Check if output directory exists and create if not.
        print("---------------------------------------------------------------" +
        '-------------------------------------------------------')
        
        print(f' Checking ouput folder exists before starting the tool.')
        
        print("---------------------------------------------------------------" +
        '-------------------------------------------------------')
        
        nagini_dir.chk_output_dir('output')  # Specify output directory.
        
        # Write csv header fields to csv file in output directory.
        # Usage: <function>(output_dir, filename, fileformat)
        nagini_csv.csv_header('output', 'prn_datacol_output', '.csv', 'prn_datac')

    def prn_desc(self):
        
        """
        Method to collect printer description from SNMP OID.
        """
        
        try:
            
            # Using SNMPv2c, we retrieve the hrDeviceDescr of the remote device.
            prn_hrdd = nagini_snmp.get(
                self.dev_ip, [self.hr_Device_Descr_oid], hlapi.CommunityData(self.snmp_cs))
            
            # find the vendor string in the hrDeviceDescr string as provided.
            if (str(prn_hrdd).find(self.vendor) != -1):
                
                print(
                    f' * Device Description: {prn_hrdd[self.hr_Device_Descr_oid]}')
                
                self.prn_info['Description'] = str(
                    prn_hrdd[self.hr_Device_Descr_oid])
                
            # find the vendor string in the hrDeviceDescr string in upper case.
            elif (str(prn_hrdd).find(self.vendor.upper()) != -1):
                print(
                    f' * Device Description: {prn_hrdd[self.hr_Device_Descr_oid]}')
                
                self.prn_info['Description'] = str(
                    prn_hrdd[self.hr_Device_Descr_oid])
                
            # find the vendor string in the hrDeviceDescr string in lower case.
            elif (str(prn_hrdd).find(self.vendor.lower()) != -1):
                
                print(
                    f' * Device Description: {prn_hrdd[self.hr_Device_Descr_oid]}')
                
                self.prn_info = str(prn_hrdd[self.hr_Device_Descr_oid])
                
            else:
                
                # Checking remote device vendor matches oids.
                print(
                    f' * Device Description: Device Model Not A {self.vendor}! '
                    f'{prn_hrdd[self.hr_Device_Descr_oid]} Detected!')
                
                msg = (f'Device Model Not A {self.vendor}! '
                       f'{prn_hrdd[self.hr_Device_Descr_oid]} Detected!')
                
                self.prn_info['Description'] = str(msg)
                
        except RuntimeError:
            
            return self.error_msg()

    def snmp_hostname(self):
        
        """
        Method to collect printer hostname from SNMP OID.
        """
        
        try:
            
            # Using SNMPv2c, we retrieve the snmp hostname of the remote device.
            prn_hn = nagini_snmp.get(
                self.dev_ip, [self.snmp_hostname_oid], hlapi.CommunityData(self.snmp_cs))
            
            print(f' * Printer Hostname: {prn_hn[self.snmp_hostname_oid]}')
            
            self.prn_info['Hostname'] = str(prn_hn[self.snmp_hostname_oid])
            
        except RuntimeError:
            
            return self.error_msg()

    def mac_addr(self):
        
        """
        Method to collect printer MAC address from SNMP OID.
        """
        
        try:
            
            # Using SNMPv2c, we retrieve the mac address of the remote device.
            prn_mac = nagini_snmp.snmpmac(self.dev_ip, self.snmp_cs, self.mac_addr_oid)
            
            print(f' * Printer MAC Address: {str(prn_mac)}')
            
            self.prn_info['MAC Address'] = str(prn_mac)
            
        except RuntimeError:
            
            return self.error_msg()

    def prn_loc(self):
        
        """
        Method to collect printer location information from SNMP OID.
        """
        
        try:
            # Using SNMPv2c, we retrieve the snmp syslocation of the remote device.
            prn_loc = nagini_snmp.get(
                self.dev_ip, [self.sys_location_oid], hlapi.CommunityData(self.snmp_cs))
            
            print(f' * Printer Location: {prn_loc[self.sys_location_oid]}')
            
            self.prn_info['Location'] = str(prn_loc[self.sys_location_oid])
            
        except RuntimeError:
            
            return self.error_msg()

    def mono_c(self):
        
        """
        Method to collect printer mono count value from SNMP OID.
        """
        
        try:
            # Using SNMPv2c, we retrieve the mono count of the remote device.
            prn_mc = nagini_snmp.get(
                self.dev_ip, [self.mono_oid], hlapi.CommunityData(self.snmp_cs))
            
            print(f' * Mono Count: {str(prn_mc[self.mono_oid])}')
            
            self.prn_info['Monocount'] = str(prn_mc[self.mono_oid])
            
        except RuntimeError:
            
            return self.error_msg()

    def color_c(self):
        
        """
        Method to collect printer color count value from SNMP OID.
        """
        
        try:
            
            # Using SNMPv2c, we retrieve the color count of the remote device.
            prn_cc = nagini_snmp.get(
                self.dev_ip, [self.color_oid], hlapi.CommunityData(self.snmp_cs))
            
            print(f' * Color Count: {str(prn_cc[self.color_oid])}')
            
            self.prn_info['Colorcount'] = str(prn_cc[self.color_oid])
            
        except RuntimeError:
            
            return self.error_msg()

    def total_c(self):
        
        """
        Method to collect printer total count value from SNMP OID.
        """
        
        try:
            # Using SNMPv2c, we retrieve total impressions of the remote device.
            prn_tc = nagini_snmp.get(
                self.dev_ip, [self.total_oid], hlapi.CommunityData(self.snmp_cs))
            
            print(f' * Total Count: {str(prn_tc[self.total_oid])}')
            
            self.prn_info['Totalcount'] = str(prn_tc[self.total_oid])
            
        except RuntimeError:
            
            return self.error_msg()

    def serial(self):
        
        """
        Method to collect printer serial number from SNMP OID.
        """
        
        try:
            
            # Using SNMPv2c, we retrieve the serial of the remote device.
            prn_sn = nagini_snmp.get(
                self.dev_ip, [self.serial_oid], hlapi.CommunityData(self.snmp_cs))
            
            print(f' * Printer Serial: {str(prn_sn[self.serial_oid])}')
            
            self.prn_info['Serial'] = str(prn_sn[self.serial_oid])
            
        except RuntimeError:
            
            return self.error_msg()

    def sys_desc(self):
        
        """
        Method to collect printer firmware information from SNMP OID.
        """
        
        try:
            
            # Using SNMPv2c, we retrieve the sysDescr of the remote device.
            prn_sys = nagini_snmp.get(
                self.dev_ip, [self.sys_Descr_oid], hlapi.CommunityData(self.snmp_cs))
            
            print(
                f' * Printer System Description: {str(prn_sys[self.sys_Descr_oid])}')
            
            self.prn_info['Firmware'] = str(prn_sys[self.sys_Descr_oid])
            
        except RuntimeError:
            
            return self.error_msg()

    def error_msg(self):
        
        """
        Method to display error information.
        """
        
        error_msg = (f' * RuntimeError: Check IP Address: {self.dev_ip} and SNMP '
                     f'Community Name: {self.snmp_cs} Are Correct!')
        
        print(" * RuntimeError: Most Likely No SNMP Response Received Before Timeout!")
        
        print(" * RuntimeError: Check IP Address and SNMP Community Name Are Correct!")
        
        nagini_log.logw('data_log', error_msg)

    def end_msg(self):
        
        """
        Method to display end of operation message.
        """
        
        print("---------------------------------------------------------------" +
        '-------------------------------------------------------')
        
        print(" The programmed operations completed! Check output & logs for results.")
        
        print("---------------------------------------------------------------" +
        '-------------------------------------------------------')

# ---------------------------------------------------------------------
#  Class Calls.
#  Class Usage: prndatacollector('csvfile.csv')
# ---------------------------------------------------------------------
#datacollector = prn_data_col('printers.csv', 'config.ini', 'HP')
