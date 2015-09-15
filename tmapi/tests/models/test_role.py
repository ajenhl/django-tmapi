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

"""Module containing tests for the Role model.

Most if not all of these tests are ported from the public domain tests
that come with the TMAPI 2.0 distribution (http://www.tmapi.org/2.0/).

"""

from tmapi.exceptions import ModelConstraintException

from .tmapi_test_case import TMAPITestCase


class RoleTest (TMAPITestCase):

    def test_parent (self):
        parent = self.create_association()
        self.assertEqual(0, parent.get_roles().count(),
                         'Expected no roles in a newly created association')
        role = parent.create_role(self.create_topic(), self.create_topic())
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
        association = self.create_association()
        self.assertEqual(0, association.get_roles().count(),
                         'Expected no roles in a newly created association')
        role_type = self.create_topic()
        player = self.create_topic()
        role = association.create_role(role_type, player)
        self.assertEqual(role_type, role.get_type(), 'Unexpected role type')
        self.assertEqual(player, role.get_player(), 'Unexpected role player')
        self.assertTrue(role in player.get_roles_played(),
                        'Role is not reported in get_roles_played()')
        player2 = self.create_topic()
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
        role = self.create_role()
        self.assertRaises(ModelConstraintException, role.set_player, None)
