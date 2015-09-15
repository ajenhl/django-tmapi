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

"""Module containing tests against the `Scoped` interface.

Most if not all of these tests are ported from the public domain tests
that come with the TMAPI 2.0 distribution (http://www.tmapi.org/2.0/).

"""

from tmapi.exceptions import ModelConstraintException
from tmapi.models import Variant

from .tmapi_test_case import TMAPITestCase


class ScopedTest (TMAPITestCase):

    def _test_scoped (self, scoped):
        """Tests addding/removing themes.

        :param scoped: the scoped Topic Maps construct to test
        :type scoped: `Scoped`

        """
        scope_size = 0
        if isinstance(scoped, Variant):
            scope_size = scoped.get_scope().count()
        self.assertEqual(scope_size, scoped.get_scope().count())
        theme1 = self.create_topic()
        scoped.add_theme(theme1)
        scope_size += 1
        self.assertEqual(scope_size, scoped.get_scope().count())
        self.assertTrue(theme1 in scoped.get_scope())
        theme2 = self.create_topic()
        self.assertFalse(theme2 in scoped.get_scope())
        scoped.add_theme(theme2)
        scope_size += 1
        self.assertEqual(scope_size, scoped.get_scope().count())
        self.assertTrue(theme1 in scoped.get_scope())
        self.assertTrue(theme2 in scoped.get_scope())
        scoped.remove_theme(theme2)
        scope_size -= 1
        self.assertEqual(scope_size, scoped.get_scope().count())
        self.assertTrue(theme1 in scoped.get_scope())
        self.assertFalse(theme2 in scoped.get_scope())
        scoped.remove_theme(theme1)
        scope_size -= 1
        self.assertEqual(scope_size, scoped.get_scope().count())
        self.assertRaises(ModelConstraintException, scoped.add_theme, None)

    def test_association (self):
        """Scoped tests against an association."""
        self._test_scoped(self.create_association())

    def test_occurrence (self):
        """Scoped tests against an occurrence."""
        self._test_scoped(self.create_occurrence())

    def test_name (self):
        """Scoped tests against a name."""
        self._test_scoped(self.create_name())

    def test_variant (self):
        """Scoped tests against a variant."""
        self._test_scoped(self.create_variant())
