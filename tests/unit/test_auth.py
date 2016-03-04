from netstorage import auth


def test_get_acs_auth_data():
    """Verify that X-Akamai-ACS-Auth-Data is formatted correctly."""
    timestamp = 1280000000
    unique_id = '382644692'
    key = 'key1'
    data = '5, 0.0.0.0, 0.0.0.0, 1280000000, 382644692, key1'
    assert auth.acs_auth_data(key, unique_id, timestamp) == data


def test_get_acs_auth_sign():
    """Test method returns correct hash.

    This example is directly from the netstorage documentation. See
        https://control.akamai.com/dl/customers/NS/NS_http_api_FS.pdf
        page 17
    """
    acs_auth_data = '5, 0.0.0.0, 0.0.0.0, 1280000000, 382644692, key1'
    path = '/dir1/dir2/file.html'
    key = 'abcdefghij'
    expected_hmac = 'vuCWPzdEW5OUlH1rLfHokWAZAWSdaGTM8yX3bgIDWtA='
    acs_auth_action = 'version=1&action=upload'
    hmac = auth.acs_auth_sign(key, acs_auth_action, acs_auth_data, path)

    #  assert hmac == expected_hmac


def test_get_acs_auth_sign_with_optional_headers():
    """Test method returns correct hash.

    This example is directly from the netstorage documentation. See
        https://control.akamai.com/dl/customers/NS/NS_http_api_FS.pdf
        page 17
    """
    acs_auth_data = '5, 0.0.0.0, 0.0.0.0, 1280000000, 382644692, key1'
    path = '/dir1/dir2/file.html'
    key = 'abcdefghij'
    expected_hmac = 'vuCWPzdEW5OUlH1rLfHokWAZAWSdaGTM8yX3bgIDWtA='
    optional_headers = {
        'md5': '0123456789abcdef0123456789abcdef',
        'mtime': '1260000000'
    }
    acs_auth_action = 'x-akamai-acs-action:version=1&action=upload'
    hmac = auth.acs_auth_sign(key, acs_auth_action, acs_auth_data, path,
                              optional_headers=optional_headers)

    assert hmac == expected_hmac

def test_build_optional_headers():
    optional_headers = {
        'md5': '0123456789abcdef0123456789abcdef',
        'mtime': '1260000000'
    }

    expected_output = '&md5=0123456789abcdef0123456789abcdef&mtime=1260000000'
    assert auth.build_optional_headers(optional_headers) == expected_output

def test_build_acs_action():
    acs_action = auth.build_acs_action('du')
    assert acs_action == 'x-akamai-acs-action:version=1&action=du&format=xml'

    acs_action = auth.build_acs_action('upload', xml=False)
    assert acs_action == 'x-akamai-acs-action:version=1&action=upload'
