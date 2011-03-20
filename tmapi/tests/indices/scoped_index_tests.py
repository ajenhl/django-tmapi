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

"""Module containing tests against the `ScopedIndex` interface.

Most if not all of these tests are ported from the public domain tests
that come with the TMAPI 2.0 distribution (http://www.tmapi.org/2.0/).

"""

from tmapi.exceptions import IllegalArgumentException
from tmapi.indices.scoped_index import ScopedIndex
from tmapi.tests.models.tmapi_test_case import TMAPITestCase


class ScopedIndexTest (TMAPITestCase):

    def setUp (self):
        super(ScopedIndexTest, self).setUp()
        self._index = self.tm.get_index(ScopedIndex)
        self._index.open()

    def tearDown (self):
        super(ScopedIndexTest, self).tearDown()
        self._index.close()

    def _update_index (self):
        if not self._index.is_auto_updated():
            self._index.reindex()

    def test_association (self):
        theme = self.create_topic()
        self._update_index()
        self.assertEqual(0, self._index.get_associations().count())
        self.assertEqual(0, self._index.get_associations(theme).count())
        self.assertEqual(0, self._index.get_association_themes().count())
        scoped = self.create_association()
        self.assertEqual(0, scoped.get_scope().count())
        self._update_index()
        self.assertEqual(1, self._index.get_associations().count())
        self.assertTrue(scoped in self._index.get_associations())
        self.assertFalse(theme in self._index.get_association_themes())
        scoped.add_theme(theme)
        self._update_index()
        self.assertEqual(0, self._index.get_associations().count())
        self.assertFalse(scoped in self._index.get_associations())
        self.assertNotEqual(0, self._index.get_association_themes().count())
        self.assertEqual(1, self._index.get_association_themes().count())
        self.assertTrue(scoped in self._index.get_associations(theme))
        self.assertTrue(theme in self._index.get_association_themes())
        scoped.remove()
        self._update_index()
        self.assertEqual(0, self._index.get_associations().count())
        self.assertFalse(scoped in self._index.get_associations())
        self.assertFalse(theme in self._index.get_association_themes())

    def test_association_match_all (self):
        theme = self.create_topic()
        theme2 = self.create_topic()
        unused_theme = self.create_topic()
        self._update_index()
        self.assertEqual(0, self._index.get_associations().count())
        self.assertEqual(0, self._index.get_associations(theme).count())
        self.assertEqual(0, self._index.get_association_themes().count())
        scoped = self.create_association()
        self.assertEqual(0, scoped.get_scope().count())
        self._update_index()
        self.assertEqual(1, self._index.get_associations().count())
        self.assertTrue(scoped in self._index.get_associations())
        self.assertFalse(theme in self._index.get_association_themes())
        scoped.add_theme(theme)
        self._update_index()
        self.assertEqual(1, self._index.get_association_themes().count())
        self.assertTrue(scoped in self._index.get_associations([theme], True))
        self.assertTrue(scoped in self._index.get_associations([theme], False))
        scoped.add_theme(theme2)
        self._update_index()
        self.assertEqual(2, self._index.get_association_themes().count())
        self.assertTrue(scoped in self._index.get_associations([theme], True))
        self.assertTrue(scoped in self._index.get_associations([theme], False))
        self.assertTrue(scoped in self._index.get_associations([theme2], True))
        self.assertTrue(scoped in self._index.get_associations([theme2], False))
        self.assertTrue(scoped in self._index.get_associations(
                [theme, theme2], False))
        self.assertTrue(scoped in self._index.get_associations(
                [theme, theme2], True))
        self.assertTrue(scoped in self._index.get_associations(
                [theme, unused_theme], False))
        self.assertTrue(scoped in self._index.get_associations(
                [theme2, unused_theme], False))
        self.assertFalse(scoped in self._index.get_associations(
                [theme, unused_theme], True))
        self.assertFalse(scoped in self._index.get_associations(
                [theme2, unused_theme], True))

    def test_association_match_all_illegal (self):
        self.assertRaises(IllegalArgumentException,
                          self._index.get_associations, None, True)
                                                               
    def test_occurrence (self):
        theme = self.create_topic()
        self._update_index()
        self.assertEqual(0, self._index.get_occurrences().count())
        self.assertEqual(0, self._index.get_occurrences(theme).count())
        self.assertEqual(0, self._index.get_occurrence_themes().count())
        scoped = self.create_occurrence()
        self.assertEqual(0, scoped.get_scope().count())
        self._update_index()
        self.assertEqual(1, self._index.get_occurrences().count())
        self.assertTrue(scoped in self._index.get_occurrences())
        self.assertFalse(theme in self._index.get_occurrence_themes())
        scoped.add_theme(theme)
        self._update_index()
        self.assertEqual(0, self._index.get_occurrences().count())
        self.assertFalse(scoped in self._index.get_occurrences())
        self.assertNotEqual(0, self._index.get_occurrence_themes().count())
        self.assertEqual(1, self._index.get_occurrence_themes().count())
        self.assertTrue(scoped in self._index.get_occurrences(theme))
        self.assertTrue(theme in self._index.get_occurrence_themes())
        scoped.remove()
        self._update_index()
        self.assertEqual(0, self._index.get_occurrences().count())
        self.assertFalse(scoped in self._index.get_occurrences())
        self.assertFalse(theme in self._index.get_occurrence_themes())

    def test_occurrence_match_all (self):
        theme = self.create_topic()
        theme2 = self.create_topic()
        unused_theme = self.create_topic()
        self._update_index()
        self.assertEqual(0, self._index.get_occurrences().count())
        self.assertEqual(0, self._index.get_occurrences(theme).count())
        self.assertEqual(0, self._index.get_occurrence_themes().count())
        scoped = self.create_occurrence()
        self.assertEqual(0, scoped.get_scope().count())
        self._update_index()
        self.assertEqual(1, self._index.get_occurrences().count())
        self.assertTrue(scoped in self._index.get_occurrences())
        self.assertFalse(theme in self._index.get_occurrence_themes())
        scoped.add_theme(theme)
        self._update_index()
        self.assertEqual(1, self._index.get_occurrence_themes().count())
        self.assertTrue(scoped in self._index.get_occurrences([theme], True))
        self.assertTrue(scoped in self._index.get_occurrences([theme], False))
        scoped.add_theme(theme2)
        self._update_index()
        self.assertEqual(2, self._index.get_occurrence_themes().count())
        self.assertTrue(scoped in self._index.get_occurrences([theme], True))
        self.assertTrue(scoped in self._index.get_occurrences([theme], False))
        self.assertTrue(scoped in self._index.get_occurrences([theme2], True))
        self.assertTrue(scoped in self._index.get_occurrences([theme2], False))
        self.assertTrue(scoped in self._index.get_occurrences(
                [theme, theme2], False))
        self.assertTrue(scoped in self._index.get_occurrences(
                [theme, theme2], True))
        self.assertTrue(scoped in self._index.get_occurrences(
                [theme, unused_theme], False))
        self.assertTrue(scoped in self._index.get_occurrences(
                [theme2, unused_theme], False))
        self.assertFalse(scoped in self._index.get_occurrences(
                [theme, unused_theme], True))
        self.assertFalse(scoped in self._index.get_occurrences(
                [theme2, unused_theme], True))

    def test_occurrence_match_all_illegal (self):
        self.assertRaises(IllegalArgumentException, self._index.get_occurrences,
                          None, True)

    def test_name (self):
        theme = self.create_topic()
        self._update_index()
        self.assertEqual(0, self._index.get_names().count())
        self.assertEqual(0, self._index.get_names(theme).count())
        self.assertEqual(0, self._index.get_name_themes().count())
        scoped = self.create_name()
        self.assertEqual(0, scoped.get_scope().count())
        self._update_index()
        self.assertEqual(1, self._index.get_names().count())
        self.assertTrue(scoped in self._index.get_names())
        self.assertFalse(theme in self._index.get_name_themes())
        scoped.add_theme(theme)
        self._update_index()
        self.assertEqual(0, self._index.get_names().count())
        self.assertFalse(scoped in self._index.get_names())
        self.assertNotEqual(0, self._index.get_name_themes().count())
        self.assertEqual(1, self._index.get_name_themes().count())
        self.assertTrue(scoped in self._index.get_names(theme))
        self.assertTrue(theme in self._index.get_name_themes())
        scoped.remove()
        self._update_index()
        self.assertEqual(0, self._index.get_names().count())
        self.assertFalse(scoped in self._index.get_names())
        self.assertFalse(theme in self._index.get_name_themes())

    def test_name_2 (self):
        theme = self.create_topic()
        self._update_index()
        self.assertEqual(0, self._index.get_names().count())
        self.assertEqual(0, self._index.get_names(theme).count())
        self.assertEqual(0, self._index.get_name_themes().count())
        scoped = self.create_topic().create_name('tinyTiM', scope=theme)
        self.assertEqual(1, scoped.get_scope().count())
        self._update_index()
        self.assertEqual(0, self._index.get_names().count())
        self.assertFalse(scoped in self._index.get_names())
        self.assertNotEqual(0, self._index.get_name_themes().count())
        self.assertEqual(1, self._index.get_name_themes().count())
        self.assertTrue(scoped in self._index.get_names(theme))
        self.assertTrue(theme in self._index.get_name_themes())
        scoped.remove()
        self._update_index()
        self.assertEqual(0, self._index.get_names().count())
        self.assertFalse(scoped in self._index.get_names())
        self.assertEqual(0, self._index.get_names(theme).count())
        self.assertFalse(theme in self._index.get_name_themes())

    def test_name_match_all (self):
        theme = self.create_topic()
        theme2 = self.create_topic()
        unused_theme = self.create_topic()
        self._update_index()
        self.assertEqual(0, self._index.get_names().count())
        self.assertEqual(0, self._index.get_names(theme).count())
        self.assertEqual(0, self._index.get_name_themes().count())
        scoped = self.create_name()
        self.assertEqual(0, scoped.get_scope().count())
        self._update_index()
        self.assertEqual(1, self._index.get_names().count())
        self.assertTrue(scoped in self._index.get_names())
        self.assertFalse(theme in self._index.get_name_themes())
        scoped.add_theme(theme)
        self._update_index()
        self.assertEqual(1, self._index.get_name_themes().count())
        self.assertTrue(scoped in self._index.get_names([theme], True))
        self.assertTrue(scoped in self._index.get_names([theme], False))
        scoped.add_theme(theme2)
        self._update_index()
        self.assertEqual(2, self._index.get_name_themes().count())
        self.assertTrue(scoped in self._index.get_names([theme], True))
        self.assertTrue(scoped in self._index.get_names([theme], False))
        self.assertTrue(scoped in self._index.get_names([theme2], True))
        self.assertTrue(scoped in self._index.get_names([theme2], False))
        self.assertTrue(scoped in self._index.get_names([theme, theme2], True))
        self.assertTrue(scoped in self._index.get_names([theme, theme2], False))
        self.assertTrue(scoped in self._index.get_names(
                [theme, unused_theme], False))
        self.assertTrue(scoped in self._index.get_names(
                [theme2, unused_theme], False))
        self.assertFalse(scoped in self._index.get_names(
                [theme, unused_theme], True))
        self.assertFalse(scoped in self._index.get_names(
                [theme2, unused_theme], True))

    def test_name_match_all_illegal (self):
        self.assertRaises(IllegalArgumentException, self._index.get_names,
                           None, True)

    def test_variant_illegal (self):
        self.assertRaises(IllegalArgumentException, self._index.get_variants,
                          None)

    def test_variant_match_all_illegal (self):
        self.assertRaises(IllegalArgumentException, self._index.get_variants,
                          None, True)

    def test_variant (self):
        theme = self.create_topic()
        theme2 = self.create_topic()
        self._update_index()
        self.assertEqual(0, self._index.get_variants(theme).count())
        self.assertEqual(0, self._index.get_variant_themes().count())
        name = self.create_name()
        self.assertEqual(0, name.get_scope().count())
        scoped = name.create_variant('Variant', theme)
        self.assertEqual(1, scoped.get_scope().count(),
                         'Unexpected variant\'s scope size')
        self._update_index()
        self.assertNotEqual(0, self._index.get_variant_themes().count())
        self.assertEqual(1, self._index.get_variant_themes().count(),
                         'Unexpected number of variant themes')
        self.assertTrue(scoped in self._index.get_variants(theme))
        self.assertTrue(theme in self._index.get_variant_themes())
        name.add_theme(theme2)
        self.assertEqual(1, name.get_scope().count())
        self.assertEqual(2, scoped.get_scope().count(), 'The scope change of the parent is not reflected in the variant\'s scope')
        self._update_index()
        self.assertEqual(2, self._index.get_variant_themes().count(), 'Change of the parent\'s scope is not reflected in the index')
        self.assertTrue(scoped in self._index.get_variants(theme))
        self.assertTrue(theme in self._index.get_variant_themes())
        self.assertTrue(scoped in self._index.get_variants(theme2))
        self.assertTrue(theme2 in self._index.get_variant_themes())
        name.remove_theme(theme2)
        self._update_index()
        self.assertNotEqual(0, self._index.get_variant_themes().count())
        self.assertEqual(1, self._index.get_variant_themes().count(), 'The scope change in the name is not reflected in the variant')
        self.assertTrue(scoped in self._index.get_variants(theme))
        self.assertTrue(theme in self._index.get_variant_themes())
        scoped.add_theme(theme2)
        self._update_index()
        self.assertEqual(2, self._index.get_variant_themes().count(), 'Change of the variant\'s scope is not reflected in the index')
        self.assertTrue(scoped in self._index.get_variants(theme))
        self.assertTrue(theme in self._index.get_variant_themes())
        self.assertTrue(scoped in self._index.get_variants(theme2))
        self.assertTrue(theme2 in self._index.get_variant_themes())
        name.add_theme(theme2)
        self._update_index()
        self.assertEqual(2, self._index.get_variant_themes().count(), 'Adding a theme to the variant\'s parent is not reflected in the index')
        self.assertTrue(scoped in self._index.get_variants(theme))
        self.assertTrue(theme in self._index.get_variant_themes())
        self.assertTrue(scoped in self._index.get_variants(theme2))
        self.assertTrue(theme2 in self._index.get_variant_themes())
        name.remove_theme(theme2)
        self._update_index()
        self.assertEqual(2, self._index.get_variant_themes().count(), 'Removing the name\'s theme MUST NOT be reflected in the variant\'s scope')
        self.assertTrue(scoped in self._index.get_variants(theme))
        self.assertTrue(theme in self._index.get_variant_themes())
        self.assertTrue(scoped in self._index.get_variants(theme2))
        self.assertTrue(theme2 in self._index.get_variant_themes())
        scoped.remove_theme(theme2)
        self.assertNotEqual(0, self._index.get_variant_themes().count())
        self.assertEqual(1, self._index.get_variant_themes().count())
        self.assertTrue(scoped in self._index.get_variants(theme))
        self.assertTrue(theme in self._index.get_variant_themes())

    def test_variant_2 (self):
        theme = self.create_topic()
        theme2 = self.create_topic()
        self._update_index()
        self.assertEqual(0, self._index.get_variants(theme).count())
        self.assertEqual(0, self._index.get_variants(theme2).count())
        self.assertEqual(0, self._index.get_variant_themes().count())
        name = self.create_topic().create_name('Name', scope=theme2)
        self.assertEqual(1, name.get_scope().count())
        scoped = name.create_variant('Variant', theme)
        self.assertEqual(2, scoped.get_scope().count())
        self._update_index()
        self.assertEqual(2, self._index.get_variant_themes().count())
        self.assertTrue(scoped in self._index.get_variants(theme))
        self.assertTrue(theme in self._index.get_variant_themes())
        self.assertTrue(scoped in self._index.get_variants(theme2))
        self.assertTrue(theme2 in self._index.get_variant_themes())
        name.remove_theme(theme2)
        self.assertEqual(0, name.get_scope().count())
        self._update_index()
        self.assertEqual(1, self._index.get_variant_themes().count())
        self.assertTrue(scoped in self._index.get_variants(theme))
        self.assertTrue(theme in self._index.get_variant_themes())

    def test_variant_match_all (self):
        theme = self.create_topic()
        theme2 = self.create_topic()
        unused_theme = self.create_topic()
        self._update_index()
        self.assertEqual(0, self._index.get_variants(theme).count())
        self.assertEqual(0, self._index.get_variants(theme2).count())
        self.assertEqual(0, self._index.get_variant_themes().count())
        name = self.create_topic().create_name('Name')
        self.assertEqual(0, name.get_scope().count())
        scoped = name.create_variant('Variant', theme)
        self.assertEqual(1, scoped.get_scope().count())
        self._update_index()
        self.assertEqual(1, self._index.get_variant_themes().count())
        self.assertTrue(scoped in self._index.get_variants([theme], True))
        self.assertTrue(scoped in self._index.get_variants([theme], False))
        self.assertFalse(scoped in self._index.get_variants([theme2], True))
        self.assertFalse(scoped in self._index.get_variants([theme2], False))
        scoped.add_theme(theme2)
        self._update_index()
        self.assertTrue(scoped in self._index.get_variants([theme], True))
        self.assertTrue(scoped in self._index.get_variants([theme], False))
        self.assertTrue(scoped in self._index.get_variants([theme2], True))
        self.assertTrue(scoped in self._index.get_variants([theme2], False))
        self.assertTrue(scoped in self._index.get_variants(
                [theme, theme2], True))
        self.assertTrue(scoped in self._index.get_variants(
                [theme, theme2], False))
        self.assertTrue(scoped in self._index.get_variants(
                [theme, theme2, unused_theme], False))
        self.assertFalse(scoped in self._index.get_variants(
                [theme, theme2, unused_theme], True))
        name_theme = self.create_topic()
        name.add_theme(name_theme)
        self._update_index()
        self.assertTrue(scoped in self._index.get_variants([theme], True))
        self.assertTrue(scoped in self._index.get_variants([theme], False))
        self.assertTrue(scoped in self._index.get_variants([theme2], True))
        self.assertTrue(scoped in self._index.get_variants([theme2], False))
        self.assertTrue(scoped in self._index.get_variants([name_theme], True))
        self.assertTrue(scoped in self._index.get_variants([name_theme], False))
        self.assertTrue(scoped in self._index.get_variants(
                [theme, theme2], True))
        self.assertTrue(scoped in self._index.get_variants(
                [theme, theme2], False))
        self.assertTrue(scoped in self._index.get_variants(
                [theme, theme2, name_theme], True))
        self.assertTrue(scoped in self._index.get_variants(
                [theme, theme2, name_theme], False))
        self.assertTrue(scoped in self._index.get_variants(
                [theme, theme2, unused_theme], False))
        self.assertFalse(scoped in self._index.get_variants(
                [theme, theme2, unused_theme], True))
        name.remove_theme(name_theme)
        self._update_index()
        self.assertFalse(scoped in self._index.get_variants([name_theme], True))
        self.assertFalse(scoped in self._index.get_variants(
                [name_theme], False))
        self.assertFalse(scoped in self._index.get_variants(
                [theme, theme2, name_theme], True))
        self.assertTrue(scoped in self._index.get_variants(
                [theme, theme2, name_theme], False))
        scoped.remove_theme(theme)
        self._update_index()
        self.assertFalse(scoped in self._index.get_variants([theme], True))
        self.assertFalse(scoped in self._index.get_variants([theme], False))
        self.assertFalse(scoped in self._index.get_variants(
                [theme, theme2], True))
        self.assertTrue(scoped in self._index.get_variants(
                [theme, theme2], False))

    def test_variant_match_all_2 (self):
        theme = self.create_topic()
        theme2 = self.create_topic()
        unused_theme = self.create_topic()
        name_theme = self.create_topic()
        self._update_index()
        self.assertEqual(0, self._index.get_variants(theme).count())
        self.assertEqual(0, self._index.get_variants(theme2).count())
        self.assertEqual(0, self._index.get_variant_themes().count())
        name = self.create_topic().create_name('Name', scope=name_theme)
        self.assertEqual(1, name.get_scope().count())
        scoped = name.create_variant('Variant', [theme, theme2])
        self.assertEqual(3, scoped.get_scope().count())
        self._update_index()
        self.assertEqual(3, self._index.get_variant_themes().count())
        self.assertTrue(scoped in self._index.get_variants([theme], True))
        self.assertTrue(scoped in self._index.get_variants([theme], False))
        self.assertTrue(scoped in self._index.get_variants([theme2], True))
        self.assertTrue(scoped in self._index.get_variants([theme2], False))
        self.assertTrue(scoped in self._index.get_variants([name_theme], True))
        self.assertTrue(scoped in self._index.get_variants([name_theme], False))
        self.assertTrue(scoped in self._index.get_variants(
                [theme, theme2], True))
        self.assertTrue(scoped in self._index.get_variants(
                [theme, theme2], False))
        self.assertTrue(scoped in self._index.get_variants(
                [theme, theme2, name_theme], False))
        self.assertTrue(scoped in self._index.get_variants(
                [theme, theme2, name_theme], False))
        self.assertTrue(scoped in self._index.get_variants(
                [theme, theme2, unused_theme], False))
        self.assertFalse(scoped in self._index.get_variants(
                [theme, theme2, unused_theme], True))
