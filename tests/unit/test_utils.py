import netstorage
import mock
import pytest


def test_urlencode():
    """Test encoding a url."""
    destination = netstorage.utils.urlencode('/cpcode/path/file.ext')
    assert destination == '%2Fcpcode%2Fpath%2Ffile.ext'


def test_stream_to_file_raises_exception():
    """Test method raises an exception."""
    response = mock.Mock(status_code=403)
    with pytest.raises(netstorage.exceptions.NetstorageError):
        netstorage.utils.stream_to_file(response, '/tmp/')
