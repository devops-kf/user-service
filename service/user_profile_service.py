from entity.user_profile import UserProfile, Gender
from repository import user_profile_repository
from util.interests_handler import serialize_interests_identifiers


def create_new_user_profile(**kwargs):

    # TODO (fivkovic): Validate shop URL domain.

    new_user_profile = UserProfile(user_account_id=kwargs['user_account_id'],
                                   display_name=kwargs['username'],
                                   profile_image_url=kwargs['profile_image_url'],
                                   first_name=kwargs['first_name'],
                                   last_name=kwargs['last_name'],
                                   bio=kwargs['bio'],
                                   phone_number=kwargs['phone_number'],
                                   date_of_birth=kwargs['date_of_birth'],
                                   gender=Gender.MALE if kwargs['gender'] == 0 else Gender.FEMALE,
                                   country=kwargs['country'],
                                   interests=serialize_interests_identifiers(kwargs['interests']),
                                   shop_url=kwargs['shop_url'],
                                   is_private=False)
    persisted_entity = user_profile_repository.create_new(user_profile=new_user_profile)

    return persisted_entity
