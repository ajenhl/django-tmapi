from django.db import models

from tmapi.exceptions import ModelConstraintException

from construct import Construct


class Reifiable (Construct, models.Model):

    """Indicates that a `Construct` is reifiable. Every Topic Maps
    construct that is not a `Topic` is reifiable."""

    reifier = models.OneToOneField('Topic', related_name='reified_%(class)s',
                                   null=True)

    class Meta:
        abstract = True
        app_label = 'tmapi'

    def get_reifier (self):
        """Returns the reifier of this construct.

        :rtype: `Topic`

        """
        return self.reifier

    def set_reifier (self, reifier):
        """Sets the reifier of this consutrct.

        The specified reifier **must not** reify another information
        item.

        :param reifier: the topic that should reify this construct or
          None if an existing reifier should be removed
        :type reifier: `Topic` or None
        :raises `ModelConstraintException`: if the specified `reifier`
          reifies another construct

        """
        if reifier is None:
            reified = None
        else:
            if self.get_topic_map() != reifier.get_topic_map():
                raise ModelConstraintException
            reified = reifier.get_reified()
        if reified is None:
            self.reifier = reifier
            self.save()
        elif reified == self:
            pass
        else:
            raise ModelConstraintException
