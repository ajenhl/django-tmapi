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

"""Module containing tests for the Association model.

Most if not all of these tests are ported from the public domain tests
that come with the TMAPI 2.0 distribution (http://www.tmapi.org/2.0/).

"""

from tmapi.exceptions import ModelConstraintException

from .tmapi_test_case import TMAPITestCase


class AssociationTest (TMAPITestCase):

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
        association = self.create_association()
        self.assertEqual(0, association.get_roles().count(),
                         'Expected no roles in a newly created association')
        role_type = self.create_topic()
        player = self.create_topic()
        self.assertEqual(0, player.get_roles_played().count())
        role = association.create_role(role_type, player)
        self.assertEqual(role_type, role.get_type(), 'Unexpected role type')
        self.assertEqual(player, role.get_player(), 'Unexpected role player')
        self.assertEqual(1, player.get_roles_played().count())
        self.assertTrue(role in player.get_roles_played())

    def test_role_types (self):
        association = self.create_association()
        type1 = self.create_topic()
        type2 = self.create_topic()
        self.assertEqual(0, association.get_role_types().count())
        role1 = association.create_role(type1, self.create_topic())
        self.assertEqual(1, association.get_role_types().count())
        self.assertTrue(type1 in association.get_role_types())
        role2 = association.create_role(type2, self.create_topic())
        self.assertEqual(2, association.get_role_types().count())
        self.assertTrue(type1 in association.get_role_types())
        self.assertTrue(type2 in association.get_role_types())
        role3 = association.create_role(type2, self.create_topic())
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
        association = self.create_association()
        type1 = self.create_topic()
        type2 = self.create_topic()
        unused_type = self.create_topic()
        self.assertEqual(0, association.get_roles(type1).count())
        self.assertEqual(0, association.get_roles(type2).count())
        self.assertEqual(0, association.get_roles(unused_type).count())
        role1 = association.create_role(type1, self.create_topic())
        self.assertEqual(1, association.get_roles(type1).count())
        self.assertTrue(role1 in association.get_roles(type1))
        self.assertEqual(0, association.get_roles(type2).count())
        self.assertEqual(0, association.get_roles(unused_type).count())
        role2 = association.create_role(type2, self.create_topic())
        self.assertEqual(1, association.get_roles(type2).count())
        self.assertTrue(role2 in association.get_roles(type2))
        role3 = association.create_role(type2, self.create_topic())
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

    def test_role_filter_illegal (self):
        # This test is not applicable in this implementation.
        pass

    def test_role_creation_invalid_player (self):
        association = self.create_association()
        self.assertEqual(0, association.get_roles().count())
        self.assertRaises(ModelConstraintException, association.create_role,
                          self.create_topic(), None)

    def test_role_creation_invalid_type (self):
        association = self.create_association()
        self.assertEqual(0, association.get_roles().count())
        self.assertRaises(ModelConstraintException, association.create_role,
                          None, self.create_topic())
