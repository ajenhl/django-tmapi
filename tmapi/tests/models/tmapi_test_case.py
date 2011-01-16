"""Module containing the base of all TMAPI test classes."""

from django.test import TestCase

from tmapi.models import TopicMapSystem


class TMAPITestCase (TestCase):

    DEFAULT_ADDRESS = 'http://www.tmapi.org/tmapi2.0'
    
    def setUp (self):
        self.tms = TopicMapSystem()
        self.tms.save()
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
