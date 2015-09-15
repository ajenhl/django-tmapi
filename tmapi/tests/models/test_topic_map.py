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

"""Module containing tests for the TopicMap model.

Most if not all of these tests are ported from the public domain tests
that come with the TMAPI 2.0 distribution (http://www.tmapi.org/2.0/).

"""

from tmapi.exceptions import ModelConstraintException, \
    UnsupportedOperationException

from .tmapi_test_case import TMAPITestCase


class TopicMapTest (TMAPITestCase):

    def test_parent (self):
        """Tests if TopicMap.get_parent() returns None."""
        self.assertEqual(None, self.tm.get_parent())

    def test_topic_creation_subject_identifier (self):
        locator = self.create_locator('http://www.example.org/')
        self.assertEqual(0, self.tm.get_topics().count())
        topic = self.tm.create_topic_by_subject_identifier(locator)
        self.assertEqual(1, self.tm.get_topics().count())
        self.assertTrue(topic in self.tm.get_topics())
        self.assertEqual(1, topic.get_subject_identifiers().count())
        self.assertEqual(0, topic.get_item_identifiers().count())
        self.assertEqual(0, topic.get_subject_locators().count())
        locator2 = topic.get_subject_identifiers()[0]
        self.assertEqual(locator, locator2)

    def test_topic_creation_subject_identifier_illegal (self):
        self.assertRaises(ModelConstraintException,
                          self.tm.create_topic_by_subject_identifier, None)

    def test_topic_creation_subject_locator (self):
        locator = self.create_locator('http://www.example.org/')
        self.assertEqual(0, self.tm.get_topics().count())
        topic = self.tm.create_topic_by_subject_locator(locator)
        self.assertEqual(1, self.tm.get_topics().count())
        self.assertTrue(topic in self.tm.get_topics())
        self.assertEqual(1, topic.get_subject_locators().count())
        self.assertEqual(0, topic.get_item_identifiers().count())
        self.assertEqual(0, topic.get_subject_identifiers().count())
        locator2 = topic.get_subject_locators()[0]
        self.assertEqual(locator, locator2)

    def test_topic_creation_subject_locator_illegal (self):
        self.assertRaises(ModelConstraintException,
                          self.tm.create_topic_by_subject_locator, None)

    def test_topic_creation_item_identifier (self):
        locator = self.create_locator('http://www.example.org/')
        self.assertEqual(0, self.tm.get_topics().count())
        topic = self.tm.create_topic_by_item_identifier(locator)
        self.assertEqual(1, self.tm.get_topics().count())
        self.assertTrue(topic in self.tm.get_topics())
        self.assertEqual(1, topic.get_item_identifiers().count())
        self.assertEqual(0, topic.get_subject_identifiers().count())
        self.assertEqual(0, topic.get_subject_locators().count())
        locator2 = topic.get_item_identifiers()[0]
        self.assertEqual(locator, locator2)

    def test_topic_creation_item_identifier_illegal (self):
        self.assertRaises(ModelConstraintException,
                          self.tm.create_topic_by_item_identifier, None)

    def test_topic_creation_automagic_item_identifier (self):
        self.assertEqual(0, self.tm.get_topics().count())
        topic = self.tm.create_topic();
        self.assertEqual(1, self.tm.get_topics().count())
        self.assertTrue(topic in self.tm.get_topics())
        self.assertEqual(1, topic.get_item_identifiers().count())
        self.assertEqual(0, topic.get_subject_identifiers().count())
        self.assertEqual(0, topic.get_subject_locators().count())

    def test_topic_by_subject_identifier (self):
        locator = self.create_locator('http://www.example.org/')
        t = self.tm.get_topic_by_subject_identifier(locator)
        self.assertEqual(None, t)
        topic = self.tm.create_topic_by_subject_identifier(locator)
        t = self.tm.get_topic_by_subject_identifier(locator)
        self.assertNotEqual(t, None)
        self.assertEqual(topic, t)
        topic.remove()
        t = self.tm.get_topic_by_subject_identifier(locator)
        self.assertEqual(None, t)

    def test_topic_by_subject_locator (self):
        locator = self.create_locator('http://www.example.org/')
        t = self.tm.get_topic_by_subject_locator(locator)
        self.assertEqual(None, t)
        topic = self.tm.create_topic_by_subject_locator(locator)
        t = self.tm.get_topic_by_subject_locator(locator)
        self.assertNotEqual(t, None)
        self.assertEqual(topic, t)
        topic.remove()
        t = self.tm.get_topic_by_subject_locator(locator)
        self.assertEqual(None, t)

    def test_association_creation_type (self):
        type_topic = self.create_topic()
        self.assertEqual(0, self.tm.get_associations().count())
        association = self.tm.create_association(type_topic)
        self.assertEqual(1, self.tm.get_associations().count())
        self.assertTrue(association in self.tm.get_associations())
        self.assertEqual(0, association.get_roles().count())
        self.assertEqual(type_topic, association.get_type())
        self.assertEqual(0, association.get_scope().count())

    def test_association_creation_type_scope_single (self):
        type_topic = self.create_topic()
        theme = self.create_topic()
        self.assertEqual(0, self.tm.get_associations().count())
        association = self.tm.create_association(type_topic, (theme,))
        self.assertEqual(1, self.tm.get_associations().count())
        self.assertTrue(association in self.tm.get_associations())
        self.assertEqual(0, association.get_roles().count())
        self.assertEqual(type_topic, association.get_type())
        self.assertEqual(1, association.get_scope().count())
        self.assertTrue(theme in association.get_scope())

    def test_association_creation_type_scope_multiple (self):
        type_topic = self.create_topic()
        theme = self.create_topic()
        theme2 = self.create_topic()
        self.assertEqual(0, self.tm.get_associations().count())
        association = self.tm.create_association(type_topic, (theme, theme2))
        self.assertEqual(1, self.tm.get_associations().count())
        self.assertTrue(association in self.tm.get_associations())
        self.assertEqual(0, association.get_roles().count())
        self.assertEqual(type_topic, association.get_type())
        self.assertEqual(2, association.get_scope().count())
        self.assertTrue(theme in association.get_scope())
        self.assertTrue(theme2 in association.get_scope())

    def test_association_creation_illegal_type (self):
        self.assertRaises(ModelConstraintException,
                          self.tm.create_association, None)

    def test_association_creation_illegal_type_scope (self):
        self.assertRaises(ModelConstraintException, self.tm.create_association,
                          None, [self.tm.create_topic()])

    def test_association_creation_illegal_null_collection_scope (self):
        # This test is not applicable in this implementation.
        pass

    def test_association_creation_illegal_null_array_scope (self):
        # This test is not applicable in this implementation.
        pass

    def test_get_from_topic_creation_subject_identifier (self):
        """Verify that create_topic_by_subject_indicator returns
        existing topic where that topic has an item identifier
        matching the subject identifier."""
        locator = self.create_locator('http://www.example.org/')
        self.assertEqual(0, self.tm.get_topics().count())
        topic = self.tm.create_topic_by_item_identifier(locator)
        self.assertEqual(1, self.tm.get_topics().count())
        self.assertTrue(topic in self.tm.get_topics())
        self.assertEqual(0, topic.get_subject_identifiers().count())
        self.assertEqual(1, topic.get_item_identifiers().count())
        self.assertEqual(0, topic.get_subject_locators().count())
        t = self.tm.create_topic_by_subject_identifier(locator)
        self.assertEqual(1, self.tm.get_topics().count())
        self.assertEqual(1, topic.get_subject_identifiers().count())
        self.assertEqual(1, topic.get_item_identifiers().count())
        self.assertEqual(0, topic.get_subject_locators().count())
        self.assertEqual(topic, t)

    def test_get_from_creation_item_identifier (self):
        """Verify that create_topic_by_item_identifier returns
        existing topic where that topic has a subject identifier
        matching the item identifier."""
        locator = self.create_locator('http://www.example.org/')
        self.assertEqual(0, self.tm.get_topics().count())
        topic = self.tm.create_topic_by_subject_identifier(locator)
        self.assertEqual(1, self.tm.get_topics().count())
        self.assertTrue(topic in self.tm.get_topics())
        self.assertEqual(1, topic.get_subject_identifiers().count())
        self.assertEqual(0, topic.get_item_identifiers().count())
        self.assertEqual(0, topic.get_subject_locators().count())
        t = self.tm.create_topic_by_item_identifier(locator)
        self.assertEqual(1, self.tm.get_topics().count())
        self.assertEqual(1, topic.get_subject_identifiers().count())
        self.assertEqual(1, topic.get_item_identifiers().count())
        self.assertEqual(0, topic.get_subject_locators().count())
        self.assertEqual(topic, t)

    def test_get_index (self):
        self.assertRaises(UnsupportedOperationException, self.tm.get_index,
                          BogusIndex)


class BogusIndex:

    pass
