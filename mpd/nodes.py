from mpd.utils import *


class XMLNode(object):
    def load(self, xmlnode):
        raise NotImplementedError('Should have implemented this')

    def save(self, file):
        raise NotImplementedError('Should have implemented this')


class Presentation(object):
    STATIC = 'static'
    DYNAMIC = 'dynamic'


class VideoScan(object):
    UNKNOWN = 'unknown'
    PROGRESSIVE = 'progressive'
    INTERLACED = 'interlaced'


class Subset(XMLNode):
    def __init__(self):
        self.id = ''                                        # xs:string
        self.contains = []                                  # UIntVectorType (required)

    def load(self, xmlnode):
        self.id = parse_attr_value(xmlnode, 'id', '')
        self.contains = parse_attr_value(xmlnode, 'contains', [int])


class URL(XMLNode):
    def __init__(self):
        self.source_url = ''                                # xs:anyURI
        self.range = ''                                     # xs:string

    def load(self, xmlnode):
        self.source_url = parse_attr_value(xmlnode, 'sourceURL', '')
        self.range = parse_attr_value(xmlnode, 'range', '')


class BaseURL(XMLNode):
    def __init__(self):
        self.base_url_value = ''                            # xs:anyURI

        self.service_location = ''                          # xs:string
        self.byte_range = ''                                # xs:string
        self.availability_time_offset = 0.0                 # xs:double
        self.availability_time_complete = False             # xs:boolean

    def load(self, xmlnode):
        self.base_url_value = parse_node_value(xmlnode, '')

        self.service_location = parse_attr_value(xmlnode, 'serviceLocation', '')
        self.byte_range = parse_attr_value(xmlnode, 'byteRange', '')
        self.availability_time_offset = parse_attr_value(xmlnode, 'availabilityTimeOffset', 0.0)
        self.availability_time_complete = parse_attr_value(xmlnode, 'availabilityTimeComplete', False)


class ProgramInformation(XMLNode):
    def __init__(self):
        self.lang = ''                                      # xs:language
        self.more_information_url = ''                      # xs:anyURI

        self.titles = None                                  # xs:string*
        self.sources = None                                 # xs:string*
        self.copyrights = None                              # xs:string*

    def load(self, xmlnode):
        self.lang = parse_attr_value(xmlnode, 'lang', '')
        self.more_information_url = parse_attr_value(xmlnode, 'moreInformationURL', '')

        self.titles = parse_child_nodes(xmlnode, 'Title', [str])
        self.sources = parse_child_nodes(xmlnode, 'Source', [str])
        self.copyrights = parse_child_nodes(xmlnode, 'Copyright', [str])


class Metrics(XMLNode):
    def __init__(self):
        self.metrics = ''                                   # xs:string (required)

        self.reportings = None                              # DescriptorType*
        self.ranges = None                                  # RangeType*

    def load(self, xmlnode):
        self.metrics = parse_attr_value(xmlnode, 'metrics', '')

        self.reportings = parse_child_nodes(xmlnode, 'Reporting', Descriptor)
        self.ranges = parse_child_nodes(xmlnode, 'Range', Range)


class Range(XMLNode):
    def __init__(self):
        self.starttime = ''                                 # xs:duration
        self.duration = ''                                  # xs:duration

    def load(self, xmlnode):
        self.starttime = parse_attr_value(xmlnode, 'starttime', '')
        self.duration = parse_attr_value(xmlnode, 'duration', '')


class SegmentURL(XMLNode):
    def __init__(self):
        self.media = ''                                     # xs:anyURI
        self.media_range = ''                               # xs:string
        self.index = ''                                     # xs:anyURI
        self.index_range = ''                                # xs:string

    def load(self, xmlnode):
        self.media = parse_attr_value(xmlnode, 'media', '')
        self.media_range = parse_attr_value(xmlnode, 'mediaRange', '')
        self.index = parse_attr_value(xmlnode, 'index', '')
        self.index_range = parse_attr_value(xmlnode, 'indexRange', '')


