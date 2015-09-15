# Copyright 2011 Jamie Norrish (jamie@artefact.org.nz)
# Copyright 2008 - 2010 Lars Heuer (heuer[at]semagia.com)
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

"""This module provides functions to copy Topic Maps constructs from
one topic map to another without creating duplicates (ie, merging
where appropriate).

It is a port of the Java code written by Lars Heuer for the tinyTiM
project (http://tinytim.sourceforget.net/).

"""

from .topic import Topic
from .merge_utils import move_role_characteristics
from .signature import generate_association_signature, generate_name_signature, \
    generate_occurrence_signature, generate_variant_signature

def copy (source, target):
    """Copies the topics and associations from the `source` to the
    `target` topic map.

    :param source: the topic map to take the topics and associations from
    :type source: `TopicMap`
    :param target: the topic map to receive the topics and associations
    :type target: `TopicMap`

    """
    if source == target:
        return
    merge_map = {}
    for topic in source.get_topics():
        for slo in topic.get_subject_locators():
            existing = target.get_topic_by_subject_locator(slo)
            if existing is not None:
                _add_merge(topic, existing, merge_map)
        for sid in topic.get_subject_identifiers():
            existing = target.get_topic_by_subject_identifier(sid)
            if existing is not None:
                _add_merge(topic, existing, merge_map)
            existing_construct = target.get_construct_by_item_identifier(sid)
            if isinstance(existing_construct, Topic):
                _add_merge(topic, existing_construct, merge_map)
        for iid in topic.get_item_identifiers():
            existing_construct = target.get_construct_by_item_identifier(iid)
            if isinstance(existing_construct, Topic):
                _add_merge(topic, existing_construct, merge_map)
            existing = target.get_topic_by_subject_identifier(iid)
            if existing is not None:
                _add_merge(topic, existing, merge_map)
    source_reifier = source.get_reifier()
    target_reifier = target.get_reifier()
    if source_reifier is not None and target_reifier is not None:
        _add_merge(source_reifier, target_reifier, merge_map)
    for topic in source.get_topics():
        if topic not in merge_map:
            _copy_topic(topic, target, merge_map)
    for topic in merge_map:
        target_topic = merge_map.get(topic)
        _copy_identities(topic, target_topic)
        _copy_types(topic, target_topic, merge_map)
        _copy_characteristics(topic, target_topic, merge_map)
    _copy_associations(source, target, merge_map)

def _add_merge (source, target, merge_map):
    """Adds a mapping from `source` to `target` into the `merge_map`.

    If `source` already has a mapping to another target topic,
    `target` is merged with the existing target topic.

    :param source: the source topic
    :type source: `Topic`
    :param target: the target topic
    :type target: `Topic`
    :param merge_map: the map that holds the merge mappings
    :type merge_map: dictionary

    """
    previous_target = merge_map.get(source)
    if previous_target is not None:
        if previous_target != target:
            previous_target.merge_in(target)
    else:
        merge_map[source] = target

def _copy_associations (source, target, merge_map):
    """Copies the associations from `source` topic map to `target`
    topic map.

    :param source: the topic map to take the associations from
    :type source: `TopicMap`
    :param target: the topic map that receives the associations
    :type target: `TopicMap`
    :param merge_map: the map that holds the merge mappings
    :type merge_map: dictionary

    """
    signatures = {}
    for association in target.get_associations():
        signature = generate_association_signature(association)
        signatures[signature] = association
    for association in source.get_associations():
        association_type = _copy_type(association, target, merge_map)
        scope = _copy_scope(association, target, merge_map)
        target_association = target.create_association(association_type, scope)
        for role in association.get_roles():
            role_type = _copy_type(role, target, merge_map)
            source_player = role.get_player()
            if source_player in merge_map:
                player = merge_map.get(source_player)
            else:
                player = _copy_topic(source_player, target, merge_map)
            target_role = target_association.create_role(role_type, player)
            _copy_item_identifiers(role, target_role)
            _copy_reifier(role, target_role, merge_map)
        signature = generate_association_signature(target_association)
        existing = signatures.get(signature)
        if existing is not None:
            move_role_characteristics(target_association, existing)
            target_association.remove()
            target_association = existing
        _copy_reifier(association, target_association, merge_map)
        _copy_item_identifiers(association, target_association)

def _copy_characteristics (topic, target_topic, merge_map):
    """Copies the occurrences and names from `topic` to the `target_topic`.

    :param topic: the topic to take the characteristics from
    :type topic: `Topic`
    :param target_topic: the topic that receives the characteristics
    :type target_topic: `Topic`
    :param merge_map: the map that holds the merge mappings
    :type merge_map: dictionary

    """
    signatures = {}
    for occurrence in target_topic.get_occurrences():
        signature = generate_occurrence_signature(occurrence)
        signatures[signature] = occurrence
    topic_map = target_topic.get_topic_map()
    for occurrence in topic.get_occurrences():
        occ_type = _copy_type(occurrence, topic_map, merge_map)
        scope = _copy_scope(occurrence, topic_map, merge_map)
        target_occurrence = target_topic.create_occurrence(
            occ_type, occurrence.get_value(), scope, occurrence.get_datatype())
        signature = generate_occurrence_signature(target_occurrence)
        existing = signatures.get(signature)
        if existing is not None:
            target_occurrence.remove()
            target_occurrence = existing
        _copy_reifier(occurrence, target_occurrence, merge_map)
        _copy_item_identifiers(occurrence, target_occurrence)
    signatures = {}
    for name in target_topic.get_names():
        signature = generate_name_signature(name)
        signatures[signature] = name
    for name in topic.get_names():
        name_type = _copy_type(name, topic_map, merge_map)
        scope = _copy_scope(name, topic_map, merge_map)
        target_name = target_topic.create_name(name.get_value(), name_type,
                                               scope)
        signature = generate_name_signature(target_name)
        existing = signatures.get(signature)
        if existing is not None:
            target_name.remove()
            target_name = existing
        _copy_reifier(name, target_name, merge_map)
        _copy_item_identifiers(name, target_name)
        _copy_variants(name, target_name, merge_map)

