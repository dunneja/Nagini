#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Filename     : nagini_global.py
# Author       : James Dunne <james.dunne1@gmail.com>
# License      : LGPL-3.0-only
# Comment      : This file is part of Nagini.
# ----------------------------------------------------------------------------

""" Global / Common functions used by all Nagini modules. """

# Import modules.
import configparser

# Import self coded functions.
from functions import nagini_csv,nagini_dir,nagini_log

def env_chk(config_file, csv_file):
    """
    Method to check directories and files exist.
    """
    # Define config file.
    config_file = config_file
    # Read the config_file contents.
    config = configparser.ConfigParser()
    config.read(config_file)
    csv_file = csv_file # Define CSV file Variable.
    # Check if log directory exists and create if not.
    print("---------------------------------------------------------------" +
         '-------------------------------------------------------')
    print(f' Checking log folder exists before starting the tool.')
    print("---------------------------------------------------------------" +
         '-------------------------------------------------------')
    log_dir = config.get('main', 'log_dir')
    nagini_dir.chk_log_dir(log_dir)  # Specify logs directory
    # Check if output directory exists and create if not.
    print("---------------------------------------------------------------" +
         '-------------------------------------------------------')
    print(f' Checking ouput folder exists before starting the tool.')
    print("---------------------------------------------------------------" +
         '-------------------------------------------------------')
    output_dir = config.get('main', 'output_dir')
    nagini_dir.chk_output_dir(output_dir)  # Specify output directory.
    # Check csv input file is present and available.
    print("---------------------------------------------------------------" +
         '-------------------------------------------------------')
    print(f' Checking {csv_file} exists before starting the tool.')
    print("---------------------------------------------------------------" +
         '-------------------------------------------------------')
    nagini_csv.csv_chk(csv_file)

def end_msg():
    """
    Method to display end of operation message.
    """
    print("---------------------------------------------------------------" +
         '-------------------------------------------------------')
    print(" The programmed operations completed! Check output & logs for results.")
    print("---------------------------------------------------------------" +
         '-------------------------------------------------------')
