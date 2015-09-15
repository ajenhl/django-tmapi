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

    def __str__ (self):
        return self.id
