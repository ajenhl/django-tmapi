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

    def get_scope (self):
        """Returns the scope of this variant.

        The returned scope is a true superset of the parent's scope.

        :rtype: `QuerySet` of `Topic`s

        """
        variant_scope = super(Variant, self).get_scope()
        name_scope = self.name.get_scope()
        return (variant_scope | name_scope).distinct()
