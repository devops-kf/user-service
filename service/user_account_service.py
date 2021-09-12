import bcrypt

from entity.user_account import UserAccount, AccountType, AccountStatus
from exception.service_errors import UserAccountError
from repository import user_account_repository


def create_new_user_account(**kwargs):
    if user_account_repository.exists_by_username(kwargs['username']):
        raise UserAccountError(message=f"Username '{kwargs['username']}' is already taken.")
    if user_account_repository.exists_by_email(kwargs['email']):
        raise UserAccountError(message=f"Email '{kwargs['email']}' is already taken.")

    account_type = AccountType.REGULAR_USER if kwargs['account_type'] == 0 else AccountType.AGENT_USER
    account_status = AccountStatus.REGISTERED if account_type == AccountType.REGULAR_USER \
        else AccountStatus.PENDING_REGISTRATION_APPROVAL
    password_hash = bcrypt.hashpw(kwargs['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    new_user_account = UserAccount(username=kwargs['username'],
                                   password=password_hash,
                                   email=kwargs['email'],
                                   account_type=account_type,
                                   account_status=account_status)
    persisted_entity = user_account_repository.create_new(user_account=new_user_account)

    return persisted_entity
