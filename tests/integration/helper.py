from netstorage import Netstorage
import unittest
import betamax
import os


class IntegrationHelper(unittest.TestCase):

    def setUp(self):
        key_name = os.environ.get('AKAMAI_KEY_NAME', 'akamai-key-name')
        key = os.environ.get('AKAMAI_KEY', 'akamai-key')
        host = os.environ.get('AKAMAI_HOST', 'akamai-host')
        self.ns =  Netstorage(key_name, key, host)
        self.recorder = betamax.Betamax(self.ns.session)

    @property
    def described_class(self):
        class_name = self.__class__.__name__
        return class_name[4:]

    def cassette_name(self, name):
        cassette_name = '_'.join([self.described_class, name])
        return cassette_name
