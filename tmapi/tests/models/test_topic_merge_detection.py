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

"""Tests if merging situations are detected.

Most if not all of these tests are ported from the public domain tests
that come with the TMAPI 2.0 distribution (http://www.tmapi.org/2.0/).

"""

from tmapi.exceptions import IdentityConstraintException
from tmapi.models import TopicMapSystemFactory

from .tmapi_test_case import TMAPITestCase


class TopicMergeDetectionTestCase (TMAPITestCase):

    def get_automerge_enabled (self):
        return None

    def setUp (self):
        self.automerge = self.get_automerge_enabled()
        factory = TopicMapSystemFactory.new_instance()
        if self.automerge is not None:
            factory.set_feature('http://tmapi.org/features/automerge',
                                self.automerge)
        self.tms = factory.new_topic_map_system()
        self.tms.save()
        self.default_locator = self.tms.create_locator(self.DEFAULT_ADDRESS)
        self.tm = self.tms.create_topic_map(self.default_locator)

    def test_existing_subject_identifier (self):
        """Tests if adding a duplicate subject identifier is
        detected."""
        if self.automerge is None:
            return
        topic1 = self.tm.create_topic()
        topic2 = self.tm.create_topic()
        self.assertEqual(2, self.tm.get_topics().count())
        loc = self.tm.create_locator('http://sf.net/projects/tinytim')
        topic1.add_subject_identifier(loc)
        self.assertTrue(loc in topic1.get_subject_identifiers())
        self.assertEqual(topic1, self.tm.get_topic_by_subject_identifier(loc))
        try:
            topic2.add_subject_identifier(loc)
            if not self.automerge:
                self.fail('The duplicate subject identifier "' + str(loc) +
                          '" is not detected')
            else:
                self.assertEqual(1, self.tm.get_topics().count())
        except IdentityConstraintException:
            if self.automerge:
                self.fail('Expected that the duplicate subject identifier ' +
                          'causes a transparent merge')
            self.assertEqual(2, self.tm.get_topics().count())
            self.assertTrue(loc in topic1.get_subject_identifiers())
            self.assertFalse(loc in topic2.get_subject_identifiers())

    def test_existing_subject_identifier_legal (self):
        """Tests if adding a duplicate subject identifier on the same
        topic is ignored."""
        if self.automerge is None:
            return
        topic = self.tm.create_topic()
        loc = self.tm.create_locator('http://sf.net/projects/tinytim')
        topic.add_subject_identifier(loc)
        self.assertEqual(1, topic.get_subject_identifiers().count())
        self.assertTrue(loc in topic.get_subject_identifiers())
        self.assertEqual(topic, self.tm.get_topic_by_subject_identifier(loc))
        topic.add_subject_identifier(loc)
        self.assertEqual(1, topic.get_subject_identifiers().count())

    def test_existing_subject_locator (self):
        """Tests if adding a duplicate subject locator is detected."""
        if self.automerge is None:
            return
        topic1 = self.tm.create_topic()
        topic2 = self.tm.create_topic()
        self.assertEqual(2, self.tm.get_topics().count())
        loc = self.tm.create_locator('http://sf.net/projects/tinytim')
        topic1.add_subject_locator(loc)
        self.assertTrue(loc in topic1.get_subject_locators())
        self.assertEqual(topic1, self.tm.get_topic_by_subject_locator(loc))
        try:
            topic2.add_subject_locator(loc)
            if not self.automerge:
                self.fail('The duplicate subject locator "' + str(loc) +
                          '" is not detected')
            else:
                self.assertEqual(1, self.tm.get_topics().count())
        except IdentityConstraintException:
            if self.automerge:
                self.fail('Expected that the duplicate subject locator ' +
                          'causes a transparent merge')
            self.assertEqual(2, self.tm.get_topics().count())
            self.assertTrue(loc in topic1.get_subject_locators())
            self.assertFalse(loc in topic2.get_subject_locators())

    def test_existing_subject_locator_legal (self):
        """Tests if adding a duplicate subject locator on the same
        topic topic is ignored."""
        if self.automerge is None:
            return
        topic = self.tm.create_topic()
        loc = self.tm.create_locator('http://sf.net/projects/tinytim')
        topic.add_subject_locator(loc)
        self.assertEqual(1, topic.get_subject_locators().count())
        self.assertTrue(loc in topic.get_subject_locators())
        self.assertEqual(topic, self.tm.get_topic_by_subject_locator(loc))
        topic.add_subject_locator(loc)
        self.assertEqual(1, topic.get_subject_locators().count())

    def test_existing_subject_identifier_add_item_identifier (self):
        """Tests if adding an item identifier equal to a subject
        identifier is detected."""
        if self.automerge is None:
            return
        topic1 = self.tm.create_topic()
        topic2 = self.tm.create_topic()
        self.assertEqual(2, self.tm.get_topics().count())
        loc = self.tm.create_locator('http://sf.net/projects/tinytim')
        topic1.add_subject_identifier(loc)
        self.assertTrue(loc in topic1.get_subject_identifiers())
        self.assertEqual(topic1, self.tm.get_topic_by_subject_identifier(loc))
        try:
            topic2.add_item_identifier(loc)
            if not self.automerge:
                self.fail('A topic with a subject identifier equal to the item identifier "' + str(loc) + '" exists')
            else:
                self.assertEqual(1, self.tm.get_topics().count())
        except IdentityConstraintException:
            if self.automerge:
                self.fail('Expected that the duplicate item identifier ' +
                          'causes a transparent merge')
            self.assertEqual(2, self.tm.get_topics().count())
            self.assertTrue(loc in topic1.get_subject_identifiers())
            self.assertFalse(loc in topic2.get_item_identifiers())

    def test_existing_subject_identifier_add_item_identifier_legal (self):
        """Tests if adding an item identifier equal to a subject
        identifier on the same topic is accepted."""
        if self.automerge is None:
            return
        loc = self.tm.create_locator('http://sf.net/projects/tinytim')
        topic = self.tm.create_topic_by_subject_identifier(loc)
        self.assertEqual(1, topic.get_subject_identifiers().count())
        self.assertEqual(0, topic.get_item_identifiers().count())
        self.assertTrue(loc in topic.get_subject_identifiers())
        self.assertEqual(topic, self.tm.get_topic_by_subject_identifier(loc))
        self.assertEqual(None, self.tm.get_construct_by_item_identifier(loc))
        topic.add_item_identifier(loc)
        self.assertEqual(1, topic.get_subject_identifiers().count())
        self.assertEqual(1, topic.get_item_identifiers().count())
        self.assertTrue(loc in topic.get_subject_identifiers())
        self.assertTrue(loc in topic.get_item_identifiers())
        self.assertEqual(topic, self.tm.get_topic_by_subject_identifier(loc))
        self.assertEqual(topic, self.tm.get_construct_by_item_identifier(loc))

    def test_existing_item_identifier_add_subject_identifier (self):
        """Tests if adding a subject identifier equal to an item
        identifier is detected."""
        if self.automerge is None:
            return
        topic1 = self.tm.create_topic()
        topic2 = self.tm.create_topic()
        self.assertEqual(2, self.tm.get_topics().count())
        loc = self.tm.create_locator('http://sf.net/projects/tinytim')
        topic1.add_item_identifier(loc)
        self.assertTrue(loc in topic1.get_item_identifiers())
        self.assertEqual(topic1, self.tm.get_construct_by_item_identifier(loc))
        try:
            topic2.add_subject_identifier(loc)
            if not self.automerge:
                self.fail('A topic with an item identifier equal to the subject identifier "' + str(loc) + '" exists')
            else:
                self.assertEqual(1, self.tm.get_topics().count())
        except IdentityConstraintException:
            if self.automerge:
                self.fail('Expected a transparent merge for a topic with an item identifier equal to the subject identifier "' + str(loc))
            self.assertEqual(2, self.tm.get_topics().count())
            self.assertTrue(loc in topic1.get_item_identifiers())
            self.assertFalse(loc in topic2.get_subject_identifiers())

    def test_existing_item_identifiers_add_subject_identifier_legal (self):
        """Tests if adding a subject identifier equal to an item
        identifier on the same topic is accepted."""
        if self.automerge is None:
            return
        loc = self.tm.create_locator('http://sf.net/projects/tinytim')
        topic = self.tm.create_topic_by_item_identifier(loc)
        self.assertEqual(1, topic.get_item_identifiers().count())
        self.assertEqual(0, topic.get_subject_identifiers().count())
        self.assertTrue(loc in topic.get_item_identifiers())
        self.assertEqual(topic, self.tm.get_construct_by_item_identifier(loc))
        self.assertEqual(None, self.tm.get_topic_by_subject_identifier(loc))
        topic.add_subject_identifier(loc)
        self.assertEqual(1, topic.get_subject_identifiers().count())
        self.assertEqual(1, topic.get_item_identifiers().count())
        self.assertTrue(loc in topic.get_subject_identifiers())
        self.assertTrue(loc in topic.get_item_identifiers())
        self.assertEqual(topic, self.tm.get_topic_by_subject_identifier(loc))
        self.assertEqual(topic, self.tm.get_construct_by_item_identifier(loc))


class TopicMergeDetectionAutomergeDisabledTest (TopicMergeDetectionTestCase):

    """Tests merge detection with feature "automerge" disabled."""

    def get_automerge_enabled (self):
        return False


class TopicMergeDetectionAutomergeEnabledTest (TopicMergeDetectionTestCase):

    """Tests merge detection with feature "automerge" enabled."""

    def get_automerge_enabled (self):
        return True
