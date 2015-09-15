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

import unicodedata
import urllib.parse

from tmapi.exceptions import MalformedIRIException


class LocatorBase:

    """Immutable representation of an IRI."""

    def generate_forms (self, reference):
        self._reference = self.unnormalise(reference)
        self._external = self.normalise(self._reference)

    def get_reference (self):
        """Returns a lexical representation of the IRI.

        :rtype: String

        """
        return self._reference

    def resolve (self, reference):
        """Resolves the `reference` against this locator.

        The returned `Locator` represents an absolute IRI.

        :param reference: the reference which should be resolved
          against this locator
        :type reference: string
        :rtype: `Locator`

        """
        return Locator(urllib.parse.urljoin(self._external, reference))

    def to_external_form (self):
        """Returns the external form of the IRI.

        Any special character will be escaped using the escaping
        conventions of RFC 3987.

        :rtype: String

        """
        return self._external

    def normalise (self, reference):
        parts = list(urllib.parse.urlsplit(str(reference)))
        if not parts[0]:
            raise MalformedIRIException('IRI has no protocol')
        parts[2] = urllib.parse.quote(parts[2], '/;')
        url = urllib.parse.urlunsplit(parts)
        if reference.endswith('?'):
            url = url + '?'
        elif reference.endswith('#'):
            url = url + '#'
        return url

    def unnormalise (self, reference):
        reference = urllib.parse.unquote(str(reference))
        return unicodedata.normalize('NFC', reference)

    def __eq__ (self, other):
        if not isinstance(other, LocatorBase):
            return False
        return self.to_external_form() == other.to_external_form()

    def __ne__ (self, other):
        return not(self.__eq__(other))


class Locator (LocatorBase):

    def __init__ (self, reference):
        self.generate_forms(reference)

    def __str__ (self):
        return self._reference
