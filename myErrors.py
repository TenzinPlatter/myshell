class myExit(Exception):
    def __init__(self, errorCode):
        self.code = errorCode

class errorMsg(Exception):
    def __init__(self, msg):
        self.msg = msg

