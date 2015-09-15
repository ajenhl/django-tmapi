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

"""Module containing tests if the TMAPI feature strings are recognised.

Most if not all of these tests are ported from the public domain tests
that come with the TMAPI 2.0 distribution (http://www.tmapi.org/2.0/).

"""

from django.test import TestCase

from tmapi.exceptions import TMAPIException, TMAPIRuntimeException, \
    FeatureNotSupportedException
from tmapi.models import TopicMapSystemFactory


class FeatureStringsTest (TestCase):

    FEATURE_BASE = 'http://tmapi.org/features/'
    TYPE_INSTANCE_ASSOCIATIONS = FEATURE_BASE + 'type-instance-associations'
    READ_ONLY = FEATURE_BASE + 'readOnly'
    AUTOMERGE = FEATURE_BASE + 'automerge'

    def setUp (self):
        self.factory = TopicMapSystemFactory()

    def make_topic_map_system (self):
        """Creates a new `TopicMapSystem` with the current
        configuration of the `factory`.

        :rtype: `TopicMapSystem`

        """
        try:
            return self.factory.new_topic_map_system()
        except TMAPIException as ex:
            raise TMAPIRuntimeException('Cannot create TopicMapSystem', ex)

    def _test_feature (self, feature_name):
        """Tests the provided `feature_name`. The `feature_name` must
        be recognised by the engine.

        :param feature_name: name of the feature to be tested
        :type feature_name: string

        """
        enabled_in_factory = self.factory.get_feature(feature_name)
        try:
            self.factory.set_feature(feature_name, enabled_in_factory)
        except FeatureNotSupportedException:
            self.fail('The engine does not allow setting the feature string to the default value returned by factory.get_feature(' + feature_name + ')')
        tms = self.make_topic_map_system()
        enabled_in_system = tms.get_feature(feature_name)
        self.assertEqual(enabled_in_factory, enabled_in_system,
                         'The system has a different value of ' + feature_name
                         + ' than the factory')

    def test_type_instance_associations (self):
        """Tests the feature string "type-instance-associations"."""
        self._test_feature(self.TYPE_INSTANCE_ASSOCIATIONS)

    def test_automerge (self):
        """Tests the feature string "automerge"."""
        self._test_feature(self.AUTOMERGE)

    def test_read_only (self):
        """Tests the feature string "readOnly"."""
        self._test_feature(self.READ_ONLY)