class S(XMLNode):
    def __init__(self):
        self.t = 0                                          # xs:unsignedLong
        self.d = 0                                          # xs:unsignedLong (required)
        self.r = 0                                          # xml:integer

    def load(self, xmlnode):
        self.t = parse_attr_value(xmlnode, 't', 0)
        self.d = parse_attr_value(xmlnode, 'd', 0)
        self.r = parse_attr_value(xmlnode, 'r', 0)


class SegmentTimeline(XMLNode):
    def __init__(self):
        self.Ss = None                                      # xs:complexType+

    def load(self, xmlnode):
        self.Ss = parse_child_nodes(xmlnode, 'S', S)


class SegmentBase(XMLNode):
    def __init__(self):
        self.timescale = 0                                  # xs:unsignedInt
        self.index_range = ''                               # xs:string
        self.index_range_exact = False                      # xs:boolean
        self.presentation_time_offset = 0                   # xs:unsignedLong
        self.availability_time_offset = 0.0                 # xs:double
        self.availability_time_complete = False             # xs:boolean

        self.initializations = None                         # URLType*
        self.representation_indexes = None                  # URLType*

    def load(self, xmlnode):
        self.timescale = parse_attr_value(xmlnode, 'timescale', 0)
        self.index_range = parse_attr_value(xmlnode, 'indexRange', '')
        self.index_range_exact = parse_attr_value(xmlnode, 'indexRangeExact', False)
        self.presentation_time_offset = parse_attr_value(xmlnode, 'presentationTimeOffset', 0)
        self.availability_time_offset = parse_attr_value(xmlnode, 'availabilityTimeOffset', 0.0)
        self.availability_time_complete = parse_attr_value(xmlnode, 'availabilityTimeComplete', False)

        self.initializations = parse_child_nodes(xmlnode, 'Initialization', URL)
        self.representation_indexes = parse_child_nodes(xmlnode, 'RepresentationIndex', URL)


class MultipleSegmentBase(SegmentBase):
    def __init__(self):
        SegmentBase.__init__(self)

        self.duration = 0                                   # xs:unsignedInt
        self.start_number = 0                               # xs:unsignedInt

        self.segment_timelines = None                       # SegmentTimelineType*
        self.bitstream_switchings = None                    # URLType*

    def load(self, xmlnode):
        SegmentBase.load(self, xmlnode)

        self.duration = parse_attr_value(xmlnode, 'duration', 0)
        self.start_number = parse_attr_value(xmlnode, 'startNumber', 0)

        self.segment_timelines = parse_child_nodes(xmlnode, 'SegmentTimeline', SegmentTimeline)
        self.bitstream_switchings = parse_child_nodes(xmlnode, 'BitstreamSwitching', URL)


class SegmentTemplate(MultipleSegmentBase):
    def __init__(self):
        MultipleSegmentBase.__init__(self)

        self.media = ''                                     # xs:string
        self.index = ''                                     # xs:string
        self.initialization = ''                            # xs:string
        self.bitstream_switching = ''                       # xs:string

    def load(self, xmlnode):
        MultipleSegmentBase.load(self, xmlnode)

        self.media = parse_attr_value(xmlnode, 'media', '')
        self.index = parse_attr_value(xmlnode, 'index', '')
        self.initialization = parse_attr_value(xmlnode, 'initialization', '')
        self.bitstream_switching = parse_attr_value(xmlnode, 'bitstreamSwitching', '')


class SegmentList(MultipleSegmentBase):
    def __init__(self):
        MultipleSegmentBase.__init__(self)

        self.segment_urls = None                            # SegmentURLType

    def load(self, xmlnode):
        MultipleSegmentBase.load(self, xmlnode)

        self.segment_urls = parse_child_nodes(xmlnode, 'SegmentURL', SegmentURL)


class Event(XMLNode):
    def __init__(self):
        self.event_value = ''                               # xs:string
        self.presentation_time = 0                          # xs:unsignedLong
        self.duration = 0                                   # xs:unsignedLong
        self.id = 0                                         # xs:unsignedInt

    def load(self, xmlnode):
        self.event_value = parse_node_value(xmlnode, '')
        self.presentation_time = parse_attr_value(xmlnode, 'presentationTime', 0)
        self.duration = parse_attr_value(xmlnode, 'duration', 0)
        self.id = parse_attr_value(xmlnode, 'id', 0)


