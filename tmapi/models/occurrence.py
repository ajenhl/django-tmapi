from django.db import models

from construct_fields import ConstructFields
from datatype_aware import DatatypeAware
from typed import Typed


class Occurrence (ConstructFields, DatatypeAware, Typed):

    topic = models.ForeignKey('Topic', related_name='occurrences')

    class Meta:
        app_label = 'tmapi'

    def get_parent (self):
        """Returns the `Topic` to which this occurrence belongs.

        :rtype: `Topic`
        
        """
        return self.topic

    def merge_into (self, topic):
        """Attaches this occurrance to `topic`, merging it as
        appropriate with an existing occurrence.

        :param topic: the `Topic` this occurrance is to be attached to
        :type topic: `Topic`

        """
        merged = False
        datatype = self.get_datatype()
        type = self.get_type()
        scope = set(self.get_scope())
        value = self.get_value()
        reifier = self.get_reifier()
        for occurrence in topic.get_occurrences(type):
            # If the value, datatype, type and scope of the two
            # occurrences match, then merge them.
            if value == occurrence.get_value() and \
                    scope == set(occurrence.get_scope()) and \
                    datatype == occurrence.get_datatype():
                # Handle reifiers.
                other_reifier = occurrence.get_reifier()
                if reifier is not None and other_reifier is None:
                    self.set_reifier(None)
                    occurrence.set_reifier(reifier)
                elif reifier is not None and other_reifier is not None:
                    self.set_reifier(None)
                    other_reifier.merge_in(other_reifier)
                # Handle item identifiers.
                for iid in self.get_item_identifiers():
                    self.item_identifiers.remove(iid)
                    occurrence.item_identifiers.add(iid)
                self.remove()
                merged = True
                break
        if not merged:
            self.topic = topic
            self.save()
        
