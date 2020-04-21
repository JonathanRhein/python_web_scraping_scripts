#!/usr/bin/env python3
# coding: iso-8859-1

__author__ = "Jonathan Rhein"
__version__ = "0.1.0"
__license__ = "ShineInternational"

"""
Module Docstring
"""
import string
import glob, os
import json

def main():



    for file in glob.glob("*.json"):
        with open(file) as f:
            prayers = dict()
            final_dict = dict()
            data = json.loads(f.read())
        for module_name in data:
            module = data[module_name]
            print(module_name)
            for prayer in module:
                prayer_wo_verses = strip_unnecessary_characters(module[prayer])
                prayers[prayer] = prayer_wo_verses
            final_dict[module_name] = prayers

        with open('without_verses/' + file, 'w') as fp:
            json.dump(final_dict, fp)
        print('File ' + file + ' done');



def strip_unnecessary_characters(verse):
    for char in string.digits:
        verse = verse.replace(char, '')
    verse = verse.replace('<>', '')
    verse = verse.replace('<br><b>', ' <b>')
    verse = verse.replace('//', '')
    return verse

if __name__ == "__main__":
    main()
