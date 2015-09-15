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

from tmapi.constants import XSD_ANY_URI, XSD_FLOAT, XSD_INT, XSD_LONG, \
    XSD_STRING
from tmapi.exceptions import ModelConstraintException

from .locator import Locator
from .reifiable import Reifiable
from .scoped import Scoped


class DatatypeAware (Reifiable, Scoped):

    """Common base interface for `Occurrence`s and `Variant`s."""

    datatype = models.CharField(max_length=512, blank=True)
    value = models.TextField()

    class Meta:
        abstract = True
        app_label = 'tmapi'

    def get_datatype (self):
        """Returns the `Locator` identifying the datatype of the value.

        :rtype: `Locator`

        """
        return Locator(self.datatype)

    def get_value (self):
        """Returns the lexical representation of the value."""
        datatype = self.datatype
        value = self.value
        if datatype == XSD_FLOAT:
            value = float(value)
        elif datatype == XSD_INT:
            value = int(value)
        elif datatype == XSD_LONG:
            value = int(value)
        return value

    def locator_value (self):
        """Returns the `Locator` representation of the value.

        :rtype: `Locator`

        """
        if self.datatype == XSD_ANY_URI:
            return Locator(self.value)
        raise TypeError('Value is not a Locator')

    def set_value (self, value, datatype=None):
        """Sets the value.

        If `datatype` is None, the datatype will be implicitly set to
        match the type of `value`.

        :param value: the value
        :param datatype: optional datatype of `value`
        :type datatype: `Locator`

        """
        if value is None:
            raise ModelConstraintException(self, 'The value may not be None')
        if datatype is None:
            # This mapping is not comprehensive, since the mapping
            # (from section 1.10.3 at
            # http://cvs.zope.org/~checkout~/Packages/WebService/doc/WebService.html)
            # has the same Python type mapped to multiple XSD types.
            if isinstance(value, str):
                datatype = XSD_STRING
            elif isinstance(value, Locator):
                datatype = XSD_ANY_URI
                value = value.to_external_form()
            elif isinstance(value, float):
                datatype = XSD_FLOAT
            elif isinstance(value, int):
                datatype = XSD_INT
        else:
            datatype = datatype.to_external_form()
        self.value = value
        self.datatype = datatype
        self.save()
