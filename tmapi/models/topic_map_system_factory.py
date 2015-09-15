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

from tmapi.constants import AUTOMERGE_FEATURE_STRING, \
    MERGE_BY_TOPIC_NAME_FEATURE_STRING, READ_ONLY_FEATURE_STRING, \
    TYPE_INSTANCE_ASSOCIATIONS_FEATURE_STRING

from tmapi.exceptions import FeatureNotRecognizedException, \
    FeatureNotSupportedException

from .tmapi_feature import TMAPIFeature
from .topic_map_system import TopicMapSystem


class TopicMapSystemFactory:

    """This factory class provides access to a topic map system.

    A new `TopicMapSystem` instance is created by invoking the
    `new_topic_map_system()` method. Configuration properties for the
    new `TopicMapSystem` instance can be set by calling the
    `set_feature(string, boolean)` and/or `set_property(string,
    object)` methods prior to invoking `new_topic_map_system()`.

    """

    # Dictionary of recognised feature strings, specifying their state
    # (enabled/disabled) and whether they are supported.
    _features = {
        AUTOMERGE_FEATURE_STRING: [True, True],
        MERGE_BY_TOPIC_NAME_FEATURE_STRING: [False, False],
        READ_ONLY_FEATURE_STRING: [False, False],
        TYPE_INSTANCE_ASSOCIATIONS_FEATURE_STRING: [False, False],
        }
    _properties = {}

    def get_feature (self, feature_name):
        """Returns the particular feature requested for in the
        underlying implementation of `TopicMapSystem`.

        :param feature_name: the name of the feature to check
        :type feature_name: string
        :rtype: Boolean

        """
        if feature_name in self._features:
            return self._features[feature_name][0]
        raise FeatureNotRecognizedException

    def get_property (self, property_name):
        """Gets the value of a property in the underlying
        implementation of `TopicMapSystem`.

        A list of the core properties defined by TMAPI can be found at
        http://tmapi.org/properties/.

        An implementation is free to support properties other than the
        core ones.

        :param property_name: the name of the property to retrieve
        :type property_name: string
        :rtype: the value set or None

        """
        return self._properties.get(property_name, None)

    def has_feature (self, feature_name):
        """Returns if the particular feature is supported by the
        `TopicMapSystem`.

        Opposite to `get_feature(string)` this method returns if the
        requested feature is generally available/supported by the
        underlying `TopicMapSystem` and does not return the state
        (enabled/disabled) of the feature.

        :param feature_name: the name of the feature to check
        :type feature_name: string
        :rtype: Boolean

        """
        has_feature = False
        if feature_name in self._features:
            has_feature = True
        return has_feature

    @staticmethod
    def new_instance ():
        """Obtain a new instance of a TopicMapSystemFactory.

        This static method creates a new factory instance. In this
        system, there is no lookup procedure to determine which
        implementation class to load, and the implementation class is
        this one. That is, calling
        TopicMapSystemFactory.new_instance() is equivalent to calling
        TopicMapSystemFactory().

        Once an application has obtained a reference to a
        TopicMapSystemFactory it can use the factory to configure and
        obtain TopicMapSystem instances.

        :rtype: `TopicMapSystemFactory`

        """
        return TopicMapSystemFactory()

    def new_topic_map_system (self):
        """Creates a new `TopicMapSystem` instance using the currently
        configured factory parameters.

        :rtype: `TopicMapSystem`

        """
        tms = TopicMapSystem()
        tms.save()
        for feature_string, values in list(self._features.items()):
            feature = TMAPIFeature(feature_string=feature_string,
                                   topic_map_system=tms, value=values[0])
            feature.save()
        return tms

    def set_feature (self, feature_name, enable):
        """Sets a particular feature in the underlying implementation
        of `TopicMapSystem`.

        A list of the core features can be found at
        http://tmapi.org/features/.

        :param feature_name: the name of the feature to be set
        :type feature_name: string
        :param enable: True to enable the feature, False to disable it
        :type enable: Boolean

        """
        if feature_name in self._features:
            if self._features[feature_name][1]:
                self._features[feature_name][0] = enable
            elif self._features[feature_name][0] == enable:
                # Do nothing if trying to set the feature to its
                # current value, even if it is not permitted to change
                # the value.
                pass
            else:
                raise FeatureNotSupportedException
        else:
            raise FeatureNotRecognizedException

    def set_property (self, property_name, value):
        """Sets a property in the underlying implementation of
        `TopicMapSystem`.

        A list of the core properties defined by TMAPI can be found at
        http://tmapi.org/properties/.

        An implementation is free to support properties other than the
        core ones.

        :param property_name: the name of the property to be set
        :type property_name: string
        :param value: the value to be of this property
        :type value: object or None to remove the property

        """
        raise Exception('Not yet implemented')
