from django.db import models

from construct import Construct


class Reifiable (Construct, models.Model):

    """Indicates that a `Construct` is reifiable. Every Topic Maps
    construct that is not a `Topic` is reifiable."""

    reifier = models.OneToOneField('Topic', related_name='reified_%(class)ss',
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
        self.reifier = reifier
        self.save()
