import enum
import uuid
from dataclasses import dataclass, asdict

from sqlalchemy import DateTime, Column, String, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from entity import Base


class AccountType(enum.Enum):
    REGULAR_USER = 0
    AGENT_USER = 1


class AccountStatus(enum.Enum):
    PENDING_VERIFICATION = 0
    PENDING_REGISTRATION_APPROVAL = 1
    REGISTERED = 2
    SUSPENDED = 3


@dataclass
class UserAccount(Base):
    __tablename__ = 'user_accounts'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(31), unique=True, nullable=False)
    password = Column(String(60), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    account_type = Column(Enum(AccountType), nullable=False)
    account_status = Column(Enum(AccountStatus), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, username, password, email, account_type, account_status):
        self.username = username
        self.password = password
        self.email = email
        self.account_type = account_type
        self.account_status = account_status

    def get_dict(self):
        return asdict(self)
