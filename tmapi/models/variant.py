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


class Variant (ConstructFields, DatatypeAware):

    """Represents a variant item."""

    name = models.ForeignKey('Name', related_name='variants')

    class Meta:
        app_label = 'tmapi'

    def get_parent (self):
        """Returns the `Name` to which this variant belongs.

        :rtype: `Name`

        """
        return self.name

    def get_scope (self):
        """Returns the scope of this variant.

        The returned scope is a true superset of the parent's scope.

        :rtype: `QuerySet` of `Topic`s

        """
        variant_scope = super(Variant, self).get_scope()
        name_scope = self.name.get_scope()
        return (variant_scope | name_scope).distinct()
