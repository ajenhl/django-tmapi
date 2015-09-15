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

"""Tests if the engine respects the constraint if a Topic is removable
or not.

Most if not all of these tests are ported from the public domain tests
that come with the TMAPI 2.0 distribution (http://www.tmapi.org/2.0/).

"""

from tmapi.exceptions import TopicInUseException

from .tmapi_test_case import TMAPITestCase


class TopicRemovableConstraintTest (TMAPITestCase):

    def _test_typed (self, typed):
        """Tests if hte topic removable constraint is respected if the
        topic is used as a type.

        :param typed: a typed construct
        :type typed: `Typed`

        """
        topic_count = self.tm.get_topics().count()
        old_type = typed.get_type()
        topic = self.create_topic()
        self.assertEqual(topic_count+1, self.tm.get_topics().count())
        typed.set_type(topic)
        try:
            topic.remove()
            self.fail('The topic is used as a type')
        except TopicInUseException as ex:
            self.assertEqual(topic, ex.get_reporter())
        self.assertEqual(topic_count+1, self.tm.get_topics().count())
        typed.set_type(old_type)
        topic.remove()
        self.assertEqual(topic_count, self.tm.get_topics().count())

    def _test_scoped (self, scoped):
        """Tests if the topic removable constraint is respected if a
        topic is used as a theme.

        :param scoped: a scoped construct
        :type scoped: `Scoped`

        """
        topic_count = self.tm.get_topics().count()
        topic = self.create_topic()
        self.assertEqual(topic_count+1, self.tm.get_topics().count())
        scoped.add_theme(topic)
        try:
            topic.remove()
            self.fail('The topic is used as a theme')
        except TopicInUseException as ex:
            self.assertEqual(topic, ex.get_reporter())
        self.assertEqual(topic_count+1, self.tm.get_topics().count())
        scoped.remove_theme(topic)
        topic.remove()
        self.assertEqual(topic_count, self.tm.get_topics().count())

    def _test_reifiable (self, reifiable):
        """Tests if the topic removable constraint is respected if a
        topic is used as a reifier.

        :param reifiable: a reifiable that is not reified
        :type reifiable: `Reifiable`

        """
        self.assertEqual(None, reifiable.get_reifier())
        topic_count = self.tm.get_topics().count()
        topic = self.tm.create_topic()
        self.assertEqual(topic_count+1, self.tm.get_topics().count())
        reifiable.set_reifier(topic)
        try:
            topic.remove()
            self.fail('The topic is used as a reifier')
        except TopicInUseException as ex:
            self.assertEqual(topic, ex.get_reporter())
        self.assertEqual(topic_count+1, self.tm.get_topics().count())
        reifiable.set_reifier(None)
        topic.remove()
        self.assertEqual(topic_count, self.tm.get_topics().count())

    def test_used_as_topic_map_reifier (self):
        """Topic map reifier removable constraint test."""
        self._test_reifiable(self.tm)

    def test_used_as_association_type (self):
        """Association type removable constraint test."""
        self._test_typed(self.create_association())

    def test_used_as_association_theme (self):
        """Association theme removable constraint test."""
        self._test_scoped(self.create_association())

    def test_used_as_association_reifier (self):
        """Association reifier removable constraint test."""
        self._test_reifiable(self.create_association())

    def test_used_as_role_type (self):
        """Role type removable constraint test."""
        self._test_typed(self.create_role())

    def test_used_as_role_reifier (self):
        """Role reifier removable constraint test."""
        self._test_reifiable(self.create_role())

    def test_used_as_occurrence_type (self):
        """Occurrence type removable constraint test."""
        self._test_typed(self.create_occurrence())

    def test_used_as_occurrence_theme (self):
        """Occurrence theme removable constraint test."""
        self._test_scoped(self.create_occurrence())

    def test_used_as_occurrence_reifier (self):
        """Occurrence reifier removable constraint test."""
        self._test_reifiable(self.create_occurrence())

    def test_used_as_name_type (self):
        """Name type removable constraint test."""
        self._test_typed(self.create_name())

    def test_used_as_name_theme (self):
        """Name theme removable constraint test."""
        self._test_scoped(self.create_name())

    def test_used_as_name_reifier (self):
        """Name reifier removable constraint test."""
        self._test_reifiable(self.create_name())

    def test_used_as_variant_theme (self):
        """Variant theme removable constraint test."""
        self._test_scoped(self.create_variant())

    def test_used_variant_reifier (self):
        """Variant reifier removable constraint test."""
        self._test_reifiable(self.create_variant())

    def test_used_as_topic_type (self):
        """Tests if the removable constraint is respected if a topic
        is used as topic type."""
        topic = self.create_topic()
        topic2 = self.create_topic()
        self.assertEqual(2, self.tm.get_topics().count())
        topic2.add_type(topic)
        try:
            topic.remove()
            self.fail('The topic is used as a topic type')
        except TopicInUseException as ex:
            self.assertEqual(topic, ex.get_reporter())
        self.assertEqual(2, self.tm.get_topics().count())
        topic2.remove_type(topic)
        topic.remove()
        self.assertEqual(1, self.tm.get_topics().count())

    def test_used_as_player (self):
        """Tests if the removable constraint is respected if a topic
        is used as player."""
        topic = self.create_topic()
        self.assertEqual(1, self.tm.get_topics().count())
        topic.remove()
        self.assertEqual(0, self.tm.get_topics().count())
        topic = self.create_topic()
        self.assertEqual(1, self.tm.get_topics().count())
        association = self.tm.create_association(self.tm.create_topic())
        self.assertEqual(2, self.tm.get_topics().count())
        role = association.create_role(self.tm.create_topic(), topic)
        self.assertEqual(3, self.tm.get_topics().count())
        try:
            topic.remove()
            self.fail('The topic is used as a player')
        except TopicInUseException as ex:
            self.assertEqual(topic, ex.get_reporter())
        role.set_player(self.tm.create_topic())
        self.assertEqual(4, self.tm.get_topics().count())
        topic.remove()
        self.assertEqual(3, self.tm.get_topics().count())
