# Datatype URIs.
XSD = 'http://www.w3.org/2001/XMLSchema#'
XSD_ANY_URI = XSD + 'anyURI'
XSD_FLOAT = XSD + 'float'
XSD_INT = XSD + 'int'
XSD_LONG = XSD + 'long'
XSD_STRING = XSD + 'string'

# TMAPI feature strings.
TMAPI_FEATURE_STRING_BASE = 'http://tmapi.org/features/'
AUTOMERGE_FEATURE_STRING = TMAPI_FEATURE_STRING_BASE + 'automerge'
MERGE_BY_TOPIC_NAME_FEATURE_STRING = TMAPI_FEATURE_STRING_BASE + \
    'merge/byTopicName'
READ_ONLY_FEATURE_STRING = TMAPI_FEATURE_STRING_BASE + 'readOnly'
TYPE_INSTANCE_ASSOCIATIONS_FEATURE_STRING = TMAPI_FEATURE_STRING_BASE + \
    'type-instance-associations'
