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

"""Module containing tests for the Topic model.

Most if not all of these tests are ported from the public domain tests
that come with the TMAPI 2.0 distribution (http://www.tmapi.org/2.0/).

"""

from tmapi.exceptions import ModelConstraintException

from .tmapi_test_case import TMAPITestCase


class TopicTest (TMAPITestCase):

    def test_parent (self):
        """Tests the parent/child relationship between topic map and topic."""
        parent = self.create_topic_map('http://www.tmapi.org/test/topic/parent')
        self.assertEqual(0, parent.get_topics().count(),
                         'Expected new topic map to be created with no topics')
        topic = parent.create_topic()
        self.assertEqual(parent, topic.get_parent(),
                         'Unexpceted topic parent after creation')
        self.assertEqual(1, parent.get_topics().count(),
                         'Expected topic list size to increment for topic map')
        self.assertTrue(topic in parent.get_topics(),
                        'Topic is not part of get_topics()')
        topic.remove()
        self.assertEqual(0, parent.get_topics().count(),
                         'Expected topic list size to decrement for topic map')

    def test_add_subject_identifier_illegal (self):
        topic = self.create_topic()
        self.assertRaises(ModelConstraintException,
                          topic.add_subject_identifier, None)

    def test_add_subject_locator_illegal (self):
        topic = self.create_topic()
        self.assertRaises(ModelConstraintException, topic.add_subject_locator,
                          None)

    def test_subject_identifiers (self):
        locator1 = self.tm.create_locator('http://www.example.org/1')
        locator2 = self.tm.create_locator('http://www.example.org/2')
        topic = self.tm.create_topic_by_subject_identifier(locator1)
        self.assertEqual(1, topic.get_subject_identifiers().count())
        self.assertTrue(locator1 in topic.get_subject_identifiers())
        topic.add_subject_identifier(locator2)
        self.assertEqual(2, topic.get_subject_identifiers().count())
        self.assertTrue(locator2 in topic.get_subject_identifiers())
        topic.remove_subject_identifier(locator1)
        self.assertEqual(1, topic.get_subject_identifiers().count())
        self.assertTrue(locator2 in topic.get_subject_identifiers())

    def test_subject_locators (self):
        locator1 = self.create_locator('http://www.example.org/1')
        locator2 = self.create_locator('http://www.example.org/2')
        topic = self.tm.create_topic_by_subject_locator(locator1)
        self.assertEqual(1, topic.get_subject_locators().count())
        self.assertTrue(locator1 in topic.get_subject_locators())
        topic.add_subject_locator(locator2)
        self.assertEqual(2, topic.get_subject_locators().count())
        self.assertTrue(locator2 in topic.get_subject_locators())
        topic.remove_subject_locator(locator1)
        self.assertEqual(1, topic.get_subject_locators().count())
        self.assertTrue(locator2 in topic.get_subject_locators())

    def test_topic_types (self):
        topic = self.create_topic()
        type1 = self.create_topic()
        type2 = self.create_topic()
        self.assertEqual(0, topic.get_types().count())
        topic.add_type(type1)
        self.assertEqual(1, topic.get_types().count())
        self.assertTrue(type1 in topic.get_types())
        topic.add_type(type2)
        self.assertEqual(2, topic.get_types().count())
        self.assertTrue(type2 in topic.get_types())
        topic.remove_type(type1)
        self.assertEqual(1, topic.get_types().count())
        self.assertTrue(type2 in topic.get_types())
        topic.remove_type(type2)
        self.assertEqual(0, topic.get_types().count())

    def test_add_type_illegal (self):
        topic = self.create_topic()
        self.assertRaises(ModelConstraintException, topic.add_type, None)

    def test_role_filter (self):
        player = self.tm.create_topic()
        type1 = self.create_topic()
        type2 = self.create_topic()
        unused_type = self.create_topic()
        association = self.create_association()
        self.assertEqual(0, player.get_roles_played(type1).count())
        self.assertEqual(0, player.get_roles_played(type2).count())
        self.assertEqual(0, player.get_roles_played(unused_type).count())
        role = association.create_role(type1, player)
        self.assertEqual(1, player.get_roles_played(type1).count())
        self.assertTrue(role in player.get_roles_played(type1))
        self.assertEqual(0, player.get_roles_played(type2).count())
        self.assertEqual(0, player.get_roles_played(unused_type).count())
        role.set_type(type2)
        self.assertEqual(1, player.get_roles_played(type2).count())
        self.assertTrue(role in player.get_roles_played(type2))
        self.assertEqual(0, player.get_roles_played(type1).count())
        self.assertEqual(0, player.get_roles_played(unused_type).count())
        role.remove()
        self.assertEqual(0, player.get_roles_played(type1).count())
        self.assertEqual(0, player.get_roles_played(type2).count())
        self.assertEqual(0, player.get_roles_played(unused_type).count())

    def test_role_filter_illegal (self):
        # This test is not applicable to this implementation.
        pass

    def test_role_association_filter (self):
        player = self.create_topic()
        association_type1 = self.create_topic()
        association_type2 = self.create_topic()
        role_type1 = self.create_topic()
        role_type2 = self.create_topic()
        association = self.tm.create_association(association_type1)
        self.assertEqual(0, player.get_roles_played(role_type1,
                                                    association_type1).count())
        self.assertEqual(0, player.get_roles_played(role_type1,
                                                    association_type2).count())
        self.assertEqual(0, player.get_roles_played(role_type2,
                                                    association_type1).count())
        self.assertEqual(0, player.get_roles_played(role_type2,
                                                    association_type2).count())
        role1 = association.create_role(role_type1, player)
        self.assertEqual(1, player.get_roles_played(role_type1,
                                                    association_type1).count())
        self.assertTrue(role1 in player.get_roles_played(role_type1,
                                                         association_type1))
        self.assertEqual(0, player.get_roles_played(role_type1,
                                                    association_type2).count())
        self.assertEqual(0, player.get_roles_played(role_type2,
                                                    association_type1).count())
        self.assertEqual(0, player.get_roles_played(role_type2,
                                                    association_type2).count())
        role2 = association.create_role(role_type2, player)
        self.assertEqual(1, player.get_roles_played(role_type1,
                                                    association_type1).count())
        self.assertTrue(role1 in player.get_roles_played(role_type1,
                                                         association_type1))
        self.assertEqual(0, player.get_roles_played(role_type1,
                                                    association_type2).count())
        self.assertEqual(1, player.get_roles_played(role_type2,
                                                    association_type1).count())
        self.assertTrue(role2 in player.get_roles_played(role_type2,
                                                         association_type1))
        self.assertEqual(0, player.get_roles_played(role_type2,
                                                    association_type2).count())
        role2.set_type(role_type1)
        self.assertEqual(2, player.get_roles_played(role_type1,
                                                    association_type1).count())
        self.assertTrue(role1 in player.get_roles_played(role_type1,
                                                         association_type1))
        self.assertTrue(role2 in player.get_roles_played(role_type1,
                                                         association_type1))
        self.assertEqual(0, player.get_roles_played(role_type1,
                                                    association_type2).count())
        self.assertEqual(0, player.get_roles_played(role_type2,
                                                    association_type1).count())
        self.assertEqual(0, player.get_roles_played(role_type2,
                                                    association_type2).count())
        role1.remove()
        self.assertEqual(1, player.get_roles_played(role_type1,
                                                    association_type1).count())
        self.assertTrue(role2 in player.get_roles_played(role_type1,
                                                         association_type1))
        self.assertEqual(0, player.get_roles_played(role_type1,
                                                    association_type2).count())
        self.assertEqual(0, player.get_roles_played(role_type2,
                                                    association_type1).count())
        self.assertEqual(0, player.get_roles_played(role_type2,
                                                    association_type2).count())
        association.remove()
        self.assertEqual(0, player.get_roles_played(role_type1,
                                                    association_type1).count())
        self.assertEqual(0, player.get_roles_played(role_type1,
                                                    association_type2).count())
        self.assertEqual(0, player.get_roles_played(role_type2,
                                                    association_type1).count())
        self.assertEqual(0, player.get_roles_played(role_type2,
                                                    association_type2).count())

    def test_role_association_filter_illegal_association (self):
        # This test is not applicable to this implementation.
        pass

    def test_role_association_filter_illegal_role (self):
        # This test is not applicable to this implementation.
        pass

    def test_occurrence_filter (self):
        topic = self.create_topic()
        type1 = self.create_topic()
        type2 = self.create_topic()
        unused_type = self.create_topic()
        self.assertEqual(0, topic.get_occurrences(type1).count())
        self.assertEqual(0, topic.get_occurrences(type2).count())
        self.assertEqual(0, topic.get_occurrences(unused_type).count())
        occurrence = topic.create_occurrence(type1, 'Occurrence')
        self.assertEqual(1, topic.get_occurrences(type1).count())
        self.assertTrue(occurrence, topic.get_occurrences(type1))
        self.assertEqual(0, topic.get_occurrences(type2).count())
        self.assertEqual(0, topic.get_occurrences(unused_type).count())
        occurrence.set_type(type2)
        self.assertEqual(1, topic.get_occurrences(type2).count())
        self.assertTrue(occurrence, topic.get_occurrences(type2))
        self.assertEqual(0, topic.get_occurrences(type1).count())
        self.assertEqual(0, topic.get_occurrences(unused_type).count())
        occurrence.remove()
        self.assertEqual(0, topic.get_occurrences(type1).count())
        self.assertEqual(0, topic.get_occurrences(type2).count())
        self.assertEqual(0, topic.get_occurrences(unused_type).count())

    def test_occurrence_filter_illegal (self):
        # This test is not applicable to this implementation.
        pass

    def test_name_filter (self):
        topic = self.create_topic()
        type1 = self.create_topic()
        type2 = self.create_topic()
        unused_type = self.create_topic()
        self.assertEqual(0, topic.get_names(type1).count())
        self.assertEqual(0, topic.get_names(type2).count())
        self.assertEqual(0, topic.get_names(unused_type).count())
        name = topic.create_name('Name', type1)
        self.assertEqual(1, topic.get_names(type1).count())
        self.assertTrue(name in topic.get_names(type1))
        self.assertEqual(0, topic.get_names(type2).count())
        self.assertEqual(0, topic.get_names(unused_type).count())
        name.set_type(type2)
        self.assertEqual(1, topic.get_names(type2).count())
        self.assertTrue(name in topic.get_names(type2))
        self.assertEqual(0, topic.get_names(type1).count())
        self.assertEqual(0, topic.get_names(unused_type).count())
        name.remove()
        self.assertEqual(0, topic.get_names(type1).count())
        self.assertEqual(0, topic.get_names(type2).count())
        self.assertEqual(0, topic.get_names(unused_type).count())

    def test_name_filter_illegal (self):
        # This test is not applicable to this implementation.
        pass

    def test_occurrence_creation_type_string (self):
        topic = self.create_topic()
        type = self.create_topic()
        value = 'Occurrence'
        dt = self.create_locator('http://www.w3.org/2001/XMLSchema#string')
        self.assertEqual(0, topic.get_occurrences().count())
        occurrence = topic.create_occurrence(type, value)
        self.assertEqual(1, topic.get_occurrences().count())
        self.assertTrue(occurrence in topic.get_occurrences())
        self.assertEqual(0, occurrence.get_scope().count())
        self.assertEqual(type, occurrence.get_type())
        self.assertEqual(value, occurrence.get_value())
        self.assertEqual(dt, occurrence.get_datatype())
        self.assertEqual(0, occurrence.get_item_identifiers().count())

    def test_occurrence_creation_type_uri (self):
        topic = self.create_topic()
        type = self.create_topic()
        value = self.create_locator('http://www.example.org/')
        dt = self.create_locator('http://www.w3.org/2001/XMLSchema#anyURI')
        self.assertEqual(0, topic.get_occurrences().count())
        occurrence = topic.create_occurrence(type, value)
        self.assertEqual(1, topic.get_occurrences().count())
        self.assertTrue(occurrence in topic.get_occurrences())
        self.assertEqual(0, occurrence.get_scope().count())
        self.assertEqual(type, occurrence.get_type())
        self.assertEqual(value, occurrence.get_value())
        self.assertEqual(dt, occurrence.get_datatype())
        self.assertEqual(0, occurrence.get_item_identifiers().count())

    def test_occurrence_creation_type_explicit_datatype (self):
        topic = self.create_topic()
        type = self.create_topic()
        value = 'Occurrence'
        dt = self.create_locator('http://www.example.org/datatype')
        self.assertEqual(0, topic.get_occurrences().count())
        occurrence = topic.create_occurrence(type, value, datatype=dt)
        self.assertEqual(1, topic.get_occurrences().count())
        self.assertTrue(occurrence in topic.get_occurrences())
        self.assertEqual(0, occurrence.get_scope().count())
        self.assertEqual(type, occurrence.get_type())
        self.assertEqual(value, occurrence.get_value())
        self.assertEqual(dt, occurrence.get_datatype())
        self.assertEqual(0, occurrence.get_item_identifiers().count())

    def test_occurrence_creation_type_scope_string (self):
        topic = self.create_topic()
        type = self.create_topic()
        theme1 = self.create_topic()
        theme2 = self.create_topic()
        value = 'Occurrence'
        dt = self.create_locator('http://www.w3.org/2001/XMLSchema#string')
        self.assertEqual(0, topic.get_occurrences().count())
        occurrence = topic.create_occurrence(type, value, [theme1, theme2])
        self.assertEqual(1, topic.get_occurrences().count())
        self.assertTrue(occurrence in topic.get_occurrences())
        self.assertEqual(2, occurrence.get_scope().count())
        self.assertTrue(theme1 in occurrence.get_scope())
        self.assertTrue(theme2 in occurrence.get_scope())
        self.assertEqual(type, occurrence.get_type())
        self.assertEqual(value, occurrence.get_value())
        self.assertEqual(dt, occurrence.get_datatype())
        self.assertEqual(0, occurrence.get_item_identifiers().count())

    def test_occurrence_creation_type_scope_uri (self):
        topic = self.create_topic()
        type = self.create_topic()
        theme1 = self.create_topic()
        theme2 = self.create_topic()
        value = self.create_locator('http://www.example.org/')
        dt = self.create_locator('http://www.w3.org/2001/XMLSchema#anyURI')
        self.assertEqual(0, topic.get_occurrences().count())
        occurrence = topic.create_occurrence(type, value, [theme1, theme2])
        self.assertEqual(1, topic.get_occurrences().count())
        self.assertTrue(occurrence in topic.get_occurrences())
        self.assertEqual(2, occurrence.get_scope().count())
        self.assertTrue(theme1 in occurrence.get_scope())
        self.assertTrue(theme2 in occurrence.get_scope())
        self.assertEqual(type, occurrence.get_type())
        self.assertEqual(value, occurrence.get_value())
        self.assertEqual(dt, occurrence.get_datatype())
        self.assertEqual(0, occurrence.get_item_identifiers().count())

    def test_occurrence_creation_type_scope_explicit_datatype (self):
        topic = self.create_topic()
        type = self.create_topic()
        theme1 = self.create_topic()
        theme2 = self.create_topic()
        value = 'Occurrence'
        dt = self.create_locator('http://www.example.org/datatype')
        self.assertEqual(0, topic.get_occurrences().count())
        occurrence = topic.create_occurrence(type, value, [theme1, theme2], dt)
        self.assertEqual(1, topic.get_occurrences().count())
        self.assertTrue(occurrence in topic.get_occurrences())
        self.assertEqual(2, occurrence.get_scope().count())
        self.assertTrue(theme1 in occurrence.get_scope())
        self.assertTrue(theme2 in occurrence.get_scope())
        self.assertEqual(type, occurrence.get_type())
        self.assertEqual(value, occurrence.get_value())
        self.assertEqual(dt, occurrence.get_datatype())
        self.assertEqual(0, occurrence.get_item_identifiers().count())

    def test_occurrence_creation_type_illegal_string (self):
        topic = self.create_topic()
        self.assertRaises(ModelConstraintException, topic.create_occurrence,
                          self.create_topic(), None)

    def test_occurrence_creation_type_illegal_uri (self):
        # Note that this is identical to the previous test, given
        # Python's lack of typing.
        topic = self.create_topic()
        self.assertRaises(ModelConstraintException, topic.create_occurrence,
                          self.create_topic(), None)

    def test_occurrence_creation_type_illegal_datatype (self):
        # This test is not applicable to this implementation.
        pass

    def test_occurrence_creation_illegal_type (self):
        topic = self.create_topic()
        self.assertRaises(ModelConstraintException, topic.create_occurrence,
                          None, 'Occurrence')

    def test_occurrence_creation_type_illegal_scope (self):
        # This test is not applicable to this implementation.
        pass

    def test_name_creation_type (self):
        topic = self.create_topic()
        type = self.create_topic()
        value = 'Name'
        self.assertEqual(0, topic.get_names().count())
        name = topic.create_name(value, type)
        self.assertEqual(1, topic.get_names().count())
        self.assertTrue(name in topic.get_names())
        self.assertEqual(0, name.get_scope().count())
        self.assertEqual(type, name.get_type())
        self.assertEqual(value, name.get_value())
        self.assertEqual(0, name.get_item_identifiers().count())

    def test_name_creation_type_scope_single (self):
        topic = self.create_topic()
        type = self.create_topic()
        theme = self.create_topic()
        value = 'Name'
        self.assertEqual(0, topic.get_names().count())
        name = topic.create_name(value, type, [theme])
        self.assertEqual(1, topic.get_names().count())
        self.assertTrue(name in topic.get_names())
        self.assertEqual(1, name.get_scope().count())
        self.assertTrue(theme in name.get_scope())
        self.assertEqual(type, name.get_type())
        self.assertEqual(value, name.get_value())
        self.assertEqual(0, name.get_item_identifiers().count())

    def test_name_creation_type_scope_multiple (self):
        topic = self.create_topic()
        type = self.create_topic()
        theme1 = self.create_topic()
        theme2 = self.create_topic()
        value = 'Name'
        self.assertEqual(0, topic.get_names().count())
        name = topic.create_name(value, type, [theme1, theme2])
        self.assertEqual(1, topic.get_names().count())
        self.assertTrue(name in topic.get_names())
        self.assertEqual(2, name.get_scope().count())
        self.assertTrue(theme1 in name.get_scope())
        self.assertTrue(theme2 in name.get_scope())
        self.assertEqual(type, name.get_type())
        self.assertEqual(value, name.get_value())
        self.assertEqual(0, name.get_item_identifiers().count())

    def test_name_creation_default_type (self):
        topic = self.create_topic()
        value = 'Name'
        locator = self.create_locator(
            'http://psi.topicmaps.org/iso13250/model/topic-name')
        self.assertEqual(0, topic.get_names().count())
        name = topic.create_name(value)
        self.assertEqual(1, topic.get_names().count())
        self.assertTrue(name in topic.get_names())
        self.assertEqual(0, name.get_scope().count())
        self.assertTrue(name.get_type())
        self.assertEqual(value, name.get_value())
        self.assertEqual(0, name.get_item_identifiers().count())
        type = name.get_type()
        self.assertTrue(locator in type.get_subject_identifiers())

    def test_name_creation_default_type_scope_single (self):
        topic = self.create_topic()
        theme = self.create_topic()
        value = 'Name'
        locator = self.create_locator(
            'http://psi.topicmaps.org/iso13250/model/topic-name')
        self.assertEqual(0, topic.get_names().count())
        name = topic.create_name(value, scope=[theme])
        self.assertEqual(1, topic.get_names().count())
        self.assertTrue(name in topic.get_names())
        self.assertEqual(1, name.get_scope().count())
        self.assertTrue(theme in name.get_scope())
        self.assertTrue(name.get_type())
        self.assertEqual(value, name.get_value())
        self.assertEqual(0, name.get_item_identifiers().count())
        type = name.get_type()
        self.assertTrue(locator in type.get_subject_identifiers())

    def test_name_creation_default_type_scope_multiple (self):
        topic = self.create_topic()
        theme1 = self.create_topic()
        theme2 = self.create_topic()
        value = 'Name'
        locator = self.create_locator(
            'http://psi.topicmaps.org/iso13250/model/topic-name')
        self.assertEqual(0, topic.get_names().count())
        name = topic.create_name(value, scope=[theme1, theme2])
        self.assertEqual(1, topic.get_names().count())
        self.assertTrue(name in topic.get_names())
        self.assertEqual(2, name.get_scope().count())
        self.assertTrue(theme1 in name.get_scope())
        self.assertTrue(theme2 in name.get_scope())
        self.assertTrue(name.get_type())
        self.assertEqual(value, name.get_value())
        self.assertEqual(0, name.get_item_identifiers().count())
        type = name.get_type()
        self.assertTrue(locator in type.get_subject_identifiers())

    def test_name_creation_type_illegal_string (self):
        topic = self.create_topic()
        self.assertRaises(ModelConstraintException, topic.create_name,
                          None, self.create_topic())

    def test_name_creation_type_illegal_scope (self):
        # This test is not applicable to this implementation.
        pass

    def test_name_creation_default_type_illegal_string (self):
        topic = self.create_topic()
        self.assertRaises(ModelConstraintException, topic.create_name, None)

    def test_name_creation_default_type_illegal_scope_array (self):
        # This test is not applicable to this implementation.
        pass

    def test_name_creation_default_type_illegal_scope_collection (self):
        # This test is not applicable to this implementation.
        pass
