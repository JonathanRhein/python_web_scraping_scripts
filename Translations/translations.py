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

session = HTMLSession()

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
        url_end = ""
        words = data.split()

        for word in words:
            url_end += word + "%20"

        url = self.url + url_end

        site_content = session.get(url).html
        translation = site_content.find('button.lmt__translations_as_text__text_btn', first=True)
        print(translation[0].text)
        #self.result += translation


def main():

    with open('de_introduction.html') as f:
        text = f.read()

    parser = DeeplHTMLParser()
    parser.feed(text)
    print(parser.result)

if __name__ == "__main__":
    main()


