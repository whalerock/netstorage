import requests


class Session(requests.session):

    def __init__(self):
        super(Session, self).__init__()
