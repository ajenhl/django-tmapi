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

"""Module containing the base of all TMAPI test classes.

Most if not all of these tests are ported from the public domain tests
that come with the TMAPI 2.0 distribution (http://www.tmapi.org/2.0/).

"""

from django.test import TestCase

from tmapi.models import TopicMapSystemFactory


class TMAPITestCase (TestCase):

    DEFAULT_ADDRESS = 'http://www.tmapi.org/tmapi2.0'

    def setUp (self):
        factory = TopicMapSystemFactory.new_instance()
        self.tms = factory.new_topic_map_system()
        self.default_locator = self.tms.create_locator(self.DEFAULT_ADDRESS)
        self.tm = self.tms.create_topic_map(self.default_locator)

    def create_topic (self):
        """Creates a topic with a random item identifier.

        :rtype: `Topic`

        """
        return self.tm.create_topic()

    def create_association (self):
        """Creates an association with a random type and no roles.

        :rtype: `Association`

        """
        return self.tm.create_association(self.create_topic())

    def create_role (self):
        """Creates a role which is part of a random association with a
        random player and type.

        :rtype: `Role`

        """
        return self.create_association().create_role(self.create_topic(),
                                                     self.create_topic())

    def create_occurrence (self):
        """Creates an occurrence which is part of a random topic with
        a random type.

        :rtype: `Occurrence`

        """
        return self.create_topic().create_occurrence(self.create_topic(),
                                                     'Occurrence')

    def create_name (self):
        """Creates a name which is part of a newly created topic using
        the default name type.

        :rtype: `Name`

        """
        return self.create_topic().create_name('Name')

    def create_variant (self):
        """Creates a variant which is part of a newly created name.

        :rtype: `Variant`

        """
        return self.create_name().create_variant('Variant',
                                                 [self.create_topic()])

    def create_locator (self, iri):
        return self.tms.create_locator(iri)

    def create_topic_map (self, iri):
        """Creates a topic map under the specified `iri`.

        :param iri: the IRI where the topic map should be stored
        :type iri: string
        :rtype: `TopicMap`

        """
        return self.tms.create_topic_map(self.tms.create_locator(iri))
