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

"""Module containing tests against the `TypeInstanceIndex` interface.

Most if not all of these tests are ported from the public domain tests
that come with the TMAPI 2.0 distribution (http://www.tmapi.org/2.0/).

"""

from tmapi.constants import TYPE_INSTANCE_ASSOCIATIONS_FEATURE_STRING
from tmapi.indices.type_instance_index import TypeInstanceIndex
from tmapi.tests.models.tmapi_test_case import TMAPITestCase


class TypeInstanceIndexTest (TMAPITestCase):

    def setUp (self):
        super(TypeInstanceIndexTest, self).setUp()
        self._index = self.tm.get_index(TypeInstanceIndex)
        self._index.open()

    def tearDown (self):
        super(TypeInstanceIndexTest, self).tearDown()
        self._index.close()

    def _update_index (self):
        if not self._index.is_auto_updated():
            self._index.reindex()
        
    def test_topic (self):
        self._update_index()
        self.assertEqual(0, self._index.get_topics().count())
        self.assertEqual(0, self._index.get_topic_types().count())
        topic = self.tm.create_topic()
        self._update_index()
        self.assertEqual(0, self._index.get_topic_types().count())
        self.assertEqual(1, self._index.get_topics().count())
        self.assertTrue(topic in self._index.get_topics())
        type1 = self.tm.create_topic()
        type2 = self.tm.create_topic()
        self._update_index()
        self.assertEqual(0, self._index.get_topic_types().count())
        self.assertEqual(3, self._index.get_topics().count())
        self.assertTrue(topic in self._index.get_topics())
        self.assertTrue(type1 in self._index.get_topics())
        self.assertTrue(type2 in self._index.get_topics())
        self.assertEqual(0, self._index.get_topics(
                [type1, type2], match_all=False).count())
        self.assertEqual(0, self._index.get_topics(
                [type1, type2], match_all=True).count())
        # Topic with one type.
        topic.add_type(type1)
        self._update_index()
        self.assertEqual(1, self._index.get_topic_types().count())
        self.assertTrue(type1 in self._index.get_topic_types())
        if self.tms.get_feature(TYPE_INSTANCE_ASSOCIATIONS_FEATURE_STRING):
            self.assertEqual(5, self._index.get_topics().count())
        else:
            self.assertEqual(2, self._index.get_topics().count())
        self.assertFalse(topic in self._index.get_topics())
        self.assertTrue(type1 in self._index.get_topics())
        self.assertTrue(type2 in self._index.get_topics())
        self.assertEqual(1, self._index.get_topics(type1).count())
        self.assertEqual(1, self._index.get_topics(
                [type1, type2], match_all=False).count())
        self.assertTrue(topic in self._index.get_topics(
                [type1, type2], match_all=False))
        self.assertEqual(0, self._index.get_topics(
                [type1, type2], match_all=True).count())
        # Topic with two types.
        topic.add_type(type2)
        self._update_index()
        self.assertEqual(2, self._index.get_topic_types().count())
        self.assertTrue(type1 in self._index.get_topic_types())
        self.assertTrue(type2 in self._index.get_topic_types())
        if self.tms.get_feature(TYPE_INSTANCE_ASSOCIATIONS_FEATURE_STRING):
            self.assertEqual(5, self._index.get_topics().count())
        else:
            self.assertEqual(2, self._index.get_topics().count())
        self.assertFalse(topic in self._index.get_topics())
        self.assertTrue(type1 in self._index.get_topics())
        self.assertTrue(type2 in self._index.get_topics())
        self.assertEqual(1, self._index.get_topics(type1).count())
        self.assertTrue(topic in self._index.get_topics(type1))
        self.assertEqual(1, self._index.get_topics(type2).count())
        self.assertTrue(topic in self._index.get_topics(type2))
        self.assertEqual(1, self._index.get_topics(
                [type1, type2], match_all=False).count())
        self.assertTrue(topic in self._index.get_topics(
                [type1, type2], match_all=False))
        self.assertEqual(1, self._index.get_topics(
                [type1, type2], match_all=True).count())
        self.assertTrue(topic in self._index.get_topics(
                [type1, type2], match_all=True))
        # Topic removal.
        topic.remove()
        self._update_index()
        self.assertEqual(0, self._index.get_topic_types().count())
        if self.tms.get_feature(TYPE_INSTANCE_ASSOCIATIONS_FEATURE_STRING):
            self.assertEqual(5, self._index.get_topics().count())
        else:
            self.assertEqual(2, self._index.get_topics().count())
        self.assertTrue(type1 in self._index.get_topics())
        self.assertTrue(type2 in self._index.get_topics())
        self.assertEqual(0, self._index.get_topics(type1).count())
        self.assertEqual(0, self._index.get_topics(type2).count())
        self.assertEqual(0, self._index.get_topics(
                [type1, type2], match_all=False).count())
        self.assertEqual(0, self._index.get_topics(
                [type1, type2], match_all=True).count())

    def test_association (self):
        type = self.create_topic()
        self._update_index()
        self.assertEqual(0, self._index.get_associations(type).count())
        self.assertEqual(0, self._index.get_association_types().count())
        typed = self.create_association()
        self._update_index()
        self.assertEqual(0, self._index.get_associations(type).count())
        self.assertFalse(type in self._index.get_association_types())
        self.assertEqual(1, self._index.get_association_types().count())
        typed.set_type(type)
        self._update_index()
        self.assertNotEqual(0, self._index.get_association_types().count())
        self.assertEqual(1, self._index.get_associations(type).count())
        self.assertTrue(typed in self._index.get_associations(type))
        self.assertTrue(type in self._index.get_association_types())
        typed.set_type(self.create_topic())
        self._update_index()
        self.assertFalse(type in self._index.get_association_types())
        self.assertEqual(1, self._index.get_association_types().count())
        typed.set_type(type)
        typed.remove()
        self._update_index()
        self.assertEqual(0, self._index.get_associations(type).count())
        self.assertEqual(0, self._index.get_association_types().count())

    def test_role (self):
        type = self.create_topic()
        self._update_index()
        self.assertEqual(0, self._index.get_roles(type).count())
        self.assertEqual(0, self._index.get_role_types().count())
        parent = self.create_association()
        typed = parent.create_role(self.create_topic(), self.create_topic())
        self._update_index()
        self.assertEqual(1, self._index.get_role_types().count())
        self.assertFalse(type in self._index.get_role_types())
        typed.set_type(type)
        self._update_index()
        self.assertEqual(1, self._index.get_role_types().count())
        self.assertEqual(1, self._index.get_roles(type).count())
        self.assertTrue(typed in self._index.get_roles(type))
        typed.set_type(self.create_topic())
        self._update_index()
        self.assertEqual(1, self._index.get_role_types().count())
        self.assertFalse(type in self._index.get_role_types())
        typed.set_type(type)
        typed.remove()
        self._update_index()
        self.assertEqual(0, self._index.get_roles(type).count())
        self.assertEqual(0, self._index.get_role_types().count())
        # The same test, but the parent is removed.
        typed = parent.create_role(type, self.create_topic())
        self._update_index()
        self.assertEqual(1, self._index.get_role_types().count())
        self.assertEqual(1, self._index.get_roles(type).count())
        self.assertTrue(typed in self._index.get_roles(type))
        parent.remove()
        self._update_index()
        self.assertEqual(0, self._index.get_roles(type).count())
        self.assertEqual(0, self._index.get_role_types().count())

    def test_occurrence (self):
        type = self.create_topic()
        self._update_index()
        self.assertEqual(0, self._index.get_occurrences(type).count())
        self.assertEqual(0, self._index.get_occurrence_types().count())
        parent = self.create_topic()
        typed = parent.create_occurrence(self.create_topic(), 'tinyTiM')
        self._update_index()
        self.assertEqual(0, self._index.get_occurrences(type).count())
        self.assertEqual(1, self._index.get_occurrence_types().count())
        self.assertFalse(type in self._index.get_occurrence_types())
        typed.set_type(type)
        self._update_index()
        self.assertEqual(1, self._index.get_occurrence_types().count())
        self.assertEqual(1, self._index.get_occurrences(type).count())
        self.assertTrue(typed in self._index.get_occurrences(type))
        self.assertTrue(type in self._index.get_occurrence_types())
        typed.set_type(self.create_topic())
        self._update_index()
        self.assertEqual(0, self._index.get_occurrences(type).count())
        self.assertEqual(1, self._index.get_occurrence_types().count())
        self.assertFalse(type in self._index.get_occurrence_types())
        typed.set_type(type)
        typed.remove()
        self._update_index()
        self.assertEqual(0, self._index.get_occurrences(type).count())
        self.assertEqual(0, self._index.get_occurrence_types().count())

    def test_name (self):
        type = self.tm.create_topic()
        self._update_index()
        self.assertEqual(0, self._index.get_names(type).count())
        self.assertEqual(0, self._index.get_name_types().count())
        parent = self.tm.create_topic()
        typed = parent.create_name('tinyTiM')
        self._update_index()
        self.assertEqual(1, self._index.get_name_types().count())
        self.assertFalse(type in self._index.get_name_types())
        self.assertEqual(0, self._index.get_names(type).count())
        typed.set_type(type)
        self._update_index()
        self.assertNotEqual(0, self._index.get_name_types().count())
        self.assertEqual(1, self._index.get_names(type).count())
        self.assertTrue(typed in self._index.get_names(type))
        self.assertTrue(type in self._index.get_name_types())
        typed.set_type(self.create_topic())
        self._update_index()
        self.assertEqual(0, self._index.get_names(type).count())
        self.assertFalse(type in self._index.get_name_types())
        self.assertEqual(1, self._index.get_name_types().count())
        typed.set_type(type)
        typed.remove()
        self._update_index()
        self.assertEqual(0, self._index.get_names(type).count())
        self.assertEqual(0, self._index.get_name_types().count())
