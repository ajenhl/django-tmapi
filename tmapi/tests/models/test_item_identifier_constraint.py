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

"""Tests if the TMDM item identifier constraint is respected.

Most if not all of these tests are ported from the public domain tests
that come with the TMAPI 2.0 distribution (http://www.tmapi.org/2.0/).

"""

from tmapi.exceptions import IdentityConstraintException
from tmapi.models import TopicMap

from .tmapi_test_case import TMAPITestCase


class ItemIdentifierConstraintTest (TMAPITestCase):

    def _test_constraint (self, tmo):
        self.assertEqual(0, tmo.get_item_identifiers().count())
        iid = self.create_locator('http://sf.net/projects/tinytim')
        iid2 = self.create_locator('http://sf.net/projects/tinytim2')
        association = self.create_association()
        association.add_item_identifier(iid)
        self.assertFalse(iid in tmo.get_item_identifiers())
        try:
            tmo.add_item_identifier(iid)
            self.fail('Topic Maps constructs with the same item identifier are not allowed')
        except IdentityConstraintException as ex:
            self.assertEqual(tmo, ex.get_reporter())
            self.assertEqual(association, ex.get_existing())
            self.assertEqual(iid, ex.get_locator())
        tmo.add_item_identifier(iid2)
        self.assertTrue(iid2 in tmo.get_item_identifiers())
        tmo.remove_item_identifier(iid2)
        association.remove_item_identifier(iid)
        self.assertFalse(iid in association.get_item_identifiers())
        tmo.add_item_identifier(iid)
        self.assertTrue(iid in tmo.get_item_identifiers())
        if not isinstance(tmo, TopicMap):
            tmo.remove()
            association.add_item_identifier(iid)
            self.assertTrue(iid in association.get_item_identifiers())

    def test_topic_map (self):
        """Tests item identifier constraint against a topic map."""
        self._test_constraint(self.tm)

    def test_topic (self):
        """Tests item identifier constraint against a topic map."""
        locator = self.create_locator('http://psi.example.org/test-this-topic-please')
        topic = self.tm.create_topic_by_subject_identifier(locator)
        self._test_constraint(topic)

    def test_association (self):
        """Tests item identifier constraint against an association."""
        self._test_constraint(self.create_association())

    def test_role (self):
        """Tests item identifier constraint against a role."""
        self._test_constraint(self.create_role())

    def test_occurrence (self):
        """Tests item identifier constraint against an occurrence."""
        self._test_constraint(self.create_occurrence())

    def test_name (self):
        """Tests item identifier constraint against a name."""
        self._test_constraint(self.create_name())

    def test_variant (self):
        """Tests item identifier constraint against a variant."""
        self._test_constraint(self.create_variant())
