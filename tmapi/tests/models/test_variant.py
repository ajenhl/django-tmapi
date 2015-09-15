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

"""Module containing tests for the `Variant` model.

Most if not all of these tests are ported from the public domain tests
that come with the TMAPI 2.0 distribution (http://www.tmapi.org/2.0/).

"""

from .datatype_aware_abstract_tests import DatatypeAwareAbstractTestCase


class VariantTest (DatatypeAwareAbstractTestCase):

    def get_datatype_aware (self):
        return self.create_variant()

    def test_parent (self):
        """Tests the parent/child relationship between name and variant."""
        parent = self.create_name()
        self.assertEqual(0, parent.get_variants().count(),
                         'Expected new name to be created with no variants')
        variant = parent.create_variant('Variant', [self.create_topic()])
        self.assertEqual(parent, variant.get_parent(),
                         'Unexpected variant parent after creation')
        self.assertEqual(1, parent.get_variants().count(),
                         'Expected variant list size to increment for name')
        self.assertTrue(variant in parent.get_variants(),
                        'Variant is not part of get_variants()')
        variant.remove()
        self.assertEqual(0, parent.get_variants().count(),
                         'Expected variant list size to decrement for name')

    def test_scope_property (self):
        """Tests if the variant's scope contains the name's scope."""
        name = self.create_name()
        self.assertEqual(0, name.get_scope().count())
        variant_theme = self.create_topic()
        variant = name.create_variant('Variant', [variant_theme])
        self.assertNotEqual(None, variant)
        self.assertEqual(1, variant.get_scope().count(),
                         'Unexpected variant\'s scope')
        self.assertTrue(variant_theme in variant.get_scope())
        name_theme = self.tm.create_topic()
        name.add_theme(name_theme)
        self.assertEqual(1, name.get_scope().count())
        self.assertTrue(name_theme in name.get_scope())
        self.assertEqual(2, variant.get_scope().count())
        self.assertTrue(name_theme in variant.get_scope())
        self.assertTrue(variant_theme in variant.get_scope())
        name.remove_theme(name_theme)
        self.assertEqual(0, name.get_scope().count())
        self.assertEqual(1, variant.get_scope().count(),
                         'Name\'s theme wasn\'t removed from the variant')
        self.assertTrue(variant_theme in variant.get_scope())

    def test_scope_property_2 (self):
        """Tests if a variant's theme equal to a name's theme stays
        even if the name's theme is removed."""
        theme = self.create_topic()
        variant_theme = self.create_topic()
        name = self.create_topic().create_name('Name', scope=[theme])
        self.assertEqual(1, name.get_scope().count())
        self.assertTrue(theme in name.get_scope())
        variant = name.create_variant('Variant', [theme, variant_theme])
        self.assertNotEqual(None, variant)
        self.assertEqual(2, variant.get_scope().count(),
                         'Unexpected variant\'s scope')
        self.assertTrue(theme in variant.get_scope())
        self.assertTrue(variant_theme in variant.get_scope())
        name.remove_theme(theme)
        self.assertEqual(0, name.get_scope().count())
        self.assertEqual(2, variant.get_scope().count(),
                         'Unexpected variant\'s scope after removal of ' +
                         '"theme" from name')
        self.assertTrue(theme in variant.get_scope())
        self.assertTrue(variant_theme in variant.get_scope())

    def test_scope_property_3 (self):
        """Tests if a variant's theme equal to a name's theme stays
        even if the variant's theme is removed."""
        theme = self.create_topic()
        variant_theme = self.create_topic()
        name = self.create_topic().create_name('Name', scope=[theme])
        self.assertEqual(1, name.get_scope().count())
        self.assertTrue(theme in name.get_scope())
        variant = name.create_variant('Variant', [theme, variant_theme])
        self.assertNotEqual(None, variant)
        self.assertEqual(2, variant.get_scope().count(),
                         'Unexpected variant\'s scope')
        self.assertTrue(theme in variant.get_scope())
        self.assertTrue(variant_theme in variant.get_scope())
        variant.remove_theme(theme)
        self.assertEqual(2, variant.get_scope().count(),
                         'The parent still contains "theme"')
        self.assertTrue(theme in variant.get_scope())
        self.assertTrue(variant_theme in variant.get_scope())
        name.remove_theme(theme)
        self.assertEqual(0, name.get_scope().count())
        self.assertEqual(1, variant.get_scope().count(),
                         '"theme" was removed from the name')
        self.assertFalse(theme in variant.get_scope())
        self.assertTrue(variant_theme in variant.get_scope())
