from http import HTTPStatus

from flask_restful import Resource

from exception.api_error import ApiError
from exception.service_errors import UserAccountError, UserProfileError
from schemas.user_accounts import RegistrationRequestBodyParamsSchema, RegistrationResponseSchema, \
    RegistrationResponseData
from service import user_account_service, user_profile_service
from util.api_request_handler import ApiRequestHandler
from util.api_response_handler import ApiResponseHandler


class UsersResource(Resource):

    # POST /users
    # noinspection PyMethodMayBeStatic
    def post(self):
        registration_request = ApiRequestHandler.handle_request(RegistrationRequestBodyParamsSchema())
        try:
            created_user_account = user_account_service.create_new_user_account(**registration_request.body)
            created_user_profile = user_profile_service.create_new_user_profile(**registration_request.body,
                                                                                user_account_id=created_user_account.id)

            # TODO (fivkovic): Publish RegularUserAccountCreated/AgentUserAccountCreated messages
            #                  Be careful about password hashing on different services.

        except UserAccountError as e:
            raise ApiError(status_code=400, title=e.message)
        except UserProfileError as e:
            raise ApiError(status_code=400, title=e.message)

        return ApiResponseHandler.create_response(
            response_schema=RegistrationResponseSchema(),
            message="Registration successful.",
            data=RegistrationResponseData(
                user_account_id=created_user_profile.user_account_id,
                user_profile_id=created_user_profile.id,
                username=created_user_account.username,
                email=created_user_account.email,
                account_type=created_user_account.account_type.value,
                created_at=str(created_user_account.created_at)
            )
        ), HTTPStatus.CREATED