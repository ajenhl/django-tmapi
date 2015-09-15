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

from django.contrib.sites.models import Site
from django.db import models

from tmapi.exceptions import ModelConstraintException, \
    UnsupportedOperationException
from tmapi.indices.literal_index import LiteralIndex
from tmapi.indices.scoped_index import ScopedIndex
from tmapi.indices.type_instance_index import TypeInstanceIndex

from .association import Association
from .construct_fields import BaseConstructFields
from .identifier import Identifier
from .item_identifier import ItemIdentifier
from .locator import Locator
from .reifiable import Reifiable
from .subject_identifier import SubjectIdentifier
from .subject_locator import SubjectLocator
from .topic import Topic
from .copy_utils import copy


class TopicMap (BaseConstructFields, Reifiable):

    """Represents a topic map item."""

    topic_map_system = models.ForeignKey('TopicMapSystem',
                                         related_name='topic_maps')
    iri = models.CharField(max_length=512)
    title = models.CharField(max_length=128, blank=True)
    base_address = models.CharField(max_length=512, blank=True)

    class Meta:
        app_label = 'tmapi'

    def __init__ (self, *args, **kwargs):
        super(TopicMap, self).__init__(*args, **kwargs)
        self._indices = {}

    def create_association (self, association_type, scope=None,
                            proxy=Association):
        """Creates an `Association` in this topic map with the
        specified type and scope.

        :param association_type: the association type
        :type association_type: `Topic`
        :param scope: scope
        :type scope: list of `Topic`s
        :param proxy: Django proxy model class
        :type proxy: class
        :rtype: `Association`

        """
        if association_type is None:
            raise ModelConstraintException(self, 'The type may not be None')
        if self != association_type.topic_map:
            raise ModelConstraintException(
                self, 'The type is not from this topic map')
        association = proxy(type=association_type, topic_map=self)
        association.save()
        if scope is None:
            scope = []
        for topic in scope:
            if self != topic.topic_map:
                raise ModelConstraintException(
                    self, 'The theme is not from this topic map')
            association.scope.add(topic)
        return association

    def create_empty_topic (self):
        """Returns a `Topic` instance with no other information.

        :rtype: `Topic`

        """
        topic = Topic(topic_map=self)
        topic.save()
        return topic

    def create_locator (self, reference):
        """Returns a `Locator` instance representing the specified IRI
        reference.

        The specified IRI reference is assumed to be absolute.

        :param reference: a string which uses the IRI notation
        :type reference: string
        :rtype: `Locator`

        """
        return Locator(reference)

    def create_topic (self, proxy=Topic):
        """Returns a `Topic` instance with an automatically generated
        item identifier.

        This method never returns an existing `Topic` but creates a
        new one with an automatically generated item identifier.

        Returns the newly created `Topic` instance with an automatically
        generated item identifier.

        :param proxy: Django proxy model class
        :type proxy: class
        :rtype: `Topic`

        """
        topic = proxy(topic_map=self)
        topic.save()
        address = 'http://%s/tmapi/iid/auto/%d' % \
            (Site.objects.get_current().domain, topic.id)
        ii = ItemIdentifier(address=address, containing_topic_map=self)
        ii.save()
        topic.item_identifiers.add(ii)
        return topic

    def create_topic_by_item_identifier (self, item_identifier):
        """Returns a `Topic` instance with the specified item identifier.

        This method returns either an existing `Topic` or creates a
        new `Topic` instance with the specified item identifier.

        If a topic with the specified item identifier exists in the
        topic map, that topic is returned. If a topic with a subject
        identifier equal to the specified item identifier exists, the
        specified item identifier is added to that topic and the topic
        is returned. If neither a topic with the specified item
        identifier nor with a subject identifier equal to the subject
        identifier exists, a topic with the item identifier is
        created.

        :param item_identifier: the item identifier the topic should contain
        :type item_identifier: `Locator`
        :rtype: `Topic`

        """
        if item_identifier is None:
            raise ModelConstraintException(
                self, 'The item identifier may not be None')
        reference = item_identifier.to_external_form()
        try:
            topic = self.topic_constructs.get(
                item_identifiers__address=reference)
        except Topic.DoesNotExist:
            try:
                topic = self.topic_constructs.get(
                    subject_identifiers__address=reference)
            except Topic.DoesNotExist:
                topic = Topic(topic_map=self)
                topic.save()
            ii = ItemIdentifier(address=reference, containing_topic_map=self)
            ii.save()
            topic.item_identifiers.add(ii)
        return topic

    def create_topic_by_subject_identifier (self, subject_identifier):
        """Returns a `Topic` instance with the specified subject identifier.

        This method returns either an existing `Topic` or creates a
        new `Topic` instance with the specified subject identifier.

        If a topic with the specified subject identifier exists in
        this topic map, that topic is returned. If a topic with an
        item identifier equal to the specified subject identifier
        exists, the specified subject identifier is added to that
        topic and the topic is returned. If neither a topic with the
        specified subject identifier nor with an item identifier equal
        to the subject identifier exists, a topic with the subject
        identifier is created.

        :param subject_identifier: the subject identifier the topic
          should contain
        :type subject_identifier: `Locator`
        :rtype: `Topic`

        """
        if subject_identifier is None:
            raise ModelConstraintException(
                self, 'The subject identifier may not be None')
        reference = subject_identifier.to_external_form()
        try:
            topic = self.topic_constructs.get(
                subject_identifiers__address=reference)
        except Topic.DoesNotExist:
            try:
                topic = self.topic_constructs.get(
                    item_identifiers__address=reference)
            except Topic.DoesNotExist:
                topic = Topic(topic_map=self)
                topic.save()
            si = SubjectIdentifier(topic=topic, address=reference,
                                   containing_topic_map=self)
            si.save()
            topic.subject_identifiers.add(si)
        return topic

    def create_topic_by_subject_locator (self, subject_locator):
        """Returns a `Topic` instance with the specified subject locator.

        This method returns either an existing `Topic` or creates a
        new `Topic` instance with the specified subject locator.

        :param subject_locator: the subject locator the topic should
          contain
        :type subject_locator: `Locator`
        :rtype: `Topic`

        """
        if subject_locator is None:
            raise ModelConstraintException(
                self, 'The subject locator may not be None')
        reference = subject_locator.to_external_form()
        try:
            topic = self.topic_constructs.get(
                subject_locators__address=reference)
        except Topic.DoesNotExist:
            topic = Topic(topic_map=self)
            topic.save()
            sl = SubjectLocator(topic=topic, address=reference,
                                containing_topic_map=self)
            sl.save()
            topic.subject_locators.add(sl)
        return topic

    def get_associations (self):
        """Returns all `Association`s contained in this topic map.

        :rtype: `QuerySet` of `Association`s

        """
        return self.association_constructs.all()

    def get_construct_by_id (self, id, proxy=None):
        """Returns a `Construct` by its (system specific) identifier.

        :param id: the identifier of the construct to be returned
        :type id: string
        :param proxy: Django proxy model
        :type proxy: class
        :rtype: `Construct`, proxy object, or None

        """
        try:
            identifier = Identifier.objects.get(pk=int(id),
                                                containing_topic_map=self)
            construct = identifier.get_construct()
            if proxy is not None and construct is not None:
                construct = proxy.objects.get(pk=construct.id)
        except Identifier.DoesNotExist:
            construct = None
        return construct

    def get_construct_by_item_identifier (self, item_identifier):
        """Returns a `Construct` by its item identifier.

        :param item_identifier: the item identifier of the construct
          to be returned
        :type item_identifier: `Locator`
        :rtype: a construct or None

        """
        address = item_identifier.to_external_form()
        try:
            ii = ItemIdentifier.objects.get(address=address,
                                            containing_topic_map=self)
            construct = ii.get_construct()
        except ItemIdentifier.DoesNotExist:
            construct = None
        return construct

    def get_index (self, index_interface):
        """Returns the specified index.

        :param index_interface: the index to return
        :type index_interface: class
        :rtype: `Index`

        """
        if index_interface not in (LiteralIndex, ScopedIndex,
                                   TypeInstanceIndex):
            raise UnsupportedOperationException(
                'This TMAPI implementation does not support that index')
        if index_interface not in self._indices:
            self._indices[index_interface] = index_interface(self)
        return self._indices[index_interface]

    def get_locator (self):
        """Returns the `Locator` that was used to create the topic map.

        Note: The returned locator represents the storage address of
        the topic map and implies no further semantics.

        :rtype: `Locator`

        """
        return Locator(self.iri)

    def get_parent (self):
        """Returns None.

        :rtype: None

        """
        return None

    def get_topics (self):
        """Returns all `Topic`s contained in this topic map.

        :rtype: `QuerySet` of `Topic`s

        """
        return self.topic_constructs.all()

    def get_topic_by_subject_identifier (self, subject_identifier):
        """Returns a topic by its subject identifier.

        If no topic with the specified subject identifier exists, this
        method returns `None`.

        :param subject_identifier: the subject identifier of the topic
          to be returned
        :type subject_identifier: `Locator`
        :rtype: `Topic` or `None`

        """
        reference = subject_identifier.to_external_form()
        try:
            topic = self.topic_constructs.get(
                subject_identifiers__address=reference)
        except Topic.DoesNotExist:
            topic = None
        return topic

    def get_topic_by_subject_locator (self, subject_locator):
        """Returns a topic by its subject locator.

        If no topic with the specified subject locator exists, this
        method returns `None`.

        :param subject_locator: the subject locator of the topic to be
          returned
        :type subject_locator: `Locator`
        :rtype: `Topic` of `None`

        """
        reference = subject_locator.to_external_form()
        try:
            topic = self.topic_constructs.get(
                subject_locators__address=reference)
        except Topic.DoesNotExist:
            topic = None
        return topic

    def get_topic_map (self):
        """Returns self.

        :rtype: `TopicMap`

        """
        return self

    def merge_in (self, other):
        """Merges the topic map `other` into this topic map.

        All `Topic`s and `Association`s and all of their contents in
        `other` will be added to this topic map.

        All information items in `other` will be merged into this
        topic map as defined by the Topic Maps - Data Model (TMDM)
        merging rules.

        The merge process will not modify `other` in any way.

        If this topic map equals `other`, no changes are made to the
        topic map.

        :param other: the topic map to be merged with this topic map
          instance
        :type other: `TopicMap`

        """
        if other is None:
            raise ModelConstraintException(
                self, 'The topic map to merge in may not be None')
        copy(other, self)

    def remove (self):
        self.delete()

    def __eq__ (self, other):
        if isinstance(other, TopicMap) and self.id == other.id:
            return True
        return False

    def __ne__ (self, other):
        return not(self.__eq__(other))

    def __str__ (self):
        name = self.title or 'Topic map'
        return '{} ({})'.format(name, self.iri)
