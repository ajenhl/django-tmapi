from django.test import TestCase

from tmapi.constants import XSD_ANY_URI
from tmapi.exceptions import ModelConstraintException
from tmapi.models import TopicMapSystem


class NameTest (TestCase):

    def setUp (self):
        self.tms = TopicMapSystem()
        self.tm = self.tms.create_topic_map('http://www.example.org/tm/')
    
    def test_parent (self):
        parent = self.tm.create_topic()
        self.assertEqual(0, parent.get_names().count())
        name = parent.create_name('Name')
        self.assertEqual(parent, name.get_parent(),
                         'Unexpected name parent after creation')
        self.assertEqual(1, parent.get_names().count(),
                         'Expected name list size to increment for topic')
        self.assertTrue(name in parent.get_names(),
                        'Name is not part of get_names()')
        name.remove()
        self.assertEqual(0, parent.get_names().count(),
                         'Expected name list size to decrement for topic')

    def test_value (self):
        value1 = 'TMAPI Name'
        value2 = 'A name'
        topic = self.tm.create_topic()
        name = topic.create_name('Name')
        name.set_value(value1)
        self.assertEqual(value1, name.get_value())
        name.set_value(value2)
        self.assertEqual(value2, name.get_value())
        self.assertRaises(ModelConstraintException, name.set_value, None)

    def test_variant_creation_string (self):
        topic = self.tm.create_topic()
        name = topic.create_name('Name')
        theme = self.tm.create_topic()
        xsd_string = self.tm.create_locator(
            'http://www.w3.org/2001/XMLSchema#string')
        variant = name.create_variant('Variant', [theme])
        self.assertEqual('Variant', variant.get_value())
        self.assertEqual(xsd_string, variant.get_datatype())
        self.assertEqual(1, variant.get_scope().count())
        self.assertTrue(theme in variant.get_scope())

    def test_variant_creation_uri (self):
        topic = self.tm.create_topic()
        name = topic.create_name('Name')
        theme = self.tm.create_topic()
        xsd_any_uri = self.tm.create_locator(XSD_ANY_URI)
        value = self.tm.create_locator('http://www.example.org/')
        variant = name.create_variant(value, [theme])
        self.assertEqual(value.get_reference(), variant.get_value())
        self.assertEqual(value, variant.locator_value())
        self.assertEqual(xsd_any_uri, variant.get_datatype())
        self.assertEqual(1, variant.get_scope().count())
        self.assertTrue(theme in variant.get_scope())

    def test_variant_creation_explicit_datatype (self):
        topic = self.tm.create_topic()
        name = topic.create_name('Name')
        theme = self.tm.create_topic()
        dt = self.tm.create_locator('http://www.example.org/datatype')
        variant = name.create_variant('Variant', [theme], dt)
        self.assertEqual('Variant', variant.get_value())
        self.assertEqual(dt, variant.get_datatype())
        self.assertEqual(1, variant.get_scope().count())
        self.assertTrue(theme in variant.get_scope())

    def test_variant_creation_illegal_string (self):
        name = self.tm.create_topic().create_name('Name')
        theme = self.tm.create_topic()
        self.assertRaises(ModelConstraintException, name.create_variant,
                          None, [theme])

    def test_variant_creation_illegal_locator (self):
        # This test is the same as the previous in this Python
        # implementation.
        pass
        
    def test_variant_creation_illegal_datatype (self):
        # This test is not applicable in Python.
        pass

    def test_variant_creation_illegal_scope (self):
        name = self.tm.create_topic().create_name('Name')
        theme = self.tm.create_topic()
        name.add_theme(theme)
        self.assertEqual(1, name.get_scope().count())
        self.assertTrue(theme in name.get_scope())
        self.assertRaises(ModelConstraintException, name.create_variant,
                          'Variant', [theme])

    def test_variant_creation_illegal_empty_scope (self):
        name = self.tm.create_topic().create_name('Name')
        self.assertRaises(ModelConstraintException, name.create_variant,
                          'Variant', [])

    def test_variant_creation_illegal_null_scope (self):
        name = self.tm.create_topic().create_name('Name')
        self.assertRaises(ModelConstraintException, name.create_variant,
                          'Variant', None)

    def test_variant_creation_illegal_empty_array_scope (self):
        # This test is not applicable in Python.
        pass

    def test_variant_creation_with_locator_illegal_empty_scope (self):
        name = self.tm.create_topic().create_name('Name')
        self.assertRaises(ModelConstraintException, name.create_variant,
                          self.tm.create_locator('http://tmapi.org/'), [])

    def test_variant_creation_with_locator_illegal_null_scope (self):
        name = self.tm.create_topic().create_name('Name')
        self.assertRaises(ModelConstraintException, name.create_variant,
                          self.tm.create_locator('http://tmapi.org/'), None)

    def test_variant_creation_with_locator_illegal_empty_array_scope (self):
        # This test is not applicable in Python.
        pass

    def test_variant_creation_with_datatype_illegal_empty_scope (self):
        name = self.tm.create_topic().create_name('Name')
        dt = self.tm.create_locator('http://tmapi.org/')
        self.assertRaises(ModelConstraintException, name.create_variant,
                          'Variant', [], dt)

    def test_variant_creation_with_datatype_illegal_null_scope (self):
        name = self.tm.create_topic().create_name('Name')
        dt = self.tm.create_locator('http://tmapi.org/')
        self.assertRaises(ModelConstraintException, name.create_variant,
                          'Variant', None, dt)

    def test_variant_creation_with_datatype_illegal_empty_array_scope (self):
        # This test is not applicable in Python.
        pass
