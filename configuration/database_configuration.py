from os import environ

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import NullPool

from entity import Base

engine = create_engine(environ.get('SQLALCHEMY_DATABASE_URI'), poolclass=NullPool)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def initialize_database():
    # NOTE (fivkovic): These entity class imports are required for the DB engine to create the tables successfully.

    from entity.user_account import UserAccount, AccountType, AccountStatus
    from entity.user_profile import UserProfile, Sex, Interests
    from entity.follow_relationship import FollowRelationship
    from entity.block_relationship import BlockRelationship

    Base.query = db_session.query_property()
    Base.metadata.create_all(bind=engine)
