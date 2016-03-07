from . import exceptions
import logging
import os
import urllib

log = logging.getLogger(__name__)


def filename_from(url):
    """Get the name of the file based off of the URL."""
    filename = url.split('/')[-1]
    return filename


def stream_to_file(response, destination):
    """Write contents of response to a file.

    :param response response: (required) requests.response
    :param destination str: (required) Destination to save file
    :returns: `str` file destination
    """
    if response.status_code != 200:
        raise exceptions.raise_exception_for(response)
    if os.path.isdir(destination):
        destination = os.path.join(destination, filename_from(response.url))
    with open(destination, 'wb') as fh:
        for chunk in response.iter_content(chunk_size=512):
            fh.write(chunk)
    return destination


def urlencode(path):
    """URL encode a destination."""
    return urllib.quote_plus(path)
