from invisibleroads_macros_disk.exceptions import PathValidationError
from os.path import basename, join
from pyramid.httpexceptions import HTTPNotFound
from pytest import raises

from invisibleroads_posts.models import Base, FolderMixin


INSTANCE_ID = 777


class TestFolderMixin(object):

    def test_get_folder(self, data_folder):
        with raises(PathValidationError):
            EnumeratedRecord(id='../1').get_folder(data_folder)
        folder = EnumeratedRecord(id=7).get_folder(data_folder)
        assert folder == join(data_folder, 'enumerated_records', '7')

    def test_get_from(self, posts_request, data_folder):
        posts_request.matchdict['random_record_id'] = 'x'
        with raises(HTTPNotFound):
            record = RandomRecord.get_from(posts_request)
        record = RandomRecord.make_unique_record(data_folder)
        record_id = record.id
        posts_request.matchdict['random_record_id'] = record_id
        record = RandomRecord.get_from(posts_request)
        assert record.id == record_id

    def test_make_enumerated_record(self, data_folder):
        record1 = EnumeratedRecord.make_unique_record(data_folder)
        record2 = EnumeratedRecord.make_unique_record(data_folder)
        assert basename(record1.folder) == '1'
        assert basename(record2.folder) == '2'

    def test_make_random_record(self, data_folder):
        record = RandomRecord.make_unique_record(data_folder)
        assert len(basename(record.folder)) == RandomRecord.id_length

    def test_get_base_folder(self, data_folder):
        base_folder = EnumeratedRecord.get_base_folder(data_folder)
        assert basename(base_folder) == EnumeratedRecord.plural_descriptor


class EnumeratedRecord(FolderMixin, Base):
    pass


class RandomRecord(FolderMixin, Base):
    id_length = 7
