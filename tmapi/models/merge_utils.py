"""Module containing utility functions for merging topics."""

from signature import generate_role_signature, generate_variant_signature


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
