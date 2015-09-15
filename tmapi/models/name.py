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

from tmapi.constants import XSD_ANY_URI, XSD_STRING
from tmapi.exceptions import ModelConstraintException

from .construct_fields import ConstructFields
from .locator import Locator
from .reifiable import Reifiable
from .scoped import Scoped
from .typed import Typed
from .variant import Variant


class Name (ConstructFields, Reifiable, Scoped, Typed):

    """Represents a topic name item."""

    topic = models.ForeignKey('Topic', related_name='names')
    value = models.TextField()

    class Meta:
        app_label = 'tmapi'

    def create_variant (self, value, scope, datatype=None):
        """Creates a `Variant` of this topic name with the specified
        string `value` and `scope`.

        If `datatype` is None, the newly created `Variant` will have
        the datatype xsd:string.

        The newly created `Variant` will contain all themes from the
        parent name and the themes specified in `scope`.

        :param value: the string value or locator which represents an IRI
        :type value: string or `Locator`
        :param scope: list of themes
        :type scope: list of `Topic`s
        :rtype: `Variant`

        """
        if value is None:
            raise ModelConstraintException(self, 'The value may not be None')
        if not scope:
            raise ModelConstraintException(self, 'The scope may not be None')
        if type(scope) not in (type([]), type(())):
            scope = [scope]
        if scope == list(self.get_scope()):
            raise ModelConstraintException(
                self, 'The variant would be in the same scope as the parent')
        if datatype is None:
            if isinstance(value, Locator):
                datatype = Locator(XSD_ANY_URI)
            elif isinstance(value, str):
                datatype = Locator(XSD_STRING)
        if isinstance(value, Locator):
            value = value.to_external_form()
        variant = Variant(name=self, datatype=datatype.to_external_form(),
                          value=value, topic_map=self.topic_map)
        variant.save()
        for theme in scope:
            variant.scope.add(theme)
        return variant

    def get_parent (self, proxy=None):
        """Returns the `Topic` to which this name belongs.

        :param proxy: Django proxy model class
        :type proxy: class
        :rtype: `Topic` or `proxy`

        """
        parent = self.topic
        if proxy is not None:
            parent = proxy.objects.get(pk=parent.id)
        return parent

    def get_value (self):
        """Returns the value of this name."""
        return self.value

    def get_variants (self):
        """Returns the variants defined for this name."""
        return self.variants.all()

    def set_value (self, value):
        """Sets the value of this name. The previous value is overridden."""
        if value is None:
            raise ModelConstraintException(self, 'The value may not be None')
        self.value = value
        self.save()

    def __str__ (self):
        return self.value
