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

"""Module containing tests against the `Reifiable` interface.

Most if not all of these tests are ported from the public domain tests
that come with the TMAPI 2.0 distribution (http://www.tmapi.org/2.0/).

"""

from tmapi.exceptions import ModelConstraintException

from .tmapi_test_case import TMAPITestCase


class ReifiableTest (TMAPITestCase):

    def _test_reification (self, reifiable):
        """Tests setting/getting the reifier for the `reifiable`.

        :param reifiable: the reifiable to run the tests against
        :type reifiable: `Reifiable`

        """
        self.assertEqual(None, reifiable.get_reifier(),
                         'Unexpected reifier property')
        reifier = self.create_topic()
        self.assertEqual(None, reifier.get_reified())
        reifiable.set_reifier(reifier)
        self.assertEqual(reifier, reifiable.get_reifier(),
                         'Unexpected reifier property')
        self.assertEqual(reifiable, reifier.get_reified(),
                         'Unexpected reified property')
        reifiable.set_reifier(None)
        self.assertEqual(None, reifiable.get_reifier(),
                         'Reifier should be None')
        self.assertEqual(None, reifier.get_reified(), 'Reified should be None')
        reifiable.set_reifier(reifier)
        self.assertEqual(reifier, reifiable.get_reifier(),
                         'Unexpected reifier property')
        self.assertEqual(reifiable, reifier.get_reified(),
                         'Unexpected reified property')
        try:
            reifiable.set_reifier(reifier)
        except ModelConstraintException:
            self.fail('Unexpected exception while setting the reifier to the same value')

    def _test_reification_collision (self, reifiable):
        """Tests if a reifier collision (the reifier is already
        assigned to another construct) is detected.

        :param reifiable: the reifiable to run the tests against
        :type reifiable: `Reifiable`

        """
        self.assertEqual(None, reifiable.get_reifier(),
                         'Unexpected reifier property')
        reifier = self.create_topic()
        self.assertEqual(None, reifier.get_reified())
        other_reifiable = self.create_association()
        other_reifiable.set_reifier(reifier)
        self.assertEqual(reifier, other_reifiable.get_reifier(),
                         'Expected a reifier property')
        self.assertEqual(other_reifiable, reifier.get_reified(),
                         'Unexpected reified property')
        try:
            reifiable.set_reifier(reifier)
            self.fail('The reifier already reifies another construct')
        except ModelConstraintException as ex:
            self.assertEqual(reifiable, ex.get_reporter())
        other_reifiable.set_reifier(None)
        self.assertEqual(None, other_reifiable.get_reifier(),
                         'Reifier property should be None')
        self.assertEqual(None, reifier.get_reified(),
                         'Reified property should be None')
        reifiable.set_reifier(reifier)
        self.assertEqual(reifier, reifiable.get_reifier(),
                         'Reifier property should have been changed')
        self.assertEqual(reifiable, reifier.get_reified(),
                         'Reified property should have been changed')

    def test_topic_map (self):
        self._test_reification(self.tm)

    def test_topic_map_reifier_collision (self):
        self._test_reification_collision(self.tm)

    def test_association (self):
        self._test_reification(self.create_association())

    def test_association_reifier_collision (self):
        self._test_reification_collision(self.create_association())

    def test_role (self):
        self._test_reification(self.create_role())

    def test_role_reifier_collision (self):
        self._test_reification_collision(self.create_role())

    def test_occurrence (self):
        self._test_reification(self.create_occurrence())

    def test_occurrence_reification_collision (self):
        self._test_reification_collision(self.create_occurrence())

    def test_name (self):
        self._test_reification(self.create_name())

    def test_name_reification_collision (self):
        self._test_reification_collision(self.create_name())

    def test_variant (self):
        self._test_reification(self.create_variant())

    def test_variant_reification_collision (self):
        self._test_reification_collision(self.create_variant())
