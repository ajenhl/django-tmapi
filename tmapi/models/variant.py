from django.db import models

from construct_fields import ConstructFields
from datatype_aware import DatatypeAware


class Variant (ConstructFields, DatatypeAware):

    """Represents a variant item."""
    
    name = models.ForeignKey('Name', related_name='variants')

    class Meta:
        app_label = 'tmapi'

    def get_parent (self):
        """Returns the `Name` to which this variant belongs.

        :rtype: `Name`

        """
        return self.name
