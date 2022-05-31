import uuid
from http import HTTPStatus

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from exception.api_error import ApiError
from exception.service_errors import FollowRelationshipError, BlockRelationshipError
from schemas.user_profiles import UserProfileRequestPathParamsSchema, FollowActionResponseSchema, \
    FollowActionResponseData, UnfollowActionResponseSchema, UnfollowActionResponseData, BlockActionResponseSchema, \
    BlockActionResponseData, UnblockActionResponseSchema, UnblockActionResponseData
from service import follow_relationship_service, block_relationship_service
from util.api_request_handler import ApiRequestHandler
from util.api_response_handler import ApiResponseHandler


class UserProfilesResource(Resource):

    # GET /user-profiles/<profile_id>
    def get(self):
        pass

    # PUT /user-profiles/<profile_id>
    def put(self):
        pass


class FollowRelationshipsResource(Resource):

    # POST /user-profiles/<target_user_profile_id>/follow
    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    @jwt_required()
    def post(self, **kwargs):
        request = ApiRequestHandler.handle_request(UserProfileRequestPathParamsSchema())
        target_user_profile_id = request.path_params["target_user_profile_id"]
        current_user_profile_id = uuid.UUID(str(get_jwt_identity()))

        try:
            created_follow_relationship = follow_relationship_service.follow_user_profile(
                source_profile_id=current_user_profile_id,
                target_profile_id=target_user_profile_id
            )
        except FollowRelationshipError as e:
            raise ApiError(status_code=400, title=e.message)

        message = "User followed successfully." if created_follow_relationship.is_accepted else "Follow request sent."
        return ApiResponseHandler.create_response(
            response_schema=FollowActionResponseSchema(),
            message=message,
            data=FollowActionResponseData(
                source_profile_id=created_follow_relationship.source_profile_id,
                target_profile_id=created_follow_relationship.target_profile_id,
                is_accepted=created_follow_relationship.is_accepted,
                is_muted=created_follow_relationship.is_muted,
                created_at=str(created_follow_relationship.created_at),
                updated_at=str(created_follow_relationship.updated_at)
            )
        ), HTTPStatus.CREATED

    # DELETE /user-profiles/<target_user_profile_id>/follow
    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    @jwt_required()
    def delete(self, **kwargs):
        request = ApiRequestHandler.handle_request(UserProfileRequestPathParamsSchema())
        target_user_profile_id = request.path_params["target_user_profile_id"]
        current_user_profile_id = uuid.UUID(str(get_jwt_identity()))

        try:
            deleted_follow_relationship = follow_relationship_service.unfollow_user_profile(
                source_profile_id=current_user_profile_id,
                target_profile_id=target_user_profile_id
            )
        except FollowRelationshipError as e:
            raise ApiError(status_code=400, title=e.message)

        message = "User unfollowed successfully." if deleted_follow_relationship.is_accepted \
            else "Follow request canceled."
        return ApiResponseHandler.create_response(
            response_schema=UnfollowActionResponseSchema(),
            message=message,
            data=UnfollowActionResponseData(
                source_profile_id=deleted_follow_relationship.source_profile_id,
                target_profile_id=deleted_follow_relationship.target_profile_id
            )
        ), HTTPStatus.OK


