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

"""Module containing tests against the `Occurrence` interface.

Most if not all of these tests are ported from the public domain tests
that come with the TMAPI 2.0 distribution (http://www.tmapi.org/2.0/).

"""

from .datatype_aware_abstract_tests import DatatypeAwareAbstractTestCase


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
