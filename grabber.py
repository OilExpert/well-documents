'''
Downloads well's document by its API number.
Copyright (C) 2015  Yan Foto, Nima Fotouhi Tehrani

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import urllib2
import logging
from urllib import quote
from cookielib import CookieJar
from lxml import html, etree
from zipfile import ZipFile


class Grabber:
    BASE_URL = "http://owr.conservation.ca.gov/Well/WellDetailPage.aspx?apinum={}"

    def __init__(self, apinum):
        """
        Initiates a new Grabber for given API
        @param apinum: API number of the well
        """
        self.cj = CookieJar()
        self.url = Grabber.BASE_URL.format(apinum)

        # Use the cookie jar in urllib2 default opener
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        urllib2.install_opener(opener)

    def grab(self, target):
        """
        Grabs well's documents and creates an archive at target.
        @param target: either a string (file name) or a file-like object
        """
        # First get only the cookies
        urllib2.urlopen(self.url).close()

        # Now read the actual content
        connection = urllib2.urlopen(self.url)
        self._parse(connection, target)
        connection.close()

    def _parse(self, content, target):
        """
        Parses the given content string and writes the archive to target.
        @param content: HTML page of well
        @param target: either a string (file name) or a file-like object
        """
        parsed = html.parse(content)
        # els = parsed.xpath('.//*[./@id = \'FormWellDetail\']//table[count(preceding-sibling::*) = 2]//tr//td[count(preceding-sibling::*) = 1]//a')
        els = parsed.xpath("//form[@id='FormWellDetail']"
                           "//table[count(preceding-sibling::*) = 2]"
                           "//tr//td[count(preceding-sibling::*) = 1]//a")

        zipF = ZipFile(target, 'w')

        for el in els:
            url = quote(el.get('href'), safe="%/:=&?~#+!$,;'@()*[]")
            name = el.text
            logging.info("Fetching and packing '{}'".format(url))
            content = urllib2.urlopen(url)
            zipF.writestr(name, content.read())
            content.close()

        zipF.close()
