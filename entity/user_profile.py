import enum
import uuid
from dataclasses import dataclass, asdict

from sqlalchemy import DateTime, Column, String, Boolean, Enum, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from entity import Base


class Sex(enum.Enum):
    MALE = 0
    FEMALE = 1


class Interests(enum.Enum):
    NONE = 0


@dataclass
class UserProfile(Base):
    __tablename__ = 'user_profiles'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user_accounts.id'), unique=True, default=uuid.uuid4)
    profile_image_url = Column(String(255), nullable=False)
    name = Column(String(63), nullable=False)
    bio = Column(String(255), nullable=False)
    phone_number = Column(String(31), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    sex = Column(Enum(Sex), nullable=False)
    country = Column(String(127), nullable=False)
    interests = Column(Enum(Interests), nullable=False)
    shop_url = Column(String(255), nullable=False)
    is_private = Column(Boolean, nullable=False)
    allow_tagging = Column(Boolean, nullable=False, default=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, user_id, profile_image_url, name, bio, phone_number,
                 date_of_birth, sex, country, interests, shop_url, is_private):
        self.user_id = user_id
        self.profile_image_url = profile_image_url
        self.name = name
        self.bio = bio
        self.phone_number = phone_number
        self.date_of_birth = date_of_birth
        self.sex = sex
        self.country = country
        self.interests = interests
        self.shop_url = shop_url
        self.is_private = is_private

    def get_dict(self):
        return asdict(self)
