from invisibleroads_macros_descriptor import classproperty
from invisibleroads_macros_disk import (
    check_absolute_path, make_enumerated_folder, make_random_folder)
from invisibleroads_macros_text import normalize_key
from os.path import basename, exists, join
from pyramid.httpexceptions import HTTPNotFound

from .variables import POSTS_REGISTRY
from .views import get_value


class RegisteredClass(type):

    def __init__(Class, name, *args):
        super().__init__(name, *args)
        POSTS_REGISTRY[name] = Class


class EnumeratedBase(object):

    def __init__(self, **kw):
        self.__dict__.update(kw)


class RandomBase(EnumeratedBase, metaclass=RegisteredClass):
    pass


class FolderMixin(object):

    def get_folder(self, data_folder):
        base_folder = self.get_base_folder(data_folder)
        return check_absolute_path(str(self.id), base_folder)

    @classmethod
    def get_from(Class, request, record_id=None):
        key = Class.singular_descriptor + 'Id'
        if record_id is None:
            record_id = get_value(request, key)
        data_folder = request.data_folder
        record = Class(id=record_id)
        record_folder = record.get_folder(data_folder)
        if not exists(record_folder):
            raise HTTPNotFound({key: 'bad'})
        return record

    @classmethod
    def make_unique_record(Class, data_folder):
        base_folder = Class.get_base_folder(data_folder)
        record = Class()
        try:
            id_length = getattr(Class, 'id_length')
        except AttributeError:
            record_folder = make_enumerated_folder(base_folder)
        else:
            record_folder = make_random_folder(base_folder, id_length)
        record.id = basename(record_folder)
        record.folder = record_folder
        return record

    @classmethod
    def get_base_folder(Class, data_folder):
        return join(data_folder, Class.plural_descriptor)

    @classproperty
    def plural_descriptor(Class):
        return Class.singular_descriptor + 's'

    @classproperty
    def singular_descriptor(Class):
        key = getattr(Class, '__name__', Class.__class__.__name__)
        return normalize_key(key, word_separator='_', separate_camel_case=True)
