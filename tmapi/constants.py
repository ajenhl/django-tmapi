# Copyright 2011 Jamie Norrish (jamie@artefact.org.nz)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
