import netstorage


def test_urlencode():
    """Test encoding a url."""
    destination = netstorage.utils.urlencode('/cpcode/path/file.ext')
    assert destination == '%2Fcpcode%2Fpath%2Ffile.ext'
