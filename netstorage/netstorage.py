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
        pass


    def du(self, path):
        """Download a file from netstorage to local file system."""
        # Remove trailing slash which causes 400 error
        path= path.rstrip('/')
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
        return response

    def download(self, path, destination):
        """Download a file from netstorage to local file system."""
        # Remove trailing slash which causes 400 error
        path= path.rstrip('/')
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
        # Successful
        if response.status_code == 200:
            log.info("Deleted file {0}".format(path))
            return True
        # File not found
        if response.status_code == 404:
            log.info("File not found {0}".format(path))
            return False

    def dir(self, path):
        """List directory contents."""
        # Remove trailing slash which causes 400 error
        path = path.rstrip('/')
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
        # TODO: Refactor this into separate methods
        if response.status_code == 200:
            return parsers.DirResponse(response.content).parse()
        else:
            raise exceptions.NetstorageBadRequest(url)


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

    def _expected_response(self, response_code, true_code, false_code):
        if response_code is None:
            if response_code == true_code:
                return True
            if response_code != status_code and response_code >= 400:
                raise Exception("Bad request.")
        return False