class Descriptor(XMLNode):
    def __init__(self):
        self.scheme_id_uri = ''                             # xs:anyURI (required)
        self.value = ''                                     # xs:string
        self.id = ''                                        # xs:string

    def load(self, xmlnode):
        self.scheme_id_uri = parse_attr_value(xmlnode, 'schemeIdUri', '')
        self.value = parse_attr_value(xmlnode, 'value', '')
        self.id = parse_attr_value(xmlnode, 'id', '')


class ContentComponent(XMLNode):
    def __init__(self):
        self.id = 0                                         # xs:unsigendInt
        self.lang = ''                                      # xs:language
        self.content_type = ''                              # xs:string
        self.par = ''                                       # RatioType

        self.accessibilities = None                         # DescriptorType*
        self.roles = None                                   # DescriptorType*
        self.ratings = None                                 # DescriptorType*
        self.viewpoints = None                              # DescriptorType*

    def load(self, xmlnode):
        self.id = parse_attr_value(xmlnode, 'id', 0)
        self.lang = parse_attr_value(xmlnode, 'lang', '')
        self.content_type = parse_attr_value(xmlnode, 'contentType', '')
        self.par = parse_attr_value(xmlnode, 'par', '')

        self.accessibilities = parse_child_nodes(xmlnode, 'Accessibility', Descriptor)
        self.roles = parse_child_nodes(xmlnode, 'Role', Descriptor)
        self.ratings = parse_child_nodes(xmlnode, 'Rating', Descriptor)
        self.viewpoints = parse_child_nodes(xmlnode, 'Viewpoint', Descriptor)


class RepresentationBase(XMLNode):
    def __init__(self):
        self.profiles = ''                                  # xs:string
        self.width = 0                                      # xs:unsigendInt
        self.height = 0                                     # xs:unsigendInt
        self.sar = ''                                       # RatioType
        self.frame_rate = ''                                # FrameRateType
        self.audio_sampling_rate = ''                       # xs:string
        self.mime_type = ''                                 # xs:string
        self.segment_profiles = ''                          # xs:string
        self.codecs = ''                                    # xs:string
        self.maximum_sap_period = 0.0                       # xs:double
        self.start_with_sap = 0                             # SAPType
        self.max_playout_rate = 0.0                         # xs:double
        self.coding_dependency = False                      # xs:boolean
        self.scan_type = ''                                 # VideoScanType

        self.frame_packings = None                          # DescriptorType*
        self.audio_channel_configurations = None            # DescriptorType*
        self.content_protections = None                     # DescriptorType*
        self.essential_properties = None                    # DescriptorType*
        self.supplemental_properties = None                 # DescriptorType*
        self.inband_event_streams = None                    # DescriptorType*

    def load(self, xmlnode):
        self.profiles = parse_attr_value(xmlnode, 'profile', '')
        self.width = parse_attr_value(xmlnode, 'width', 0)
        self.height = parse_attr_value(xmlnode, 'height', 0)
        self.sar = parse_attr_value(xmlnode, 'sar', '')
        self.frame_rate = parse_attr_value(xmlnode, 'frameRate', '')
        self.audio_sampling_rate = parse_attr_value(xmlnode, 'audioSamplingRate', '')
        self.mime_type = parse_attr_value(xmlnode, 'mimeType', '')
        self.segment_profiles = parse_attr_value(xmlnode, 'segmentProfiles', '')
        self.codecs = parse_attr_value(xmlnode, 'codecs', '')
        self.maximum_sap_period = parse_attr_value(xmlnode, 'maximumSAPPeriod', 0.0)
        self.start_with_sap = parse_attr_value(xmlnode, 'startWithSAP', 0)
        self.max_playout_rate = parse_attr_value(xmlnode, 'maxPlayoutRate', 0.0)
        self.coding_dependency = parse_attr_value(xmlnode, 'codingDependency', False)
        self.scan_type = parse_attr_value(xmlnode, 'scanType', VideoScan.UNKNOWN)

        self.frame_packings = parse_child_nodes(xmlnode, 'FramePacking', Descriptor)
        self.audio_channel_configurations = parse_child_nodes(xmlnode, 'AudioChannelConfiguration', Descriptor)
        self.content_protections = parse_child_nodes(xmlnode, 'ContentProtection', Descriptor)
        self.essential_properties = parse_child_nodes(xmlnode, 'EssentialProperty', Descriptor)
        self.supplemental_properties = parse_child_nodes(xmlnode, 'SupplementalProperty', Descriptor)
        self.inband_event_streams = parse_child_nodes(xmlnode, 'InbandEventStream', Descriptor)


