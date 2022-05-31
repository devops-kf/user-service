import uuid
from http import HTTPStatus

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from exception.api_error import ApiError
from exception.service_errors import FollowRelationshipError
from schemas.follow_requests import FollowRequestsResponseSchema, FollowRequestResponseData, \
    FollowRequestsResponseData, FollowRequestActionRequestPathParamsSchema
from schemas.user_profiles import FollowActionResponseSchema, FollowActionResponseData
from service import follow_relationship_service
from util.api_request_handler import ApiRequestHandler
from util.api_response_handler import ApiResponseHandler


class FollowRequestsResource(Resource):

    # GET /follow-requests
    # noinspection PyMethodMayBeStatic
    @jwt_required()
    def get(self):
        current_user_profile_id = uuid.UUID(str(get_jwt_identity()))
        try:
            follow_requests = follow_relationship_service.get_all_follow_requests(current_user_profile_id)
        except FollowRelationshipError as e:
            raise ApiError(status_code=400, title=e.message)

        data = [FollowRequestResponseData(follow_request_id=follow_relationship.id,
                                          source_profile_id=follow_relationship.source_profile.id,
                                          source_profile_username=follow_relationship.source_profile.display_name,
                                          source_profile_image_url=follow_relationship.source_profile.profile_image_url,
                                          created_at=follow_relationship.created_at)
                for follow_relationship in follow_requests]

        return ApiResponseHandler.create_response(
            response_schema=FollowRequestsResponseSchema(),
            message="",
            data=FollowRequestsResponseData(data)
        ), HTTPStatus.OK


class AcceptFollowRequestResource(Resource):

    # PUT /follow-requests/<request_id>/accept
    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    @jwt_required()
    def put(self, **kwargs):
        request = ApiRequestHandler.handle_request(FollowRequestActionRequestPathParamsSchema())
        current_user_profile_id = uuid.UUID(str(get_jwt_identity()))

        try:
            updated_follow_relationship = follow_relationship_service.update_follow_request(
                follow_relationship_id=request.path_params.request_id,
                current_user_profile_id=current_user_profile_id,
                is_accepted=True
            )
        except FollowRelationshipError as e:
            raise ApiError(status_code=400, title=e.message)

        return ApiResponseHandler.create_response(
            response_schema=FollowActionResponseSchema(),
            message=f"Follow request accepted successfully. "
                    f"User {updated_follow_relationship.target_profile.display_name} followed back.",
            data=FollowActionResponseData(
                source_profile_id=updated_follow_relationship.source_profile_id,
                target_profile_id=updated_follow_relationship.target_profile_id,
                is_accepted=updated_follow_relationship.is_accepted,
                is_muted=updated_follow_relationship.is_muted,
                created_at=str(updated_follow_relationship.created_at),
                updated_at=str(updated_follow_relationship.updated_at)
            )
        ), HTTPStatus.OK


class RejectFollowRequestResource(Resource):

    # PUT /follow-requests/<request_id>/reject
    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def put(self, **kwargs):
        request = ApiRequestHandler.handle_request(FollowRequestActionRequestPathParamsSchema())
        current_user_profile_id = uuid.UUID(str(get_jwt_identity()))

        try:
            updated_follow_relationship = follow_relationship_service.update_follow_request(
                follow_relationship_id=request.path_params.request_id,
                current_user_profile_id=current_user_profile_id,
                is_accepted=False
            )
        except FollowRelationshipError as e:
            raise ApiError(status_code=400, title=e.message)

        return ApiResponseHandler.create_response(
            response_schema=FollowActionResponseSchema(),
            message=f"Follow request from user {updated_follow_relationship.target_profile.display_name} declined.",
            data=FollowActionResponseData(
                source_profile_id=updated_follow_relationship.source_profile_id,
                target_profile_id=updated_follow_relationship.target_profile_id,
                is_accepted=updated_follow_relationship.is_accepted,
                is_muted=updated_follow_relationship.is_muted,
                created_at=str(updated_follow_relationship.created_at),
                updated_at=str(updated_follow_relationship.updated_at)
            )
        ), HTTPStatus.OK
