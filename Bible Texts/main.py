#!/usr/bin/env python3
# coding: iso-8859-1

__author__ = "Jonathan Rhein"
__version__ = "0.1.0"
__license__ = "ShineInternational"

"""
Module Docstring
"""
from requests_html import HTMLSession
import string
import sys
import io
import json
import subprocess




modules = ['de_eu', 'de_elb', 'de_lut', 'de_ngü', 'de_hfa', 'en_kjv', 'en_esv', 'en_niv']

modules = ['de_elb']

psalms = dict()
psalmNumbers = [1, 2, 3, 4, 5, 6, 8, 12, 13, 15, 16, 19, 20, 23, 24, 25, 26, 27, 29, 30, 34, 41, 43, 45, 46, 47, 51,
                54, 57, 61, 63, 67, 70,
                84, 85, 86, 87, 91, 93, 96, 97, 98, 99, 100, 101, 110, 111, 112, 113, 116, 117, 118, 119, 120, 121,
                122, 123,
                124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 137, 138, 141, 142, 143, 146, 147]

psalmNumbers = [51, 116, 147, 119, 23]



scriptures = dict()
scriptureReferences = ['ephesians_4,1-5', 'john_1,1-17', 'john_14,26-15,4', 'matthew_5,1-16', 'luke_9,10-17', 'luke_4,38-41',
                    'luke_2,25-32', 'matthew_25,1-13', 'luke_7,36-50', 'luke_12,32-46', 'luke_2,29-31']

scriptureReferences = []

session = HTMLSession()

def main():

    for module in modules:

        translation = module.split('_', 1)[1]
        language = module.split('_', 1)[0]

        for psalmNumber in psalmNumbers:

            url_reference_psalm = 'https://www.bibleserver.com/niv/ps' + str(psalmNumber)
            site_content_reference_psalm = session.get(url_reference_psalm).html
            verses_reference_psalm = site_content_reference_psalm.find('span.verse-content--hover')

            url = 'https://www.bibleserver.com/' + translation + '/ps' + str(psalmNumber)
            site_content = session.get(url).html
            verses = site_content.find('span.verse-content--hover')

            text = ""
            number_of_verses_reference_psalm = len(verses_reference_psalm)
            delta = len(verses) - number_of_verses_reference_psalm
            for i, verses_reference_psalm in enumerate(reversed(verses_reference_psalm)):
                verse_number = number_of_verses_reference_psalm - i
                verse = strip_unnecessary_characters(verses[verse_number + delta - 1].text)
                if i == 0:
                    if language == "en":
                        if "Alleluja!" in verse:
                            verse = verse.replace('Alleluja!', '')
                        text += '<b>Alleluja!</b>'
                    if language == "de":
                        if "Halleluja!" in verse:
                            verse = verse.replace('Halleluja!', '')
                        text += '<b>Halleluja!</b>'
                text = '<' + str(verse_number) + '>' + verse + '<br>' + text

            if language == "en": psalm_end = '<b>Alleluja!</b>'
            if language == "de": psalm_end = '<b>Halleluja!</b>'

            if psalmNumber == 116:
                text = text.split('<10>')
                psalms['psalm_' + str(psalmNumber) + '_1'] = text[0] + psalm_end
                psalms['psalm_' + str(psalmNumber) + '_2'] = '<10>' + text[1]

            elif psalmNumber == 147:
                text = text.split('<12>')
                psalms['psalm_' + str(psalmNumber) + '_1'] = text[0] + psalm_end
                psalms['psalm_' + str(psalmNumber) + '_2'] = '<12>' + text[1]


            elif psalmNumber == 119:
                if language == "en": psalm_119_end = '<b>Glory be to you O lover of mankind!</b>'
                if language == "de": psalm_119_end = '<b>Ehre sei dir, Du Liebhaber der Menschheit!</b>'
                for i in range(22):
                    i += 1
                    verse_number = i * 8 + 1
                    verse_identifier = '<' + str(verse_number) + '>'
                    if i == 22:
                        psalms['psalm_' + str(psalmNumber) + '_' + str(i)] = text + psalm_119_end
                        text = text.split(str('<170>'))[1]
                        psalms['psalm_' + str(psalmNumber) + '_' + str(i) + '_partial'] = '<170>' + text + psalm_end
                    else:
                        text = text.split(str(verse_identifier))
                        psalms['psalm_' + str(psalmNumber) + '_' + str(i)] = text[0] + psalm_119_end
                    text = verse_identifier + text[1]

            else:
                psalms['psalm_' + str(psalmNumber)] = text


        for passage in scriptureReferences:
            url = 'https://www.bibleserver.com/' + translation + '/' + passage
            site_content = session.get(url).html
            verses = site_content.find('span.verse-content--hover')

            if passage.count(',') == 1:
                temp = passage.split(',', 1)[1]
                verse_start_number = int(temp.split('-', 1)[0])
                verse_end_number = int(temp.split('-', 1)[1])

                text = ""
                temp_index = 0
                for i, verse in enumerate(verses):
                    i += 1
                    if i < verse_start_number or i > verse_end_number:
                        pass
                    else:
                        verse = strip_unnecessary_characters(verse.text)
                        if temp_index + 1 == verse_end_number - verse_start_number:
                            pass
                        else:
                            text += ' <' + str(i) + '>' + verse + '<br>'
                if module == 'ephesians_4,1-5':
                    pass
                else:
                    if language == 'de':
                        text += '<b>Ehre sei Gott in Ewigkeit!</b>'
                    if language == 'en':
                        text += '<b>Glory be to God forever!</b>'
            else:
                'joh_14,26-15,4'
                temp = passage.split(',', 1)[1]
                book = passage.split('_', 1)[0]
                verse_start_number = int(temp.split('-', 1)[0])
                chapter_end_number = int(temp.split('-', 1)[1].split(',')[0])
                verse_end_number = int(temp.split('-', 1)[1].split(',')[1])

                text = ""
                temp_index = 0
                for i, verse in enumerate(verses):
                    if i < verse_start_number:
                        pass
                    else:
                        verse = strip_unnecessary_characters(verse.text)
                        if temp_index + 1 == verse_end_number - verse_start_number:
                            pass
                        else:
                            text += ' <' + str(i) + '>' + verse + '<br>'
                        i += 1
                url = 'https://www.bibleserver.com/' + translation + '/' + book + str(chapter_end_number)
                site_content = session.get(url).html
                verses = site_content.find('span.verse-content--hover')
                temp_index = 0
                for i, verse in enumerate(verses):
                    if i > verse_end_number:
                        pass
                    else:
                        verse = strip_unnecessary_characters(verse.text)
                        if temp_index + 1 == verse_end_number - verse_start_number:
                            pass
                        else:
                            text += ' <' + str(i+1) + '>' + verse + '<br>'
                        i += 1
                if module == 'ephesians_4,1-5':
                    pass
                else:
                    if language == 'de':
                        text += '<b>Ehre sei Gott in Ewigkeit!</b>'
                    if language == 'en':
                        text += '<b>Glory be to God forever!</b>'

            scriptures[passage] = text

        data = dict()
        if module == 'de_ngü': module = 'de_ngu'
        data[module] = {**psalms, **scriptures}

        # subprocess.run("pbcopy", universal_newlines=True, input=str(data))

        with open(module + '.json', 'w') as fp:
            json.dump(data, fp)

        print('Module ' + module + ' done');

def strip_unnecessary_characters(verse):
    for char in string.digits:
        verse = verse.replace(char, '')
    verse = verse.replace('[', '')
    verse = verse.replace(']', '')
    return verse

if __name__ == "__main__":
    main()
