NAME_COMBINATIONS = [ '{}{}', '{}.{}' ]

def _get_numbered_emails(root, max_num):
    numbered_emails = [ '{:s}{:d}'.format(root, i) for i in range(max_num + 1) ]
    return [ root ] + numbered_emails # also add root w/o number

def _get_full_name_emails(first_name, second_name, max_num_to_try_per_combo):
    roots = [
        (first_name, second_name),
        (first_name[:1], second_name),
        (first_name, second_name[:1]),
        #(first_name[:1], second_name[:1]) # TODO: even have this?
    ]
    # Add lowercase variants for each root
    lower_case_roots = [ (r[0].lower(), r[1].lower()) for r in roots ]

    # Now take all the roots and combine them in every hard-coded way
    combinations = []
    for r in lower_case_roots + roots:
        combinations += [ c.format(r[0], r[1]) for c in NAME_COMBINATIONS ]

    # Add numbered variants for each variant
    full_emails = []
    for c in combinations:
        full_emails += _get_numbered_emails(c, max_num_to_try_per_combo)
    return full_emails

def _combine_into_set(*lists):
    result = set()
    for l in lists:
        result = result.union(set(l))
    return result

def get_possible_addresses_for(first_name, second_name, max_num_to_try):
    return _combine_into_set(
        _get_numbered_emails(first_name, max_num_to_try),
        _get_numbered_emails(first_name.lower(), max_num_to_try),
        _get_numbered_emails(second_name, max_num_to_try),
        _get_numbered_emails(second_name.lower(), max_num_to_try),
        _get_full_name_emails(first_name, second_name, max_num_to_try)
    )
