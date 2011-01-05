"""Module containing tests for the Role model."""

from django.test import TestCase

from tmapi.exceptions import ModelConstraintException
from tmapi.models import TopicMapSystem


class RoleTest (TestCase):

    def setUp (self):
        self.tms = TopicMapSystem()
        self.tm = self.tms.create_topic_map('http://www.example.org/tm/')
    
    def test_parent (self):
        parent = self.tm.create_association(self.tm.create_topic())
        self.assertEqual(0, parent.get_roles().count(),
                         'Expected no roles in a newly created association')
        role = parent.create_role(self.tm.create_topic(),
                                  self.tm.create_topic())
        self.assertEqual(parent, role.get_parent(),
                         'Unexpected role parent after creation')
        self.assertEqual(1, parent.get_roles().count(),
                         'Expected role list size to increment for association')
        self.assertTrue(role in parent.get_roles(),
                        'Role is not part of get_roles()')
        role.remove()
        self.assertEqual(0, parent.get_roles().count(),
                         'Expected role list size to decrement for association')
        
    def test_role_player_set_get (self):
        association = self.tm.create_association(self.tm.create_topic())
        self.assertEqual(0, association.get_roles().count(),
                         'Expected no roles in a newly created association')
        role_type = self.tm.create_topic()
        player = self.tm.create_topic()
        role = association.create_role(role_type, player)
        self.assertEqual(role_type, role.get_type(), 'Unexpected role type')
        self.assertEqual(player, role.get_player(), 'Unexpected role player')
        self.assertTrue(role in player.get_roles_played(),
                        'Role is not reported in get_roles_played()')
        player2 = self.tm.create_topic()
        role.set_player(player2)
        self.assertEqual(player2, role.get_player(),
                         'Unexpected role player after setting to "player2"')
        self.assertTrue(role in player2.get_roles_played(),
                        'Role is not reported in get_roles_played()')
        self.assertEqual(0, player.get_roles_played().count(),
                         '"player" should not play the role any more')
        role.set_player(player)
        self.assertEqual(player, role.get_player(),
                         'Unexpected role player after setting to "player"')

    def test_illegal_player (self):
        association = self.tm.create_association(self.tm.create_topic())
        role = association.create_role(self.tm.create_topic(),
                                       self.tm.create_topic())
        self.assertRaises(ModelConstraintException, role.set_player, None)
