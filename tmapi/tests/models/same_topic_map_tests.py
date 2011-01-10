from django.test import TestCase

from tmapi.exceptions import ModelConstraintException
from tmapi.models import TopicMapSystem


class SameTopicMapTest (TestCase):

    def setUp (self):
        self.tms = TopicMapSystem()
        self.tm = self.tms.create_topic_map('http://www.example.org/tm/')
        self.tm2 = self.tms.create_topic_map('http://www.example.org/tm2/')

    def test_association_creation_illegal_type (self):
        self.assertRaises(ModelConstraintException, self.tm.create_association,
                          self.tm2.create_topic())

    def test_association_creation_illegal_scope (self):
        self.assertRaises(ModelConstraintException, self.tm.create_association,
            self.tm.create_topic(), [self.tm.create_topic(),
            self.tm2.create_topic()])

    def test_name_creation_illegal_type (self):
        topic = self.tm.create_topic()
        self.assertRaises(ModelConstraintException, topic.create_name,
                          'value', self.tm2.create_topic())

    def test_name_creation_illegal_scope (self):
        topic = self.tm.create_topic()
        self.assertRaises(ModelConstraintException, topic.create_name,
                          'value', self.tm.create_topic(),
                          [self.tm2.create_topic()])

    def test_occurrence_creation_illegal_type (self):
        topic = self.tm.create_topic()
        self.assertRaises(ModelConstraintException, topic.create_occurrence,
                          self.tm2.create_topic(), 'value')

    def test_occurrence_creation_illegal_scope (self):
        topic = self.tm.create_topic()
        self.assertRaises(ModelConstraintException, topic.create_occurrence,
                          self.tm.create_topic(), 'value',
                          [self.tm.create_topic(), self.tm2.create_topic()])

    def test_role_creation_illegal_type (self):
        association = self.tm.create_association(self.tm.create_topic())
        self.assertRaises(ModelConstraintException, association.create_role,
                          self.tm2.create_topic(), self.tm.create_topic())

    def test_role_creation_illegal_player (self):
        association = self.tm.create_association(self.tm.create_topic())
        self.assertRaises(ModelConstraintException, association.create_role,
                          self.tm.create_topic(), self.tm2.create_topic())

    def _test_illegal_theme (self, scoped):
        self.assertRaises(ModelConstraintException, scoped.add_theme,
                          self.tm2.create_topic())

    def test_association_illegal_theme (self):
        self._test_illegal_theme(self.tm.create_association(
                self.tm.create_topic()))

    def test_occurrence_illegal_theme (self):
        self._test_illegal_theme(self.tm.create_topic().create_occurrence(
                self.tm.create_topic(), 'value'))

    def test_name_illegal_theme (self):
        self._test_illegal_theme(self.tm.create_topic().create_name('value'))

    def test_variant_illegal_theme (self):
        name = self.tm.create_topic().create_name('value')
        self._test_illegal_theme(name.create_variant(
                'value', [self.tm.create_topic()]))

    def _test_illegal_type (self, typed):
        self.assertRaises(ModelConstraintException, typed.set_type,
                          self.tm2.create_topic())

    def test_association_illegal_type (self):
        self._test_illegal_type(self.tm.create_association(
                self.tm.create_topic()))

    def test_role_illegal_type (self):
        association = self.tm.create_association(self.tm.create_topic())
        self._test_illegal_type(association.create_role(
                self.tm.create_topic(), self.tm.create_topic()))

    def test_occurrence_illegal_type (self):
        self._test_illegal_type(self.tm.create_topic().create_occurrence(
                self.tm.create_topic(), 'value'))

    def test_name_illegal_type (self):
        self._test_illegal_type(self.tm.create_topic().create_name('value'))

    def test_role_illegal_player (self):
        association = self.tm.create_association(self.tm.create_topic())
        role = association.create_role(self.tm.create_topic(),
                                       self.tm.create_topic())
        self.assertRaises(ModelConstraintException, role.set_player,
                          self.tm2.create_topic())

    def _test_illegal_reifier (self, reifiable):
        self.assertRaises(ModelConstraintException, reifiable.set_reifier,
                          self.tm2.create_topic())

    def test_topic_map_illegal_reifier (self):
        self._test_illegal_reifier(self.tm)

    def test_association_illegal_reifier (self):
        self._test_illegal_reifier(self.tm.create_association(
                self.tm.create_topic()))

    def test_role_illegal_reifier (self):
        association = self.tm.create_association(self.tm.create_topic())
        self._test_illegal_reifier(association.create_role(
                self.tm.create_topic(), self.tm.create_topic()))

    def test_occurrence_illegal_reifier (self):
        self._test_illegal_reifier(self.tm.create_topic().create_occurrence(
                self.tm.create_topic(), 'value'))

    def test_name_illegal_reifier (self):
        self._test_illegal_reifier(self.tm.create_topic().create_name('value'))

    def test_variant_illegal_reifier (self):
        name = self.tm.create_topic().create_name('value')
        self._test_illegal_reifier(name.create_variant(
                'value', [self.tm.create_topic()]))

    def test_illegal_topic_type (self):
        self.assertRaises(
            ModelConstraintException, self.tm.create_topic().add_type,
            self.tm2.create_topic())
