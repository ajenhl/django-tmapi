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

from tmapi.constants import XSD_ANY_URI, XSD_STRING
from tmapi.exceptions import IllegalArgumentException
from tmapi.indices.index import Index
from tmapi.models import Locator, Name, Occurrence
from tmapi.models.variant import Variant


class LiteralIndex (Index):

    def get_names (self, value):
        """Retrieves the topic names in the topic map that have a
        value equal to `value`.

        The return value may be empty but must never be None.

        :param value: the value of the `Name`s to be returned
        :type value: string
        :rtype: `QuerySet` of `Name`s

        """
        if value is None:
            raise IllegalArgumentException('value must not be None')
        return Name.objects.filter(topic__topic_map=self.topic_map).filter(
            value=value)

    def get_occurrences (self, value, datatype=None):
        """Returns the `Occurrence`s in the topic map whose value
        property matches `value` (or if `value` is a `Locator`, the
        IRI represented by `value`).

        If `value` is a string and `datatype` is None, the
        `Occurrence`s' datatype property must be xsd:string.

        If `value` is a `Locator`, the `Occurrence`s' datatype
        property must be xsd:anyURI.

        If `datatype` is not None, the `Occurrence`s returned must be
        of that datatype.

        The return value may be empty but must never be None.

        :param value: the value of the `Occurrence`s to be returned
        :type value: string or `Locator`
        :param datatype: optional datatype of the `Occurrence`s to be returned
        :type datatype: `Locator`
        :rtype: `QuerySet` of `Occurrence`s

        """
        if value is None:
            raise IllegalArgumentException('value must not be None')
        if isinstance(value, Locator):
            value = value.get_reference()
            datatype = XSD_ANY_URI
        elif datatype is None:
            datatype = XSD_STRING
        else:
            datatype = datatype.get_reference()
        return Occurrence.objects.filter(topic__topic_map=self.topic_map).filter(value=value).filter(datatype=datatype)

    def get_variants (self, value, datatype=None):
        """Returns the `Variant`s in teh topic map whose value
        property matches `value` (or if `value` is a `Locator`, the
        IRI represented by `value`).

        If `value` is a string and `datatype` is None, the
        `Variant`s' datatype property must be xsd:string.

        If `value` is a `Locator`, the `Variant`s' datatype
        property must be xsd:anyURI.

        If `datatype` is not None, the `Variant`s returned must be
        of that datatype.

        The return value may be empty but must never be None.

        :param value: the value of the `Variant`s to be returned
        :type value: string or `Locator`
        :param datatype: optional datatype of the `Variant`s to be returned
        :type datatype: `Locator`
        :rtype: `QuerySet` of `Variant`s

        """
        if value is None:
            raise IllegalArgumentException('value must not be None')
        if isinstance(value, Locator):
            value = value.get_reference()
            datatype = XSD_ANY_URI
        elif datatype is None:
            datatype = XSD_STRING
        else:
            datatype = datatype.get_reference()
        return Variant.objects.filter(name__topic__topic_map=self.topic_map).filter(value=value).filter(datatype=datatype)
