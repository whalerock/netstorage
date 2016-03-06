from collections import namedtuple
import os
import betamax

class AkamaiActionMatcher(betamax.BaseMatcher):

    name = 'akamai-action'

    def match(self, request, recorded_request):
        request_action = request.headers.get('X-Akamai-ACS-Action', '--')
        recorded_action = ''.join(recorded_request['headers'].get('X-Akamai-ACS-Action'))
        action_matches = True if request_action == recorded_action else False
        return action_matches

betamax.Betamax.register_request_matcher(AkamaiActionMatcher)


def akamai_config():
    AkamaiConfig= namedtuple('AkamaiConfig', 'key_name key host')
    key_name = os.environ.get('AKAMAI_KEY_NAME', 'akamai-key-name')
    key = os.environ.get('AKAMAI_KEY', 'akamai-key')
    host = os.environ.get('AKAMAI_HOST', 'akamai-host')
    return AkamaiConfig(key_name, key, host)

with betamax.Betamax.configure() as config:

    config.cassette_library_dir = 'tests/cassettes'
    akamaiconfig = akamai_config()
    config.define_cassette_placeholder('<key-name>',akamaiconfig.key_name)
    config.define_cassette_placeholder('<host>', akamaiconfig.host)
