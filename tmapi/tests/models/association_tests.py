"""Module containing tests for the Association model."""

from django.test import TestCase

from tmapi.exceptions import ModelConstraintException
from tmapi.models import TopicMapSystem


class AssociationTest (TestCase):

    def setUp (self):
        self.tms = TopicMapSystem()
    
    def test_parent (self):
        parent = self.tms.create_topic_map(
            'http://www.tmapi.org/test/assoc/parent')
        self.assertEqual(parent.get_associations().count(), 0,
                         'Expected new topic maps to be created with no ' +
                         'associations')
        association = parent.create_association(parent.create_topic())
        self.assertEqual(parent, association.get_parent(), 'Unexpected ' +
                         'association parent after creation')
        self.assertEqual(1, parent.get_associations().count(),
                         'Expected association list size to increment for ' +
                         'topic map')
        self.assertTrue(association in parent.get_associations(),
                        'Association is not part of get_associations()')
        association.remove()
        self.assertEqual(0, parent.get_associations().count(),
                         'Expected association list size to decrement for ' +
                         'topic map')

    def test_role_creation (self):
        tm = self.tms.create_topic_map('http://www.tmapi.org/test/assoc/parent')
        association = tm.create_association(tm.create_topic())
        self.assertEqual(0, association.get_roles().count())
        role_type = tm.create_topic()
        player = tm.create_topic()
        self.assertEqual(0, player.get_roles_played().count())
        role = association.create_role(role_type, player)
        self.assertEqual(role_type, role.get_type(), 'Unexpected role type')
        self.assertEqual(player, role.get_player(), 'Unexpected role player')
        self.assertEqual(1, player.get_roles_played().count())
        self.assertTrue(role in player.get_roles_played())

    def test_role_types (self):
        tm = self.tms.create_topic_map('http://www.tmapi.org/test/assoc/parent')
        association = tm.create_association(tm.create_topic())
        type1 = tm.create_topic()
        type2 = tm.create_topic()
        self.assertEqual(0, association.get_role_types().count())
        role1 = association.create_role(type1, tm.create_topic())
        self.assertEqual(1, association.get_role_types().count())
        self.assertTrue(type1 in association.get_role_types())
        role2 = association.create_role(type2, tm.create_topic())
        self.assertEqual(2, association.get_role_types().count())
        self.assertTrue(type1 in association.get_role_types())
        self.assertTrue(type2 in association.get_role_types())
        role3 = association.create_role(type2, tm.create_topic())
        self.assertEqual(2, association.get_role_types().count())
        self.assertTrue(type1 in association.get_role_types())
        self.assertTrue(type2 in association.get_role_types())
        role3.remove()
        self.assertEqual(2, association.get_role_types().count())
        self.assertTrue(type1 in association.get_role_types())
        self.assertTrue(type2 in association.get_role_types())
        role2.remove()
        self.assertEqual(1, association.get_role_types().count())
        self.assertTrue(type1 in association.get_role_types())
        self.assertFalse(type2 in association.get_role_types())
        role1.remove()
        self.assertEqual(0, association.get_role_types().count())
        
    def test_role_filter (self):
        tm = self.tms.create_topic_map('http://www.tmapi.org/test/assoc/parent')
        association = tm.create_association(tm.create_topic())
        type1 = tm.create_topic()
        type2 = tm.create_topic()
        unused_type = tm.create_topic()
        self.assertEqual(0, association.get_roles(type1).count())
        self.assertEqual(0, association.get_roles(type2).count())
        self.assertEqual(0, association.get_roles(unused_type).count())
        role1 = association.create_role(type1, tm.create_topic())
        self.assertEqual(1, association.get_roles(type1).count())
        self.assertTrue(role1 in association.get_roles(type1))
        self.assertEqual(0, association.get_roles(type2).count())
        self.assertEqual(0, association.get_roles(unused_type).count())
        role2 = association.create_role(type2, tm.create_topic())
        self.assertEqual(1, association.get_roles(type2).count())
        self.assertTrue(role2 in association.get_roles(type2))
        role3 = association.create_role(type2, tm.create_topic())
        self.assertEqual(2, association.get_roles(type2).count())
        self.assertTrue(role2 in association.get_roles(type2))
        self.assertTrue(role3 in association.get_roles(type2))
        self.assertEqual(0, association.get_roles(unused_type).count())
        role3.remove()
        self.assertEqual(1, association.get_roles(type2).count())
        self.assertTrue(role2 in association.get_roles(type2))
        role2.remove()
        self.assertEqual(0, association.get_roles(type2).count())
        role1.remove()
        self.assertEqual(0, association.get_roles(type1).count())
        self.assertEqual(0, association.get_roles(unused_type).count())

    def test_role_creation_invalid_player (self):
        tm = self.tms.create_topic_map('http://www.tmapi.org/test/assoc/parent')
        association = tm.create_association(tm.create_topic())
        self.assertEqual(0, association.get_roles().count())
        self.assertRaises(ModelConstraintException, association.create_role,
                          tm.create_topic(), None)

    def test_role_creation_invalid_type (self):
        tm = self.tms.create_topic_map('http://www.tmapi.org/test/assoc/parent')
        association = tm.create_association(tm.create_topic())
        self.assertEqual(0, association.get_roles().count())
        self.assertRaises(ModelConstraintException, association.create_role,
                          None, tm.create_topic())
