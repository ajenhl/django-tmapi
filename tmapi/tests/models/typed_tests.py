"""Module containing tests against the `Typed` interface."""

from tmapi.exceptions import ModelConstraintException

from tmapi_test_case import TMAPITestCase


class TypedTest (TMAPITestCase):

    def _test_typed (self, typed):
        old_type = typed.get_type()
        self.assertNotEqual(None, old_type)
        new_type = self.create_topic()
        typed.set_type(new_type)
        self.assertEqual(new_type, typed.get_type(),
                         'Expected another type')
        typed.set_type(old_type)
        self.assertEqual(old_type, typed.get_type(),
                         'Expected the previous type')
        self.assertRaises(ModelConstraintException, typed.set_type, None)

    def test_association (self):
        """Typed tests against an association."""
        self._test_typed(self.create_association())

    def test_role (self):
        """Typed tests against a role."""
        self._test_typed(self.create_role())

    def test_occurrence (self):
        """Typed tests against an occurrence."""
        self._test_typed(self.create_occurrence())

    def test_name (self):
        """Typed tests against a name."""
        self._test_typed(self.create_name())
