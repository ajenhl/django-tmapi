"""Module containing tests for the TopicMapSystem module."""

from tmapi.exceptions import TopicMapExistsException

from tmapi_test_case import TMAPITestCase

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

