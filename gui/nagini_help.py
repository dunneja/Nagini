#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Filename     : nagini_help.py
# Author       : James Dunne <james.dunne1@gmail.com>
# License      : GPL-3.0
# Comment      : This file is part of Nagini.
# ----------------------------------------------------------------------------

""" Help Functions """

# Import python core modules.
import PySimpleGUI as sg
from icons.nagini_icons import info
from icons.nagini_icons import git_hub

# Define icon base64 strings
info_base64 = info
git_hub_base64 = git_hub

def about():
    """
    About information.
    """
    popup = sg.popup_no_buttons('Nagini - Printer Information Collection Tool',
                                'Version: 1.0',
                                'Core Components:',
                                '  * Python: >=3.10.5',
                                '  * PySimpleGUI: 4.60.4',
                                'Dependencies:',
                                '  * Clipboard: 0.0.4',
                                '  * Pysnmp: 4.4.12',
                                '  * Requests: 2.28.1',
                                '  * Urllib3: 1.26.12',
                                title='About', keep_on_top='True', icon=info_base64,
                                relative_location=(0, 0))

def usage():
    """
    Usage information.
    """
    popup = sg.popup_no_buttons('DISCLAIMER',
                                'THE SOFTWARE TOOL IS PROVIDED "AS IS", WITHOUT WARRANTY',
                                'OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT',
                                'LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS',
                                'FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO',
                                'EVENT SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES',
                                'OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT',
                                'TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION',
                                'WITH THE SOFTWARE TOOL OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.',
                                title='Usage Policy Notification', keep_on_top='True', icon=info_base64,
                                relative_location=(0, 0))

def notice():
    """
    Notice information.
    """
    popup = sg.popup_no_buttons('This Software Tool was created as a python related educational project.',
                                'The tool is not endorsed or supported and was created initially to learn.',
                                'This tool can be used in production environments at the approval of the '
                                'network security officer or equivalent authority prior to use.',
                                title='Software Notice', keep_on_top='True', icon=info_base64,
                                relative_location=(0, 0))

def github():
    """
    Github information.
    """
    popup = sg.popup_no_buttons('Github:',
                                ' * Code: https://github.com/dunneja/Nagini/',
                                ' * Issues: https://github.com/dunneja/Nagini/issues/',
                                'Author: James Dunne - <james.dunne1@gmail.com>',
                                title='Github Information', keep_on_top='True', icon=git_hub_base64,
                                relative_location=(0, 0))