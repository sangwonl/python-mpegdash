from xml.dom import minidom

# python3 support
try:
    from urllib2 import urlopen
except:
    from urllib.request import urlopen

from mpegdash.nodes import MPEGDASH
from mpegdash.utils import parse_child_nodes, write_child_node


class MPEGDASHParser(object):
    @classmethod
    def load_xmldom(cls, string_or_url):
        if '<MPD' in string_or_url:
            mpd_string = string_or_url
        else:
            try:
                mpd_string = urlopen(string_or_url).read()
            except ValueError:
                with open(string_or_url, 'r') as f:
                    mpd_string = f.read()

        return minidom.parseString(mpd_string)

    @classmethod
    def parse(cls, string_or_url):
        xml_root_node = cls.load_xmldom(string_or_url)
        return parse_child_nodes(xml_root_node, 'MPD', MPEGDASH)[0]

    @classmethod
    def write(cls, mpd, filepath):
        xml_doc = minidom.Document()
        write_child_node(xml_doc, 'MPD', mpd)
        with open(filepath, 'w') as f:
            xml_doc.writexml(f, indent='    ', addindent='    ', newl='\n')
