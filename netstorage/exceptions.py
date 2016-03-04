class NetstorageException(Exception):
    pass

class NetstorageFileNotFound(NetstorageException):
    pass

class NetstorageBadRequest(NetstorageException):
    pass
