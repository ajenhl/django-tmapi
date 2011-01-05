from django.db import models

from construct import Construct


class Typed (Construct, models.Model):

    """Indicates that a Topic Maps construct is typed. `Association`s,
    `Role`s, `Occurrence`s, and `Name`s are typed."""

    type = models.ForeignKey('Topic', related_name='typed_%(class)ss')
    
    class Meta:
        abstract = True
        app_label = 'tmapi'
    
    def get_type (self):
        """Returns the type of this construct.

        :rtype: the `Topic` that represents the type

        """
        return self.type

    def set_type (self, construct_type):
        """Sets the type of this construct. Any previous type is overridden.

        :param construct_type: the `Topic` that should define the
          nature of this construct

        """
        self.type = construct_type
        self.save()
