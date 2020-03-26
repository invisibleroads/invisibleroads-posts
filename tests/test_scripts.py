from invisibleroads.scripts import launch
from os.path import exists


class TestInitializePostsScript(object):

    def test_run(self, mocker, tmpdir):
        data_folder = tmpdir.join('data')
        mocker.patch(
            'invisibleroads_posts.scripts.get_appsettings',
            return_value={'data.folder': data_folder})
        assert not exists(data_folder)
        launch(['invisibleroads', 'initialize', 'development.ini', '--restart'])
        assert exists(data_folder)
