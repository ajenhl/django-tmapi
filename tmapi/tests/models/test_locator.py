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

"""Module containing tests against the `Locator` interface.

Most if not all of these tests are ported from the public domain tests
that come with the TMAPI 2.0 distribution (http://www.tmapi.org/2.0/).

"""

from tmapi.exceptions import MalformedIRIException

from .tmapi_test_case import TMAPITestCase


class LocatorTest (TMAPITestCase):

    def test_normalization (self):
        locator = self.tm.create_locator('http://www.example.org/test%20me/')
        self.assertEqual('http://www.example.org/test me/',
                         locator.get_reference())
        self.assertEqual('http://www.example.org/test%20me/',
                         locator.to_external_form())
        locator2 = locator.resolve('./too')
        self.assertEqual('http://www.example.org/test me/too',
                         locator2.get_reference());
        self.assertEqual('http://www.example.org/test%20me/too',
                         locator2.to_external_form())
        locator3 = self.tms.create_locator('http://www.example.org/test me/')
        self.assertEqual('http://www.example.org/test me/',
                         locator3.get_reference())
        self.assertEqual('http://www.example.org/test%20me/',
                         locator3.to_external_form())
        self.assertEqual(locator, locator3)

    def test_illegal_locator_addresses (self):
        illegal = ('', '#fragment')
        for address in illegal:
            self.assertRaises(MalformedIRIException, self.tms.create_locator,
                              address)
            self.assertRaises(MalformedIRIException, self.tm.create_locator,
                              address)

    def test_RFC3986_5_4_1_normal_examples (self):
        iris = (
            ('g:h', 'g:h'),
            ('g', 'http://a/b/c/g'),
            ('./g', 'http://a/b/c/g'),
            ('/g', 'http://a/g'),
            ('//g/x', 'http://g/x'),
            ('g?y', 'http://a/b/c/g?y'),
            ('#s', 'http://a/b/c/d;p?q#s'),
            ('g#s', 'http://a/b/c/g#s'),
            ('g?y#s', 'http://a/b/c/g?y#s'),
            (';x', 'http://a/b/c/;x'),
            ('g;x', 'http://a/b/c/g;x'),
            ('g;x?y#s', 'http://a/b/c/g;x?y#s'),
            ('.', 'http://a/b/c/'),
            ('./', 'http://a/b/c/'),
            ('..', 'http://a/b/'),
            ('../', 'http://a/b/'),
            ('../g', 'http://a/b/g'),
            ('../..', 'http://a/'),
            ('../../', 'http://a/'),
            ('../../g', 'http://a/g'),
            )
        reference = 'http://a/b/c/d;p?q'
        base = self.tm.create_locator(reference)
        for part, expected in iris:
            self.assertEqual(expected, base.resolve(part).to_external_form())

    def test_normalization_preserve_empty (self):
        reference = 'http://www.tmapi.org/x?'
        self.assertEqual(reference,
                         self.tm.create_locator(reference).to_external_form())
        reference = 'http://www.tmapi.org/x#'
        self.assertEqual(reference,
                         self.tm.create_locator(reference).to_external_form())
