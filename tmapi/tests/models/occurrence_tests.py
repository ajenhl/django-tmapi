"""Module containing tests against the `Occurrence` interface."""

from datatype_aware_abstract_tests import DatatypeAwareAbstractTestCase


class OccurrenceTest (DatatypeAwareAbstractTestCase):

    def get_datatype_aware (self):
        return self.tm.create_topic().create_occurrence(
            self.tm.create_topic(), 'Occurrence')

    def test_parent (self):
        parent = self.create_topic()
        self.assertEqual(0, parent.get_occurrences().count(),
                         'Expected new topic to be created with no occurrences')
        occurrence = parent.create_occurrence(self.tm.create_topic(),
                                              'Occurrence')
        self.assertEqual(parent, occurrence.get_parent(),
                         'Unexpected occurrence parent after creation')
        self.assertEqual(1, parent.get_occurrences().count(),
                         'Expected occurrence list size to increment for topic')
        self.assertTrue(occurrence in parent.get_occurrences(),
                        'Occurrence is not part of get_occurrences()')
        occurrence.remove()
        self.assertEqual(0, parent.get_occurrences().count(),
                         'Expected occurrence list size to decrement for topic')
