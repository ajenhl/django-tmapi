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

from .identifier import Identifier


class BaseConstructFields (models.Model):

    identifier = models.OneToOneField('Identifier', related_name='%(class)s',
                                      unique=True)
    # This is a many to many field because it links ItemIdenfitier
    # with many different models, thus precluding another type of
    # relationship. The constraint that an item identifier may be
    # associated with only a single construct within a given topic map
    # must be enforced elsewhere.
    item_identifiers = models.ManyToManyField('ItemIdentifier',
                                              related_name='%(class)s')

    class Meta:
        abstract = True
        app_label = 'tmapi'

    def save (self, *args, **kwargs):
        if not hasattr(self, 'identifier'):
            try:
                topic_map = self.topic_map
            except AttributeError:
                # This is a TopicMap instance being saved for the
                # first time, so it is not possible to set the
                # database ID yet.
                topic_map = None
            identifier = Identifier(containing_topic_map=topic_map)
            identifier.save()
            self.identifier = identifier
        super(BaseConstructFields, self).save(*args, **kwargs)
        if self.identifier.containing_topic_map is None:
            # In the case of a TopicMap instance being saved for the
            # first time, the containing_topic_map will not have been
            # set (see above), so set it once the TopicMap is saved.
            self.identifier.containing_topic_map = self
            self.identifier.save()


class ConstructFields (BaseConstructFields):

    topic_map = models.ForeignKey('TopicMap',
                                  related_name='%(class)s_constructs')

    class Meta:
        abstract = True
        app_label = 'tmapi'
