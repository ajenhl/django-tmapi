from django.db import models


class ConstructFields (models.Model):

    # This is a many to many field because it links ItemIdenfitier
    # with many different models, thus precluding another type of
    # relationship. The constraint that an item identifier may be
    # associated with only a single construct within a given topic map
    # must be enforced elsewhere.
    item_identifiers = models.ManyToManyField('ItemIdentifier',
                                              related_name='%(class)s')
    topic_map = models.ForeignKey('TopicMap',
                                  related_name='%(class)s_constructs')

    class Meta:
        abstract = True
        app_label = 'tmapi'
