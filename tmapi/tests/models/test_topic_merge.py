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

"""Module containing tests of topic merging.

Most if not all of these tests are ported from the public domain tests
that come with the TMAPI 2.0 distribution (http://www.tmapi.org/2.0/).

"""

from tmapi.exceptions import ModelConstraintException

from .tmapi_test_case import TMAPITestCase


class TopicMergeTest (TMAPITestCase):

    def test_topic_merge_noop (self):
        """Tests if a.merge_in(a) is accepted without raising an
        exception. Must have no side effects."""
        sid = self.create_locator('http://www.tmapi.org/test/me')
        topic = self.tm.create_topic_by_subject_identifier(sid)
        self.assertEqual(1, self.tm.get_topics().count())
        self.assertEqual(topic, self.tm.get_topic_by_subject_identifier(sid))
        topic.merge_in(topic)
        self.assertEqual(1, self.tm.get_topics().count())
        self.assertEqual(topic, self.tm.get_topic_by_subject_identifier(sid))

    def test_types_merged (self):
        """Tests if the types are also merged."""
        t1 = self.create_topic()
        t2 = self.create_topic()
        t3 = self.create_topic()
        t2.add_type(t3)
        self.assertTrue(t3 in t2.get_types())
        self.assertEqual(0, t1.get_types().count())
        t1.merge_in(t2)
        self.assertTrue(t3 in t1.get_types(), 'Topic must have a type now')

    def test_reified_clash (self):
        """If topics reify different Topic Maps constructs, they
        cannot be merged."""
        topic1 = self.create_topic()
        topic2 = self.create_topic()
        association1 = self.create_association()
        association2 = self.create_association()
        association1.set_reifier(topic1)
        association2.set_reifier(topic2)
        self.assertEqual(topic1, association1.get_reifier())
        self.assertEqual(topic2, association2.get_reifier())
        self.assertRaises(ModelConstraintException, topic1.merge_in, topic2)

    def test_role_playing (self):
        """Tests if a topic takes over all roles played of the other
        topic."""
        topic1 = self.create_topic()
        topic2 = self.create_topic()
        association = self.create_association()
        role = association.create_role(self.create_topic(), topic2)
        self.assertEqual(4, self.tm.get_topics().count())
        self.assertFalse(role in topic1.get_roles_played())
        self.assertTrue(role in topic2.get_roles_played())
        topic1.merge_in(topic2)
        self.assertEqual(3, self.tm.get_topics().count())
        self.assertTrue(role in topic1.get_roles_played())

    def test_identity_subject_identifier (self):
        """Tests if the subject identifiers are taken over."""
        sid1 = self.tm.create_locator('http://psi.example.org/sid-1')
        sid2 = self.tm.create_locator('http://psi.example.org/sid-2')
        topic1 = self.tm.create_topic_by_subject_identifier(sid1)
        topic2 = self.tm.create_topic_by_subject_identifier(sid2)
        self.assertTrue(sid1 in topic1.get_subject_identifiers())
        self.assertFalse(sid2 in topic1.get_subject_identifiers())
        self.assertFalse(sid1 in topic2.get_subject_identifiers())
        self.assertTrue(sid2 in topic2.get_subject_identifiers())
        topic1.merge_in(topic2)
        self.assertEqual(2, topic1.get_subject_identifiers().count())
        self.assertTrue(sid1 in topic1.get_subject_identifiers())
        self.assertTrue(sid2 in topic1.get_subject_identifiers())

    def test_identity_subject_locator (self):
        """Tests if the subject locator are taken over."""
        slo1 = self.tm.create_locator('http://tinytim.sf.net')
        slo2 = self.tm.create_locator('http://tinytim.sourceforge.net')
        topic1 = self.tm.create_topic_by_subject_locator(slo1)
        topic2 = self.tm.create_topic_by_subject_locator(slo2)
        self.assertTrue(slo1 in topic1.get_subject_locators())
        self.assertFalse(slo2 in topic1.get_subject_locators())
        self.assertFalse(slo1 in topic2.get_subject_locators())
        self.assertTrue(slo2 in topic2.get_subject_locators())
        topic1.merge_in(topic2)
        self.assertEqual(2, topic1.get_subject_locators().count())
        self.assertTrue(slo1 in topic1.get_subject_locators())
        self.assertTrue(slo2 in topic1.get_subject_locators())

    def test_identity_item_identifier (self):
        """Tests if the item identifiers are taken over."""
        iid1 = self.tm.create_locator('http://tinytim.sf.net/test#1')
        iid2 = self.tm.create_locator('http://tinytim.sf.net/test#2')
        topic1 = self.tm.create_topic_by_item_identifier(iid1)
        topic2 = self.tm.create_topic_by_item_identifier(iid2)
        self.assertTrue(iid1 in topic1.get_item_identifiers())
        self.assertFalse(iid2 in topic1.get_item_identifiers())
        self.assertFalse(iid1 in topic2.get_item_identifiers())
        self.assertTrue(iid2 in topic2.get_item_identifiers())
        topic1.merge_in(topic2)
        self.assertEqual(2, topic1.get_item_identifiers().count())
        self.assertTrue(iid1 in topic1.get_item_identifiers())
        self.assertTrue(iid2 in topic1.get_item_identifiers())

    def test_duplicate_detection_reifier (self):
        """Tests if merging detects duplicates and that the reifier is
        kept."""
        topic1 = self.tm.create_topic()
        topic2 = self.tm.create_topic()
        reifier = self.tm.create_topic()
        name_type = self.tm.create_topic()
        name1 = topic1.create_name('TMAPI', name_type)
        name2 = topic2.create_name('TMAPI', name_type)
        self.assertEqual(4, self.tm.get_topics().count())
        name1.set_reifier(reifier)
        self.assertEqual(reifier, name1.get_reifier())
        self.assertEqual(1, topic1.get_names().count())
        self.assertTrue(name1 in topic1.get_names())
        self.assertEqual(1, topic2.get_names().count())
        self.assertTrue(name2 in topic2.get_names())
        topic1.merge_in(topic2)
        self.assertEqual(3, self.tm.get_topics().count())
        self.assertEqual(1, topic1.get_names().count())
        name = topic1.get_names()[0]
        self.assertEqual(reifier, name.get_reifier())

    def test_duplicate_name_detection_reifier_merge (self):
        """Tests if merging detects duplicate names and merges the reifiers
        of the duplicates."""
        topic1 = self.tm.create_topic()
        topic2 = self.tm.create_topic()
        reifier1 = self.tm.create_topic()
        reifier2 = self.tm.create_topic()
        name_type = self.tm.create_topic()
        name1 = topic1.create_name('TMAPI', name_type)
        name2 = topic2.create_name('TMAPI', name_type)
        self.assertEqual(5, self.tm.get_topics().count())
        name1.set_reifier(reifier1)
        name2.set_reifier(reifier2)
        self.assertEqual(reifier1, name1.get_reifier())
        self.assertEqual(reifier2, name2.get_reifier())
        self.assertEqual(1, topic1.get_names().count())
        self.assertTrue(name1 in topic1.get_names())
        self.assertEqual(1, topic2.get_names().count())
        self.assertTrue(name2 in topic2.get_names())
        topic1.merge_in(topic2)
        self.assertEqual(3, self.tm.get_topics().count())
        self.assertEqual(1, topic1.get_names().count())
        name = topic1.get_names()[0]
        reifier = None
        for topic in self.tm.get_topics():
            if topic != topic1 and topic != name_type:
                reifier = topic
                break
        self.assertEqual(reifier, name.get_reifier())

    def test_duplicate_suppression_association (self):
        """Tests if merging detects duplicate associations."""
        topic1 = self.create_topic()
        topic2 = self.create_topic()
        role_type = self.create_topic()
        type = self.create_topic()
        association1 = self.tm.create_association(type)
        association2 = self.tm.create_association(type)
        role1 = association1.create_role(role_type, topic1)
        role2 = association2.create_role(role_type, topic2)
        self.assertEqual(4, self.tm.get_topics().count())
        self.assertEqual(2, self.tm.get_associations().count())
        self.assertTrue(role1 in topic1.get_roles_played())
        self.assertTrue(role2 in topic2.get_roles_played())
        self.assertEqual(1, topic1.get_roles_played().count())
        self.assertEqual(1, topic2.get_roles_played().count())
        topic1.merge_in(topic2)
        self.assertEqual(3, self.tm.get_topics().count())
        self.assertEqual(1, self.tm.get_associations().count())
        role = topic1.get_roles_played()[0]
        self.assertEqual(role_type, role.get_type())

    def test_duplicate_suppression_name (self):
        """Tests if merging detects duplicate names."""
        topic1 = self.tm.create_topic()
        topic2 = self.tm.create_topic()
        name1 = topic1.create_name('TMAPI')
        name2 = topic2.create_name('TMAPI')
        name3 = topic2.create_name('tiny Topic Maps engine')
        self.assertEqual(1, topic1.get_names().count())
        self.assertTrue(name1 in topic1.get_names())
        self.assertEqual(2, topic2.get_names().count())
        self.assertTrue(name2 in topic2.get_names())
        self.assertTrue(name3 in topic2.get_names())
        topic1.merge_in(topic2)
        self.assertEqual(2, topic1.get_names().count())

    def test_duplicate_suppression_name_2 (self):
        """Tests if merging detects duplicate names and moves the
        variants."""
        topic1 = self.tm.create_topic()
        topic2 = self.tm.create_topic()
        name1 = topic1.create_name('TMAPI')
        name2 = topic2.create_name('TMAPI')
        variant = name2.create_variant('tiny', [self.create_topic()])
        self.assertEqual(1, topic1.get_names().count())
        self.assertTrue(name1 in topic1.get_names())
        self.assertEqual(0, name1.get_variants().count())
        self.assertEqual(1, topic2.get_names().count())
        self.assertTrue(name2 in topic2.get_names())
        self.assertEqual(1, name2.get_variants().count())
        self.assertTrue(variant in name2.get_variants())
        topic1.merge_in(topic2)
        self.assertEqual(1, topic1.get_names().count())
        tmp_name = topic1.get_names()[0]
        self.assertEqual(1, tmp_name.get_variants().count())
        tmp_var = tmp_name.get_variants()[0]
        self.assertEqual('tiny', tmp_var.get_value())

    def test_duplicate_suppression_name_move_item_identifiers (self):
        """Tests if merging detects duplicate names and sets the item
        identifier to the union of both names."""
        topic1 = self.tm.create_topic()
        topic2 = self.tm.create_topic()
        iid1 = self.tm.create_locator('http://example.org/iid-1')
        iid2 = self.tm.create_locator('http://example.org/iid-2')
        name1 = topic1.create_name('TMAPI')
        name2 = topic2.create_name('TMAPI')
        name1.add_item_identifier(iid1)
        name2.add_item_identifier(iid2)
        self.assertTrue(iid1 in name1.get_item_identifiers())
        self.assertTrue(iid2 in name2.get_item_identifiers())
        self.assertEqual(1, topic1.get_names().count())
        self.assertTrue(name1 in topic1.get_names())
        self.assertEqual(1, topic2.get_names().count())
        self.assertTrue(name2 in topic2.get_names())
        topic1.merge_in(topic2)
        self.assertEqual(1, topic1.get_names().count())
        name = topic1.get_names()[0]
        self.assertEqual(2, name.get_item_identifiers().count())
        self.assertTrue(iid1 in name.get_item_identifiers())
        self.assertTrue(iid2 in name.get_item_identifiers())
        self.assertEqual('TMAPI', name.get_value())

    def test_duplicate_suppression_occurrences (self):
        """Tests if merging detects duplicate occurrences."""
        topic1 = self.tm.create_topic()
        topic2 = self.tm.create_topic()
        occ_type = self.create_topic()
        occ1 = topic1.create_occurrence(occ_type, 'TMAPI')
        occ2 = topic2.create_occurrence(occ_type, 'TMAPI')
        occ3 = topic2.create_occurrence(occ_type, 'tiny Topic Maps engine')
        self.assertEqual(1, topic1.get_occurrences().count())
        self.assertTrue(occ1 in topic1.get_occurrences())
        self.assertEqual(2, topic2.get_occurrences().count())
        self.assertTrue(occ2 in topic2.get_occurrences())
        self.assertTrue(occ3 in topic2.get_occurrences())
        topic1.merge_in(topic2)
        self.assertEqual(2, topic1.get_occurrences().count())

    def test_duplicate_suppression_occurrence_move_item_identifiers (self):
        """Tests if merging detects duplicate occurrences and sets the
        item identifier to the union of both occurrences."""
        topic1 = self.tm.create_topic()
        topic2 = self.tm.create_topic()
        iid1 = self.tm.create_locator('http://example.org/iid-1')
        iid2 = self.tm.create_locator('http://example.org/iid-2')
        occ_type = self.create_topic()
        occ1 = topic1.create_occurrence(occ_type, 'TMAPI')
        occ1.add_item_identifier(iid1)
        self.assertTrue(iid1 in occ1.get_item_identifiers())
        occ2 = topic2.create_occurrence(occ_type, 'TMAPI')
        occ2.add_item_identifier(iid2)
        self.assertTrue(iid2 in occ2.get_item_identifiers())
        self.assertEqual(1, topic1.get_occurrences().count())
        self.assertTrue(occ1 in topic1.get_occurrences())
        self.assertEqual(1, topic2.get_occurrences().count())
        self.assertTrue(occ2 in topic2.get_occurrences())
        topic1.merge_in(topic2)
        self.assertEqual(1, topic1.get_occurrences().count())
        occ = topic1.get_occurrences()[0]
        self.assertEqual(2, occ.get_item_identifiers().count())
        self.assertTrue(iid1 in occ.get_item_identifiers())
        self.assertTrue(iid2 in occ.get_item_identifiers())
        self.assertEqual('TMAPI', occ.get_value())

    def test_duplicate_occurrence_detection_reifier_merge (self):
        """Tests if merging detects duplicate occurrences and merges
        the reifiers of the duplicates."""
        topic1 = self.tm.create_topic()
        topic2 = self.tm.create_topic()
        reifier1 = self.tm.create_topic()
        reifier2 = self.tm.create_topic()
        occ_type = self.tm.create_topic()
        occ1 = topic1.create_occurrence(occ_type, 'TMAPI')
        occ2 = topic2.create_occurrence(occ_type, 'TMAPI')
        self.assertEqual(5, self.tm.get_topics().count())
        occ1.set_reifier(reifier1)
        occ2.set_reifier(reifier2)
        self.assertEqual(reifier1, occ1.get_reifier())
        self.assertEqual(reifier2, occ2.get_reifier())
        self.assertEqual(1, topic1.get_occurrences().count())
        self.assertTrue(occ1 in topic1.get_occurrences())
        self.assertEqual(1, topic2.get_occurrences().count())
        self.assertTrue(occ2 in topic2.get_occurrences())
        topic1.merge_in(topic2)
        self.assertEqual(3, self.tm.get_topics().count())
        self.assertEqual(1, topic1.get_occurrences().count())
        occ = topic1.get_occurrences()[0]
        reifier = None
        for topic in self.tm.get_topics():
            if topic != topic1 and topic != occ_type:
                reifier = topic
                break
        self.assertEqual(reifier, occ.get_reifier())
