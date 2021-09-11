import uuid
from dataclasses import dataclass, asdict

from sqlalchemy import DateTime, Column, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from entity import Base


@dataclass
class FollowRelationship(Base):
    __tablename__ = 'follow_relationships'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    follower_profile_id = Column(UUID(as_uuid=True), ForeignKey('user_profiles.id'), default=uuid.uuid4)
    following_profile_id = Column(UUID(as_uuid=True), ForeignKey('user_profiles.id'), default=uuid.uuid4)
    is_accepted = Column(Boolean, nullable=False)
    is_muted = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, follower_profile_id, following_profile_id, is_accepted=True):
        self.follower_profile_id = follower_profile_id
        self.following_profile_id = following_profile_id
        self.is_accepted = is_accepted

    def get_dict(self):
        return asdict(self)