class Representation(RepresentationBase):
    def __init__(self):
        RepresentationBase.__init__(self)

        self.id = ''                                        # StringNoWhitespaceType (Required)
        self.bandwidth = 0                                  # xs:unsignedInt (required)
        self.quality_ranking = 0                            # xs:unsignedInt
        self.dependency_id = ''                             # StringVectorType
        self.num_channels = 0                               # xs:unsignedInt
        self.sample_rate = 0                                # xs:unsignedLong

        self.base_urls = None                               # BaseURLType*
        self.segment_bases = None                           # SegmentBaseType*
        self.segment_lists = None                           # SegmentListType*
        self.segment_templates = None                       # SegmentTemplateType*
        self.sub_representations = None                     # SubRepresentationType*

    def load(self, xmlnode):
        self.id = parse_attr_value(xmlnode, 'id', '')
        self.width = parse_attr_value(xmlnode, 'width', 0)
        self.height = parse_attr_value(xmlnode, 'height', 0)
        self.bandwidth = parse_attr_value(xmlnode, 'bandwidth', 0)
        self.mime_type = parse_attr_value(xmlnode, 'mimeType', '')
        self.codecs = parse_attr_value(xmlnode, 'codecs', '')

        self.base_urls = parse_child_nodes(xmlnode, 'BaseURL', BaseURL)
        self.segment_bases = parse_child_nodes(xmlnode, 'SegmentBase', SegmentBase)
        self.segment_lists = parse_child_nodes(xmlnode, 'SegmentList', SegmentList)
        self.segment_templates = parse_child_nodes(xmlnode, 'SegmentTemplate', SegmentTemplate)
        self.sub_representations = parse_child_nodes(xmlnode, 'SubRepresentation', SubRepresentation)


class SubRepresentation(RepresentationBase):
    def __init__(self):
        RepresentationBase.__init__(self)

        self.level = 0                                      # xs:unsigendInt
        self.bandwidth = 0                                  # xs:unsignedInt
        self.dependency_level = 0                           # UIntVectorType
        self.content_component = ''                         # StringVectorType

    def load(self, xmlnode):
        RepresentationBase.load(self, xmlnode)

        self.level = parse_attr_value(xmlnode, 'level', 0)
        self.bandwidth = parse_attr_value(xmlnode, 'bandwidth', 0)
        self.dependency_level = parse_attr_value(xmlnode, 'dependencyLevel', [int])
        self.content_component = parse_attr_value(xmlnode, 'contentComponent', [str])


