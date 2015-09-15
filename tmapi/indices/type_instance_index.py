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

from django.db.models import Q

from tmapi.indices.index import Index
from tmapi.models import Name, Occurrence, Role, Topic


class TypeInstanceIndex (Index):

    """Index for type-instance relationships between `Topic`s and for
    `Typed` Topic Maps constructs.

    This index provides access to `Topic`s used in type-instance
    relationships or as type of a `Typed` construct. Further, the
    retrieval of `Association`s, `Role`s, `Occurrence`s and `Name`s by
    their `type` property is supported.

    """

    def get_associations (self, association_type):
        """Returns the associations in the topic map whose type
        property equals `topic_type`.

        The return value may be empty but must never be None.

        :param topic_type: the type of the `Association`s to be returned
        :type association_type: `Topic`
        :rtype: `QuerySet` of `Association`s

        """
        return self.topic_map.get_associations().filter(type=association_type)

    def get_association_types (self):
        """Returns the topics in the topic map used in the type
        property as `Association`s.

        The return value may be empty but must never be None.

        :rtype: `QuerySet` of `Topic`s

        """
        return self.topic_map.get_topics().exclude(typed_associations=None)

    def get_names (self, name_type):
        """Returns the topic names in the topic map whose type
        property equals `name_type`.

        The return value may be empty but must never be None.

        :param name_type: the type of the `Name`s to be returned
        :type name_type: `Topic`
        :rtype: `QuerySet` of `Name`s

        """
        return Name.objects.filter(topic__topic_map=self.topic_map).filter(
            type=name_type)

    def get_name_types (self):
        """Returns the topics in the topic map used in the type
        property of `Name`s.

        The return value may be empty but must never be None.

        :rtype: `QuerySet` of `Topic`s

        """
        return self.topic_map.get_topics().exclude(typed_names=None)

    def get_occurrences (self, occurrence_type):
        """Returns the occurrences in the topic map whose type
        property equals `occurrence_type`.

        The return value may be empty but must never be None.

        :param occurrence_type: the type of the `Occurrence`s to be returned
        :type occurrence_type: `Topic`
        :rtype: `QuerySet` of `Occurrence`s

        """
        return Occurrence.objects.filter(
            topic__topic_map=self.topic_map).filter(type=occurrence_type)

    def get_occurrence_types (self):
        """Returns the topics in the topic map used in the type
        property of `Occurrence`s.

        The return value may be empty but must never be None.

        :rtype: `QuerySet` of `Topic`s

        """
        return self.topic_map.get_topics().exclude(typed_occurrences=None)

    def get_roles (self, role_type):
        """Returns the roles in the topic map whose type property
        equals `role_type`.

        The return value may be empty but must never be None.

        :param role_type: the type of the `Role`s to be returned
        :type role_type: `Topic`
        :rtype: `QuerySet` of `Role`s

        """
        return Role.objects.filter(topic_map=self.topic_map).filter(
            type=role_type)

    def get_role_types (self):
        """Returns the topics in the topic map used in the type
        property of `Role`s.

        The return value may be empty but must never be None.

        :rtype: `QuerySet` of `Topic`s

        """
        return self.topic_map.get_topics().exclude(typed_roles=None)

    def get_topics (self, topic_types=None, match_all=False):
        """Returns the topics which are an instance of at least one of
        the specified `topic_types`, or all topics which are not an
        instance of another topic (iff `topic_types` is None).

        If `match_all` is True, a topic must be an instance of all
        `topic_types`; if False, the topic must be an instace of at
        least one type.

        The return value may be empty but must never by None.

        :param topic_types: types of the `Topic`s to be returned
        :type topic_types: `Topic` or list of `Topic`s
        :param match_all: whether a topic must be an instance of only
          one or all `topic_types`
        :type match_all: boolean
        :rtype: `QuerySet` of `Topic`s

        """
        topics = self.topic_map.get_topics()
        if topic_types is not None:
            if isinstance(topic_types, Topic):
                topics = topics.filter(types=topic_types)
            elif match_all:
                for topic_type in topic_types:
                    topics = topics.filter(types=topic_type)
            else:
                query = None
                for topic_type in topic_types:
                    if query is None:
                        query = Q(types=topic_type)
                    else:
                        query = query | Q(types=topic_type)
                topics = topics.filter(query)
        else:
            # Return all topics that are not an instance of another
            # topic.
            topics = topics.filter(types=None)
        return topics.distinct()

    def get_topic_types (self):
        """Returns the topics in the topic map that are used as type
        in a type-instance relationship.

        :rtype: `QuerySet` of `Topic`s

        """
        return self.topic_map.get_topics().exclude(typed_topics=None)
