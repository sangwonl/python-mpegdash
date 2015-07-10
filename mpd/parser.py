from xml.dom import minidom
from urllib2 import urlopen

from mpd.nodes import MPD
from mpd.utils import *


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
        xml_root_node = cls.load_xmldom(string_or_url)
        return parse_child_nodes(xml_root_node, 'MPD', MPD)[0]
