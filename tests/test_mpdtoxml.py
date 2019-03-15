try:
    import unittest2 as unittest
except:
    import unittest

from mpegdash.parser import MPEGDASHParser


class MPD2XMLTestCase(unittest.TestCase):
    def test_mpd2xml(self):
        mpd = MPEGDASHParser.parse('./tests/mpd-samples/sample-001.mpd')
        MPEGDASHParser.write(mpd, './tests/mpd-samples/output.mpd')

        mpd2 = MPEGDASHParser.parse('./tests/mpd-samples/output.mpd')

        all_reprs = []
        for period in mpd.periods:
            for adapt_set in period.adaptation_sets:
                for repr in adapt_set.representations:
                    all_reprs.append(repr)

        all_reprs2 = []
        for period in mpd2.periods:
            for adapt_set in period.adaptation_sets:
                for repr in adapt_set.representations:
                    all_reprs2.append(repr)

        self.assertTrue(len(all_reprs) == 5)
        self.assertTrue(len(all_reprs) == len(all_reprs2))

    def test_mpd2xmlstr(self):
        with open('./tests/mpd-samples/sample-001.mpd') as f:
            # read the test MPD
            mpd = MPEGDASHParser.parse(f.read())
            # get the MPD as an XML string
            xmlstrout = MPEGDASHParser.toprettyxml(mpd)
            # then parse that string
            mpd2 = MPEGDASHParser.parse(xmlstrout)
            # get the reparsed MPD as a string
            xmlstrout2 = MPEGDASHParser.toprettyxml(mpd2)
            # and check the are equal
            self.assertEqual(xmlstrout, xmlstrout2)