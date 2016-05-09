[travis]: https://travis-ci.org/caststack/python-mpd-parser.svg?branch=master

![travis]

# python-mdp-parser
MPEG-DASH MPD(Media Presentation Description) Parser
compatible with Python2.6+ and Python3

## Test
    $ python -m unittest discover
    $ python3 -m unittest discover

## Usage
    from mpd.parser import MPDParser
    
    # Parse from file path
    mpd_path = './tests/mpd-samples/sample-001.mpd'
    mpd = MPDParser.parse(mpd_path)
    
    # Parse from url
    mpd_url = 'http://yt-dash-mse-test.commondatastorage.googleapis.com/media/motion-20120802-manifest.mpd'
    mpd = MPDParser.parse(mpd_url)
    
    # Parse from string
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
    mpd = MPDParser.parse(mpd_string)
    
    # Write to xml file
    MPDParser.write(mpd, './tests/mpd-samples/output.mpd')
    
