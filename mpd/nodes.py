def parse_attr(xmlnode, attr_name, def_val):
    val_type = type(def_val)
    if not xmlnode.attributes.has_key(attr_name):
        return val_type(def_val)
    return val_type(xmlnode.attributes[attr_name].nodeValue)


def parse_nodes(xmlnode, tag_name, node_type):
    tag_nodes = xmlnode.getElementsByTagName(tag_name)
    if not tag_nodes:
        return None
    return [node_type.load(tag_node) for tag_node in tag_nodes]


def parse_value(xmlnode, def_val):
    val_type = type(def_val)
    node_val = xmlnode.firstChild.nodeValue
    if node_val == '':
        return val_type(def_val)
    return val_type(node_val)



class INode(object):
    @classmethod
    def load(cls, xmlnode):
        raise NotImplementedError('Should have implemented this')

    @classmethod
    def save(cls, file):
        raise NotImplementedError('Should have implemented this')


class Presentation(object):
    STATIC = 'static'
    DYNAMIC = 'dynamic'


class VideoScan(object):
    UNKNOWN = 'unknown'
    PROGRESSIVE = 'progressive'
    INTERLACED = 'interlaced'


class Subset(INode):
    def __init__(self):
        self.contains = 0                                   # UIntVectorType
        self.id = ''                                        # xs:string


class URL(INode):
    def __init__(self):
        self.source_url = ''                                # xs:anyURI
        self.range = ''                                     # xs:string

    @classmethod
    def load(cls, xmlnode):
        pass


class BaseURL(INode):
    def __init__(self):
        self.base_url_value = ''                            # xs:anyURI

        self.service_location = ''                          # xs:string
        self.byte_range = ''                                # xs:string
        self.availability_time_offset = 0.0                 # xs:double
        self.availability_time_complete = False             # xs:boolean

    @classmethod
    def load(cls, xmlnode):
        base_url = cls()
        base_url.base_url_value = parse_value(xmlnode, '')

        return base_url


class ProgramInformation(INode):
    def __init__(self):
        self.titles = None                                  # xs:string*
        self.sources = None                                 # xs:string*
        self.copyrights = None                              # xs:string*

        self.lang = ''                                      # xs:language
        self.more_information_url = ''                      # xs:anyURI


class Metrics(INode):
    def __init__(self):
        self.reportings = None                              # DescriptorType*
        self.ranges = None                                  # RangeType*

        self.metrics = ''                                   # xs:string (required)


class Range(INode):
    def __init__(self):
        self.starttime = ''                                 # xs:duration
        self.duration = ''                                  # xs:duration


class SegmentURL(INode):
    def __init__(self):
        self.media = ''                                     # xs:anyURI
        self.media_range = ''                               # xs:string
        self.index = ''                                     # xs:anyURI
        self.indx_range = ''                                # xs:string


class SegmentTimeline(INode):
    def __init__(self):
        self.Ss = None                                      # xs:complexType+


class SegmentBase(INode):
    def __init__(self):
        self.initializations = None                         # URLType*
        self.representation_indexes = None                  # URLType*

        self.time_scale = 0                                 # xs:unsignedInt
        self.presentation_time_offset = 0                   # xs:unsignedLong
        self.index_range = ''                               # xs:string
        self.index_range_exact = False                      # xs:boolean
        self.availability_time_offset = 0.0                 # xs:double
        self.availability_time_complete = False             # xs:boolean

    @classmethod
    def load(cls, xmlnode):
        segment_base = cls()
        segment_base.index_range = parse_attr(xmlnode, 'indexRange', '')
        segment_base.initializations = parse_nodes(xmlnode, 'Initialization', URL)

        return segment_base


class MultipleSegmentBase(SegmentBase):
    def __init__(self):
        self.segment_timelines = None                       # SegmentTimelineType*
        self.bitstream_switchings = None                    # URLType*

        self.duration = 0                                   # xs:unsignedInt
        self.start_number = 0                               # xs:unsignedInt


class SegmentTemplate(MultipleSegmentBase):
    def __init__(self):
        self.media = ''                                     # xs:string
        self.index = ''                                     # xs:string
        self.initialization = ''                            # xs:string
        self.bitstream_switching = ''                       # xs:string

class SegmentList(MultipleSegmentBase):
    def __init__(self):
        self.segment_urls = None                            # SegmentURLType


class Event(INode):
    def __init__(self):
        self.event_value = ''                               # xs:string

        self.presentation_time = 0                          # xs:unsignedLong
        self.duration = 0                                   # xs:unsignedLong
        self.id = 0                                         # xs:unsignedInt


class Descriptor(INode):
    def __init__(self):
        self.scheme_id_uri = ''                             # xs:anyURI (required)
        self.value = ''                                     # xs:string
        self.id = ''                                        # xs:string


class ContentComponent(INode):
    def __init__(self):
        self.accessibilities = None                         # DescriptorType*
        self.roles = None                                   # DescriptorType*
        self.ratings = None                                 # DescriptorType*
        self.viewpoints = None                              # DescriptorType*

        self.id = 0                                         # xs:unsigendInt
        self.lang = ''                                      # xs:language
        self.content_type = ''                              # xs:string
        self.par = ''                                       # RatioType

    @classmethod
    def load(cls, xmlnode):
        content_comp = cls()
        content_comp.id = parse_attr(xmlnode, 'id', 0)
        content_comp.content_type = parse_attr(xmlnode, 'contentType', '')

        return content_comp


