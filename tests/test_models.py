from invisibleroads_posts.models import FolderMixin


INSTANCE_ID = 777


class TestFolderMixin(object):

    def test_make_enumerated_record(self, data_folder):
        class X(FolderMixin, DummyBase):
            pass
        folder = X.make_unique_record(data_folder)

    def test_make_random_record(self, data_folder):
        class X(FolderMixin, DummyBase):
            id_length = 7
        folder = X.make_unique_record(data_folder)

    def test_get_parent_folder(self, data_folder):
        pass

    def test_get_folder(self, data_folder):
        pass


class DummyBase(object):

    def __init__(self, **kw):
        self.__dict__.update(kw)
