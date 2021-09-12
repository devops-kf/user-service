
from schemas.base import ResponseSchema


class ApiResponseHandler:

    @classmethod
    def create_response(cls, response_schema: ResponseSchema, message=None, data=None):
        return {
            'message': message,
            'data': response_schema.dump(data),
        }
