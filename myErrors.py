class myExit(Exception):
    def __init__(self, errorCode):
        self.code = errorCode
