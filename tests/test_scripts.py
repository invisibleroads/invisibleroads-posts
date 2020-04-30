from invisibleroads.scripts import launch
from os.path import exists


class TestInitializePostsScript(object):

    def test_run(self, mocker, tmpdir):
        data_folder = tmpdir.join('data')
        assert not exists(data_folder)
        mocker.patch(
            'invisibleroads_posts.routines.configuration.'
            'load_bootstrapped_settings',
            return_value={'data.folder': data_folder})
        launch([
            'invisibleroads',
            'initialize',
            'test.ini',
            '--restart',
        ])
        assert exists(data_folder)
