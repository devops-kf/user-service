import uuid
from dataclasses import dataclass, asdict

from sqlalchemy import DateTime, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from entity import Base


@dataclass
class BlockRelationship(Base):
    __tablename__ = 'block_relationships'

    id = Column(UUID(as_uuid=True), default=uuid.uuid4)
    blocker_profile_id = Column(UUID(as_uuid=True), ForeignKey('user_profiles.id'),
                                primary_key=True, default=uuid.uuid4)
    blocked_profile_id = Column(UUID(as_uuid=True), ForeignKey('user_profiles.id'),
                                primary_key=True, default=uuid.uuid4)
    blocked_at = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, blocker_profile_id, blocked_profile_id):
        self.blocker_profile_id = blocker_profile_id
        self.blocked_profile_id = blocked_profile_id

    def get_dict(self):
        return asdict(self)
