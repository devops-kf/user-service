from flask import request
from marshmallow import ValidationError

from exception.api_error import ApiError
from schemas.base import RequestPathParamsSchema, RequestQueryParamsSchema, RequestBodyParamsSchema


class APIUtils:

    @classmethod
    def schema_check(cls, schema=None, json_data=None, title=None):
        try:
            return schema.load(data=json_data)  # TODO (fivkovic): Add support for partial data - partial=True
        except ValidationError as err:
            raise ApiError(
                status_code=400,
                title=title,
                messages=err.messages,
                data=err.data,
                valid_data=err.valid_data,
            )

    @classmethod
    def request_schemas_load(cls, schemas):
        if not isinstance(schemas, list):
            schemas = [schemas]

        result_path, result_query, result_body = {}, {}, {}
        for schema in schemas:
            if isinstance(schema, RequestPathParamsSchema):
                # path params
                result_path.update(cls.schema_check(
                    schema=schema,
                    json_data=request.view_args,
                    title='One or more request URL path parameters did not validate'))

            if isinstance(schema, RequestQueryParamsSchema):
                # query params
                result_query.update(cls.schema_check(
                    schema=schema,
                    json_data=request.args,
                    title='One or more request URL query parameters did not validate'))

            if isinstance(schema, RequestBodyParamsSchema):
                # body params
                result_body.update(cls.schema_check(
                    schema=schema,
                    json_data=request.get_json(),
                    title='One or more request body parameters did not validate'))

        return {
            'path': result_path,
            'query': result_query,
            'body': result_body,
        }

    # @classmethod
    # def get_by_id_or_404(cls, res, res_id, res_name, res_id_name):
    #     obj = app_db.session.query(res).get(res_id)
    #     if obj is None:
    #         raise APIError(
    #             status_code=404,
    #             title='The requested resource could not be found',
    #             messages={
    #                 res_name: [
    #                     'Not found',
    #                 ]
    #             },
    #             data={
    #                 res_id_name: res_id,
    #             },
    #         )
    #     return obj