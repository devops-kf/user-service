from uuid import UUID

from configuration.database_configuration import db_scoped_session
from entity.user_profile import UserProfile


def create_new(user_profile: UserProfile):
    db_scoped_session.add(user_profile)
    db_scoped_session.commit()

    return user_profile


def get_by_id(user_profile_id: UUID) -> UserProfile:
    user_profile = UserProfile.query.get(user_profile_id)
    return user_profile
