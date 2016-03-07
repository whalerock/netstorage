import netstorage
import pytest

from . import helper


class TestNetstorage(helper.IntegrationHelper):

    def test_dir(self):
        """Test the ability to list the directory contents."""
        cassette_name = self.cassette_name('dir')
        betamax_kwargs = {
            'match_requests_on': ['akamai-action', 'uri']
        }
        with self.recorder.use_cassette(cassette_name, **betamax_kwargs):
            directory_contents = self.ns.dir('/398030')

        assert isinstance(directory_contents, list)
        assert len(directory_contents) > 0
        for item in directory_contents:
            assert isinstance(item, netstorage.models.NetstorageFile)


    def test_du(self):
        """Test the ability to retrieve disk usage statistics."""
        cassette_name = self.cassette_name('du')
        betamax_kwargs = {
            'match_requests_on': ['akamai-action', 'uri']
        }
        with self.recorder.use_cassette(cassette_name, **betamax_kwargs):
            disk_usage = self.ns.du('/398030')

        assert isinstance(disk_usage, netstorage.models.NetstorageDiskUsage)


    def test_du_on_wrong_path(self):
        """Test the ability to retrieve disk usage statistics."""
        cassette_name = self.cassette_name('du_wrong_path')
        betamax_kwargs = {
            'match_requests_on': ['akamai-action', 'uri']
        }
        with self.recorder.use_cassette(cassette_name, **betamax_kwargs):
            with pytest.raises(netstorage.exceptions.ForbiddenError):
                self.ns.du('/123456')


    def test_rename(self):
        """Test the ability to rename a file."""
        cassette_name = self.cassette_name('rename')
        betamax_kwargs = {
            'match_requests_on': ['akamai-action', 'uri']
        }
        with self.recorder.use_cassette(cassette_name, **betamax_kwargs):
            renamed = self.ns.rename('/415822/new.txt', '/415822/old.txt')
        assert renamed is True
