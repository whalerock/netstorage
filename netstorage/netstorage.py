from . import auth
import requests


class Netstorage(object):

    def __init__(self, keyname, key, host):
        self.key = key
        self.keyname = keyname
        self.host = host
        pass

    def download(self, local, remote):
        """Download a file from netstorage to local file system."""
        acs_auth_data = auth.acs_auth_data(self.keyname)
        acs_auth_sign = auth.acs_auth_sign(self.key, acs_auth_data, remote, 'download')
        remote = '/' + remote.lstrip('/')
        headers = {
            'X-Akamai-ACS-Auth-Data': acs_auth_data,
            'X-Akamai-ACS-Auth-Sign': acs_auth_sign,
            'X-Akamai-ACS-Action': 'version=1&action=download',
            'Host': self.host,
            'User-Agent': 'netstorage/1.0'
        }

        hostname = 'https://' + self.host
        url = hostname + remote
        response = requests.get(url, headers=headers)
        return response

    def du(self, remote):
        """Download a file from netstorage to local file system."""
        acs_action = 'version=1&action=du&format=xml'
        acs_auth_action = auth.build_acs_action('du', xml=True)
        acs_auth_data = auth.acs_auth_data(self.keyname)
        acs_auth_sign = auth.acs_auth_sign(self.key, acs_auth_action, acs_auth_data, remote)
        remote = '/' + remote.lstrip('/')
        headers = {
            'X-Akamai-ACS-Auth-Data': acs_auth_data,
            'X-Akamai-ACS-Auth-Sign': acs_auth_sign,
            'X-Akamai-ACS-Action': acs_action,
            'Host': self.host
        }

        hostname = 'http://' + self.host
        url = hostname + remote
        response = requests.get(url, headers=headers)
        return response

