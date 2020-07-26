from invisibleroads.scripts import launch


CONFIGURATION_TEXT = '''\
[app:main]
use = egg:pyramid
data.folder = %(here)s/data
'''


class TestInitializePostsScript(object):

    def test_run(self, mocker, tmp_path):
        data_folder = tmp_path / 'data'
        assert not data_folder.exists()

        for function_name in [
            'load_bootstrapped_settings',
            'load_filled_settings',
        ]:
            module_uri = 'invisibleroads_posts.routines.configuration'
            mocker.patch(module_uri + '.' + function_name, return_value={
                'data.folder': data_folder})

        launch([
            'invisibleroads',
            'initialize',
            'test.ini',
            '--restart',
        ])
        assert data_folder.exists()
