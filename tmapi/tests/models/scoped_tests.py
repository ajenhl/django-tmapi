from django.test import TestCase

from tmapi.exceptions import ModelConstraintException
from tmapi.models import TopicMapSystem, Variant


class ScopedTest (TestCase):

    def setUp (self):
        self.tms = TopicMapSystem()
        self.tm = self.tms.create_topic_map('http://www.example.org/tm/')
    
    def _test_scoped (self, scoped):
        """Tests addding/removing themes.

        :param scoped: the scoped Topic Maps construct to test

        """
        scope_size = 0
        if isinstance(scoped, Variant):
            scope_size = scoped.get_scope().count()
        self.assertEqual(scope_size, scoped.get_scope().count())
        theme1 = self.tm.create_topic()
        scoped.add_theme(theme1)
        scope_size += 1
        self.assertEqual(scope_size, scoped.get_scope().count())
        self.assertTrue(theme1 in scoped.get_scope())
        theme2 = self.tm.create_topic()
        self.assertFalse(theme2 in scoped.get_scope())
        scoped.add_theme(theme2)
        scope_size += 1
        self.assertEqual(scope_size, scoped.get_scope().count())
        self.assertTrue(theme1 in scoped.get_scope())
        self.assertTrue(theme2 in scoped.get_scope())
        scoped.remove_theme(theme2)
        scope_size -= 1
        self.assertEqual(scope_size, scoped.get_scope().count())
        self.assertTrue(theme1 in scoped.get_scope())
        self.assertFalse(theme2 in scoped.get_scope())
        scoped.remove_theme(theme1)
        scope_size -= 1
        self.assertEqual(scope_size, scoped.get_scope().count())
        self.assertRaises(ModelConstraintException, scoped.add_theme, None)

    def test_association (self):
        """Scoped tests against an association."""
        association = self.tm.create_association(self.tm.create_topic())
        self._test_scoped(association)

    def test_occurrence (self):
        """Scoped tests against an occurrence."""
        occurrence = self.tm.create_topic().create_occurrence(
            self.tm.create_topic(), 'Occurrence')
        self._test_scoped(occurrence)

    def test_name (self):
        """Scoped tests against a name."""
        name = self.tm.create_topic().create_name('Name')
        self._test_scoped(name)

    def test_variant (self):
        """Scoped tests against a variant."""
        name = self.tm.create_topic().create_name('Name')
        variant = name.create_variant('Variant', [self.tm.create_topic()])
        self._test_scoped(variant)
