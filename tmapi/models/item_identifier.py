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

from .locator import LocatorBase


class ItemIdentifier (models.Model, LocatorBase):

    address = models.CharField(max_length=512)
    # Include a reference to the topic map of the construct this
    # identifier is associated with. This greatly eases checking for
    # duplicate identifiers within a topic map, given that there isn't
    # a single relationship back to the construct.
    containing_topic_map = models.ForeignKey(
        'TopicMap', related_name='item_identifiers_in_map')

    class Meta:
        app_label = 'tmapi'
        unique_together = (('address', 'containing_topic_map'),)

    def __init__ (self, *args, **kwargs):
        super(ItemIdentifier, self).__init__(*args, **kwargs)
        self.generate_forms(self.address)

    def save (self, *args, **kwargs):
        super(ItemIdentifier, self).save(*args, **kwargs)
        self.generate_forms(self.address)

    def get_construct (self):
        """Returns the `Construct` that this is an item identifier for.

        :rtype: `Construct` or None

        """
        construct = None
        construct_types = ('association', 'name', 'occurrence', 'role',
                           'topic', 'topicmap', 'variant')
        for construct_type in construct_types:
            manager = getattr(self, construct_type)
            try:
                construct = manager.get()
                break
            except:
                pass
        return construct

    def __str__ (self):
        return self.address
