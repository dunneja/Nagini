# Printer Connection Test & Data Collector Tool.

 - This GUI tool was designed to test HP & Xerox Printer Connectivity, and to collect HP/Xerox printer mib information.

## Table of Contents

* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Setup](#setup)
* [Usage](#usage)
* [Contact](#contact)

## General Information

- This project was developed for the requirements of a large customer with an inconsistent fleet configuration.
- The purpose of this project is to enable the customer to perform discovery on HP & Xerox Devices on the existing printer estate.
- Due to the technical challenges around device configurations, a tool was required to enable the team to feed in 30,000 IP's, and 1500+ SNMP Community strings from a CSV file based on a location identifier. 
- Some printers had ICMP turned off. 
- All printers allowed HTTP(s) Connections. 
- Printers hostname was unique - DNS FQDN naming convention partly used the printer vendor name. This could be used to identify printer type during discovery.
- This tool tests printer connectivity via ICMP, HTTP/s and DNS, it also collects device information via SNMP and outputs results to a csv file for analysis.

## Technologies Used

- Python - version >=3.10.5 - https://docs.python.org/3/
    - Modules - https://docs.python.org/3/tutorial/modules.html
        - csv - https://docs.python.org/3/library/csv.html#module-csv
        - os - https://docs.python.org/3/library/os.html#module-os
        - os.path - https://docs.python.org/3/library/os.path.html
        - datetime - https://docs.python.org/3/library/datetime.html
        - pysnmp - https://pypi.org/project/pysnmp/
        - sys -  https://docs.python.org/3/library/sys.html
        - re - https://docs.python.org/3/library/re.html#module-re
        - clipboard - https://pypi.org/project/clipboard/
        - PySimpleGUI - https://www.pysimplegui.org/en/latest/
        - requests - https://pypi.org/project/requests/
        - pysnmp - https://pysnmp.readthedocs.io/en/latest/
        - urllib3 - https://pypi.org/project/urllib3/

## Features

The tool provides the following capabilities:

* Printer Connection Checker. (Is there a printer on the IP? What Type?)
  - Ingest Printer information from CSV (Location ID, Printer IP, Vendor Default SNMP Community String). 
  - Test Printer Connectivity via ICMP Ping.
  - Test Printer Connectivity via HTTP(s) Request. (Some Devices had ICMP Disabled but HTTP enabled).
  - HTTP check will do a web scrape and look for HP/Xerox identifiers to see what type of vendor the web service is running on. 
  - Resolve Printer DNS to FQDN. (Customer used naming conventions for each printer vendor to allow for identification via CSV analaysis). 
  - Output of results / information to csv format.
  - Output of logging for all functions to txt file.

* SNMP Password Checker / Brute Forcer. (What Password matches what location/printer?)
  - Ingest SNMP Community passwords from csv (Location ID, SNMP Community String for Site).
  - Ingest Printer information from csv (Location ID, Printer IP, Vendor Default SNMP Community String). 
  - This function will try to match the printer csv Location ID, to the passwords csv Location ID. 
  - If there is a location match between printers and passwords, matched SNMP Community string ID will be used.
  - If no match then it defaults to the printers default SNMP password in printers csv.
  - The function will use either the location matched SNMP password, or the vendor default SNMP password to try and extract the printer serial number with said password.
  - If the SNMP Password used doesn't work, the serial value in output csv will be blank. 
  - Output of results / information to csv format.
  - Output of logging for all functions to txt file.

* SNMP Printer Data Collector (IPs and SNMP Passwords from previous two features can be fed into this DCA!)
  - Ingest Printer information from CSV (Location ID, Printer IP, SNMP Community String).
  - The tool is designed to collect the following SNMP OID data;
    - Site Code (Trigram)
    - Device Description (Model)
    - IP Address
    - MAC Address
    - Hostname
    - Location
    - Mono Counts
    - Color Counts
    - Total Counts
    - Serial
    - SNMPGET Community String
    - System Information (Firmware Versions)
  - Output of results / information to csv format.
  - Output of logging for all functions to txt file.

* CSV File Viewer
  - Feature allows to select a CSV and then presents the information in a GUI Table. 
  - Designed to be used if tool is being executed from a server with no excel for example.
  - Easier to view thousands of entries when not on a desktop. 
 
## Screenshots

![Example screenshot](./screenshots/Nagini-SS-01.png)

![Example screenshot](./screenshots/Nagini-SS-02.png)

![Example screenshot](./screenshots/Nagini-SS-03.png)

![Example screenshot](./screenshots/Nagini-SS-04.png)

![Example screenshot](./screenshots/Nagini-SS-05.png)

![Example screenshot](./screenshots/Nagini-SS-06.png)

![Example screenshot](./screenshots/Nagini-SS-07.png)

## Setup

* Setup the project from source files;

    - Download and install Python >=3.10.5 from https://www.python.org/downloads/

    - Ensure Python is added to environment SYS Path.

    - Clone this repo to local file system.

    - Install deps from the provided requirements.txt file as per below;
        
        ```
        pip3 install -r requirements.txt
        ```

## Usage

* Running the project from source files;

    - Ensure all Dependencies are installed.
    - Populate the CSV file(s) as per the example entry provided. 
    - Run 
     ```
    'python -m  nagini' 
     ```
    - Check Output dir for output results and logs dir for error logs. 

## Notes

   - All of the code is tested and the tool works.
   - Some of the code still needs refactoring into a decent state, i was in a rush! :o)
   - Some of the information on this README, and comments in code was to accomodate Code / Security Reviews.
   - I'm not responsible for how this tool is used.
