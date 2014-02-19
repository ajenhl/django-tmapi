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

"""Module caontaining tests against the `LiteralIndex` interface.

Most if not all of these tests are ported from the public domain tests
that come with the TMAPI 2.0 distribution (http://www.tmapi.org/2.0/).

"""

from tmapi.constants import XSD_ANY_URI, XSD_STRING
from tmapi.exceptions import IllegalArgumentException
from tmapi.indices.literal_index import LiteralIndex
from tmapi.tests.models.tmapi_test_case import TMAPITestCase


class LiteralIndexTest (TMAPITestCase):

    def setUp (self):
        super(LiteralIndexTest, self).setUp()
        self._index = self.tm.get_index(LiteralIndex)
        self._index.open()
        self._XSD_ANY_URI = self.create_locator(XSD_ANY_URI)
        self._XSD_STRING = self.create_locator(XSD_STRING)

    def tearDown (self):
        super(LiteralIndexTest, self).tearDown()
        self._index.close()

    def _update_index (self):
        if not self._index.is_auto_updated():
            self._index.reindex()
        
    def test_name (self):
        value = 'Value'
        value2 = 'Value2'
        self._update_index()
        self.assertEqual(0, self._index.get_names(value).count())
        name = self.create_topic().create_name(value)
        self._update_index()
        self.assertEqual(1, self._index.get_names(value).count())
        self.assertTrue(name in self._index.get_names(value))
        name.set_value(value2)
        self._update_index()
        self.assertEqual(0, self._index.get_names(value).count())
        self.assertEqual(1, self._index.get_names(value2).count())
        self.assertTrue(name in self._index.get_names(value2))
        name.remove()
        self._update_index()
        self.assertEqual(0, self._index.get_names(value).count())
        self.assertEqual(0, self._index.get_names(value2).count())

    def test_name_illegal_string (self):
        self.assertRaises(IllegalArgumentException, self._index.get_names,
                          None)

    def test_occurrence_string (self):
        value = 'Value'
        value2 = 'Value2'
        self._update_index()
        self.assertEqual(0, self._index.get_occurrences(value).count())
        self.assertEqual(0, self._index.get_occurrences(
                value, self._XSD_STRING).count())
        type = self.create_topic()
        occurrence = self.create_topic().create_occurrence(type, value)
        self._update_index()
        self.assertEqual(1, self._index.get_occurrences(value).count())
        self.assertTrue(occurrence in self._index.get_occurrences(value))
        self.assertEqual(1, self._index.get_occurrences(
                value, self._XSD_STRING).count())
        self.assertTrue(occurrence in self._index.get_occurrences(
                value, self._XSD_STRING))
        occurrence.set_value(value2)
        self._update_index()
        self.assertEqual(0, self._index.get_occurrences(value).count())
        self.assertEqual(0, self._index.get_occurrences(
                value, self._XSD_STRING).count())
        self.assertEqual(1, self._index.get_occurrences(value2).count())
        self.assertTrue(occurrence in self._index.get_occurrences(value2))
        self.assertEqual(1, self._index.get_occurrences(
                value2, self._XSD_STRING).count())
        self.assertTrue(occurrence in self._index.get_occurrences(
                value2, self._XSD_STRING))
        occurrence.remove()
        self._update_index()
        self.assertEqual(0, self._index.get_occurrences(value).count())
        self.assertEqual(0, self._index.get_occurrences(
                value, self._XSD_STRING).count())
        self.assertEqual(0, self._index.get_occurrences(value2).count())
        self.assertEqual(0, self._index.get_occurrences(
                value2, self._XSD_STRING).count())

    def test_occurrence_uri (self):
        value = self.create_locator('http://www.example.org/1')
        value2 = self.create_locator('http://www.example.org/2')
        self._update_index()
        self.assertEqual(0, self._index.get_occurrences(value).count())
        self.assertEqual(0, self._index.get_occurrences(
                value.get_reference(), self._XSD_ANY_URI).count())
        type = self.create_topic()
        occurrence = self.create_topic().create_occurrence(type, value)
        self._update_index()
        self.assertEqual(1, self._index.get_occurrences(value).count())
        self.assertTrue(occurrence in self._index.get_occurrences(value))
        self.assertEqual(1, self._index.get_occurrences(
                value.get_reference(), self._XSD_ANY_URI).count())
        self.assertTrue(occurrence in self._index.get_occurrences(
                value.get_reference(), self._XSD_ANY_URI))
        occurrence.set_value(value2)
        self._update_index()
        self.assertEqual(0, self._index.get_occurrences(value).count())
        self.assertEqual(0, self._index.get_occurrences(
                value.get_reference(), self._XSD_ANY_URI).count())
        self.assertEqual(1, self._index.get_occurrences(value2).count())
        self.assertTrue(occurrence in self._index.get_occurrences(value2))
        self.assertEqual(1, self._index.get_occurrences(
                value2.get_reference(), self._XSD_ANY_URI).count())
        self.assertTrue(occurrence in self._index.get_occurrences(
                value2.get_reference(), self._XSD_ANY_URI))
        occurrence.remove()
        self._update_index()
        self.assertEqual(0, self._index.get_occurrences(value).count())
        self.assertEqual(0, self._index.get_occurrences(
                value.get_reference(), self._XSD_ANY_URI).count())
        self.assertEqual(0, self._index.get_occurrences(value2).count())
        self.assertEqual(0, self._index.get_occurrences(
                value2.get_reference(), self._XSD_ANY_URI).count())

    def test_occurrence_explicit_datatype (self):
        value = 'http://www.example.org/1'
        value2 = 'http://www.example.org/2'
        datatype = self.create_locator('http://www.example.org/datatype')
        self._update_index()
        self.assertEqual(0, self._index.get_occurrences(value).count())
        self.assertEqual(0, self._index.get_occurrences(
                value, datatype).count())
        type = self.create_topic()
        occurrence = self.create_topic().create_occurrence(
            type, value, datatype=datatype)
        self._update_index()
        self.assertEqual(0, self._index.get_occurrences(value).count())
        self.assertEqual(1, self._index.get_occurrences(
                value, datatype).count())
        self.assertTrue(occurrence in self._index.get_occurrences(
                value, datatype))
        occurrence.set_value(value2, datatype)
        self._update_index()
        self.assertEqual(0, self._index.get_occurrences(value).count())
        self.assertEqual(0, self._index.get_occurrences(
                value, datatype).count())
        self.assertEqual(0, self._index.get_occurrences(value2).count())
        self.assertEqual(1, self._index.get_occurrences(
                value2, datatype).count())
        self.assertTrue(occurrence in self._index.get_occurrences(
                value2, datatype))
        occurrence.remove()
        self._update_index()
        self.assertEqual(0, self._index.get_occurrences(value2).count())
        self.assertEqual(0, self._index.get_occurrences(
                value2, datatype).count())

    def test_occurrence_illegal_string (self):
        self.assertRaises(IllegalArgumentException, self._index.get_occurrences,
                          None)

    def test_occurrence_illegal_uri (self):
        self.assertRaises(IllegalArgumentException, self._index.get_occurrences,
                          None)

    def test_occurrence_illegal_datatype (self):
        # This test is not applicable to this implementation.
        pass

    def test_variant_string (self):
        value = 'Value'
        value2 = 'Value2'
        self._update_index()
        self.assertEqual(0, self._index.get_variants(value).count())
        self.assertEqual(0, self._index.get_variants(
                value, self._XSD_STRING).count())
        theme = self.create_topic()
        variant = self.create_name().create_variant(value, theme)
        self._update_index()
        self.assertEqual(1, self._index.get_variants(value).count())
        self.assertTrue(variant in self._index.get_variants(value))
        self.assertEqual(1, self._index.get_variants(
                value, self._XSD_STRING).count())
        self.assertTrue(variant in self._index.get_variants(
                value, self._XSD_STRING))
        variant.set_value(value2)
        self._update_index()
        self.assertEqual(0, self._index.get_variants(value).count())
        self.assertEqual(0, self._index.get_variants(
                value, self._XSD_STRING).count())
        self.assertEqual(1, self._index.get_variants(value2).count())
        self.assertTrue(variant in self._index.get_variants(value2))
        self.assertEqual(1, self._index.get_variants(
                value2, self._XSD_STRING).count())
        self.assertTrue(variant in self._index.get_variants(
                value2, self._XSD_STRING))
        variant.remove()
        self._update_index()
        self.assertEqual(0, self._index.get_variants(value).count())
        self.assertEqual(0, self._index.get_variants(
                value, self._XSD_STRING).count())
        self.assertEqual(0, self._index.get_variants(value2).count())
        self.assertEqual(0, self._index.get_variants(
                value2, self._XSD_STRING).count())

    def test_variant_uri (self):
        value = self.create_locator('http://www.example.org/1')
        value2 = self.create_locator('http://www.example.org/2')
        self._update_index()
        self.assertEqual(0, self._index.get_variants(value).count())
        self.assertEqual(0, self._index.get_variants(
                value.get_reference(), self._XSD_ANY_URI).count())
        theme = self.create_topic()
        variant = self.create_name().create_variant(value, theme)
        self._update_index()
        self.assertEqual(1, self._index.get_variants(value).count())
        self.assertTrue(variant in self._index.get_variants(value))
        self.assertEqual(1, self._index.get_variants(
                value.get_reference(), self._XSD_ANY_URI).count())
        self.assertTrue(variant in self._index.get_variants(
                value.get_reference(), self._XSD_ANY_URI))
        variant.set_value(value2)
        self._update_index()
        self.assertEqual(0, self._index.get_variants(value).count())
        self.assertEqual(0, self._index.get_variants(
                value.get_reference(), self._XSD_ANY_URI).count())
        self.assertEqual(1, self._index.get_variants(value2).count())
        self.assertTrue(variant in self._index.get_variants(value2))
        self.assertEqual(1, self._index.get_variants(
                value2.get_reference(), self._XSD_ANY_URI).count())
        self.assertTrue(variant in self._index.get_variants(
                value2.get_reference(), self._XSD_ANY_URI))
        variant.remove()
        self._update_index()
        self.assertEqual(0, self._index.get_variants(value).count())
        self.assertEqual(0, self._index.get_variants(
                value.get_reference(), self._XSD_ANY_URI).count())
        self.assertEqual(0, self._index.get_variants(value2).count())
        self.assertEqual(0, self._index.get_variants(
                value2.get_reference(), self._XSD_ANY_URI).count())

    def test_variant_explicit_datatype (self):
        value = 'http://www.example.org/1'
        value2 = 'http://www.example.org/2'
        datatype = self.create_locator('http://www.example.org/datatype')
        self._update_index()
        self.assertEqual(0, self._index.get_variants(value).count())
        self.assertEqual(0, self._index.get_variants(value, datatype).count())
        theme = self.create_topic()
        variant = self.create_name().create_variant(value, theme, datatype)
        self._update_index()
        self.assertEqual(0, self._index.get_variants(value).count())
        self.assertEqual(1, self._index.get_variants(value, datatype).count())
        self.assertTrue(variant in self._index.get_variants(value, datatype))
        variant.set_value(value2, datatype)
        self._update_index()
        self.assertEqual(0, self._index.get_variants(value).count())
        self.assertEqual(0, self._index.get_variants(value, datatype).count())
        self.assertEqual(0, self._index.get_variants(value2).count())
        self.assertEqual(1, self._index.get_variants(value2, datatype).count())
        self.assertTrue(variant in self._index.get_variants(value2, datatype))
        variant.remove()
        self._update_index()
        self.assertEqual(0, self._index.get_variants(value2).count())
        self.assertEqual(0, self._index.get_variants(value2, datatype).count())

    def test_variant_illegal_string (self):
        # This test is not applicable to this implementation.
        self.assertRaises(IllegalArgumentException, self._index.get_variants,
                          None)

    def test_variant_illegal_uri (self):
        self.assertRaises(IllegalArgumentException, self._index.get_variants,
                          None)

    def test_variant_illegal_datatype (self):
        # This test is not applicable to this implementation.
        pass
