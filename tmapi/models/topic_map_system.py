from tmapi.exceptions import TopicMapExistsException
from locator import Locator
from topic_map import TopicMap


class TopicMapSystem (object):

    """A generic interface to this TMAPI system."""

    def create_locator (self, reference):
        """Returns a `Locator` instance representing the specified IRI
        `reference`.

        The specified IRI `reference` is assumed to be absolute.

        :param reference: a string which uses the IRI notation
        :type reference: String
        :rtype: `Locator`

        """
        return Locator(reference)
    
    def create_topic_map (self, iri):
        """Creates a new `TopicMap` and stores it within the system
        under the specified `iri`.

        :param iri: the address which should be used to store the `TopicMap`
        :type iri: `Locator` or String
        :rtype: `TopicMap`

        """
        if not isinstance(iri, Locator):
            iri = self.create_locator(iri)
        if self.get_topic_map(iri) is not None:
            raise TopicMapExistsException()
        reference = iri.to_external_form()
        tm = TopicMap(iri=reference)
        tm.save()
        return tm

    def get_locators (self):
        """Returns all storage addresses of `TopicMap` instances known
        by this system.

        :rtype: list of `Locator`s

        """
        return TopicMap.objects.values_list('iri', flat=True)
    
    def get_topic_map (self, iri):
        """Retrieves a `TopicMap` managed by this system with the
        specified storage address `iri`.

        :param iri: the storage address to retrieve the `TopicMap` from
        :type iri: `Locator` or String
        :rtype: `TopicMap` or None

        """
        if not isinstance(iri, Locator):
            iri = self.create_locator(iri)
        iri = iri.to_external_form()
        try:
            tm = TopicMap.objects.get(iri=iri)
        except TopicMap.DoesNotExist:
            tm = None
        return tm
        
