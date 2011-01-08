"""Module containing tests for Typed models."""

from django.test import TestCase

from tmapi.exceptions import ModelConstraintException
from tmapi.models import TopicMapSystem


class TypedTest (TestCase):

    def setUp (self):
        self.tms = TopicMapSystem()
        self.tm = self.tms.create_topic_map('http://www.example.org/tm/')
    
    def _test_typed (self, typed):
        old_type = typed.get_type()
        self.assertNotEqual(None, old_type)
        new_type = self.tm.create_topic()
        typed.set_type(new_type)
        self.assertEqual(new_type, typed.get_type(),
                         'Expected another type')
        typed.set_type(old_type)
        self.assertEqual(old_type, typed.get_type(),
                         'Expected the previous type')
        self.assertRaises(ModelConstraintException, typed.set_type, None)

    def test_association (self):
        """Typed tests against an association."""
        association = self.tm.create_association(self.tm.create_topic())
        self._test_typed(association)

    def test_role (self):
        """Typed tests against a role."""
        association = self.tm.create_association(self.tm.create_topic())
        role = association.create_role(self.tm.create_topic(),
                                       self.tm.create_topic())
        self._test_typed(role)

    def test_occurrence (self):
        """Typed tests against an occurrence."""
        topic = self.tm.create_topic()
        occurrence = topic.create_occurrence(self.tm.create_topic(),
                                             'Occurrence')
        self._test_typed(occurrence)

    def test_name (self):
        """Typed tests against a name."""
        name = self.tm.create_topic().create_name('Name')
        self._test_typed(name)
