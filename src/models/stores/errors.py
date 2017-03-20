

class StoreException(Exception):
    def __int__(self, message):
        self.message = message

class StoreNotFoundException(StoreException):
    pass