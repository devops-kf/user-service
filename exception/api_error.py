from flask import jsonify


class ApiError(Exception):

    def __init__(self, status_code=None, title='Error', messages=None, data=None, valid_data=None):
        super().__init__(title)
        self.status_code = status_code if status_code else 400
        self.title = title
        self.messages = messages
        self.data = data
        self.valid_data = valid_data

    def __to_dict(self):
        return {
            'title': self.title,
            'messages': self.messages,
            'data': self.data,
            'valid_data': self.valid_data
        }

    def to_response(self):
        response_data = jsonify(self.__to_dict())
        return response_data, self.status_code
