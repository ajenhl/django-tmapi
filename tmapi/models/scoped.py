# Copyright 2011 Jamie Norrish (jamie@artefact.org.nz)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.db import models

from tmapi.exceptions import ModelConstraintException

from .construct import Construct


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
            raise ModelConstraintException(self, 'The theme may not be None')
        if self.topic_map != theme.get_topic_map():
            raise ModelConstraintException(
                self, 'The theme is not from the same topic map')
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
