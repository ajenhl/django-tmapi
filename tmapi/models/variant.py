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

    def merge_into (self, name):
        """Attaches this variant to `name`, merging it as
        appropriate with an existing variant.

        :param name: the `Name` this variant is to be attached to
        :type topic: `Name`

        """
        merged = False
        datatype = self.get_datatype()
        scope = set(self.get_scope())
        value = self.get_value()
        reifier = self.get_reifier()
        for variant in name.get_variants():
            # If the value, datatype, type and scope of the two
            # variants match, then merge them.
            if value == variant.get_value() and \
                    scope == set(variant.get_scope()) and \
                    datatype == variant.get_datatype():
                # Handle reifiers.
                other_reifier = variant.get_reifier()
                if reifier is not None and other_reifier is None:
                    self.set_reifier(None)
                    variant.set_reifier(reifier)
                elif reifier is not None and other_reifier is not None:
                    self.set_reifier(None)
                    other_reifier.merge_in(reifier)
                # Handle item identifiers.
                for iid in self.get_item_identifiers():
                    self.item_identifiers.remove(iid)
                    variant.item_identifiers.add(iid)
                self.remove()
                merged = True
                break
        if not merged:
            self.name = name
            self.save()
