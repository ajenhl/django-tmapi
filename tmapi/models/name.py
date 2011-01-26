from django.db import models

from tmapi.constants import XSD_ANY_URI, XSD_STRING
from tmapi.exceptions import ModelConstraintException

from construct_fields import ConstructFields
from locator import Locator
from reifiable import Reifiable
from scoped import Scoped
from typed import Typed
from variant import Variant


class Name (ConstructFields, Reifiable, Scoped, Typed):

    """Represents a topic name item."""
    
    topic = models.ForeignKey('Topic', related_name='names')
    value = models.TextField()

    class Meta:
        app_label = 'tmapi'

    def create_variant (self, value, scope, datatype=None):
        """Creates a `Variant` of this topic name with the specified
        string `value` and `scope`.

        If `datatype` is None, the newly created `Variant` will have
        the datatype xsd:string.

        The newly created `Variant` will contain all themes from the
        parent name and the themes specified in `scope`.

        :param value: the string value or locator which represents an IRI
        :type value: string or `Locator`
        :param scope: list of themes
        :type scope: list of `Topic`s
        :rtype: `Variant`

        """
        if value is None:
            raise ModelConstraintException(self, 'The value may not be None')
        if not scope:
            raise ModelConstraintException(self, 'The scope may not be None')
        if scope == list(self.get_scope()):
            raise ModelConstraintException(
                self, 'The variant would be in the same scope as the parent')
        if datatype is None:
            if isinstance(value, Locator):
                datatype = Locator(XSD_ANY_URI)
            elif isinstance(value, str):
                datatype = Locator(XSD_STRING)
        if isinstance(value, Locator):
            value = value.to_external_form()
        variant = Variant(name=self, datatype=datatype.to_external_form(),
                          value=value, topic_map=self.topic_map)
        variant.save()
        for theme in scope:
            variant.scope.add(theme)
        return variant
        
    def get_parent (self):
        """Returns the `Topic` to which this name belongs."""
        return self.topic

    def get_value (self):
        """Returns the value of this name."""
        return self.value

    def get_variants (self):
        """Returns the variants defined for this name."""
        return self.variants.all()

    def merge_into (self, topic):
        """Attaches this name to `topic`, merging it as
        appropriate with an existing name.

        :param topic: the `Topic` this name is to be attached to
        :type topic: `Topic`

        """
        merged = False
        value = self.get_value()
        name_type = self.get_type()
        scope = set(self.get_scope())
        reifier = self.get_reifier()
        variants = self.get_variants()
        for name in topic.get_names(name_type):
            if value == name.get_value() and scope == set(name.get_scope()):
                # Handle reifiers.
                other_reifier = name.get_reifier()
                if reifier is not None and other_reifier is None:
                    self.set_reifier(None)
                    name.set_reifier(reifier)
                elif reifier is not None and other_reifier is not None:
                    self.set_reifier(None)
                    other_reifier.merge_in(reifier)
                # Handle item identifiers.
                for iid in self.get_item_identifiers():
                    self.item_identifiers.remove(iid)
                    name.item_identifiers.add(iid)
                # Handle variants.
                for variant in variants:
                    variant.merge_into(name)
                self.remove()
                merged = True
                break
        if not merged:
            self.topic = topic
            self.save()
                
    def set_value (self, value):
        """Sets the value of this name. The previous value is overridden."""
        if value is None:
            raise ModelConstraintException(self, 'The value may not be None')
        self.value = value
        self.save()