class AdaptationSet(RepresentationBase):
    def __init__(self):
        RepresentationBase.__init__(self)

        self.id = 0                                         # xs:unsignedInt
        self.group = 0                                      # xs:unsignedInt
        self.lang = ''                                      # xs:language
        self.content_type = ''                              # xs:string
        self.par = ''                                       # RatioType
        self.min_bandwidth = 0                              # xs:unsignedInt
        self.max_bandwidth = 0                              # xs:unsignedInt
        self.min_width = 0                                  # xs:unsignedInt
        self.max_width = 0                                  # xs:unsignedInt
        self.min_height = 0                                 # xs:unsignedInt
        self.max_height = 0                                 # xs:unsignedInt
        self.min_frame_rate = ''                            # FrameRateType
        self.max_frame_rate = ''                            # FrameRateType
        self.segment_alignment = False                      # ConditionalUintType
        self.subsegment_alignment = False                   # ConditionalUintType
        self.subsegment_starts_with_sap = 0                 # SAPType
        self.bitstream_switching = False                    # xs:boolean

        self.accessibilities = None                         # DescriptorType*
        self.roles = None                                   # DescriptorType*
        self.ratings = None                                 # DescriptorType*
        self.viewpoints = None                              # DescriptorType*
        self.content_components = None                      # DescriptorType*
        self.base_urls = None                               # BaseURLType*
        self.segment_bases = None                           # SegmentBase*
        self.segment_lists = None                           # SegmentListType*
        self.segment_templates = None                       # SegmentTemplateType*
        self.representations = None                         # RepresentationType*

    def load(self, xmlnode):
        self.id = parse_attr_value(xmlnode, 'id', 0)
        self.group = parse_attr_value(xmlnode, 'group', 0)
        self.lang = parse_attr_value(xmlnode, 'lang', '')
        self.content_type = parse_attr_value(xmlnode, 'contentType', '')
        self.par = parse_attr_value(xmlnode, 'par', '')
        self.min_bandwidth = parse_attr_value(xmlnode, 'minBandwidth', 0)
        self.max_bandwidth = parse_attr_value(xmlnode, 'maxBandwidth', 0)
        self.min_width = parse_attr_value(xmlnode, 'minWidth', 0)
        self.max_width = parse_attr_value(xmlnode, 'maxWidth', 0)
        self.min_height = parse_attr_value(xmlnode, 'minHeight', 0)
        self.max_height = parse_attr_value(xmlnode, 'maxHeight', 0)
        self.min_frame_rate = parse_attr_value(xmlnode, 'minFrameRate', '')
        self.max_frame_rate = parse_attr_value(xmlnode, 'maxFrameRate', '')
        self.segment_alignment = parse_attr_value(xmlnode, 'segmentAlignment', False)
        self.subsegment_alignment = parse_attr_value(xmlnode, 'subsegmentAlignment', False)
        self.subsegment_starts_with_sap = parse_attr_value(xmlnode, 'subsegmentStartsWithSAP', 0)
        self.bitstream_switching = parse_attr_value(xmlnode, 'bitstreamSwitching', False)

        self.accessibilities = parse_child_nodes(xmlnode, 'Accessibility', Descriptor)
        self.roles = parse_child_nodes(xmlnode, 'Role', Descriptor)
        self.ratings = parse_child_nodes(xmlnode, 'Rating', Descriptor)
        self.viewpoints = parse_child_nodes(xmlnode, 'Viewpoint', Descriptor)
        self.content_components = parse_child_nodes(xmlnode, 'ContentComponent', ContentComponent)
        self.base_urls = parse_child_nodes(xmlnode, 'BaseURL', BaseURL)
        self.segment_bases = parse_child_nodes(xmlnode, 'SegmentBase', SegmentBase)
        self.segment_lists = parse_child_nodes(xmlnode, 'SegmentList', SegmentList)
        self.segment_templates = parse_child_nodes(xmlnode, 'SegmentTemplate', SegmentTemplate)
        self.representations = parse_child_nodes(xmlnode, 'Representation', Representation)


class EventStream(XMLNode):
    def __init__(self):
        self.scheme_id_uri = ''                             # xs:anyURI (required)
        self.value = ''                                     # xs:string
        self.timescale = 0                                  # xs:unsignedInt

        self.events = None                                  # EventType*

    def load(self, xmlnode):
        self.scheme_id_uri = parse_attr_value(xmlnode, 'schemeIdUri', '')
        self.value = parse_attr_value(xmlnode, 'value', '')
        self.timescale = parse_attr_value(xmlnode, 'timescale', 0)

        self.events = parse_child_nodes(xmlnode, 'Event', Event)


