class NetstorageError(Exception):

    def __init__(self, response, *args, **kwargs):
        super(NetstorageError, self).__init__(response)
        self.msg = kwargs.get('message')


class NotFoundError(NetstorageError):
    def __init__(self, response, *args, **kwargs):
        message = ('Can occur if the targeted object can not be found in the '
                   'specified path. Check the path provided and try again')

        super(NotFoundError, self).__init__(response, message=message)


class BadRequestError(NetstorageError):
    pass


class UnauthorizedError(NetstorageError):
    pass


class ForbiddenError(NetstorageError):
    def __init__(self, response):
        message = ('The Akamai Edge server has denied access to the call. '
                   'Please verify that the call is properly formatted '
                   'and retry')
        super(ForbiddenError, self).__init__(response, message=message)


class NotAcceptableError(NetstorageError):
    pass


class ConflictError(NetstorageError):
    pass


class PreconditionFailedError(NetstorageError):
    pass


class UnprocessableEntityError(NetstorageError):
    pass


class LockedError(NetstorageError):
    pass


class InternalServerError(NetstorageError):
    pass


class NotImplementedError(NetstorageError):
    pass


class ClientError(NetstorageError):
    pass


class ServerError(NetstorageError):
    pass


error_classes = {
    400: BadRequestError,
    401: UnauthorizedError,
    403: ForbiddenError,
    404: NotFoundError,
    406: NotAcceptableError,
    409: ConflictError,
    412: PreconditionFailedError,
    422: UnprocessableEntityError,
    423: LockedError,
    500: InternalServerError,
    501: NotImplementedError
}


def raise_exception_for(response):
    error_class = error_classes.get(response.status_code)
    if error_class is None:
        if 400 <= response.status_code <= 500:
            error_class = ClientError
        if 500 <= response.status_code <= 600:
            error_class = ServerError
    return error_class(response)