def _copy_identities (topic, target_topic):
    """Copies the identities (item identifiers, subject identifiers
    and subject locators) from the `source` to the `target_topic`.

    :param topic: the topic to take the identities from
    :type topic: `Topic`
    :param target_topic: the topic that receives the identities
    :type target_topic: `Topic`

    """
    for sid in topic.get_subject_identifiers():
        target_topic.add_subject_identifier(sid)
    for slo in topic.get_subject_locators():
        target_topic.add_subject_locator(slo)
    _copy_item_identifiers(topic, target_topic)

def _copy_item_identifiers (source, target):
    """Copies the item identifiers from `source` to `target`.

    :param source: the Topic Maps construct to take the item identifiers from
    :type source: `Construct`
    :param target: the Topic Maps construct that receives the item identifiers
    :type target: `Construct`

    """
    for iid in source.get_item_identifiers():
        target.add_item_identifier(iid)

def _copy_reifier (source, target, merge_map):
    """Copies the reifier of `source` to the `target`.

    :param source: the reifiable Topic Maps construct to take the reifier from
    :type source: `Reifiable`
    :param target: the target Topic Maps construct that receives the reifier
    :type target: `Reifiable`
    :param merge_map: the map that holds the merge mappings
    :type merge_map: dictionary

    """
    source_reifier = source.get_reifier()
    if source_reifier is not None:
        if source_reifier in merge_map:
            reifier = merge_map.get(source_reifier)
        else:
            reifier = _copy_topic(source_reifier, target.get_topic_map(),
                                  merge_map)
        target.set_reifier(reifier)

def _copy_scope (source, topic_map, merge_map):
    """Copes and returns all themes from `source` into `topic_map`.

    :param source: the source to take the scope from
    :type source: `Scoped`
    :param topic_map: the Topic Map that receives the scope
    :type topic_map: `TopicMap`
    ::param merge_map: the map that holds the merge mappings
    :type merge_map: dictionary
    :rtype:

    """
    themes = []
    for source_theme in source.get_scope():
        if source_theme in merge_map:
            theme = merge_map.get(source_theme)
        else:
            theme = _copy_topic(source_theme, topic_map, merge_map)
        themes.append(theme)
    return themes

def _copy_topic (topic, target, merge_map):
    """Copies the `topic` to the `target` topic map.

    Returns the newly created topic.

    :param topic: the topic to copy
    :type topic: `Topic`
    :param target: the target topic map
    :type target: `TopicMap`
    :param merge_map: the map that holds the merge mappings
    :type merge_map: dictionary
    :rtype: `Topic`

    """
    target_topic = target.create_empty_topic()
    _copy_identities(topic, target_topic)
    _copy_types(topic, target_topic, merge_map)
    _copy_characteristics(topic, target_topic, merge_map)
    return target_topic

def _copy_type (source, topic_map, merge_map):
    """Copies and returns the type of `source` into `topic_map`.

    :param source: the Topic Maps construct to take the type from
    :type source: `Typed`
    :param topic_map: the Topic Map that receives the type
    :type topic_map: `TopicMap`
    :param merge_map: the map that holds the merge mappings
    :type merge_map: dictionary
    :rtype: `Topic`

    """
    source_type = source.get_type()
    if source_type in merge_map:
        target_type = merge_map.get(source_type)
    else:
        target_type = _copy_topic(source_type, topic_map, merge_map)
    return target_type

def _copy_types (topic, target_topic, merge_map):
    """Copes the types from the `topic` to the `target_topic`.

    :param topic: the topic to take the types from
    :type topic: `Topic`
    :param target_topic: the topic that receives the types
    :type target_topic: `Topic`
    :param merge_map: the map that holds the merge mappings
    :type merge_map: dictionary

    """
    for topic_type in topic.get_types():
        target_type = merge_map.get(topic_type)
        if target_type is None:
            target_type = _copy_topic(type, target_topic.get_topic_map(),
                                      merge_map)
        target_topic.add_type(target_type)

def _copy_variants (source, target, merge_map):
    """Copies the variants from `source` to `target`.

    :param source: the name to take the variants from
    :type source: `Name`
    :param target: the name that receives the variants
    :type target: `Name`
    :merge_map: the map that holds the merge mappings
    :type merge_map: dictionary

    """
    signatures = {}
    for variant in target.get_variants():
        signature = generate_variant_signature(variant)
        signatures[signature] = variant
    topic_map = target.get_topic_map()
    for variant in source.get_variants():
        scope = _copy_scope(variant, topic_map, merge_map)
        target_variant = target.create_variant(variant.get_value(), scope,
                                               variant.get_datatype())
        signature = generate_variant_signature(target_variant)
        existing = signatures.get(signature)
        if existing is not None:
            target_variant.remove()
            target_variant = existing
        _copy_reifier(variant, target_variant, merge_map)
        _copy_item_identifiers(variant, target_variant)
