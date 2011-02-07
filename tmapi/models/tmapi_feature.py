from django.db import models

class TMAPIFeature (models.Model):

    topic_map_system = models.ForeignKey('TopicMapSystem',
                                         related_name='features')
    feature_string = models.CharField(max_length=512)
    value = models.BooleanField()

    class Meta:
        app_label = 'tmapi'
        unique_together = ('topic_map_system', 'feature_string')
