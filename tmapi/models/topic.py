"""Module defining the Topic model and its managers."""

from django.db import models

from tmapi.constants import XSD_ANY_URI, XSD_STRING
from tmapi.exceptions import ModelConstraintException

from construct import Construct
from construct_fields import ConstructFields
from locator import Locator
from name import Name
from subject_identifier import SubjectIdentifier
from subject_locator import SubjectLocator
from occurrence import Occurrence


class Topic (Construct, ConstructFields):

    """Represents a topic item."""
    
    types = models.ManyToManyField('self', symmetrical=False, blank=True,
                                   related_name='type_instances')

    class Meta:
        app_label = 'tmapi'

    def add_subject_identifier (self, subject_identifier):
        """Adds a subject identifier to this topic.

        :param subject_identifier: the subject identifier to be added
        :type subject_identifier: `Locator`
        
        """
        if subject_identifier is None:
            raise ModelConstraintException
        si = SubjectIdentifier(topic=self,
                               address=subject_identifier.to_external_form())
        si.save()
        self.subject_identifiers.add(si)

    def add_subject_locator (self, subject_locator):
        """Adds a subject locator to this topic.

        :param subject_locator: the subject locator to be added

        """
        if subject_locator is None:
            raise ModelConstraintException
        sl = SubjectLocator(topic=self,
                            address=subject_locator.to_external_form())
        sl.save()
        self.subject_locators.add(sl)
    
    def add_type (self, type):
        """Adds a type to this topic.

        :param type: the type of which this topic should become an instance
        :type type: `Topic`
        
        """
        if type is None:
            raise ModelConstraintException
        if self.topic_map != type.topic_map:
            raise ModelConstraintException
        self.types.add(type)

    def create_name (self, value, type=None, scope=None):
        """Creates a `Name` for this topic with the specified `value`,
        `type` and `scope`.

        If `type` is None, the created `Name` will have the default
        name type (a `Topic` with the subject identifier
        http://psi.topicmaps.org/iso13250/model/topic-name).

        If `scope` is None or an empty list, the name will be in the
        unconstrained scope.

        :param value: the string value of the name
        :type value: string
        :param type: the name type
        :type type: `Topic`
        :param scope: a list of themes
        :type scope: list
        :rtype: `Name`

        """
        if value is None:
            raise ModelConstraintException
        if type is None:
            type = self.topic_map.create_topic_by_subject_identifier(
                Locator('http://psi.topicmaps.org/iso13250/model/topic-name'))
        elif self.topic_map != type.topic_map:
            raise ModelConstraintException
        name = Name(topic=self, value=value, topic_map=self.topic_map,
                    type=type)
        name.save()
        if scope is not None:
            for theme in scope:
                if self.topic_map != theme.topic_map:
                    raise ModelConstraintException
                name.scope.add(theme)
        return name

    def create_occurrence (self, type, value, scope=None, datatype=None):
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
        :rtype: `Occurrence`
        
        """
        if type is None:
            raise ModelConstraintException
        if value is None:
            raise ModelConstraintException
        if datatype is None:
            if isinstance(value, Locator):
                datatype = Locator(XSD_ANY_URI)
            else:
                datatype = Locator(XSD_STRING)
        if self.topic_map != type.topic_map:
            raise ModelConstraintException
        occurrence = Occurrence(type=type, value=value,
                                datatype=datatype.to_external_form(),
                                topic=self, topic_map=self.topic_map)
        occurrence.save()
        if scope is not None:
            for theme in scope:
                if self.topic_map != theme.topic_map:
                    raise ModelConstraintException
                occurrence.scope.add(theme)
        return occurrence
    
    def get_names (self, name_type=None):
        """Returns a QuerySet of the names of this topic.

        If `name_type` is not None, only names of the specified
        type are returned.

        :param name_type: the type of the `Name`s to be returned
        
        """
        if name_type is None:
            return self.names.all()
        else:
            return self.names.filter(type=name_type)

    def get_occurrences (self, occurrence_type=None):
        """Returns the `Occurrence`s of this topic.

        If occurrence_type is not None, returns the `Occurrence`s of
        this topic where the occurrence type is `occurrence_type`.

        :param occurrence_type: the type of the `Occurrence`s to be returned

        """
        if occurrence_type is None:
            return self.occurrences.all()
        else:
            return self.occurrences.filter(type__pk=occurrence_type.id)

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
        reifiable_types = (
            'reified_association', 'reified_name', 'reified_occurrence',
            'reified_role', 'reified_topicmap', 'reified_variant')
        for reifiable_type in reifiable_types:
            try:
                reified = getattr(self, reifiable_type)
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
        
        """
        roles = []
        if role_type is not None:
            roles = self.role_players.filter(type=role_type)
            if association_type is not None:
                roles = roles.filter(association__type=association_type)
        elif association_type is not None:
            raise Exception('This is a broken call to get_roles_played, specifying an assocation type but not a role type')
        else:
            roles = self.role_players.all()
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
        is an instance."""
        return self.types.all()

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
