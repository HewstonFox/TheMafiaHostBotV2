class InvalidSessionIdError(Exception):
    def __init__(self, *args):
        super(InvalidSessionIdError, self).__init__(*args)


class SessionAlreadyActiveError(Exception):
    def __init__(self, *args):
        super(SessionAlreadyActiveError, self).__init__(*args)


class InvalidSessionStatusError(Exception):
    def __init__(self, *args):
        super(InvalidSessionStatusError, self).__init__(*args)


class UserNotExistsError(Exception):
    def __init__(self, *args):
        super(UserNotExistsError, self).__init__(*args)
