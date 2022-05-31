import uuid
from dataclasses import dataclass, asdict

from sqlalchemy import DateTime, Column, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from entity import Base
from entity.user_profile import UserProfile


@dataclass
class FollowRelationship(Base):
    __tablename__ = 'follow_relationships'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_profile_id = Column(UUID(as_uuid=True), ForeignKey('user_profiles.id'), default=uuid.uuid4)
    target_profile_id = Column(UUID(as_uuid=True), ForeignKey('user_profiles.id'), default=uuid.uuid4)
    is_accepted = Column(Boolean, nullable=False)
    is_muted = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    source_profile = relationship(UserProfile,
                                  primaryjoin="and_(FollowRelationship.source_profile_id==UserProfile.id)",
                                  backref='follow_relationships_source')
    target_profile = relationship(UserProfile,
                                  primaryjoin="and_(FollowRelationship.target_profile_id==UserProfile.id)",
                                  backref='follow_relationships_target')

    def __init__(self, source_profile_id, target_profile_id, is_accepted=True):
        self.source_profile_id = source_profile_id
        self.target_profile_id = target_profile_id
        self.is_accepted = is_accepted

    def get_dict(self):
        return asdict(self)
