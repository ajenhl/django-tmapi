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

"""Tests merging of topic maps.

Most if not all of these tests are ported from the public domain tests
that come with the TMAPI 2.0 distribution (http://www.tmapi.org/2.0/).

"""

from .tmapi_test_case import TMAPITestCase


class TopicMapMergeTest (TMAPITestCase):

    TM2_BASE = 'http://www.sf.net/projects/tinytim/tm-2'

    def setUp (self):
        super(TopicMapMergeTest, self).setUp()
        self.tm2 = self.create_topic_map(self.TM2_BASE)

    def test_topic_merge_noop (self):
        """Tests if a.merge_in(a) is accepted with no exception.

        Must have no side effects.

        """
        locator = self.create_locator('http://www.tmapi.org/test/tm-merge-noop')
        tm = self.tms.create_topic_map(locator)
        self.assertEqual(tm, self.tms.get_topic_map(locator))
        tm.merge_in(self.tms.get_topic_map(locator))
        self.assertEqual(tm, self.tms.get_topic_map(locator))

    def test_merge_by_item_identifier (self):
        """Tests merging of topcs by equal item identifiers."""
        reference = 'http://sf.net/projects/tinytim/loc'
        iidA = self.tm.create_locator(reference)
        topicA = self.tm.create_topic_by_item_identifier(iidA)
        iidB = self.tm2.create_locator(reference)
        topicB = self.tm2.create_topic_by_item_identifier(iidB)
        self.assertEqual(1, self.tm.get_topics().count())
        self.assertEqual(1, self.tm2.get_topics().count())

        self.tm.merge_in(self.tm2)
        self.assertEqual(1, self.tm.get_topics().count())
        self.assertEqual(topicA, self.tm.get_construct_by_item_identifier(iidA))
        self.assertEqual(1, topicA.get_item_identifiers().count())
        self.assertEqual(iidA, topicA.get_item_identifiers()[0])
        self.assertEqual(0, topicA.get_subject_identifiers().count())
        self.assertEqual(0, topicA.get_subject_locators().count())

        # mergin_in must not have any side effects on tm2.
        self.assertEqual(1, self.tm2.get_topics().count())
        self.assertEqual(topicB,
                         self.tm2.get_construct_by_item_identifier(iidB))
        self.assertEqual(1, topicB.get_item_identifiers().count())
        self.assertEqual(iidB, topicB.get_item_identifiers()[0])
        self.assertEqual(0, topicB.get_subject_identifiers().count())
        self.assertEqual(0, topicB.get_subject_locators().count())

    def test_merge_by_subject_identifier (self):
        """Tests merging of topics by equal subject identifiers."""
        reference = 'http://sf.net/projects/tinytim/loc'
        sidA = self.tm.create_locator(reference)
        topicA = self.tm.create_topic_by_subject_identifier(sidA)
        sidB = self.tm2.create_locator(reference)
        topicB = self.tm2.create_topic_by_subject_identifier(sidB)
        self.assertEqual(1, self.tm.get_topics().count())
        self.assertEqual(1, self.tm2.get_topics().count())

        self.tm.merge_in(self.tm2)
        self.assertEqual(1, self.tm.get_topics().count())
        self.assertEqual(topicA, self.tm.get_topic_by_subject_identifier(sidA))
        self.assertEqual(1, topicA.get_subject_identifiers().count())
        self.assertEqual(sidA, topicA.get_subject_identifiers()[0])
        self.assertEqual(0, topicA.get_item_identifiers().count())
        self.assertEqual(0, topicA.get_subject_locators().count())

        # merge_in must not have any side effects on tm2.
        self.assertEqual(1, self.tm2.get_topics().count())
        self.assertEqual(topicB, self.tm2.get_topic_by_subject_identifier(sidB))
        self.assertEqual(1, topicB.get_subject_identifiers().count())
        self.assertEqual(sidB, topicB.get_subject_identifiers()[0])
        self.assertEqual(0, topicB.get_item_identifiers().count())
        self.assertEqual(0, topicB.get_subject_locators().count())

    def test_merge_by_subject_locator (self):
        """Tests merging of topics by equal subject locators."""
        reference = 'http://sf.net/projects/tinytim/loc'
        sloA = self.tm.create_locator(reference)
        topicA = self.tm.create_topic_by_subject_locator(sloA)
        sloB = self.tm2.create_locator(reference)
        topicB = self.tm2.create_topic_by_subject_locator(sloB)
        self.assertEqual(1, self.tm.get_topics().count())
        self.assertEqual(1, self.tm2.get_topics().count())

        self.tm.merge_in(self.tm2)
        self.assertEqual(1, self.tm.get_topics().count())
        self.assertEqual(topicA, self.tm.get_topic_by_subject_locator(sloA))
        self.assertEqual(1, topicA.get_subject_locators().count())
        self.assertEqual(sloA, topicA.get_subject_locators()[0])
        self.assertEqual(0, topicA.get_item_identifiers().count())
        self.assertEqual(0, topicA.get_subject_identifiers().count())

        # merge_in must not have any side effects on tm2.
        self.assertEqual(1, self.tm2.get_topics().count())
        self.assertEqual(topicB, self.tm2.get_topic_by_subject_locator(sloB))
        self.assertEqual(1, topicB.get_subject_locators().count())
        self.assertEqual(sloB, topicB.get_subject_locators()[0])
        self.assertEqual(0, topicB.get_item_identifiers().count())
        self.assertEqual(0, topicB.get_subject_identifiers().count())

    def test_merge_item_idenfier_eq_subject_identifier (self):
        """Tests merging of topics by existing topic with item
        identifer equal to a topic's subject identifier from the other
        map."""
        reference = 'http://sf.net/projects/tinytim/loc'
        locA = self.tm.create_locator(reference)
        topicA = self.tm.create_topic_by_item_identifier(locA)
        locB = self.tm2.create_locator(reference)
        topicB = self.tm2.create_topic_by_subject_identifier(locB)
        self.assertEqual(1, self.tm.get_topics().count())
        self.assertEqual(1, self.tm2.get_topics().count())
        self.assertEqual(topicA, self.tm.get_construct_by_item_identifier(locA))
        self.assertEqual(None, self.tm.get_topic_by_subject_identifier(locA))

        self.tm.merge_in(self.tm2)
        self.assertEqual(1, self.tm.get_topics().count())
        self.assertEqual(topicA, self.tm.get_construct_by_item_identifier(locA))
        self.assertEqual(topicA, self.tm.get_topic_by_subject_identifier(locA))
        self.assertEqual(1, topicA.get_subject_identifiers().count())
        self.assertEqual(locA, topicA.get_subject_identifiers()[0])
        self.assertEqual(1, topicA.get_item_identifiers().count())
        self.assertEqual(locA, topicA.get_item_identifiers()[0])
        self.assertEqual(0, topicA.get_subject_locators().count())

        # merge_in must not have any side effects on tm2.
        self.assertEqual(1, self.tm2.get_topics().count())
        self.assertEqual(None, self.tm2.get_construct_by_item_identifier(locB))
        self.assertEqual(topicB, self.tm2.get_topic_by_subject_identifier(locB))
        self.assertEqual(1, topicB.get_subject_identifiers().count())
        self.assertEqual(locB, topicB.get_subject_identifiers()[0])
        self.assertEqual(0, topicB.get_item_identifiers().count())
        self.assertEqual(0, topicB.get_subject_locators().count())

    def test_merge_subject_identifier_eq_item_identifier (self):
        """Tests merging of topics by existing topic with subject
        identifier equal to a topic's item identifier from the other
        map."""
        reference = 'http://sf.net/projects/tinytim/loc'
        locA = self.tm.create_locator(reference)
        topicA = self.tm.create_topic_by_subject_identifier(locA)
        locB = self.tm2.create_locator(reference)
        topicB = self.tm2.create_topic_by_item_identifier(locB)
        self.assertEqual(1, self.tm.get_topics().count())
        self.assertEqual(1, self.tm2.get_topics().count())
        self.assertEqual(None, self.tm.get_construct_by_item_identifier(locA))
        self.assertEqual(topicA, self.tm.get_topic_by_subject_identifier(locA))

        self.tm.merge_in(self.tm2)
        self.assertEqual(1, self.tm.get_topics().count())
        self.assertEqual(topicA, self.tm.get_construct_by_item_identifier(locA))
        self.assertEqual(topicA, self.tm.get_topic_by_subject_identifier(locA))
        self.assertEqual(1, topicA.get_subject_identifiers().count())
        self.assertEqual(locA, topicA.get_subject_identifiers()[0])
        self.assertEqual(1, topicA.get_item_identifiers().count())
        self.assertEqual(locA, topicA.get_item_identifiers()[0])
        self.assertEqual(0, topicA.get_subject_locators().count())

        # merge_in must not have any side effects on tm2.
        self.assertEqual(1, self.tm2.get_topics().count())
        self.assertEqual(None, self.tm2.get_topic_by_subject_identifier(locB))
        self.assertEqual(topicB,
                         self.tm2.get_construct_by_item_identifier(locB))
        self.assertEqual(1, topicB.get_item_identifiers().count())
        self.assertEqual(locB, topicB.get_item_identifiers()[0])
        self.assertEqual(0, topicB.get_subject_identifiers().count())
        self.assertEqual(0, topicB.get_subject_locators().count())

    def test_add_topics_from_other_map (self):
        """Tests if topics are added to a topic map from another topic
        map."""
        referenceA = 'http://www.tmapi.org/#iid-A'
        referenceB = 'http://www.tmapi.org/#iid-B'
        locA = self.tm.create_locator(referenceA)
        topicA = self.tm.create_topic_by_item_identifier(locA)
        locB = self.tm2.create_locator(referenceB)
        topicB = self.tm2.create_topic_by_item_identifier(locB)
        # Check tm.
        self.assertEqual(1, self.tm.get_topics().count())
        self.assertEqual(topicA, self.tm.get_construct_by_item_identifier(locA))
        self.assertEqual(None, self.tm.get_construct_by_item_identifier(locB))
        # Check tm2.
        self.assertEqual(1, self.tm2.get_topics().count())
        self.assertEqual(topicB,
                         self.tm2.get_construct_by_item_identifier(locB))
        self.assertEqual(None, self.tm2.get_construct_by_item_identifier(locA))
        self.tm.merge_in(self.tm2)
        self.assertEqual(2, self.tm.get_topics().count())
        # Check that topicA is unchanged.
        self.assertEqual(topicA, self.tm.get_construct_by_item_identifier(locA))
        self.assertEqual(1, topicA.get_item_identifiers().count())
        self.assertEqual(locA, topicA.get_item_identifiers()[0])
        self.assertEqual(0, topicA.get_subject_identifiers().count())
        self.assertEqual(0, topicA.get_subject_locators().count())
        # Check the new topic (which is topicB in tm2).
        new_topic = self.tm.get_construct_by_item_identifier(locB)
        self.assertNotEqual(None, new_topic)
        self.assertEqual(1, new_topic.get_item_identifiers().count())
        self.assertEqual(locB, new_topic.get_item_identifiers()[0])
        self.assertEqual(0, new_topic.get_subject_identifiers().count())
        self.assertEqual(0, new_topic.get_subject_locators().count())
