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

from tmapi.exceptions import IdentityConstraintException, \
    ModelConstraintException

from .item_identifier import ItemIdentifier


class Construct:

    # Properly item_identifier and topic_map fields should be defined
    # here. However, due to inheritance, this causes Django problems,
    # and so they are defined separately in ConstructFields and the
    # specific models inherit from that class directly.

    def add_item_identifier (self, item_identifier):
        """Adds an item identifier.

        It is not allowed to have two `Construct`s in the same
        `TopicMap` with the same item identifier. If the two objects
        are `Topic`s, then they must be merged. If at least one of the
        two objects is not a `Topic`, an `IdentityConstraintException`
        must be reported.

        :param item_identifier: the item identifier to be added
        :type item_identifier: `Locator`
        :raises `IdentityConstraintException`: if another construct
          has an item identifier which is equal to `item_identifier`

        """
        if item_identifier is None:
            raise ModelConstraintException(
                self, 'The item identifier may not be None')
        address = item_identifier.to_external_form()
        topic_map = self.get_topic_map()
        try:
            ii = ItemIdentifier.objects.get(address=address,
                                            containing_topic_map=topic_map)
            construct = ii.get_construct()
            if construct == self:
                return
            # While an ItemIdentifier may legitimately (in the
            # database's terms) exist while not being associated with
            # any constructs, the only valid ways to remove an item
            # identifier from a construct (remove_item_identifier()
            # and remove()) delete the item identifier. Therefore,
            # raise an exception without checking that construct is
            # not None.
            raise IdentityConstraintException(
                self, ii.get_construct(), item_identifier,
                'This item identifier is already associated with another construct')
        except ItemIdentifier.DoesNotExist:
            ii = ItemIdentifier(address=address,
                                containing_topic_map=topic_map)
            ii.save()
            self.item_identifiers.add(ii)

    def get_id (self):
        """Returns the identifier of this construct.

        This property has no representation in the Topic Maps - Data Model.

        The ID can be anything, so long as no other `Construct` in the
        same topic map has the same ID.

        :rtype: String

        """
        return self.identifier.pk

    def get_item_identifiers (self):
        """Returns the item identifiers of this Topic Maps construct.

        :rtype: `QuerySet` of `Locator`s

        """
        return self.item_identifiers.all()

    def get_parent (self):
        """Returns the parent of this construct.

        This method returns None iff this construct is a `TopicMap`
        instance.

        """
        raise NotImplementedError

    def get_topic_map (self, proxy=None):
        """Returns the `TopicMap` instance to which this Topic Maps
        construct belongs.

        A `TopicMap` instance returns itself.

        :rtype: `TopicMap`

        """
        if proxy is None:
            topic_map = self.topic_map
        else:
            topic_map = proxy.objects.get(pk=self.topic_map.id)
        return topic_map

    def remove (self):
        """Deletes this construct from its parent container.

        After invocation of this method, the construct is in an
        undefined state and must not be used further.

        """
        # item identifiers are joined to a construct in a many to many
        # relationship, so they need to be explicitly deleted.
        self.get_item_identifiers().delete()
        self.delete()

    def remove_item_identifier (self, item_identifier):
        """Remove an item identifier.

        :param item_identifier: the item identifier to be removed from
          this construct
        :type item_identifier: `Locator`

        """
        address = item_identifier.to_external_form()
        try:
            topic_map = self.topic_map
        except AttributeError:
            topic_map = self
        try:
            ii = ItemIdentifier.objects.get(
                address=address, containing_topic_map=topic_map)
            ii.delete()
        except ItemIdentifier.DoesNotExist:
            pass
