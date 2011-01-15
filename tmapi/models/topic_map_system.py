from tmapi.exceptions import TopicMapExistsException, \
    FeatureNotRecognizedException
from locator import Locator
from topic_map import TopicMap


class TopicMapSystem (object):

    """A generic interface to this TMAPI system."""

    _features = {}
    _properties = {}

    def __init__ (self, features=None, properties=None):
        self._features = features or {}
        self._properties = properties or {}

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

    def get_feature (self, feature_name):
        """Returns the value of the feature specified by
        `feature_name` for this TopicMapSystem instance.

        The features supported by the TopicMapSystem and the value for
        each feature are set when the TopicMapSystem is created by a
        call to `TopicMapSystemFactory.new_topic_map_system()` and
        cannot be modified subsequently.

        :param feature_name: the name of the feature to check
        :type feature_name: string
        :rtype: Boolean

        """
        feature = self._features.get(feature_name)
        if feature is None:
            raise FeatureNotRecognizedException
        return feature

    def get_locators (self):
        """Returns all storage addresses of `TopicMap` instances known
        by this system.

        :rtype: list of `Locator`s

        """
        return TopicMap.objects.values_list('iri', flat=True)

    def get_property (self, property_name):
        """Returns a property in the underlying implementation of
        `TopicMapSystem`.

        A list of the core properties defined by TMAPI can be found at
        http://tmapi.org/properties/.

        An implementation is free to support properties other than the
        core ones.

        The properties supported by the TopicMapSystem and the value
        for each property is set when the TopicMapSystem is created by
        a call to `TopicMapSystemFactory.new_topic_map_system()` and
        cannot be modified subsequently.

        :param property_name: the name of the property to retrieve
        :type property_name: string
        :rtype: object value set for the property or None if no value is set

        """
        return self._properties.get(property_name)
    
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
        
