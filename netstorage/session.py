import requests


class Session(requests.Session):

    def __init__(self):
        super(Session, self).__init__()
