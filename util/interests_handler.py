from entity.interest import Interest

default_interests = {
    0: Interest(identifier=0, name="Sports"),
    1: Interest(identifier=1, name="Politics"),
    2: Interest(identifier=2, name="Nature"),
    3: Interest(identifier=3, name="Movies"),
    4: Interest(identifier=4, name="Books"),
    5: Interest(identifier=5, name="Fashion"),
    6: Interest(identifier=6, name="Makeup")
}


def serialize_interests_identifiers(interest_identifiers):
    for identifier in interest_identifiers:
        if identifier not in default_interests:
            raise ValueError("Invalid interest identifier.")

    return ', '.join(map(str, interest_identifiers))


def deserialize_interests_identifiers(interest_identifiers_string):
    return map(int, interest_identifiers_string.split(','))


def check_if_interest_in(interest_id: int, interest_identifiers_string: str):
    return interest_id in deserialize_interests_identifiers(interest_identifiers_string)
