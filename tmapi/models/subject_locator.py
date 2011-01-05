from django.db import models

from locator import LocatorBase


class SubjectLocator (LocatorBase, models.Model):

    topic = models.ForeignKey('Topic', related_name='subject_locators')
    address = models.CharField(max_length=512)

    class Meta:
        app_label = 'tmapi'

    def __init__ (self, *args, **kwargs):
        super(SubjectLocator, self).__init__(*args, **kwargs)
        self.generate_forms(self.address)
        
    def save (self, *args, **kwargs):
        super(SubjectLocator, self).save(*args, **kwargs)
        self.generate_forms(self.address)
        
    def __unicode__ (self):
        return self.address
