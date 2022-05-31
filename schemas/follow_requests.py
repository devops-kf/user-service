from collections import namedtuple

from marshmallow import fields

from schemas.base import RequestPathParamsSchema, ResponseSchema


class FollowRequestActionRequestPathParamsSchema(RequestPathParamsSchema):
    request_id = fields.UUID(required=True)


class FollowRequestResponseSchema(ResponseSchema):
    follow_request_id = fields.String()
    source_profile_id = fields.String()
    source_profile_username = fields.String()
    source_profile_image_url = fields.String()
    created_at = fields.String()


class FollowRequestsResponseSchema(ResponseSchema):
    follow_requests = fields.List(fields.Nested(FollowRequestResponseSchema))


FollowRequestResponseData = namedtuple(
    typename='FollowRequestResponseData',
    field_names=['follow_request_id', 'source_profile_id', 'source_profile_username', 'source_profile_image_url',
                 'created_at']
)

FollowRequestsResponseData = namedtuple(
    typename='FollowRequestsResponseData',
    field_names=['follow_requests']
)
