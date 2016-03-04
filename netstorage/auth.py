from time import time
import random
import hmac
import hashlib


def acs_auth_data(keyname, unique_id=None, timestamp=None):
    """Creates X-Akamai-ACS-Auth-Data contents

    See also: https://control.akamai.com/dl/customers/NS/NS_http_api_FS.pdf
        page 17

    :param key str: (required) Key
    :param unique_id str: (optional) A unique ID for the request
    :param timestamp str: (optional) A timestamp in epoch format
    """

    VERSION = '5'
    RESERVE_FIELDS = '0.0.0.0, 0.0.0.0'
    timestamp = str(int(timestamp)) if timestamp else str(int(time()))
    unique_id = str(unique_id) if unique_id else str(random.getrandbits(64))
    data = ', '.join([VERSION, RESERVE_FIELDS, timestamp, unique_id, keyname])
    return data


def acs_auth_sign(key, acs_action, acs_auth_data, path, optional_headers=None):
    """Creates X-Akamai-ACS-Auth-Sign value.

    See also: https://control.akamai.com/dl/customers/NS/NS_http_api_FS.pdf
        page 17

    :param key str: (required) API key
    :param acs_auth_data str: (required) Message to hash. This will be the
        contents of X-Akamai-ACS-Auth-Data
    :param path str: (required): Filesystem path e.g ("/302386")
    :param optional_headers dict: (optional) Optional headers (e.g "md5,
        mtime")
    """
    path = path.rstrip('\n') + '\n'
    optional_headers = build_optional_headers(optional_headers)
    message = ''.join([acs_auth_data, path, acs_action, optional_headers, '\n'])
    digest = hmac.new(str(key), msg=message, digestmod=hashlib.sha256).digest()
    sign = digest.encode('base64').strip()
    return sign


def build_acs_action(action, xml=True):
    """
    Returns a string similar to
    x-akamai-acs-action:version=1&action=du&format=xml'
    """
    acs_action = 'x-akamai-acs-action:version=1&action={0}'.format(action)
    acs_action = acs_action + '&format=xml' if xml else acs_action
    return acs_action


def build_optional_headers(headers):
    """
    :param headers dict: (required)
    :returns: str

    example_dict = {
        'md5': '0123456789abcdef0123456789abcdef',
        'mtime': '1260000000'
    }
    """
    # sorted so that we product a consistent string
    if not headers:
        return ''
    keys = sorted(headers.keys(), key=str)
    optional_headers = ['{0}={1}'.format(key, headers[key]) for key in keys]
    optional_headers = '&'.join(optional_headers)
    optional_headers = '&' + optional_headers
    return optional_headers
