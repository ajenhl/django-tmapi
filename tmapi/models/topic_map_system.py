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

from django.db import models

from tmapi.exceptions import TopicMapExistsException, \
    FeatureNotRecognizedException
from .locator import Locator
from .tmapi_feature import TMAPIFeature
from .topic_map import TopicMap


class TopicMapSystem (models.Model):

    """A generic interface to this TMAPI system."""

    class Meta:
        app_label = 'tmapi'

    def create_locator (self, reference):
        """Returns a `Locator` instance representing the specified IRI
        `reference`.

        The specified IRI `reference` is assumed to be absolute.

        :param reference: a string which uses the IRI notation
        :type reference: String
        :rtype: `Locator`

        """
        return Locator(reference)

    def create_topic_map (self, iri, proxy=TopicMap):
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
        tm = proxy(topic_map_system=self, iri=reference)
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
        try:
            feature = self.features.get(feature_string=feature_name)
        except TMAPIFeature.DoesNotExist:
            raise FeatureNotRecognizedException
        return feature.value

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
        # There are no core TMAPI properties, and this implementation
        # supports no others, so there is no need even for a store of
        # such.
        return None

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
