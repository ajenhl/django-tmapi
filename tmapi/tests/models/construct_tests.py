from django.test import TestCase

from tmapi.exceptions import ModelConstraintException
from tmapi.models import TopicMap, TopicMapSystem


class ConstructTest (TestCase):

    def setUp (self):
        self.tms = TopicMapSystem()
        self.tm = self.tms.create_topic_map('http://www.example.org/tm/')
    
    def _test_construct (self, construct):
        tm = self.tm
        self.assertEqual(0, construct.get_item_identifiers().count())
        iid = tm.create_locator('http://www.tmapi.org/test#test')
        construct.add_item_identifier(iid)
        self.assertEqual(1, construct.get_item_identifiers().count(),
                         'Expected an item identifier')
        self.assertTrue(iid in construct.get_item_identifiers(),
                        'Unexpected item identifier in item identifier property')
        self.assertEqual(construct, tm.get_construct_by_item_identifier(iid),
                         'Unexpected construct retrieved')
        construct.remove_item_identifier(iid)
        self.assertEqual(0, construct.get_item_identifiers().count(),
                         'Item identifier was not removed')
        self.assertFalse(iid in construct.get_item_identifiers())
        self.assertEqual(None, tm.get_construct_by_item_identifier(iid),
                         'Got a construct even if the item identifier is ' +
                         'unassigned')
        self.assertRaises(ModelConstraintException,
                          construct.add_item_identifier, None)
        if isinstance(construct, TopicMap):
            self.assertEqual(None, construct.get_parent())
        else:
            self.assertFalse(None, construct.get_parent())
        self.assertEqual(tm, construct.get_topic_map())
        id = construct.get_id()
        self.assertEqual(construct, tm.get_construct_by_id(id),
                         'Unexpected result from get_construct_by_id')

    def test_topic_map (self):
        """Construct tests against a topic map."""
        self._test_construct(self.tm)

    def test_topic (self):
        """Construct tests against a topic."""
        topic = self.tm.create_topic_by_subject_locator(
            self.tm.create_locator('http://www.tmapi.org/'))
        self._test_construct(topic)

    def test_association (self):
        """Construct tests against an association."""
        association = self.tm.create_association(self.tm.create_topic())
        self._test_construct(association)

    def test_role (self):
        """Construct tests against a role."""
        association = self.tm.create_association(self.tm.create_topic())
        role = association.create_role(self.tm.create_topic(),
                                       self.tm.create_topic())
        self._test_construct(role)

    def test_occurrence (self):
        """Construct tests against an occurrence."""
        occurrence = self.tm.create_topic().create_occurrence(
            self.tm.create_topic(), 'Occurrence')
        self._test_construct(occurrence)

    def test_name (self):
        """Construct tests against a name."""
        name = self.tm.create_topic().create_name('Name')
        self._test_construct(name)

    def test_variant (self):
        """Construct tests against a variant."""
        name = self.tm.create_topic().create_name('Name')
        variant = name.create_variant('Variant', [self.tm.create_topic()])
        self._test_construct(variant)
