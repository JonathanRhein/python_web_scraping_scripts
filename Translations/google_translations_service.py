#!/usr/bin/env python3
# coding: iso-8859-1

__author__ = "Jonathan Rhein"
__version__ = "0.1.0"
__license__ = "ShineInternational"

"""
Module Docstring
"""
from requests_html import HTMLSession
from html.parser import HTMLParser
from googletrans import Translator

translator = Translator()

class DeeplHTMLParser(HTMLParser):

    url = 'https://www.deepl.com/translator#de/en/'
    result = ''

    def handle_starttag(self, tag, attrs):
        #print("Encountered a start tag: ", tag)
        self.result += "<" + tag + ">"

    def handle_endtag(self, tag):
        # print("Encountered an end tag: ", tag)
        self.result += "</" + tag + ">"

    def handle_data(self, data):
        pass
        translation = translator.translate(data, dest='en')
        self.result += translation.text


def main():

    with open('de_introduction.html') as f:
        text = f.read()

    parser = DeeplHTMLParser()
    parser.feed(text)

    with open("en_introduction.html", "w") as file:
        file.write(parser.result)

if __name__ == "__main__":
    main()


