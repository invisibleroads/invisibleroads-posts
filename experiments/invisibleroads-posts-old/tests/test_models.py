from invisibleroads_macros.exceptions import BadPath
from invisibleroads_posts.models import DummyBase, FolderMixin
from os.path import basename, join
from pytest import raises


class TestFolderMixin(object):

    id_length = 10
    instance_id = 100

    def test_spawn(self, data_folder):
        x = X.spawn(data_folder)
        assert basename(x.folder) == '1'

    def test_spawn_enumerated_folder(self, data_folder):
        folder = X.spawn_folder(data_folder)
        assert basename(folder) == '1'

    def test_spawn_random_folder(self, data_folder):
        folder = X.spawn_folder(data_folder, self.id_length)
        assert len(basename(folder)) == self.id_length

    def test_get_parent_folder(self, data_folder):
        parent_folder = X.get_parent_folder(data_folder)
        assert basename(parent_folder) == X._plural

    def test_get_folder(self, data_folder):
        with raises(BadPath):
            X(id='../1').get_folder(data_folder)
        folder = X(id=self.instance_id).get_folder(data_folder)
        assert basename(folder) == str(self.instance_id)
        assert folder == join(data_folder, 'xs', str(self.instance_id))


class X(FolderMixin, DummyBase):
    pass
