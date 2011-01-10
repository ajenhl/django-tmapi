"""Module containing tests for Reifiable models."""

from django.test import TestCase

from tmapi.exceptions import ModelConstraintException
from tmapi.models import TopicMapSystem


class ReifiableTest (TestCase):

    def setUp (self):
        self.tms = TopicMapSystem()
        self.tm = self.tms.create_topic_map('http://www.example.org/tm/')
    
    def _test_reification (self, reifiable):
        self.assertEqual(None, reifiable.get_reifier(),
                         'Unexpected reifier property')
        reifier = self.tm.create_topic()
        self.assertEqual(None, reifier.get_reified())
        reifiable.set_reifier(reifier)
        self.assertEqual(reifier, reifiable.get_reifier(),
                         'Unexpected reifier property')
        self.assertEqual(reifiable, reifier.get_reified(),
                         'Unexpected reified property')
        reifiable.set_reifier(None)
        self.assertEqual(None, reifiable.get_reifier(),
                         'Reifier should be None')
        self.assertEqual(None, reifier.get_reified(), 'Reified should be None')
        reifiable.set_reifier(reifier)
        self.assertEqual(reifier, reifiable.get_reifier(),
                         'Unexpected reifier property')
        self.assertEqual(reifiable, reifier.get_reified(),
                         'Unexpected reified property')
        try:
            reifiable.set_reifier(reifier)
        except ModelConstraintException:
            self.fail('Unexpected exception while setting the reifier to the same value')

    def _test_reification_collision (self, reifiable):
        """Tests if a reifier collision (the reifier is already
        assigned to another construct) is detected."""
        self.assertEqual(None, reifiable.get_reifier(),
                         'Unexpected reifier property')
        reifier = self.tm.create_topic()
        self.assertEqual(None, reifier.get_reified())
        other_reifiable = self.tm.create_topic().create_occurrence(
            self.tm.create_topic(), 'Occurrence')
        other_reifiable.set_reifier(reifier)
        self.assertEqual(reifier, other_reifiable.get_reifier(),
                         'Expected a reifier property')
        self.assertEqual(other_reifiable, reifier.get_reified(),
                         'Unexpected reified property')
        self.assertRaises(ModelConstraintException, reifiable.set_reifier,
                          reifier)
        other_reifiable.set_reifier(None)
        self.assertEqual(None, other_reifiable.get_reifier(),
                         'Reifier property should be None')
        self.assertEqual(None, reifier.get_reified(),
                         'Reified property should be None')
        reifiable.set_reifier(reifier)
        self.assertEqual(reifier, reifiable.get_reifier(),
                         'Reifier property should have been changed')
        self.assertEqual(reifiable, reifier.get_reified(),
                         'Reified property should have been changed')

    def test_topic_map (self):
        self._test_reification(self.tm)

    def test_topic_map_reifier_collision (self):
        self._test_reification_collision(self.tm)

    def test_association (self):
        association = self.tm.create_association(self.tm.create_topic())
        self._test_reification(association)

    def test_association_reifier_collision (self):
        association = self.tm.create_association(self.tm.create_topic())
        self._test_reification_collision(association)

    def test_role (self):
        association = self.tm.create_association(self.tm.create_topic())
        role = association.create_role(self.tm.create_topic(),
                                       self.tm.create_topic())
        self._test_reification(role)

    def test_role_reifier_collision (self):
        association = self.tm.create_association(self.tm.create_topic())
        role = association.create_role(self.tm.create_topic(),
                                       self.tm.create_topic())
        self._test_reification_collision(role)

    def test_occurrence (self):
        occurrence = self.tm.create_topic().create_occurrence(
            self.tm.create_topic(), 'Occurrence')
        self._test_reification(occurrence)

    def test_occurrence_reification_collision (self):
        occurrence = self.tm.create_topic().create_occurrence(
            self.tm.create_topic(), 'Occurrence')
        self._test_reification_collision(occurrence)

    def test_name (self):
        name = self.tm.create_topic().create_name('Name')
        self._test_reification(name)

    def test_name_reification_collision (self):
        name = self.tm.create_topic().create_name('Name')
        self._test_reification_collision(name)

    def test_variant (self):
        name = self.tm.create_topic().create_name('Name')
        variant = name.create_variant('Variant', [self.tm.create_topic()])
        self._test_reification(variant)

    def test_variant_reification_collision (self):
        name = self.tm.create_topic().create_name('Name')
        variant = name.create_variant('Variant', [self.tm.create_topic()])
        self._test_reification_collision(variant)
