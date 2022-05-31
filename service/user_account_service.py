from uuid import UUID

import bcrypt

from entity.user_account import UserAccount, AccountType, AccountStatus
from exception.service_errors import UserAccountError
from repository import user_account_repository


def create_new_user_account(**kwargs):
    if user_account_repository.exists_by_username(kwargs['username']):
        raise UserAccountError(message=f"Username '{kwargs['username']}' is already taken.")
    if user_account_repository.exists_by_email(kwargs['email']):
        raise UserAccountError(message=f"Email '{kwargs['email']}' is already taken.")

    account_type = __get_account_type(kwargs['account_type'])
    account_status = __get_initial_account_status(account_type)
    password_hash = __get_password_hash(kwargs['password'])

    new_user_account = UserAccount(username=kwargs['username'],
                                   password=password_hash,
                                   email=kwargs['email'],
                                   account_type=account_type,
                                   account_status=account_status)
    persisted_entity = user_account_repository.create_new(user_account=new_user_account)

    return persisted_entity


def handle_agent_request_approved(user_account_id: UUID):
    # TODO (fivkovic): Handle integration event
    pass


def handle_agent_request_rejected(user_account_id: UUID):
    # TODO (fivkovic): Handle integration event
    pass


def handle_user_account_marked_for_suspension(user_account_id: UUID):
    # TODO (fivkovic): Handle integration event
    pass


def __get_account_type(account_type_id: int):
    if account_type_id == 0:
        return AccountType.REGULAR_USER
    if account_type_id == 1:
        return AccountType.AGENT_USER

    raise ValueError("Unsupported account type.")


def __get_initial_account_status(account_type: AccountType):
    if account_type == AccountType.REGULAR_USER:
        return AccountStatus.ACTIVE
    if account_type == AccountType.AGENT_USER:
        return AccountStatus.PENDING_APPROVAL

    raise ValueError("Unsupported account type.")


def __get_password_hash(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
