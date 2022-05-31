from collections import namedtuple

from marshmallow import fields

from schemas.base import RequestPathParamsSchema, ResponseSchema


class UserProfileRequestPathParamsSchema(RequestPathParamsSchema):
    target_user_profile_id = fields.UUID(required=True)


class FollowActionResponseSchema(ResponseSchema):
    source_profile_id = fields.String()
    target_profile_id = fields.String()
    is_accepted = fields.Boolean()
    is_muted = fields.Boolean()
    created_at = fields.String()
    updated_at = fields.String()


class UnfollowActionResponseSchema(ResponseSchema):
    source_profile_id = fields.String()
    target_profile_id = fields.String()


class BlockActionResponseSchema(ResponseSchema):
    blocker_profile_id = fields.String()
    blocked_profile_id = fields.String()
    blocked_at = fields.String()


class UnblockActionResponseSchema(ResponseSchema):
    blocker_profile_id = fields.String()
    blocked_profile_id = fields.String()


FollowActionResponseData = namedtuple(
    typename='FollowResponseData',
    field_names=['source_profile_id', 'target_profile_id', 'is_accepted', 'is_muted', 'created_at', 'updated_at']
)

UnfollowActionResponseData = namedtuple(
    typename='UnfollowResponseData',
    field_names=['source_profile_id', 'target_profile_id']
)

BlockActionResponseData = namedtuple(
    typename='BlockActionResponseData',
    field_names=['blocker_profile_id', 'blocked_profile_id', 'blocked_at']
)

UnblockActionResponseData = namedtuple(
    typename='UnblockActionResponseData',
    field_names=['blocker_profile_id', 'blocked_profile_id']
)
