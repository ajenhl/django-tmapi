"""Tests if the TMDM item identifier constraint is respect."""

from tmapi.exceptions import IdentityConstraintException
from tmapi.models import TopicMap

from tmapi_test_case import TMAPITestCase


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
        except IdentityConstraintException, ex:
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
