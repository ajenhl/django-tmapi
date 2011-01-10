"""Tests if the engine respects the constraint if a Topic is removable
or not."""

from django.test import TestCase

from tmapi.exceptions import TopicInUseException
from tmapi.models import TopicMapSystem


class TopicRemovableConstraintTest (TestCase):

    def setUp (self):
        self.tms = TopicMapSystem()
        self.tm = self.tms.create_topic_map('http://www.example.org/tm/')
    
    def _test_typed (self, typed):
        """Tests if hte topic removable constraint is respected if the
        topic is used as a type.

        :param typed: a typed construct
        :type typed: `Typed`

        """
        topic_count = self.tm.get_topics().count()
        old_type = typed.get_type()
        topic = self.tm.create_topic()
        self.assertEqual(topic_count+1, self.tm.get_topics().count())
        typed.set_type(topic)
        self.assertRaises(TopicInUseException, topic.remove)
        self.assertEqual(topic_count+1, self.tm.get_topics().count())
        typed.set_type(old_type)
        topic.remove()
        self.assertEqual(topic_count, self.tm.get_topics().count())

    def _test_scoped (self, scoped):
        """Tests if the topic removable constraint is respected if a
        topic is used as a theme.

        :param scoped: a scoped construct
        :type scoped: `Scoped`

        """
        topic_count = self.tm.get_topics().count()
        topic = self.tm.create_topic()
        self.assertEqual(topic_count+1, self.tm.get_topics().count())
        scoped.add_theme(topic)
        self.assertRaises(TopicInUseException, topic.remove)
        self.assertEqual(topic_count+1, self.tm.get_topics().count())
        scoped.remove_theme(topic)
        topic.remove()
        self.assertEqual(topic_count, self.tm.get_topics().count())
        
    def _test_reifiable (self, reifiable):
        """Tests if the topic removable constraint is respected if a
        topic is used as a reifier.

        :param reifiable: a reifiable that is not reified
        :type reifiable: `Reifiable`

        """
        self.assertEqual(None, reifiable.get_reifier())
        topic_count = self.tm.get_topics().count()
        topic = self.tm.create_topic()
        self.assertEqual(topic_count+1, self.tm.get_topics().count())
        reifiable.set_reifier(topic)
        self.assertRaises(TopicInUseException, topic.remove)
        self.assertEqual(topic_count+1, self.tm.get_topics().count())
        reifiable.set_reifier(None)
        topic.remove()
        self.assertEqual(topic_count, self.tm.get_topics().count())

    def test_used_as_topic_map_reifier (self):
        """Topic map reifier removable constraint test."""
        self._test_reifiable(self.tm)
        
    def test_used_as_association_type (self):
        """Association type removable constraint test."""
        self._test_typed(self.tm.create_association(self.tm.create_topic()))

    def test_used_as_association_theme (self):
        """Association theme removable constraint test."""
        self._test_scoped(self.tm.create_association(self.tm.create_topic()))

    def test_used_as_association_reifier (self):
        """Association reifier removable constraint test."""
        self._test_reifiable(self.tm.create_association(self.tm.create_topic()))

    def test_used_as_role_type (self):
        """Role type removable constraint test."""
        association = self.tm.create_association(self.tm.create_topic())
        self._test_typed(association.create_role(self.tm.create_topic(),
                                                 self.tm.create_topic()))

    def test_used_as_role_reifier (self):
        """Role reifier removable constraint test."""
        association = self.tm.create_association(self.tm.create_topic())
        self._test_reifiable(association.create_role(self.tm.create_topic(),
                                                     self.tm.create_topic()))

    def test_used_as_occurrence_type (self):
        """Occurrence type removable constraint test."""
        self._test_typed(self.tm.create_topic().create_occurrence(
                self.tm.create_topic(), 'value'))

    def test_used_as_occurrence_theme (self):
        """Occurrence theme removable constraint test."""
        self._test_scoped(self.tm.create_topic().create_occurrence(
                self.tm.create_topic(), 'value'))

    def test_used_as_occurrence_reifier (self):
        """Occurrence reifier removable constraint test."""
        self._test_reifiable(self.tm.create_topic().create_occurrence(
                self.tm.create_topic(), 'value'))

    def test_used_as_name_type (self):
        """Name type removable constraint test."""
        self._test_typed(self.tm.create_topic().create_name('value'))

    def test_used_as_name_theme (self):
        """Name theme removable constraint test."""
        self._test_scoped(self.tm.create_topic().create_name('value'))

    def test_used_as_name_reifier (self):
        """Name reifier removable constraint test."""
        self._test_reifiable(self.tm.create_topic().create_name('value'))

    def test_used_as_variant_theme (self):
        """Variant theme removable constraint test."""
        name = self.tm.create_topic().create_name('value')
        self._test_scoped(name.create_variant('value',
                                              [self.tm.create_topic()]))

    def test_used_variant_reifier (self):
        """Variant reifier removable constraint test."""
        name = self.tm.create_topic().create_name('value')
        self._test_reifiable(name.create_variant('value',
                                                 [self.tm.create_topic()]))

    def test_used_as_topic_type (self):
        """Tests if the removable constraint is respected if a topic
        is used as topic type."""
        topic = self.tm.create_topic()
        topic2 = self.tm.create_topic()
        self.assertEqual(2, self.tm.get_topics().count())
        topic2.add_type(topic)
        self.assertRaises(TopicInUseException, topic.remove)
        self.assertEqual(2, self.tm.get_topics().count())
        topic2.remove_type(topic)
        topic.remove()
        self.assertEqual(1, self.tm.get_topics().count())

    def test_used_as_player (self):
        """Tests if the removable constraint is respected if a topic
        is used as player."""
        topic = self.tm.create_topic()
        self.assertEqual(1, self.tm.get_topics().count())
        topic.remove()
        self.assertEqual(0, self.tm.get_topics().count())
        topic = self.tm.create_topic()
        self.assertEqual(1, self.tm.get_topics().count())
        association = self.tm.create_association(self.tm.create_topic())
        self.assertEqual(2, self.tm.get_topics().count())
        role = association.create_role(self.tm.create_topic(), topic)
        self.assertEqual(3, self.tm.get_topics().count())
        self.assertRaises(TopicInUseException, topic.remove)
        role.set_player(self.tm.create_topic())
        self.assertEqual(4, self.tm.get_topics().count())
        topic.remove()
        self.assertEqual(3, self.tm.get_topics().count())
