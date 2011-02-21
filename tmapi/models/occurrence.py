from django.db import models

from construct_fields import ConstructFields
from datatype_aware import DatatypeAware
from typed import Typed

from tmapi.models.merge_utils import handle_existing_construct


class Occurrence (ConstructFields, DatatypeAware, Typed):

    topic = models.ForeignKey('Topic', related_name='occurrences')

    class Meta:
        app_label = 'tmapi'

    def get_parent (self):
        """Returns the `Topic` to which this occurrence belongs.

        :rtype: `Topic`
        
        """
        return self.topic
        
