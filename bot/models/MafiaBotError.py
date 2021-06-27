class InvalidSessionId(Exception):
    def __init__(self, *args):
        super(InvalidSessionId, self).__init__(*args)
