#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Filename     : logfunc.py
# version      : 1.0
# Created By   : James Dunne (HP UK&I Technology Consultant)
# Created Date : 14/03/2022
# ----------------------------------------------------------------------------
# Import Python Modules.
from datetime import datetime

def logw(stdout_lfn, output):
    
    """
    function to write output to txt log file.
    """
    
    #log file date time format
    file_dt = datetime.now().strftime("%d-%m-%Y")
    
    #log file directory
    log_dir = 'logs'
    
    #log file format
    log_format = '.txt'
    
    #stdout final log file
    stdout_lf = log_dir + '/' + stdout_lfn + '_' + file_dt + log_format
    
    #write stdout list to log file
    try:
        
        with open(stdout_lf, 'a') as fout:
            
            fout.write(
                str(datetime.now().strftime("%d-%m-%Y_%I-%M-%S-%p")))
            
            fout.write(" %s\n" % output)
            
    except FileNotFoundError:
        
        print(' * Error: No such file or directory!')
