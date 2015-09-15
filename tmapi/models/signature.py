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

"""Module containing functions for generating signatures for Topic
Maps constructs.

These functions can be used to detect duplicates: if two Topic Maps
constructs have the same signature, they should be merged (if they
belong to the same parent).

Neither the topic map, the parent, the reifier, nor item identifiers
are accounted for in generating the signature.

It is a port of the Java code written by Lars Heuer for the tinyTiM
project (http://tinytim.sourceforget.net/).

"""

from .name import Name


def generate_association_signature (association):
    """Generates the signature for an association.

    :param association: the association to generate the signature for
    :type association: `Assocation`
    :rtype: tuple

    """
    return (_generate_type_signature(association),
            _generate_scope_signature(association),
            _generate_roles_signature(association.get_roles()))

def generate_name_signature (name):
    """Generates the signature for the specified name.

    The parent and the variants are not taken into account.

    :param name: the name to generate the signature for
    :type name: `Name`
    :rtype: tuple

    """
    return (_generate_type_signature(name),
            _generate_scope_signature(name),
            _generate_data_signature(name))

def generate_occurrence_signature (occurrence):
    """Generates the signature for an occurrence.

    :param occurrence: the occurrence to generate the signature for
    :type occurrence: `Occurrence`
    :rtype: tuple

    """
    return (_generate_type_signature(occurrence),
            _generate_scope_signature(occurrence),
            _generate_data_signature(occurrence))

def generate_role_signature (role):
    """Generates the signature for a role.

    :param role: the role to generate the signature for
    :type role: `Role`
    :rtype: tuple

    """
    return (_signature(role.get_type()), _signature(role.get_player()))

def generate_variant_signature (variant):
    """Generates the signature for the specified `variant`.

    :param variant: the variant to generate the signature for
    :type variant: `Variant`
    :rtype: tuple

    """
    return (_generate_scope_signature(variant),
            _generate_data_signature(variant))

def _generate_data_signature (construct):
    """Returns the signature for a value/datatype pair.

    :param construct: the construct to generate the signature for
    :type construct: `Occurrence` or `Variant`
    :rtype: tuple

    """
    if isinstance(construct, Name):
        datatype = None
    else:
        datatype = hash(construct.get_datatype().to_external_form())
    return (datatype, hash(construct.get_value()))

def _generate_roles_signature (roles):
    """Returns the signature for the specified roles.

    :param roles: the roles to generate the signature for
    :type roles: `QuerySet` of `Role`s
    :rtype: frozenset

    """
    if len(roles) == 0:
        return 0
    signature = []
    for role in roles:
        signature.append(generate_role_signature(role))
    return frozenset(signature)

def _generate_scope_signature (scoped):
    """Returns the signature for the scope of a scoped Topic Maps
    construct.

    This function returns the signature for the scope only. No other
    properties of the scoped construct are taken into account.

    :param scoped: the scoped Topic Maps construct
    :type scoped: `Scoped`
    :rtype: frozenset

    """
    return frozenset(scoped.get_scope())

def _generate_type_signature (typed):
    """Returns the signature for the type of a typed Topic Maps construct.

    :param typed: the typed Topic Maps construct
    :type typed: `Typed`
    :rtype: integer

    """
    return _signature(typed.get_type())

def _signature (topic):
    """Returns the signature of the specified topic.

    :param topic: the topic to generate the signature for
    :type topic: `Topic`
    :rtype: integer

    """
    return topic.id
