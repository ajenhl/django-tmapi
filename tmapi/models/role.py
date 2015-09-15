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

from django.db import models

from tmapi.exceptions import ModelConstraintException

from .construct_fields import ConstructFields
from .reifiable import Reifiable
from .typed import Typed


class Role (ConstructFields, Reifiable, Typed):

    """Represents an association role item."""

    association = models.ForeignKey('Association', related_name='roles')
    player = models.ForeignKey('Topic', related_name='roles')

    class Meta:
        app_label = 'tmapi'

    def get_parent (self, proxy=None):
        """Returns the `Association` to which this role belongs.

        :rtype: `Association`

        """
        parent = self.association
        if proxy is not None:
            parent = proxy.objects.get(pk=parent.id)
        return parent

    def get_player (self, proxy=None):
        """Returns the topic playing this role.

        :rtype: `Topic`

        """
        player = self.player
        if proxy is not None:
            player = proxy.objects.get(pk=player.id)
        return player

    def set_player (self, player):
        """Sets the role player.

        Any previous role player will be overridden by `player`.

        :param player: the `Topic` which should play this role
        :type player: `Topic`

        """
        if player is None:
            raise ModelConstraintException(self, 'The player may not be None')
        if self.topic_map != player.topic_map:
            raise ModelConstraintException(
                self, 'The player is not from the same topic map')
        self.player = player
        self.save()
