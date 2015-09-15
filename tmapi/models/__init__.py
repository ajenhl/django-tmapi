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

"""Model definitions for the TMAPI application.

The models defined here are based on the SQL used in the Ontopia Topic
Maps engine (http://www.ontopia.net/), the Topic Maps API (TMAPI) 2.0,
and ultimately on "ISO 13250-2: Topic Maps - Data Model"
(http://www.isotopicmaps.org/sam/).

"""

from .association import Association
from .construct import Construct
from .construct_fields import ConstructFields
from .datatype_aware import DatatypeAware
from .identifier import Identifier
from .item_identifier import ItemIdentifier
from .locator import Locator
from .name import Name
from .occurrence import Occurrence
from .reifiable import Reifiable
from .role import Role
from .scoped import Scoped
from .subject_identifier import SubjectIdentifier
from .subject_locator import SubjectLocator
from .tmapi_feature import TMAPIFeature
from .topic import Topic
from .topic_map import TopicMap
from .topic_map_system import TopicMapSystem
from .topic_map_system_factory import TopicMapSystemFactory
from .typed import Typed
from .variant import Variant
