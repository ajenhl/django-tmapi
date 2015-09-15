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

"""Module containing tests for the TopicMapSystem module.

Most if not all of these tests are ported from the public domain tests
that come with the TMAPI 2.0 distribution (http://www.tmapi.org/2.0/).

"""

from tmapi.exceptions import TopicMapExistsException

from .tmapi_test_case import TMAPITestCase

class TopicMapSystemTest (TMAPITestCase):

    def test_load (self):
        tm = self.tms.get_topic_map(self.default_locator)
        self.assertTrue(tm, 'TopicMap was not created in setUp or was not ' +
                        'retrieved')
        self.assertTrue(tm.get_id(), 'There is no identifier for TopicMap')
        self.assertEqual(self.tm.get_id(), tm.get_id())

    def test_same_locator (self):
        """Verify two TopicMaps can't be created with the same locator."""
        self.assertRaises(TopicMapExistsException, self.tms.create_topic_map,
                          self.default_locator)

    def test_set (self):
        base = 'http://www.tmapi.org/test-tm-system/'
        tm1 = self.create_topic_map(base + 'test1')
        tm2 = self.create_topic_map(base + 'test2')
        tm3 = self.create_topic_map(base + 'test3')
        self.assertTrue(tm1, 'TopicMap 1 was not created')
        self.assertTrue(tm2, 'TopicMap 2 was not created')
        self.assertTrue(tm3, 'TopicMap 3 was not created')

    def test_remove_topic_maps (self):
        base = 'http://www.tmapi.org/test-tm-system/'
        tm1 = self.create_topic_map(base + 'test1')
        tm2 = self.create_topic_map(base + 'test2')
        tm3 = self.create_topic_map(base + 'test3')
        self.assertTrue(tm1, 'TopicMap 1 was not created')
        self.assertTrue(tm2, 'TopicMap 2 was not created')
        self.assertTrue(tm3, 'TopicMap 3 was not created')
        tmcount = len(self.tms.get_locators())
        tm3.remove()
        self.assertEqual(tmcount-1, len(self.tms.get_locators()),
                         'Expected locator list size to decrement for the '
                         'topic map system')
        tm3 = self.tms.get_topic_map(base + 'test3')
        self.assertFalse(tm3, 'Expected TopicMap 3 to be deleted')

    def test_locator_creation (self):
        reference = 'http://www.tmapi.org/'
        locator = self.tms.create_locator(reference)
        self.assertEqual(reference, locator.get_reference())

    def test_topic_map_locator (self):
        reference = 'http://www.tmapi.org/'
        locator = self.tms.create_locator(reference + '2')
        tm = self.tms.create_topic_map(reference)
        self.assertEqual(reference, tm.get_locator().get_reference())
        self.assertEqual(tm, self.tms.get_topic_map(reference))
        tm.remove()
        tm = self.tms.create_topic_map(locator)
        self.assertEqual(locator, tm.get_locator())
        self.assertEqual(tm, self.tms.get_topic_map(locator))