class BlockRelationshipsResource(Resource):

    # POST /user-profiles/<target_user_profile_id>/block
    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def post(self, **kwargs):
        request = ApiRequestHandler.handle_request(UserProfileRequestPathParamsSchema())
        target_user_profile_id = request.path_params["target_user_profile_id"]
        current_user_profile_id = uuid.UUID(str(get_jwt_identity()))

        try:
            created_block_relationship = block_relationship_service.block_user_profile(
                blocker_profile_id=current_user_profile_id,
                blocked_profile_id=target_user_profile_id
            )
        except BlockRelationshipError as e:
            raise ApiError(status_code=400, title=e.message)

        return ApiResponseHandler.create_response(
            response_schema=BlockActionResponseSchema(),
            message="User blocked successfully.",
            data=BlockActionResponseData(
                blocker_profile_id=created_block_relationship.blocker_profile_id,
                blocked_profile_id=created_block_relationship.blocked_profile_id,
                blocked_at=str(created_block_relationship.blocked_at)
            )
        ), HTTPStatus.CREATED

    # DELETE /user-profiles/<target_user_profile_id>/block
    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def delete(self, **kwargs):
        request = ApiRequestHandler.handle_request(UserProfileRequestPathParamsSchema())
        target_user_profile_id = request.path_params["target_user_profile_id"]
        current_user_profile_id = uuid.UUID(str(get_jwt_identity()))

        try:
            deleted_block_relationship = block_relationship_service.unblock_user_profile(
                blocker_profile_id=current_user_profile_id,
                blocked_profile_id=target_user_profile_id
            )
        except BlockRelationshipError as e:
            raise ApiError(status_code=400, title=e.message)

        return ApiResponseHandler.create_response(
            response_schema=UnblockActionResponseSchema(),
            message="User unblocked successfully.",
            data=UnblockActionResponseData(
                blocker_profile_id=deleted_block_relationship.blocker_profile_id,
                blocked_profile_id=deleted_block_relationship.blocked_profile_id
            )
        ), HTTPStatus.OK


class MuteUserProfileResource(Resource):

    # PUT /user-profiles/<target_user_profile_id>/mute
    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    @jwt_required()
    def put(self, **kwargs):
        request = ApiRequestHandler.handle_request(UserProfileRequestPathParamsSchema())
        target_user_profile_id = request.path_params["target_user_profile_id"]
        current_user_profile_id = uuid.UUID(str(get_jwt_identity()))

        try:
            updated_follow_relationship = follow_relationship_service.update_follow_relationship(
                source_profile_id=current_user_profile_id,
                target_profile_id=target_user_profile_id,
                is_muted=True
            )
        except FollowRelationshipError as e:
            raise ApiError(status_code=400, title=e.message)

        return ApiResponseHandler.create_response(
            response_schema=FollowActionResponseSchema(),
            message="User muted successfully.",
            data=FollowActionResponseData(
                source_profile_id=updated_follow_relationship.source_profile_id,
                target_profile_id=updated_follow_relationship.target_profile_id,
                is_accepted=updated_follow_relationship.is_accepted,
                is_muted=updated_follow_relationship.is_muted,
                created_at=str(updated_follow_relationship.created_at),
                updated_at=str(updated_follow_relationship.updated_at)
            )
        ), HTTPStatus.OK


class UnMuteUserProfileResource(Resource):

    # /user-profiles/<target_user_profile_id>/un-mute
    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    @jwt_required()
    def put(self, **kwargs):
        request = ApiRequestHandler.handle_request(UserProfileRequestPathParamsSchema())
        target_user_profile_id = request.path_params["target_user_profile_id"]
        current_user_profile_id = uuid.UUID(str(get_jwt_identity()))

        try:
            updated_follow_relationship = follow_relationship_service.update_follow_relationship(
                source_profile_id=current_user_profile_id,
                target_profile_id=target_user_profile_id,
                is_muted=False
            )
        except FollowRelationshipError as e:
            raise ApiError(status_code=400, title=e.message)

        return ApiResponseHandler.create_response(
            response_schema=FollowActionResponseSchema(),
            message="User un-muted successfully.",
            data=FollowActionResponseData(
                source_profile_id=updated_follow_relationship.source_profile_id,
                target_profile_id=updated_follow_relationship.target_profile_id,
                is_accepted=updated_follow_relationship.is_accepted,
                is_muted=updated_follow_relationship.is_muted,
                created_at=str(updated_follow_relationship.created_at),
                updated_at=str(updated_follow_relationship.updated_at)
            )
        ), HTTPStatus.OK
