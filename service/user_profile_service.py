from entity.user_profile import UserProfile, Sex
from repository import user_profile_repository


def create_new_user_profile(**kwargs):
    new_user_profile = UserProfile(user_id=kwargs['user_account_id'],
                                   profile_image_url=kwargs['profile_image_url'],
                                   name=kwargs['name'],
                                   bio=kwargs['bio'],
                                   phone_number=kwargs['phone_number'],
                                   date_of_birth=kwargs['date_of_birth'],
                                   sex=Sex.MALE if kwargs['gender'] == 0 else Sex.FEMALE,
                                   country=kwargs['country'],
                                   interests=kwargs['interests'],
                                   shop_url=kwargs['shop_url'],
                                   is_private=False)
    persisted_entity = user_profile_repository.create_new(user_profile=new_user_profile)

    return persisted_entity
