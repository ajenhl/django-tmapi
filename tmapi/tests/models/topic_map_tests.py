"""Module containing tests for the TopicMap model."""

from django.test import TestCase

from tmapi.exceptions import ModelConstraintException
from tmapi.models import TopicMapSystem


class TopicMapTest (TestCase):

    def setUp (self):
        self.tms = TopicMapSystem()
        self.tm = self.tms.create_topic_map('http://www.example.org/tm/')
    
    def test_topic_creation_subject_identifier (self):
        locator = self.tms.create_locator('http://www.example.org/')
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
        locator = self.tms.create_locator('http://www.example.org/')
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
        locator = self.tms.create_locator('http://www.example.org/')
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
        locator = self.tms.create_locator('http://www.example.org/')
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
        locator = self.tms.create_locator('http://www.example.org/')
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
        type_topic = self.tm.create_topic()
        self.assertEqual(0, self.tm.get_associations().count())
        association = self.tm.create_association(type_topic)
        self.assertEqual(1, self.tm.get_associations().count())
        self.assertTrue(association in self.tm.get_associations())
        self.assertEqual(0, association.get_roles().count())
        self.assertEqual(type_topic, association.get_type())
        self.assertEqual(0, association.get_scope().count())

    def test_association_creation_type_scope_single (self):
        type_topic = self.tm.create_topic()
        theme = self.tm.create_topic()
        self.assertEqual(0, self.tm.get_associations().count())
        association = self.tm.create_association(type_topic, (theme,))
        self.assertEqual(1, self.tm.get_associations().count())
        self.assertTrue(association in self.tm.get_associations())
        self.assertEqual(0, association.get_roles().count())
        self.assertEqual(type_topic, association.get_type())
        self.assertEqual(1, association.get_scope().count())
        self.assertTrue(theme in association.get_scope())

    def test_association_creation_type_scope_multiple (self):
        type_topic = self.tm.create_topic()
        theme = self.tm.create_topic()
        theme2 = self.tm.create_topic()
        self.assertEqual(0, self.tm.get_associations().count())
        association = self.tm.create_association(type_topic, (theme, theme2))
        self.assertEqual(1, self.tm.get_associations().count())
        self.assertTrue(association in self.tm.get_associations())
        self.assertEqual(0, association.get_roles().count())
        self.assertEqual(type_topic, association.get_type())
        self.assertEqual(2, association.get_scope().count())
        self.assertTrue(theme in association.get_scope())
        self.assertTrue(theme2 in association.get_scope())

    def test_association_creation_illegal_type_scope (self):
        self.assertRaises(ModelConstraintException,
                          self.tm.create_association, None)

    def test_get_from_topic_creation_subject_identifier (self):
        """Verify that create_topic_by_subject_indicator returns
        existing topic where that topic has an item identifier
        matching the subject identifier."""
        locator = self.tms.create_locator('http://www.example.org/')
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
        locator = self.tms.create_locator('http://www.example.org/')
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
