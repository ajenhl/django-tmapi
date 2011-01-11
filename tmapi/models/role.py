from django.db import models

from tmapi.exceptions import ModelConstraintException

from construct_fields import ConstructFields
from reifiable import Reifiable
from typed import Typed


class Role (ConstructFields, Reifiable, Typed):

    """Represents an association role item."""
    
    association = models.ForeignKey('Association', related_name='roles')
    player = models.ForeignKey('Topic', related_name='role_players')

    class Meta:
        app_label = 'tmapi'

    def get_parent (self):
        """Returns the `Association` to which this role belongs.

        :rtype: `Association`
        
        """
        return self.association

    def get_player (self):
        """Returns the topic playing this role.

        :rtype: `Topic`
        
        """
        return self.player

    def set_player (self, player):
        """Sets the role player.

        Any previous role player will be overridden by `player`.

        :param player: the `Topic` which should play this role

        """
        if player is None:
            raise ModelConstraintException(self, 'The player may not be None')
        if self.topic_map != player.topic_map:
            raise ModelConstraintException(
                self, 'The player is not from the same topic map')
        self.player = player
        self.save()
