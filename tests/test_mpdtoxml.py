import unittest

from mpd.parser import MPDParser


class MDP2XMLTestCase(unittest.TestCase):
    def test_mdp2xml(self):
        mpd = MPDParser.parse('./tests/mpd-samples/sample-001.mpd')
        MPDParser.write(mpd, './tests/mpd-samples/output.mpd')

        mpd2 = MPDParser.parse('./tests/mpd-samples/output.mpd')

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
