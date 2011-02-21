"""Module containing utility functions for merging topics."""

from name import Name


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

def handle_existing_construct (source, target):
    """Moves the item identifiers and reifier from `source` to
    `target`.

    If the `source` is reifier, `target`'s reifier is set to the
    source reifier unless `target_reifier` is not None. If `source`
    and `target` are reified, the reifiers are merged.

    :param source: the source Topic Maps construct
    :type source: `Construct`
    :param target: the target Topic Maps construct
    :type target: `Construct`
    :param target_reifier: the target's reifier
    :type target_reifier: `Topic` or None

    """
    # Handle item identifiers.
    for iid in source.get_item_identifiers():
        source.item_identifiers.remove(iid)
        target.item_identifiers.add(iid)
    # Handle reifiers.
    source_reifier = source.get_reifier()
    if source_reifier is None:
        return
    target_reifier = target.get_reifier()
    if target_reifier is not None:
        source.set_reifier(None)
        target_reifier.merge_in(source_reifier)
    else:
        source.set_reifier(None)
        target.set_reifier(source_reifier)

def move_role_characteristics (source, target):
    """Move role item identifiers and reifier from the `source` to the
    `target`s equivalent role.

    :param source: the association to remove the characteristics from
    :type source: `Association`
    :param target: the association that takes the role characteristics
    :type target: `Association`

    """
    signatures = {}
    for role in target.get_roles():
        signature = generate_role_signature(role)
        signatures[signature] = role
    for role in source.get_roles():
        signature = generate_role_signature(role)
        handle_existing_construct(role, signatures.get(signature))
        role.remove()

def move_variants (source, target):
    """Moves the variants from `source` to `target`.

    :param source: the name to take the variants from
    :type source: `Name`
    :param target: the name to add the variants to
    :type target: `Name`

    """
    signatures = {}
    for variant in target.get_variants():
        signature = generate_variant_signature(variant)
        signatures[signature] = variant
    for variant in source.get_variants():
        signature = generate_variant_signature(variant)
        existing = signatures.get(signature)
        if existing is not None:
            handle_existing_construct(variant, existing)
            variant.remove()
        else:
            variant.name = target
            variant.save()
        
def _signature (topic):
    """Returns the signature of the specified topic.

    :param topic: the topic to generate the signature for
    :type topic: `Topic`
    :rtype: integer

    """
    return topic.id
