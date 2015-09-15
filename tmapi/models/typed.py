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


class Typed (Construct, models.Model):

    """Indicates that a Topic Maps construct is typed. `Association`s,
    `Role`s, `Occurrence`s, and `Name`s are typed."""

    type = models.ForeignKey('Topic', related_name='typed_%(class)ss')

    class Meta:
        abstract = True
        app_label = 'tmapi'

    def get_type (self, proxy=None):
        """Returns the type of this construct.

        :param proxy: Django proxy model
        :type proxy: class
        :rtype: the `Topic` that represents the type

        """
        construct_type = self.type
        if proxy is not None:
            construct_type = proxy.objects.get(pk=construct_type.pk)
        return construct_type

    def set_type (self, construct_type):
        """Sets the type of this construct. Any previous type is overridden.

        :param construct_type: the `Topic` that should define the
          nature of this construct
        :type construct_type: `Topic`

        """
        if construct_type is None:
            raise ModelConstraintException(self, 'The type may not be None')
        if self.topic_map != construct_type.topic_map:
            raise ModelConstraintException(
                self, 'The type is not from the same topic map')
        self.type = construct_type
        self.save()
