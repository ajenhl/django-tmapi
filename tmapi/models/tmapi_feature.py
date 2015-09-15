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


class TMAPIFeature (models.Model):

    topic_map_system = models.ForeignKey('TopicMapSystem',
                                         related_name='features')
    feature_string = models.CharField(max_length=512)
    value = models.BooleanField()

    class Meta:
        app_label = 'tmapi'
        unique_together = ('topic_map_system', 'feature_string')
