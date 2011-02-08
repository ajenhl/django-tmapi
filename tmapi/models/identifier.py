from django.db import models


class Identifier (models.Model):

    # containing_topic_map may be null because when a TopicMap object
    # is first created (before it is saved) it has no database ID.
    containing_topic_map = models.ForeignKey(
        'TopicMap', related_name='identifiers_in_map', null=True)

    class Meta:
        app_label = 'tmapi'

    def get_construct (self):
        """Returns the `Construct` that this is an identifier for.

        :rtype: `Construct` or None

        """
        construct = None
        construct_types = ('association', 'name', 'occurrence', 'role',
                           'topic', 'topicmap', 'variant')
        for construct_type in construct_types:
            try:
                construct = getattr(self, construct_type)
            except:
                pass
        return construct

    def __unicode__ (self):
        return unicode(self.id)
