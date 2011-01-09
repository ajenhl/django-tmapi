from django.test import TestCase

from tmapi.constants import XSD_ANY_URI, XSD_INT, XSD_STRING
from tmapi.models import TopicMapSystem


class DatatypeAwareAbstractTestCase (TestCase):

    def get_datatype_aware (self):
        raise NotImplementedError
    
    def setUp (self):
        self.tms = TopicMapSystem()
        self.tm = self.tms.create_topic_map('http://www.example.org/tm/')
        self._xsd_any_uri = self.tms.create_locator(XSD_ANY_URI)
        self._xsd_int = self.tms.create_locator(XSD_INT)
        self._xsd_string = self.tms.create_locator(XSD_STRING)

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
