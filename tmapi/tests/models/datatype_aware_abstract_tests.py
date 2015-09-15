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

"""Module containing abstract test against the `DatatypeAware` interface.

Most if not all of these tests are ported from the public domain tests
that come with the TMAPI 2.0 distribution (http://www.tmapi.org/2.0/).

"""

from tmapi.exceptions import ModelConstraintException

from .tmapi_test_case import TMAPITestCase


class DatatypeAwareAbstractTestCase (TMAPITestCase):

    _XSD = 'http://www.w3.org/2001/XMLSchema#'
    _XSD_ANY_URI = _XSD + 'anyURI'
    _XSD_FLOAT = _XSD + 'float'
    _XSD_INT = _XSD + 'int'
    _XSD_LONG = _XSD + 'long'
    _XSD_STRING = _XSD + 'string'

    def get_datatype_aware (self):
        raise NotImplementedError

    def setUp (self):
        super(DatatypeAwareAbstractTestCase, self).setUp()
        self.tm = self.tms.create_topic_map('http://www.example.org/tm/')
        self._xsd_any_uri = self.tms.create_locator(self._XSD_ANY_URI)
        self._xsd_float = self.tms.create_locator(self._XSD_FLOAT)
        self._xsd_int = self.tms.create_locator(self._XSD_INT)
        self._xsd_long = self.tms.create_locator(self._XSD_LONG)
        self._xsd_string = self.tms.create_locator(self._XSD_STRING)

    def test_float (self):
        try:
            dt = self.get_datatype_aware()
        except NotImplementedError:
            return
        value = 1.3
        dt.set_value(value)
        self.assertEqual(value, dt.get_value())
        self.assertEqual(self._xsd_float, dt.get_datatype())

    def test_float_explicit (self):
        try:
            dt = self.get_datatype_aware()
        except NotImplementedError:
            return
        value = 1.3
        dt.set_value(value, self._xsd_float)
        self.assertEqual(value, dt.get_value())
        self.assertEqual(self._xsd_float, dt.get_datatype())

    def test_int (self):
        try:
            dt = self.get_datatype_aware()
        except NotImplementedError:
            return
        value = 1
        dt.set_value(value)
        self.assertEqual(value, dt.get_value())
        self.assertEqual(self._xsd_int, dt.get_datatype())

    def test_int_explicit (self):
        try:
            dt = self.get_datatype_aware()
        except NotImplementedError:
            return
        value = 1
        dt.set_value(value, self._xsd_int)
        self.assertEqual(value, dt.get_value())
        self.assertEqual(self._xsd_int, dt.get_datatype())

    def test_long (self):
        # This test is not applicable to this implementation.
        pass

    def test_long_explicit (self):
        # This test is not applicable to this implementation.
        pass

    def test_string (self):
        try:
            dt = self.get_datatype_aware()
        except NotImplementedError:
            return
        value = 'a string'
        dt.set_value(value)
        self.assertEqual(value, dt.get_value())
        self.assertEqual(self._xsd_string, dt.get_datatype())

    def test_string_explicit (self):
        try:
            dt = self.get_datatype_aware()
        except NotImplementedError:
            return
        value = 'a string'
        dt.set_value(value, self._xsd_string)
        self.assertEqual(value, dt.get_value())
        self.assertEqual(self._xsd_string, dt.get_datatype())

    def test_uri (self):
        try:
            dt = self.get_datatype_aware()
        except NotImplementedError:
            return
        iri = 'http://www.example.org/'
        value = self.tm.create_locator(iri)
        dt.set_value(value)
        self.assertEqual(iri, dt.get_value())
        self.assertEqual(self._xsd_any_uri, dt.get_datatype())
        self.assertEqual(value, dt.locator_value())

    def test_uri_explicit (self):
        try:
            dt = self.get_datatype_aware()
        except NotImplementedError:
            return
        iri = 'http://www.example.org/'
        value = self.tm.create_locator(iri)
        dt.set_value(iri, self._xsd_any_uri)
        self.assertEqual(iri, dt.get_value())
        self.assertEqual(self._xsd_any_uri, dt.get_datatype())
        self.assertEqual(value, dt.locator_value())

    def test_user_datatype (self):
        try:
            dt = self.get_datatype_aware()
        except NotImplementedError:
            return
        datatype = self.tm.create_locator('http://www.example.org/datatype')
        value = 'Value'
        dt.set_value(value, datatype)
        self.assertEqual(datatype, dt.get_datatype())
        self.assertEqual(value, dt.get_value())

    def test_illegal_datatype (self):
        # This test is not applicable in Python.
        pass

    def test_illegal_string_value (self):
        try:
            dt = self.get_datatype_aware()
        except NotImplementedError:
            return
        self.assertRaises(ModelConstraintException, dt.set_value, None)

    def test_illegal_string_value_explicit (self):
        try:
            dt = self.get_datatype_aware()
        except NotImplementedError:
            return
        self.assertRaises(ModelConstraintException, dt.set_value, None,
                          self._xsd_string)
