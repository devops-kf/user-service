from flask import request
from marshmallow import ValidationError

from exception.api_error import ApiError
from schemas.base import RequestPathParamsSchema, RequestQueryParamsSchema, RequestBodyParamsSchema


class ApiRequestData:
    def __init__(self, path_params_data, query_params_data, body_data):
        self.path_params = path_params_data
        self.query_params = query_params_data
        self.body = body_data


class ApiRequestHandler:

    @classmethod
    def __schema_check(cls, schema=None, json_data=None, title=None):
        try:
            return schema.load(data=json_data)  # TODO (fivkovic): Add support for partial data - partial=True
        except ValidationError as err:
            raise ApiError(status_code=400, title=title, messages=err.messages,
                           data=err.data, valid_data=err.valid_data)

    @classmethod
    def handle_request(cls, schemas):
        if not isinstance(schemas, list):
            schemas = [schemas]

        path_params_data, query_params_data, body_data = {}, {}, {}
        for schema in schemas:
            if isinstance(schema, RequestPathParamsSchema):
                path_params_data.update(cls.__schema_check(schema=schema, json_data=request.view_args,
                                                           title='One or more request URL path parameters invalid.'))
            if isinstance(schema, RequestQueryParamsSchema):
                query_params_data.update(cls.__schema_check(schema=schema, json_data=request.args,
                                                            title='One or more request URL query parameters invalid.'))
            if isinstance(schema, RequestBodyParamsSchema):
                body_data.update(cls.__schema_check(schema=schema, json_data=request.get_json(),
                                                    title='One or more request body parameters invalid.'))

        return ApiRequestData(path_params_data, query_params_data, body_data)
