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

from .construct_fields import ConstructFields
from .datatype_aware import DatatypeAware
from .typed import Typed


class Occurrence (ConstructFields, DatatypeAware, Typed):

    topic = models.ForeignKey('Topic', related_name='occurrences')

    class Meta:
        app_label = 'tmapi'

    def get_parent (self, proxy=None):
        """Returns the `Topic` to which this occurrence belongs.

        :param proxy: Django proxy model
        :type proxy: class
        :rtype: `Topic`

        """
        if proxy is None:
            topic = self.topic
        else:
            topic = proxy.objects.get(pk=self.topic.id)
        return topic
