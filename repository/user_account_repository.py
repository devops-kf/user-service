from configuration.database_configuration import db_scoped_session
from entity.user_account import UserAccount


def create_new(user_account: UserAccount):
    db_scoped_session.add(user_account)
    db_scoped_session.commit()

    return user_account


def exists_by_username(username: str):
    return db_scoped_session.query(UserAccount.username).filter_by(username=username).first() is not None


def exists_by_email(email: str):
    return db_scoped_session.query(UserAccount.email).filter_by(username=email).first() is not None

