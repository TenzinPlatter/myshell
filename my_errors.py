"""
Contains custom error classes
"""

class ErrorMsg(Exception):
    """
    Custom error containing a message
    """
    def __init__(self, msg):
        self.msg = msg
