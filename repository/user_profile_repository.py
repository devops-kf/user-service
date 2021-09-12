from configuration.database_configuration import db_scoped_session
from entity.user_profile import UserProfile


def create_new(user_profile: UserProfile):
    db_scoped_session.add(user_profile)
    db_scoped_session.commit()

    return user_profile

