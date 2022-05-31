from typing import Optional
from uuid import UUID

from configuration.database_configuration import db_scoped_session
from entity.block_relationship import BlockRelationship


def create_new(block_relationship: BlockRelationship) -> BlockRelationship:
    db_scoped_session.add(block_relationship)
    db_scoped_session.commit()

    return block_relationship


def get_all_blocked(blocked_profile_id: UUID):
    return db_scoped_session.query(BlockRelationship).filter_by(
        blocked_profile_id=blocked_profile_id
    ).all()


def get_by_id(block_relationship_id: UUID) -> Optional[BlockRelationship]:
    return db_scoped_session.query(BlockRelationship).filter_by(
        id=block_relationship_id
    ).first()


def get_by_profile(blocker_profile_id: UUID, blocked_profile_id: UUID) -> Optional[BlockRelationship]:
    return db_scoped_session.query(BlockRelationship).filter_by(
        blocker_profile_id=blocker_profile_id,
        blocked_profile_id=blocked_profile_id
    ).first()


def exists_by_profile(blocker_profile_id: UUID, blocked_profile_id: UUID) -> bool:
    return db_scoped_session.query(BlockRelationship).filter_by(
        blocker_profile_id=blocker_profile_id,
        blocked_profile_id=blocked_profile_id
    ).first() is not None


def delete(block_relationship: BlockRelationship):
    db_scoped_session.delete(block_relationship)
    db_scoped_session.commit()
