from . import auth
from . import utils
from . import session
from . import exceptions
from . import parsers
import logging

log = logging.getLogger(__name__)


class Netstorage(object):

    def __init__(self, keyname, key, host):
        self.key = key
        self.keyname = keyname
        self.host = host
        self.session = session.Session()

    def du(self, path):
        """Download a file from netstorage to local file system."""
        # Remove trailing slash which causes 400 error
        path = path.rstrip('/')
        acs_auth_action = auth.build_acs_action('du', xml=True)
        acs_auth_data = auth.acs_auth_data(self.keyname)
        acs_auth_sign = auth.acs_auth_sign(self.key, acs_auth_action, acs_auth_data, path)
        headers = {
            'X-Akamai-ACS-Auth-Data': acs_auth_data,
            'X-Akamai-ACS-Auth-Sign': acs_auth_sign,
            'X-Akamai-ACS-Action': acs_auth_action.split(':')[1],
            'Host': self.host
        }

        url = self._build_url(self.host, path)
        response = self.session.get(url, headers=headers)
        parser = parsers.DuResponse(response.content)
        return self._parse(response, 200, parser)

    def download(self, path, destination):
        """Download a file from netstorage to local file system."""
        # Remove trailing slash which causes 400 error
        path = '/' + path.strip('/')
        acs_auth_action = auth.build_acs_action('download', xml=False)
        acs_auth_data = auth.acs_auth_data(self.keyname)
        acs_auth_sign = auth.acs_auth_sign(self.key, acs_auth_action, acs_auth_data, path)
        headers = {
            'X-Akamai-ACS-Auth-Data': acs_auth_data,
            'X-Akamai-ACS-Auth-Sign': acs_auth_sign,
            'X-Akamai-ACS-Action': acs_auth_action.split(':')[1],
            'Host': self.host
        }

        url = self._build_url(self.host, path)
        response = self.session.get(url, headers=headers)
        downloaded = utils.stream_to_file(response, destination)
        log.info('Created {0}'.format(downloaded))
        return downloaded

    def delete(self, path):
        """Delete a file on netstorage"""
        # Remove trailing slash which causes 400 error
        path = path.rstrip('/')
        acs_auth_action = auth.build_acs_action('delete', xml=False)
        acs_auth_data = auth.acs_auth_data(self.keyname)
        acs_auth_sign = auth.acs_auth_sign(self.key, acs_auth_action, acs_auth_data, path)
        headers = {
            'X-Akamai-ACS-Auth-Data': acs_auth_data,
            'X-Akamai-ACS-Auth-Sign': acs_auth_sign,
            'X-Akamai-ACS-Action': acs_auth_action.split(':')[1],
            'Host': self.host
        }

        url = self._build_url(self.host, path)
        response = self.session.put(url, headers=headers)
        response.raise_for_status()
        return

    def upload(self, local, destination):
        """Upload a local file to nestorage.

        :param local string: (required) Path to local file to upload
        :param destination string: (required) Destination on netstorage to
            save file to
        :returns: None
        """
        # Remove trailing slash which causes 400 error
        path = destination
        path = '/' + path.strip('/')
        acs_auth_action = auth.build_acs_action('upload', xml=False)
        acs_auth_data = auth.acs_auth_data(self.keyname)
        acs_auth_sign = auth.acs_auth_sign(self.key, acs_auth_action, acs_auth_data, path)
        headers = {
            'X-Akamai-ACS-Auth-Data': acs_auth_data,
            'X-Akamai-ACS-Auth-Sign': acs_auth_sign,
            'X-Akamai-ACS-Action': acs_auth_action.split(':')[1],
            'Host': self.host
        }

        url = self._build_url(self.host, path)
        with open(local) as fh:
            data = fh.read()
        response = self.session.put(url, headers=headers, data=data)
        response.raise_for_status()
        return

    def dir(self, path):
        """List directory contents."""
        # Remove trailing slash which causes 400 error
        path = '/' + path.strip('/')
        acs_auth_action = auth.build_acs_action('dir', xml=True)
        acs_auth_data = auth.acs_auth_data(self.keyname)
        acs_auth_sign = auth.acs_auth_sign(self.key, acs_auth_action, acs_auth_data, path)
        headers = {
            'X-Akamai-ACS-Auth-Data': acs_auth_data,
            'X-Akamai-ACS-Auth-Sign': acs_auth_sign,
            'X-Akamai-ACS-Action': acs_auth_action.split(':')[1],
            'Host': self.host
        }

        url = self._build_url(self.host, path)
        response = self.session.get(url, headers=headers)
        parser = parsers.DirResponse(response.content)
        return self._parse(response, 200, parser)


    def mkdir(self, path):
        """Make a directory specified by path."""
        # Remove trailing slash which causes 400 error
        path = '/' + path.strip('/')
        acs_auth_action = auth.build_acs_action('mkdir', xml=False)
        acs_auth_data = auth.acs_auth_data(self.keyname)
        acs_auth_sign = auth.acs_auth_sign(self.key, acs_auth_action, acs_auth_data, path)
        headers = {
            'X-Akamai-ACS-Auth-Data': acs_auth_data,
            'X-Akamai-ACS-Auth-Sign': acs_auth_sign,
            'X-Akamai-ACS-Action': acs_auth_action.split(':')[1],
            'Host': self.host
        }

        url = self._build_url(self.host, path)
        response = self.session.put(url, headers=headers)
        self.response_successful(response, 200)

    def rename(self, path, destination):
        """Rename a file on nestorage

        :param path str: path of file to be renamed (e.g "/39650/new.txt")
        :param destination str: new path (e.g "/39650/old.txt")
        :returns:
        """
        # Remove trailing slash which causes 400 error
        path = path.rstrip('/')
        encoded_destination = 'destination={}'.format(utils.urlencode(destination))
        acs_auth_action = auth.build_acs_action('rename', xml=False)
        acs_auth_action = '&'.join([acs_auth_action, encoded_destination])
        acs_auth_data = auth.acs_auth_data(self.keyname)
        acs_auth_sign = auth.acs_auth_sign(self.key, acs_auth_action, acs_auth_data, path)
        headers = {
            'X-Akamai-ACS-Auth-Data': acs_auth_data,
            'X-Akamai-ACS-Auth-Sign': acs_auth_sign,
            'X-Akamai-ACS-Action': acs_auth_action.split(':')[1],
            'Host': self.host
        }

        url = self._build_url(self.host, path)
        response = self.session.post(url, headers=headers)
        expected_response = self._expected_response(response, 200, 404)
        return expected_response

    def _build_url(self, hostname, uri, secure=True):
        """Builds a properly formatted URL.

        By default, we will use HTTPS but allow nonsecure for troubleshooting
            purposes (i.e "tcpdump", "wireshark")

        :param hostname str: (required) Resolvable hostname
        :param uri str: (required) URI
        :param secure boolean: False for http. Default is True
        """
        protocol = 'https://' if secure else 'http://'
        url = '{0}{1}{2}'.format(protocol, hostname, uri)
        return url

    def response_successful(self, response, true_code):
        if response.status_code != true_code:
            raise exceptions.raise_exception_for(response)

    def _expected_response(self, response, true_code, false_code):
        if response.status_code is not None:
            if response.status_code == true_code:
                return True
            if response.status_code != false_code and response.status_code >= 400:
                raise exceptions.raise_exception_for(response)
        return False

    @staticmethod
    def _parse(response, expected_status_code, parser):
        if response.status_code == expected_status_code:
            return parser.parse()
        else:
            raise exceptions.raise_exception_for(response)
