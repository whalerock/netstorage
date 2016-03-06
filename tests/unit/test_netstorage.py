import mock
import netstorage

def test_parse():
    response = mock.Mock(status_code=200)
    parser = mock.Mock()
    netstorage.Netstorage._parse(response, 200, parser)
    assert parser.parse.called is True

