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

"""Module containing tests against the `Typed` interface.

Most if not all of these tests are ported from the public domain tests
that come with the TMAPI 2.0 distribution (http://www.tmapi.org/2.0/).

"""

from tmapi.exceptions import ModelConstraintException

from .tmapi_test_case import TMAPITestCase


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
