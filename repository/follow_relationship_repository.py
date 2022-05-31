from typing import Optional
from uuid import UUID

from configuration.database_configuration import db_scoped_session
from entity.follow_relationship import FollowRelationship


def create_new(follow_relationship: FollowRelationship) -> FollowRelationship:
    db_scoped_session.add(follow_relationship)
    db_scoped_session.commit()

    return follow_relationship


def get_by_id(follow_relationship_id: UUID) -> Optional[FollowRelationship]:
    return db_scoped_session.query(FollowRelationship).filter_by(
        id=follow_relationship_id
    ).first()


def get_by_profile(source_profile_id: UUID, target_profile_id: UUID) -> Optional[FollowRelationship]:
    return db_scoped_session.query(FollowRelationship).filter_by(
        source_profile_id=source_profile_id,
        target_profile_id=target_profile_id
    ).first()


def get_all_pending(target_profile_id: UUID):
    return db_scoped_session.query(FollowRelationship).filter_by(
        target_profile_id=target_profile_id,
        is_accepted=False
    ).all()


# TODO (fivkovic): Fix this, it's a mess
def update(follow_relationship: FollowRelationship):
    db_scoped_session.commit()

    return follow_relationship


def delete(follow_relationship: FollowRelationship):
    db_scoped_session.delete(follow_relationship)
    db_scoped_session.commit()


def delete_by_id(follow_relationship_id: UUID):
    follow_relationship = get_by_id(follow_relationship_id)
    db_scoped_session.delete(follow_relationship)
    db_scoped_session.commit()


def delete_by_profile(source_profile_id: UUID, target_profile_id: UUID):
    follow_relationship = get_by_profile(source_profile_id, target_profile_id)
    db_scoped_session.delete(follow_relationship)
    db_scoped_session.commit()

