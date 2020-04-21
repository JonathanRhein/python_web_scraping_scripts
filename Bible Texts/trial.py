#!/usr/bin/env python3
"""
Module Docstring
"""
import glob

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"

import string



def trial():
    """ Main entry point of the app """
    for file in glob.glob("*.json"):
        print(file)

def strip_unnecessary_characters(verse):
    for char in string.digits:
        char = '<' + char + '>'
        print(char)
        verse = verse.replace(char, '')
    return verse

if __name__ == "__main__":
    """ This is executed when run from the command line """
    trial()