class Period(XMLNode):
    def __init__(self):
        self.id = ''                                        # xs:string
        self.start = ''                                     # xs:duration
        self.duration = ''                                  # xs:duration
        self.bitstream_switching = False                    # xs:boolean

        self.base_urls = None                               # BaseURLType*
        self.segment_bases = None                           # SegmentBaseType*
        self.segment_lists = None                           # SegmentListType*
        self.segment_templates = None                       # SegmentTemplateType*
        self.asset_identifiers = None                       # DescriptorType*
        self.event_streams = None                           # EventStreamType*
        self.adaptation_sets = None                         # AdaptationSetType*
        self.subsets = None                                 # SubsetType*

    def load(self, xmlnode):
        self.id = parse_attr_value(xmlnode, 'id', '')
        self.start = parse_attr_value(xmlnode, 'start', '')
        self.duration = parse_attr_value(xmlnode, 'duration', '')
        self.bitstream_switching = parse_attr_value(xmlnode, 'bitstreamSwitching', False)

        self.base_urls = parse_child_nodes(xmlnode, 'BaseURL', BaseURL)
        self.segment_bases = parse_child_nodes(xmlnode, 'SegmentBase', SegmentBase)
        self.segment_lists = parse_child_nodes(xmlnode, 'SegmentList', SegmentList)
        self.segment_templates = parse_attr_value(xmlnode, 'SegmentTemplate', SegmentTemplate)
        self.asset_identifiers = parse_child_nodes(xmlnode, 'AssetIdentifier', Descriptor)
        self.event_streams = parse_child_nodes(xmlnode, 'EventStream', EventStream)
        self.adaptation_sets = parse_child_nodes(xmlnode, 'AdaptationSet', AdaptationSet)
        self.subsets = parse_child_nodes(xmlnode, 'Subset', Subset)


class MPD(XMLNode):
    def __init__(self):
        self.id = ''                                        # xs:string
        self.type = Presentation.STATIC                     # PresentationType
        self.profiles = ''                                  # xs:string (required)
        self.availability_start_time = ''                   # xs:dateTime
        self.availability_end_time = ''                     # xs:dateTime
        self.publish_time = ''                              # xs:dateTime
        self.media_presentation_duration = ''               # xs:duration
        self.minimum_update_period = ''                     # xs:duration
        self.min_buffer_time = ''                           # xs:duration
        self.time_shift_buffer_depth = ''                   # xs:duration
        self.suggested_presentation_delay = ''              # xs:duration
        self.max_segment_duration = ''                      # xs:duration
        self.max_subsegment_duration = ''                   # xs:duration

        self.program_informations = None                    # ProgramInformationType*
        self.base_urls = None                               # BaseURLType*
        self.locations = None                               # xs:anyURI*
        self.periods = None                                 # PeriodType+
        self.metrics = None                                 # MetricsType*

    def load(self, xmlnode):
        self.id = parse_attr_value(xmlnode, 'id', '')
        self.type = parse_attr_value(xmlnode, 'type', Presentation.STATIC)
        self.profiles = parse_attr_value(xmlnode, 'profiles', '')
        self.availability_start_time = parse_attr_value(xmlnode, 'availabilityStartTime', '')
        self.availability_end_time = parse_attr_value(xmlnode, 'availabilityEndTime', '')
        self.publish_time = parse_attr_value(xmlnode, 'publishTime', '')
        self.media_presentation_duration = parse_attr_value(xmlnode, 'mediaPresentationDuration', '')
        self.minimum_update_period = parse_attr_value(xmlnode, 'minimumUpdatePeriod', '')
        self.min_buffer_time = parse_attr_value(xmlnode, 'minBufferTime', '')
        self.time_shift_buffer_depth = parse_attr_value(xmlnode, 'timeShiftBufferDepth', '')
        self.suggested_presentation_delay = parse_attr_value(xmlnode, 'suggestedPresentationDelay', '')
        self.max_segment_duration = parse_attr_value(xmlnode, 'maxSegmentDuration', '')
        self.max_subsegment_duration = parse_attr_value(xmlnode, 'maxSubsegmentDuration', '')

        self.program_informations = parse_child_nodes(xmlnode, 'ProgramInformation', ProgramInformation)
        self.base_urls = parse_child_nodes(xmlnode, 'BaseURL', BaseURL)
        self.locations = parse_child_nodes(xmlnode, 'Location', str)
        self.periods = parse_child_nodes(xmlnode, 'Period', Period)
        self.metrics = parse_child_nodes(xmlnode, 'Metrics', Metrics)
