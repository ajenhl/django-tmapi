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

"""Module containing tests of the 'same topic map' constraint.

Most if not all of these tests are ported from the public domain tests
that come with the TMAPI 2.0 distribution (http://www.tmapi.org/2.0/).

"""

from tmapi.exceptions import ModelConstraintException

from .tmapi_test_case import TMAPITestCase


class SameTopicMapTest (TMAPITestCase):

    def setUp (self):
        super(SameTopicMapTest, self).setUp()
        self.tm2 = self.tms.create_topic_map(
            'http://www.tmapi.org/same-topicmap')

    def test_association_creation_illegal_type (self):
        self.assertRaises(ModelConstraintException, self.tm.create_association,
                          self.tm2.create_topic())

    def test_association_creation_illegal_scope (self):
        self.assertRaises(ModelConstraintException, self.tm.create_association,
            self.create_topic(), [self.create_topic(),
            self.tm2.create_topic()])

    def test_association_creation_illegal_scope_collection (self):
        # This test is not applicable to this implementation.
        pass

    def test_name_creation_illegal_type (self):
        topic = self.create_topic()
        self.assertRaises(ModelConstraintException, topic.create_name,
                          'value', self.tm2.create_topic())

    def test_name_creation_illegal_scope (self):
        topic = self.create_topic()
        self.assertRaises(ModelConstraintException, topic.create_name,
                          'value', self.create_topic(),
                          [self.tm2.create_topic()])

    def test_name_creation_illegal_scope_collection (self):
        # This test is not applicable to this implementation.
        pass

    def test_occurrence_creation_illegal_type (self):
        topic = self.create_topic()
        self.assertRaises(ModelConstraintException, topic.create_occurrence,
                          self.tm2.create_topic(), 'value')

    def test_occurrence_creation_illegal_scope (self):
        topic = self.tm.create_topic()
        self.assertRaises(ModelConstraintException, topic.create_occurrence,
                          self.tm.create_topic(), 'value',
                          [self.tm.create_topic(), self.tm2.create_topic()])

    def test_occurrence_creation_illegal_scope_collection (self):
        # This test is not applicable to this implementation.
        pass

    def test_role_creation_illegal_type (self):
        association = self.create_association()
        self.assertRaises(ModelConstraintException, association.create_role,
                          self.tm2.create_topic(), self.create_topic())

    def test_role_creation_illegal_player (self):
        association = self.create_association()
        self.assertRaises(ModelConstraintException, association.create_role,
                          self.create_topic(), self.tm2.create_topic())

    def _test_illegal_theme (self, scoped):
        self.assertRaises(ModelConstraintException, scoped.add_theme,
                          self.tm2.create_topic())

    def test_association_illegal_theme (self):
        self._test_illegal_theme(self.create_association())

    def test_occurrence_illegal_theme (self):
        self._test_illegal_theme(self.create_occurrence())

    def test_name_illegal_theme (self):
        self._test_illegal_theme(self.create_name())

    def test_variant_illegal_theme (self):
        self._test_illegal_theme(self.create_variant())

    def _test_illegal_type (self, typed):
        self.assertRaises(ModelConstraintException, typed.set_type,
                          self.tm2.create_topic())

    def test_association_illegal_type (self):
        self._test_illegal_type(self.create_association())

    def test_role_illegal_type (self):
        self._test_illegal_type(self.create_role())

    def test_occurrence_illegal_type (self):
        self._test_illegal_type(self.create_occurrence())

    def test_name_illegal_type (self):
        self._test_illegal_type(self.create_name())

    def test_role_illegal_player (self):
        role = self.create_role()
        self.assertRaises(ModelConstraintException, role.set_player,
                          self.tm2.create_topic())

    def _test_illegal_reifier (self, reifiable):
        self.assertRaises(ModelConstraintException, reifiable.set_reifier,
                          self.tm2.create_topic())

    def test_topic_map_illegal_reifier (self):
        self._test_illegal_reifier(self.tm)

    def test_association_illegal_reifier (self):
        self._test_illegal_reifier(self.create_association())

    def test_role_illegal_reifier (self):
        self._test_illegal_reifier(self.create_role())

    def test_occurrence_illegal_reifier (self):
        self._test_illegal_reifier(self.create_occurrence())

    def test_name_illegal_reifier (self):
        self._test_illegal_reifier(self.create_name())

    def test_variant_illegal_reifier (self):
        self._test_illegal_reifier(self.create_variant())

    def test_illegal_topic_type (self):
        self.assertRaises(
            ModelConstraintException, self.create_topic().add_type,
            self.tm2.create_topic())
