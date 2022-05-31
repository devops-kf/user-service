from collections import namedtuple

from marshmallow import validate, fields

from schemas.base import RequestBodyParamsSchema, ResponseSchema


class RegistrationRequestBodyParamsSchema(RequestBodyParamsSchema):
    username = fields.String(required=True, validate=validate.Length(min=3, max=30))
    password = fields.String(required=True, validate=validate.Length(min=3, max=30))
    email = fields.Email(required=True)
    account_type = fields.Integer(required=True, validate=validate.OneOf([0, 1]),
                                  error_messages={'out_of_range': "Unsupported account type."})
    profile_image_url = fields.URL(required=True, schemes=['http', 'https'],
                                   error_messages={'unsupported_url': "Invalid profile image URL."})
    first_name = fields.String(required=True, validate=validate.Length(min=2, max=60))
    last_name = fields.String(required=True, validate=validate.Length(min=2, max=60))
    bio = fields.String(required=True, validate=validate.Length(min=1, max=255))
    phone_number = fields.String(required=True, validate=validate.Length(min=6, max=30))
    date_of_birth = fields.Date(required=True)
    gender = fields.Integer(required=True, validate=validate.OneOf([0, 1]),
                            error_messages={'unsupported_type': "Unsupported gender type."})
    country = fields.String(required=True, validate=validate.Length(min=2, max=60))
    interests = fields.List(fields.Integer(), required=True, validate=validate.Length(min=1, max=7))
    shop_url = fields.URL(required=False, schemes=['http', 'https'],
                          error_messages={'unsupported_url': "Invalid shop URL."})


class RegistrationResponseSchema(ResponseSchema):
    user_account_id = fields.String()
    user_profile_id = fields.String()
    username = fields.String()
    email = fields.Email()
    account_type = fields.Integer()
    created_at = fields.String()


RegistrationResponseData = namedtuple(
    typename='RegistrationResponseData',
    field_names=['user_account_id', 'user_profile_id', 'username', 'email', 'account_type', 'created_at']
)
