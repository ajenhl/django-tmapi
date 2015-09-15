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

"""Module defining the Topic model and its managers."""

from django.db import models

from tmapi.constants import AUTOMERGE_FEATURE_STRING, XSD_ANY_URI, XSD_FLOAT, \
    XSD_INT, XSD_STRING
from tmapi.exceptions import IdentityConstraintException, \
    ModelConstraintException, TopicInUseException

from .construct import Construct
from .construct_fields import ConstructFields
from .item_identifier import ItemIdentifier
from .locator import Locator
from .name import Name
from .subject_identifier import SubjectIdentifier
from .subject_locator import SubjectLocator
from .occurrence import Occurrence
from .merge_utils import handle_existing_construct, \
    move_role_characteristics, move_variants
from .signature import generate_association_signature, \
    generate_name_signature, generate_occurrence_signature


class Topic (Construct, ConstructFields):

    """Represents a topic item."""

    types = models.ManyToManyField('self', symmetrical=False, blank=True,
                                   related_name='typed_topics')

    class Meta:
        app_label = 'tmapi'

    def add_item_identifier (self, item_identifier):
        """Adds an item identifier to this topic.

        If adding the specified item identifier would make this topic
        represent the same subject as another topic and the feature
        "automerge" (http://tmapi.org/features/automerge/) is
        disabled, an `IdentityConstraintException` is thrown.

        :param item_identifier: the item identifier to be added
        :type item_identifier: `Locator`

        """
        if item_identifier is None:
            raise ModelConstraintException(
                self, 'The item identifier may not be None')
        address = item_identifier.to_external_form()
        try:
            ii = ItemIdentifier.objects.get(address=address,
                                            containing_topic_map=self.topic_map)
            construct = ii.get_construct()
            if construct == self:
                return
            if not isinstance(construct, Topic):
                raise IdentityConstraintException(
                    self, construct, item_identifier, 'This item identifier is already associated with another non-Topic construct')
            if self.topic_map.topic_map_system.get_feature(
                AUTOMERGE_FEATURE_STRING):
                self.merge_in(construct)
            else:
                raise IdentityConstraintException(
                    self, construct, item_identifier, 'Another topic has the same item identifier and automerge is disabled')
        except ItemIdentifier.DoesNotExist:
            try:
                # Check that there is no topic with a subject
                # indicator whose address matches item_identifier's.
                topic = self.topic_map.topic_constructs.get(
                    subject_identifiers__address=address)
                if topic == self:
                    self._add_item_identifier(address)
                elif self.topic_map.topic_map_system.get_feature(
                    AUTOMERGE_FEATURE_STRING):
                    self.merge_in(topic)
                else:
                    raise IdentityConstraintException(
                        self, topic, item_identifier, 'Another topic has the same subject identifier and automerge is disabled')
            except Topic.DoesNotExist:
                self._add_item_identifier(address)

    def _add_item_identifier (self, address):
        """Adds an item identifier to this topic.

        This method performs only the actual database operation to add
        the item identifier, and is only called after appropriate
        checking in add_item_identifier().

        :param address: external form of a locator
        :type address: string

        """
        ii = ItemIdentifier(address=address,
                            containing_topic_map=self.topic_map)
        ii.save()
        self.item_identifiers.add(ii)

    def add_subject_identifier (self, subject_identifier):
        """Adds a subject identifier to this topic.

        If adding the specified subject identifier would make this
        topic represent the same subject as another topic and the
        feature "automerge" (http://tmapi.org/features/automerge/) is
        disabled, an `IdentityConstraintException` is thrown.

        :param subject_identifier: the subject identifier to be added
        :type subject_identifier: `Locator`

        """
        if subject_identifier is None:
            raise ModelConstraintException(
                self, 'The subject identifier may not be None')
        address = subject_identifier.to_external_form()
        try:
            # Check if there is an existing topic with the same
            # subject identifier or item identifier.
            topic = self.topic_map.topic_constructs.get(
                models.Q(subject_identifiers__address=address) |
                models.Q(item_identifiers__address=address))
            if topic == self:
                # If the match was because this topic has an item
                # identifier equal to subject_identifier, add the
                # subject identifier. Otherwise do nothing.
                if not SubjectIdentifier.objects.filter(topic=self,
                                                        address=address):
                    self._add_subject_identifier(address)
            elif self.topic_map.topic_map_system.get_feature(
                AUTOMERGE_FEATURE_STRING):
                self.merge_in(topic)
            else:
                raise IdentityConstraintException(
                    self, topic, subject_identifier, 'Another topic has the same subject/item identifier and automerge is disabled')
        except Topic.DoesNotExist:
            self._add_subject_identifier(address)

    def _add_subject_identifier (self, address):
        """Adds a subject identifier to this topic.

        This method performs only the actual database operation to add
        the subject identifier, and is only called after appropriate
        checking in add_subject_identifier().

        :param address: external form of a locator
        :type address: string

        """
        si = SubjectIdentifier(topic=self, address=address,
                               containing_topic_map=self.topic_map)
        si.save()
        self.subject_identifiers.add(si)

    def add_subject_locator (self, subject_locator):
        """Adds a subject locator to this topic.

        If adding the specified subject locator would make this topic
        represent teh same subject as another topic and the feature
        'automerge' (http://tmapi.org/features/automerge/) is
        disabled, an `IdentityConstraintException` is thrown.

        :param subject_locator: the subject locator to be added
        :type subject_locator: `Locator`

        """
        if subject_locator is None:
            raise ModelConstraintException(
                self, 'The subject locator may not be None')
        address = subject_locator.to_external_form()
        try:
            topic = self.topic_map.topic_constructs.get(
                subject_locators__address=address)
            if topic == self:
                return
            elif self.topic_map.topic_map_system.get_feature(
                AUTOMERGE_FEATURE_STRING):
                self.merge_in(topic)
            else:
                raise IdentityConstraintException(
                    self, topic, subject_locator, 'Another topic has the same subject locator and automerge is disabled')
        except Topic.DoesNotExist:
            sl = SubjectLocator(topic=self, address=address,
                                containing_topic_map=self.topic_map)
            sl.save()
            self.subject_locators.add(sl)

    def add_type (self, type):
        """Adds a type to this topic.

        :param type: the type of which this topic should become an instance
        :type type: `Topic`

        """
        if type is None:
            raise ModelConstraintException(self, 'The type may not be None')
        if self.topic_map != type.topic_map:
            raise ModelConstraintException(
                self, 'The type is not from the same topic map')
        self.types.add(type)

    def create_name (self, value, name_type=None, scope=None, proxy=Name):
        """Creates a `Name` for this topic with the specified `value`,
        `type` and `scope`.

        If `name_type` is None, the created `Name` will have the default
        name type (a `Topic` with the subject identifier
        http://psi.topicmaps.org/iso13250/model/topic-name).

        If `scope` is None or an empty list, the name will be in the
        unconstrained scope.

        :param value: the string value of the name
        :type value: string
        :param name_type: the name type
        :type name_type: `Topic`
        :param scope: a list of themes
        :type scope: `Topic` or list of `Topic`s
        :param proxy: Django proxy model
        :type proxy: class
        :rtype: `Name`

        """
        if value is None:
            raise ModelConstraintException(self, 'The value may not be None')
        if name_type is None:
            name_type = self.topic_map.create_topic_by_subject_identifier(
                Locator('http://psi.topicmaps.org/iso13250/model/topic-name'))
        elif self.topic_map != name_type.topic_map:
            raise ModelConstraintException(
                self, 'The type is not from the same topic map')
        name = proxy(topic=self, value=value, topic_map=self.topic_map,
                    type=name_type)
        name.save()
        if scope is not None:
            if type(scope) not in (type([]), type(())):
                scope = [scope]
            for theme in scope:
                if self.topic_map != theme.topic_map:
                    raise ModelConstraintException(
                        self, 'The theme is not from the same topic map')
                name.scope.add(theme)
        return name

    def create_occurrence (self, type, value, scope=None, datatype=None,
                           proxy=Occurrence):
        """Creates an `Occurrence` for this topic with the specified
        `type`, `value`, and `scope`.

        If `datatype` is not None, the newly created `Occurrence` will
        have the datatype specified by `datatype`.

        :param type: the occurrence type
        :type type: `Topic`
        :param value: the value of the occurrence
        :type value: String or `Locator`
        :param scope: optional list of themes
        :type scope: list of `Topic`s
        :param datatype: optional locator indicating the datatype of `value`
        :type datatype: `Locator`
        :param proxy: Django proxy model
        :type proxy: class
        :rtype: `Occurrence`

        """
        if type is None:
            raise ModelConstraintException(self, 'The type may not be None')
        if value is None:
            raise ModelConstraintException(self, 'The value may not be None')
        if datatype is None:
            if isinstance(value, Locator):
                datatype = Locator(XSD_ANY_URI)
            elif isinstance(value, float):
                datatype = Locator(XSD_FLOAT)
            elif isinstance(value, int):
                datatype = Locator(XSD_INT)
            else:
                datatype = Locator(XSD_STRING)
        if self.topic_map != type.topic_map:
            raise ModelConstraintException(
                self, 'The type is not from the same topic map')
        occurrence = proxy(type=type, value=value,
                           datatype=datatype.to_external_form(),
                           topic=self, topic_map=self.topic_map)
        occurrence.save()
        if scope is not None:
            for theme in scope:
                if self.topic_map != theme.topic_map:
                    raise ModelConstraintException(
                        self, 'The theme is not from the same topic map')
                occurrence.scope.add(theme)
        return occurrence

    @models.permalink
    def get_absolute_url (self):
        return ('tmapi_topic_display', (), {'topic_id': self.id})

    def get_names (self, name_type=None):
        """Returns a QuerySet of the names of this topic.

        If `name_type` is not None, only names of the specified
        type are returned.

        :param name_type: the type of the `Name`s to be returned
        :type name_type: `Topic`
        :rtype: `QuerySet` of `Name`s

        """
        if name_type is None:
            return self.names.all()
        else:
            return self.names.filter(type=name_type)

    def get_occurrences (self, occurrence_type=None, proxy=None):
        """Returns the `Occurrence`s of this topic.

        If `occurrence_type` is not None, returns the `Occurrence`s of
        this topic where the occurrence type is `occurrence_type`.

        :param occurrence_type: the type of the `Occurrence`s to be returned
        :type occurrence_type: `Topic`
        :param proxy: Django proxy model
        :type proxy: class
        :rtype: `QuerySet` of `Occurrence`s

        """
        if proxy is not None:
            occurrences = proxy.objects.filter(topic=self)
            if occurrence_type is not None:
                occurrences = occurrences.filter(type=occurrence_type)
        else:
            if occurrence_type is None:
                occurrences = self.occurrences.all()
            else:
                occurrences = self.occurrences.filter(type=occurrence_type)
        return occurrences

    def get_parent (self):
        """Returns the `TopicMap` to which this topic belongs.

        :rtype: `TopicMap`

        """
        return self.topic_map

    def get_reified (self):
        """Returns the `Construct` which is reified by this topic.

        :rtype: `Construct` or None

        """
        reified = None
        reifiable_types = ('association', 'name', 'occurrence', 'role',
                           'topicmap', 'variant')
        for reifiable_type in reifiable_types:
            try:
                reified = getattr(self, 'reified_' + reifiable_type)
                break
            except:
                pass
        return reified

    def get_roles_played (self, role_type=None, association_type=None):
        """Returns the roles played by this topic.

        If `role_type` is not None, returns the roles played by this
        topic where the role type is `role_type`.

        If `role_type` and `association_type` are not None, returns
        the roles played by this topic where the role type is
        `role_type` and the association type is `association_type`.

        :param role_type: the type of the `Role`s to be returned
        :type role_type: `Topic` or None
        :param association_type: the type of the `Association` of
          which the returned roles must be part
        :type association_type: `Topic` or None
        :rtype: `QuerySet` of `Role`s

        """
        roles = []
        if role_type is not None:
            roles = self.roles.filter(type=role_type)
            if association_type is not None:
                roles = roles.filter(association__type=association_type)
        elif association_type is not None:
            raise Exception('This is a broken call to get_roles_played, specifying an assocation type but not a role type')
        else:
            roles = self.roles.all()
        return roles

    def get_subject_identifiers (self):
        """Returns the subject identifiers assigned to this topic.

        :rtype: `QuerySet` of `Locator`s

        """
        return self.subject_identifiers.all()

    def get_subject_locators (self):
        """Returns the subject locators assigned to this topic.

        :rtype: `QuerySet` of `Locator`s

        """
        return self.subject_locators.all()

    def get_types (self):
        """Returns a QuerySet containing the types of which this topic
        is an instance.

        :rtype: `QuerySet` of `Topic`s

        """
        return self.types.all()

    def merge_in (self, other):
        """Merges another topic into this topic.

        Merging a topic into this topic causes this topic to gain all
        of the characteristics of the other topic and to replace the
        other topic wherever it is used as type, theme, or
        reifier. After this method completes, `other` will have been
        removed from the `TopicMap`.

        If `self` equals `other` no changes are made to the topic.

        NOTE: The other topic must belong to the same `TopicMap`
        instance as this topic.

        :param other: the topic to be merged into this topic
        :type other: `Topic`

        """
        if other is None:
            raise ModelConstraintException(
                self, 'The topic to merge in may not be None')
        if other == self:
            return
        if self.topic_map != other.topic_map:
            raise ModelConstraintException(
                self, 'The topic to merge in is not from the same topic map')
        other_reified = other.get_reified()
        if self.get_reified() is not None and other_reified is not None:
            raise ModelConstraintException(
                self, 'Both topics are being used as reifiers')
        if other_reified is not None:
            other_reified.set_reifier(self)
        for topic_type in other.get_types():
            self.add_type(topic_type)
        for subject_identifier in other.get_subject_identifiers():
            subject_identifier.topic = self
            subject_identifier.save()
        for subject_locator in other.get_subject_locators():
            subject_locator.topic = self
            subject_locator.save()
        for item_identifier in other.get_item_identifiers():
            other.item_identifiers.remove(item_identifier)
            self.item_identifiers.add(item_identifier)
        signatures = {}
        for name in self.get_names():
            signature = generate_name_signature(name)
            signatures[signature] = name
        for name in other.get_names():
            signature = generate_name_signature(name)
            existing = signatures.get(signature)
            if existing is not None:
                handle_existing_construct(name, existing)
                move_variants(name, existing)
                name.remove()
            else:
                name.topic = self
                name.save()
        signatures = {}
        for occurrence in self.get_occurrences():
            signature = generate_occurrence_signature(occurrence)
            signatures[signature] = occurrence
        for occurrence in other.get_occurrences():
            signature = generate_occurrence_signature(occurrence)
            existing = signatures.get(signature)
            if existing is not None:
                handle_existing_construct(occurrence, existing)
                occurrence.remove()
            else:
                occurrence.topic = self
                occurrence.save()
        signatures = {}
        for role in self.get_roles_played():
            parent = role.get_parent()
            signature = generate_association_signature(parent)
            signatures[signature] = parent
        for role in other.get_roles_played():
            role.set_player(self)
            parent = role.get_parent()
            signature = generate_association_signature(parent)
            existing = signatures.get(signature)
            if existing is not None:
                handle_existing_construct(parent, existing)
                move_role_characteristics(parent, existing)
                parent.remove()
        other.remove()

    def remove (self):
        """Removes this topic from the containing `TopicMap` instance.

        This method throws a `TopicInUseException` if the topic plays
        a `Role`, is used as type of a `Typed` construct, or if it is
        used as a theme for a `Scoped` construct, or if it reifies a
        `Reifiable`.

        """
        if self.roles.count():
            raise TopicInUseException(self, 'This topic is used as a player')
        if self.get_reified() is not None:
            raise TopicInUseException(self, 'This topic is used as a reifier')
        if self._has_scoped_constructs():
            raise TopicInUseException(self, 'This topic is used as a theme')
        if self._has_typed_constructs():
            raise TopicInUseException(self, 'This topic is used as a type')
        super(Topic, self).remove()

    def remove_subject_identifier (self, subject_identifier):
        """Removes a subject identifer from this topic.

        :param subject_identifier: the subject identifier to be remove
          from this topic
        :type subject_identifier: `Locator`

        """
        try:
            si = SubjectIdentifier.objects.get(
                topic=self, address=subject_identifier.to_external_form())
            si.delete()
        except SubjectIdentifier.DoesNotExist:
            pass

    def remove_subject_locator (self, subject_locator):
        """Removes a subject locator from this topic.

        :param subject_locator: the subject locator to be removed from
          this topic
        :type subject_locator: `Locator`

        """
        try:
            sl = SubjectLocator.objects.get(
                topic=self, address=subject_locator.to_external_form())
            sl.delete()
        except SubjectLocator.DoesNotExist:
            pass

    def remove_type (self, topic_type):
        """Removes a type from this topic.

        :param topic_type: the type to be removed from this topic
        :type topic_type: `Topic`

        """
        self.types.remove(topic_type)

    def _has_scoped_constructs (self):
        """Returns True if there are constructs scoped by this topic.

        :rtype: Boolean

        """
        has_scoped_constructs = False
        scopable_types = ('associations', 'names', 'occurrences', 'variants')
        for scopable_type in scopable_types:
            if getattr(self, 'scoped_' + scopable_type).count():
                has_scoped_constructs = True
                break
        return has_scoped_constructs

    def _has_typed_constructs (self):
        """Returns True if there are constructs typed by this topic.

        :rtype: Boolean

        """
        has_typed_constructs = False
        typable_types = ('associations', 'names', 'occurrences', 'roles',
                         'topics')
        for typable_type in typable_types:
            if getattr(self, 'typed_' + typable_type).count():
                has_typed_constructs = True
                break
        return has_typed_constructs
