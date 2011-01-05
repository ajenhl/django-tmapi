from django.db import models

from locator import LocatorBase


class ItemIdentifier (LocatorBase, models.Model):

    address = models.CharField(max_length=512)

    class Meta:
        app_label = 'tmapi'

    def __init__ (self, *args, **kwargs):
        super(ItemIdentifier, self).__init__(*args, **kwargs)
        self.generate_forms(self.address)
        
    def save (self, *args, **kwargs):
        super(ItemIdentifier, self).save(*args, **kwargs)
        self.generate_forms(self.address)
        
    def __unicode__ (self):
        return self.address
