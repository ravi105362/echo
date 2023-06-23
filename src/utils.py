class CustomException(Exception):
    def __init__(self, name: str, msg: str):
        self.name = name
        self.msg = msg
