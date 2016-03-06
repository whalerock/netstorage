from . import helper


class TestApi(helper.IntegrationHelper):

    def test_dir(self):
        """Test the ability to list the directory contents."""
        cassette_name = self.cassette_name('dir')
        with self.recorder.use_cassette(cassette_name):
            directory_contents = self.ns.dir('/398030')

        assert isinstance(directory_contents, list)
        assert len(directory_contents) > 0
