from . import helper


class TestNetstorage(helper.IntegrationHelper):

    def test_dir(self):
        """Test the ability to list the directory contents."""
        cassette_name = self.cassette_name('dir')
        with self.recorder.use_cassette(cassette_name):
            directory_contents = self.ns.dir('/398030')

        assert isinstance(directory_contents, list)
        assert len(directory_contents) > 0

    def test_du(self):
        """Test the ability to retrieve disk usage statistics."""
        cassette_name = self.cassette_name('du')
        with self.recorder.use_cassette(cassette_name):
            disk_usage = self.ns.du('/398030')

        assert disk_usage
