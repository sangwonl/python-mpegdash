import unittest

from mpegdash.parser import MPEGDASHParser


class XML2MPDTestCase(unittest.TestCase):
    def test_xml2mpd_from_string(self):
        mpd_string = '''
        <MPD xmlns="urn:mpeg:DASH:schema:MPD:2011" mediaPresentationDuration="PT0H1M52.43S" minBufferTime="PT1.5S"
        profiles="urn:mpeg:dash:profile:isoff-on-demand:2011" type="static">
          <Period duration="PT0H1M52.43S" start="PT0S">
            <AdaptationSet>
              <ContentComponent contentType="video" id="1" />
              <Representation bandwidth="4190760" codecs="avc1.640028" height="1080" id="1" mimeType="video/mp4" width="1920">
                <BaseURL>motion-20120802-89.mp4</BaseURL>
                <SegmentBase indexRange="674-981">
                  <Initialization range="0-673" />
                </SegmentBase>
              </Representation>
            </AdaptationSet>
          </Period>
        </MPD>
        '''
        self.assert_mpd(MPEGDASHParser.parse(mpd_string))

    def test_xml2mpd_from_file(self):
        self.assert_mpd(MPEGDASHParser.parse('./tests/mpd-samples/sample-001.mpd'))
        self.assert_mpd(MPEGDASHParser.parse('./tests/mpd-samples/motion-20120802-manifest.mpd'))
        self.assert_mpd(MPEGDASHParser.parse('./tests/mpd-samples/oops-20120802-manifest.mpd'))
        self.assert_mpd(MPEGDASHParser.parse('./tests/mpd-samples/360p_speciment_dash.mpd'))

    def test_xml2mpd_from_url(self):
        mpd_url = 'http://yt-dash-mse-test.commondatastorage.googleapis.com/media/motion-20120802-manifest.mpd'
        self.assert_mpd(MPEGDASHParser.parse(mpd_url))

    def test_xml2mpd_from_file_with_utc_timing(self):
        mpd = MPEGDASHParser.parse('./tests/mpd-samples/utc_timing.mpd')
        self.assertEqual(mpd.utc_timings[0].scheme_id_uri, 'urn:mpeg:dash:utc:http-iso:2014')
        self.assertEqual(mpd.utc_timings[0].value, 'https://time.akamai.com/?iso')

    def test_xml2mpd_from_file_with_event_messagedata(self):
        mpd = MPEGDASHParser.parse('./tests/mpd-samples/with_event_message_data.mpd')
        self.assertTrue(mpd.periods[0].event_streams[0].events[0].message_data is not None)
        self.assertTrue(mpd.periods[0].event_streams[0].events[0].event_value is None)
        self.assertTrue(mpd.periods[0].event_streams[0].events[1].message_data is None)
        self.assertEqual(mpd.periods[0].event_streams[0].events[1].event_value, "Some Random Event Text")

    def test_xml2mpd_parse_vector_type_attributes(self):
        mpd_string = '''
        <MPD xmlns="urn:mpeg:DASH:schema:MPD:2011" mediaPresentationDuration="PT0H1M52.43S" minBufferTime="PT1.5S"
        profiles="urn:mpeg:dash:profile:isoff-on-demand:2011" type="static">
          <Period duration="PT0H1M52.43S" start="PT0S">
            <AdaptationSet>
              <ContentComponent contentType="video" id="1" />
              <Representation bandwidth="4190760" codecs="avc1.640028" height="1080" id="1" mimeType="video/mp4" width="1920">
                <SubRepresentation bandwidth="117600" codecs="mp4a.40.5" contentComponent="102 104"></SubRepresentation>
                <BaseURL>motion-20120802-89.mp4</BaseURL>
                <SegmentBase indexRange="674-981">
                  <Initialization range="0-673" />
                </SegmentBase>
              </Representation>
            </AdaptationSet>
          </Period>
        </MPD>
        '''
        mpd = MPEGDASHParser.parse(mpd_string)
        self.assert_mpd(mpd)

        sub_rep = mpd.periods[0].adaptation_sets[0].representations[0].sub_representations[0]
        self.assertEqual(len(sub_rep.content_component), 2)
        self.assertEqual(sub_rep.content_component[0], '102')
        self.assertEqual(sub_rep.content_component[1], '104')

    def test_xml2mpd_from_file_with_content_protection(self):
        mpd = MPEGDASHParser.parse('./tests/mpd-samples/with_content_protection.mpd')
        self.assertEqual(
          "6c28b624-5854-5b8c-8033-9d61ac0c039c",
          mpd.periods[0].adaptation_sets[0].content_protections[0].cenc_default_kid
        )
        self.assertEqual(
          "urn:mpeg:dash:mp4protection:2011",
          mpd.periods[0].adaptation_sets[0].content_protections[0].scheme_id_uri
        )
        self.assertTrue(mpd.periods[0].adaptation_sets[0].content_protections[1].pssh[0].pssh is not None)

    def assert_mpd(self, mpd):
        self.assertTrue(mpd is not None)
        self.assertTrue(len(mpd.periods) > 0)
        self.assertTrue(mpd.periods[0].adaptation_sets is not None)
        self.assertTrue(len(mpd.periods[0].adaptation_sets) > 0)
        self.assertTrue(mpd.periods[0].adaptation_sets[0].representations is not None)
        self.assertTrue(len(mpd.periods[0].adaptation_sets[0].representations) > 0)
        self.assertTrue(len(mpd.periods[0].adaptation_sets[0].representations[0].id) > 0)
