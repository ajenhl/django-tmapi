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

"""Module containing tests against the `Construct` interface.

Most if not all of these tests are ported from the public domain tests
that come with the TMAPI 2.0 distribution (http://www.tmapi.org/2.0/).

"""

from tmapi.exceptions import ModelConstraintException
from tmapi.models import TopicMap

from .tmapi_test_case import TMAPITestCase


class ConstructTest (TMAPITestCase):

    def _test_construct (self, construct):
        """Tests adding/removing item identifiers, retrieval by item
        identifier, and retrieval by the system specific id.

        :param construct: the Topic Maps construct to test
        :type construct: `Construct`

        """
        tm = self.tm
        self.assertEqual(0, construct.get_item_identifiers().count(),
                         'Unexpected item identifiers')
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
