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


class SubjectIdentifier (models.Model, LocatorBase):

    topic = models.ForeignKey('Topic', related_name='subject_identifiers')
    address = models.CharField(db_index=True, max_length=512)
    containing_topic_map = models.ForeignKey(
        'TopicMap', related_name='subject_identifiers_in_map')

    class Meta:
        app_label = 'tmapi'

    def __init__ (self, *args, **kwargs):
        super(SubjectIdentifier, self).__init__(*args, **kwargs)
        self.generate_forms(self.address)

    def save (self, *args, **kwargs):
        super(SubjectIdentifier, self).save(*args, **kwargs)
        self.generate_forms(self.address)

    def __str__ (self):
        return self.address
