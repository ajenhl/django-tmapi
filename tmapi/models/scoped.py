from django.db import models

from tmapi.exceptions import ModelConstraintException

from construct import Construct


class Scoped (Construct, models.Model):

    """Indicates that a statement (Topic Maps construct) has a
    scope. `Association`s, `Occurrence`s, `Name`s, and `Variant`s are
    scoped."""

    scope = models.ManyToManyField('Topic', related_name='scoped_%(class)ss')

    class Meta:
        abstract = True
        app_label = 'tmapi'

    def add_theme (self, theme):
        """Adds a topic to the scope.

        :param theme: the topic which should be added to the scope
        :type theme: `Topic`

        """
        if theme is None:
            raise ModelConstraintException
        self.scope.add(theme)
        
    def get_scope (self):
        """Returns the topics which define the scope. An empty set
        represents the unconstrained scope.

        :rtype: `QuerySet` of `Topic`s
        
        """
        return self.scope.all()

    def remove_theme (self, theme):
        """Removes a topic from the scope.

        :param theme: the topic which should be removed from the scope
        :type theme: `Topic`

        """
        self.scope.remove(theme)
