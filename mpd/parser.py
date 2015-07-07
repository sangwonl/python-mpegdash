from xml.dom import minidom
from urllib2 import urlopen

from mpd.nodes import MPD

class MPDParser(object):
    @classmethod
    def load_xmldom(cls, string_or_url):
        if '<MPD' in string_or_url:
            mpd_string = string_or_url
        else:
            try:
                mpd_string = urlopen(string_or_url).read()
            except ValueError:
                mpd_string = open(string_or_url).read()

        return minidom.parseString(mpd_string)

    @classmethod
    def parse(cls, string_or_url):
        xmldom = cls.load_xmldom(string_or_url)
        mpd_root_node = xmldom.getElementsByTagName('MPD')

        return MPD.load(mpd_root_node[0])
