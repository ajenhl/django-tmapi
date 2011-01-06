from django.db import models

from locator import LocatorBase


class ItemIdentifier (LocatorBase, models.Model):

    address = models.CharField(max_length=512)
    # Include a reference to the topic map of the construct this
    # identifier is associated with. This greatly eases checking for
    # duplicate identifiers within a topic map, given that there isn't
    # a single relationship back to the construct.
    containing_topic_map = models.ForeignKey(
        'TopicMap', related_name='item_identifiers_in_map')

    class Meta:
        app_label = 'tmapi'
        unique_together = (('address', 'containing_topic_map'),)

    def __init__ (self, *args, **kwargs):
        super(ItemIdentifier, self).__init__(*args, **kwargs)
        self.generate_forms(self.address)
        
    def save (self, *args, **kwargs):
        super(ItemIdentifier, self).save(*args, **kwargs)
        self.generate_forms(self.address)

    def get_construct (self):
        """Returns the `Construct` that this is an item identifier for.

        :rtype: `Construct`

        """
        construct = None
        construct_types = ('association', 'name', 'occurrence', 'role',
                           'topic', 'topic_map', 'variant')
        for construct_type in construct_types:
            manager = getattr(self, construct_type)
            try:
                construct = manager.get()
                break
            except:
                pass
        return construct

    def __unicode__ (self):
        return self.address
