from django.db import models


class ConstructFields (models.Model):

    item_identifiers = models.ManyToManyField('ItemIdentifier',
                                              related_name='%(class)ss')
    topic_map = models.ForeignKey('TopicMap',
                                  related_name='%(class)s_constructs')

    class Meta:
        abstract = True
        app_label = 'tmapi'
