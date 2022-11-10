#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Filename     : nagini.py
# Author       : James Dunne <james.dunne1@gmail.com>
# License      : LGPL-3.0-only
# Comment      : This file is part of Nagini.
# ----------------------------------------------------------------------------

""" Check DIR functions. """

# Import modules.
import os
from functions import nagini_log


def chk_log_dir(log_dir):
    
    """
    check if the log dir exists if not make.
    """
    
    if (os.path.isdir(log_dir)):
        
        print(f' * {log_dir} directory exists!')
        
    else:
        
        try:
            
            print(f" * {log_dir} directory doesn't exist!")
            
            os.mkdir(log_dir)
            
            print(f' * Sucessfully created the {log_dir} directory.')
            
            emsg = f'Sucessfully created the {log_dir} directory.'
            
            nagini_log.logw('sys_log', emsg)
            
        except OSError:
            
            print(f' * Creation of the {log_dir} directory failed.')

def chk_output_dir(output_dir):
    
    """
    check if the output dir exists if not make.
    """
    
    if (os.path.isdir(output_dir)):
        
        print(f' * {output_dir} directory exists!')
        
    else:
        
        try:
            
            print(f" * {output_dir} directory doesn't exist!")
            
            os.mkdir(output_dir)
            
            print(f' * Sucessfully created the {output_dir} directory.')
            
            emsg = f'Sucessfully created the {output_dir} directory.'
            
            nagini_log.logw('sys_log', emsg)
            
        except OSError:
            
            print(f' * Creation of the {output_dir} directory failed.')
            
            emsg = f' * Creation of the {output_dir} directory failed.'
            
            nagini_log.logw('sys_log', emsg)
