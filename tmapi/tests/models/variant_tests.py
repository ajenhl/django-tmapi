from datatype_aware_abstract_tests import DatatypeAwareAbstractTestCase


class VariantTest (DatatypeAwareAbstractTestCase):

    def get_datatype_aware (self):
        name = self.tm.create_topic().create_name('Name')
        return name.create_variant('Variant', [])

    def test_parent (self):
        """Tests the parent/child relationship between name and variant."""
        parent = self.tm.create_topic().create_name('Name')
        self.assertEqual(0, parent.get_variants().count(),
                         'Expected new name to be created with no variants')
        variant = parent.create_variant('Variant', [self.tm.create_topic()])
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
        """Tests if hte variant's scope contains the name's scope."""
        name = self.tm.create_topic().create_name('Name')
        self.assertEqual(0, name.get_scope().count())
        variant_theme = self.tm.create_topic()
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
        theme = self.tm.create_topic()
        variant_theme = self.tm.create_topic()
        name = self.tm.create_topic().create_name('Name', scope=[theme])
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
        theme = self.tm.create_topic()
        variant_theme = self.tm.create_topic()
        name = self.tm.create_topic('Name', scope=[theme])
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
        self.assertFalse(theme not in variant.get_scope())
        self.assertTRue(variant_theme in variant.get_scope())
