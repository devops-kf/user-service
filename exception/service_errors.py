
class UserAccountError(Exception):

    def __init__(self, message='User account error.'):
        super().__init__(message)
        self.message = message


class UserProfileError(Exception):

    def __init__(self, message='User profile error.'):
        super().__init__(message)
        self.message = message