class RepresentationBase(INode):
    def __init__(self):
        self.frame_packings = None                          # DescriptorType*
        self.audio_channel_configurations = None            # DescriptorType*
        self.content_protections = None                     # DescriptorType*
        self.essential_properties = None                    # DescriptorType*
        self.supplemental_properties = None                 # DescriptorType*
        self.inband_event_streams = None                    # DescriptorType*

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

class Representation(RepresentationBase):
    def __init__(self):
        self.base_urls = None                               # BaseURLType*
        self.sub_representations = None                     # SubRepresentationType*
        self.segment_bases = None                           # SegmentBaseType*
        self.segment_lists = None                           # SegmentListType*
        self.segment_templates = None                       # SegmentTemplateType*

        self.id = ''                                        # StringNoWhitespaceType (Required)
        self.bandwidth = 0                                  # xs:unsignedInt (required)
        self.quality_ranking = 0                            # xs:unsignedInt
        self.dependency_id = ''                             # StringVectorType
        self.num_channels = 0                               # xs:unsignedInt
        self.sample_rate = 0                                # xs:unsignedLong

    @classmethod
    def load(cls, xmlnode):
        representation = cls()
        representation.id = parse_attr(xmlnode, 'id', 0)
        representation.width = parse_attr(xmlnode, 'width', 0)
        representation.height = parse_attr(xmlnode, 'height', 0)
        representation.bandwidth = parse_attr(xmlnode, 'bandwidth', 0)
        representation.mime_type = parse_attr(xmlnode, 'mimeType', '')
        representation.codecs = parse_attr(xmlnode, 'codecs', '')

        representation.base_urls = parse_nodes(xmlnode, 'BaseURL', BaseURL)
        representation.segment_bases = parse_nodes(xmlnode, 'SegmentBase', SegmentBase)

        return representation


class SubRepresentation(RepresentationBase):
    def __init__(self):
        self.level = 0                                      # xs:unsigendInt
        self.dependency_level = 0                           # UIntVectorType
        self.bandwidth = 0                                  # xs:unsignedInt
        self.content_component = ''                         # StringVectorType


class AdaptationSet(RepresentationBase):
    def __init__(self):
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

    @classmethod
    def load(cls, xmlnode):
        adapt_set = cls()

        adapt_set.content_components = parse_nodes(xmlnode, 'ContentComponent', ContentComponent)
        adapt_set.representations = parse_nodes(xmlnode, 'Representation', Representation)

        return adapt_set


class EventStream(INode):
    def __init__(self):
        self.events = None                                  # EventType*

        self.scheme_id_uri = ''                             # xs:anyURI
        self.value = ''                                     # xs:string
        self.timescale = 0                                  # xs:unsignedInt


class Period(INode):
    def __init__(self):
        self.base_urls = None                               # BaseURLType*
        self.segment_bases = None                           # SegmentBaseType*
        self.segment_lists = None                           # SegmentListType*
        self.segment_templates = None                       # SegmentTemplateType*
        self.asset_identifiers = None                       # DescriptorType*
        self.event_streams = None                           # EventStreamType*
        self.adaptation_sets = None                         # AdaptationSetType*
        self.subsets = None                                 # SubsetType*

        self.id = ''                                        # xs:string
        self.start = ''                                     # xs:duration
        self.duration = ''                                  # xs:duration
        self.bitstream_switching = False                    # xs:boolean

    @classmethod
    def load(cls, xmlnode):
        period = cls()
        period.start = parse_attr(xmlnode, 'start', '')
        period.duration = parse_attr(xmlnode, 'duration', '')

        period.adaptation_sets = parse_nodes(xmlnode, 'AdaptationSet', AdaptationSet)
        period.segment_templates = parse_attr(xmlnode, 'SegmentTemplate', SegmentTemplate)

        return period


class MPD(INode):
    def __init__(self):
        self.program_informations = None                    # ProgramInformationType*
        self.base_urls = None                               # BaseURLType*
        self.locations = None                               # xs:anyURI*
        self.periods = None                                 # PeriodType+
        self.metrics = None                                 # MetricsType*

        self.id = ''                                        # xs:string
        self.profiles = ''                                  # xs:string (required)
        self.type = Presentation.STATIC                     # PresentationType
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

    @classmethod
    def load(cls, xmlnode):
        mpd = cls()
        mpd.type = parse_attr(xmlnode, 'type', Presentation.STATIC)
        mpd.profiles = parse_attr(xmlnode, 'profiles', '')
        mpd.min_buffer_time = parse_attr(xmlnode, 'minBufferTime', '')
        mpd.media_presentation_duration = parse_attr(xmlnode, 'mediaPresentationDuration', '')

        mpd.periods = parse_nodes(xmlnode, 'Period', Period)
        mpd.program_informations = parse_nodes(xmlnode, 'ProgramInformation', ProgramInformation)

        return mpd

