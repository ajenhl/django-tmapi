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

from tmapi.exceptions import ModelConstraintException

from .construct_fields import ConstructFields
from .reifiable import Reifiable
from .role import Role
from .scoped import Scoped
from .topic import Topic
from .typed import Typed


class Association (ConstructFields, Reifiable, Scoped, Typed):

    class Meta:
        app_label = 'tmapi'

    def create_role (self, role_type, player):
        """Creates a new role representing a role in this association.

        :param role_type: the role type
        :type role_type: `Topic`
        :param player: the role player
        :type player: `Topic`
        :rtype: `Role`

        """
        if role_type is None:
            raise ModelConstraintException(self, 'The type may not be None')
        if player is None:
            raise ModelConstraintException(self, 'The player may not be None')
        if self.topic_map != role_type.topic_map:
            raise ModelConstraintException(
                self, 'The type is not from the same topic map')
        if self.topic_map != player.topic_map:
            raise ModelConstraintException(
                self, 'The player is not from the same topic map')
        role = Role(association=self, type=role_type, player=player,
                    topic_map=self.topic_map)
        role.save()
        return role

    def get_parent (self):
        """Returns the `TopicMap` to which this association belongs.

        :rtype: `TopicMap`

        """
        return self.topic_map

    def get_roles (self, role_type=None):
        """Returns the `Role`s participating in this association.

        If `role_type` is not None, returns all roles with the
        specified type.

        :param role_type: the type of the `Role` instances to be returned
        :type role_type: `Topic`
        :rtype: `QuerySet` of `Role`s

        """
        if role_type is None:
            roles = self.roles.all()
        else:
            roles = self.roles.filter(type=role_type)
        return roles

    def get_role_types (self):
        """Returns the role types participating in this association.

        :rtype: `QuerySet` of `Topic`s

        """
        return Topic.objects.filter(typed_roles__association=self).distinct()
