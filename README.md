# HP & Xerox Printer Connection Tester & Data Collector Tool.
 - This console tool was designed to collect Xerox printer MI information for MPS discovery purposes.

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Setup](#setup)
* [Usage](#usage)
* [Contact](#contact)

## General Information
- This project was developed for the requirements of a customer in the UK&I.
- The customer has 30,000 devices with 1500+ SNMP Get community Passwords. This meant that HP WJA was unable to be used for collecting device information.
- The purpose of this project is to enable the HP UK&I MPS team to perform discovery on Xerox Devices on the customer printer estate.
- Due to the technical challenges around device configurations, a tool was required to enable the team to feed in 30,000 IP's and SNMP Community strings from a CSV file.
- This tool collects device information via SNMP and outputs to a csv file for analysis.

## Technologies Used
- Python - version 3.10.4 - https://docs.python.org/3/
    - Modules - https://docs.python.org/3/tutorial/modules.html
        - csv - https://docs.python.org/3/library/csv.html#module-csv
        - os - https://docs.python.org/3/library/os.html#module-os
        - os.path - https://docs.python.org/3/library/os.path.html
        - datetime - https://docs.python.org/3/library/datetime.html
        - pysnmp - https://pypi.org/project/pysnmp/
        - sys -  https://docs.python.org/3/library/sys.html
        - re - https://docs.python.org/3/library/re.html#module-re
- Pyinstaller - version 4.10 - https://pyinstaller.readthedocs.io/en/stable/ (Only used to create EXE from *.py files)

## Features
The tool provides the following capabilities:

- Import of information from csv format.
- Output of information in csv format.
- Output of logging for all functions to txt file.
- The tool is designed to collect the following SNMP OID data;
    - Site Code (Trigram)
    - Device Description (Model)
    - IP Address
    - MAC Address
    - Hostname
    - Location
    - MonoCounts
    - ColorCounts
    - TotalCounts
    - Serial
    - SNMPGET Community String
    - System Information (Firmware Versions)

## Screenshots
![Example screenshot](./img/screenshot1.PNG)

![Example screenshot](./img/screenshot2.PNG)

## Setup
The project dependencies as are follows;

- Python - version 3.10.4 - https://docs.python.org/3/
    - Modules - https://docs.python.org/3/tutorial/modules.html
        - csv - https://docs.python.org/3/library/csv.html#module-csv
        - os - https://docs.python.org/3/library/os.html#module-os
        - os.path - https://docs.python.org/3/library/os.path.html
        - datetime - https://docs.python.org/3/library/datetime.html
        - pysnmp - https://pypi.org/project/pysnmp/
        - sys -  https://docs.python.org/3/library/sys.html
        - re - https://docs.python.org/3/library/re.html#module-re

* Setup the project from source files;

    - Download and install Python 3.10.4 from https://www.python.org/downloads/

    - Ensure Python is added to environment SYS Path.

    - Install deps from the provided requirements.txt file as per below;
 
        - pip3 install -r requirements.txt

    - Extract prndatac_src.zip

* Setup the project from binary file;

    - Unzip prndatac_bin.zip

## Usage
* Running the project from source files;

    - Ensure all Dependencies are installed.
    - Populate the CSV file as per the example entry provided. 
    - Run 'python prndatac.py'
    - Check Output dir for output and logs for errors. 

* Running the project from EXE;

    - Populate the CSV file as per the example entry provided. 
    - Run the EXE file 'prndatac.exe' 
    - Check Output dir for output and logs for errors.

## Contact
Created by James Dunne, Technology Consultant - HP UK&I - James.Dunne@hp.com
