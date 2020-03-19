from invisibleroads_macros_descriptor import classproperty
from invisibleroads_macros_disk import (
    check_absolute_path, make_enumerated_folder, make_random_folder)
from invisibleroads_macros_text import normalize_key
from os.path import join


class Base(object):

    def __init__(self, **kw):
        self.__dict__.update(kw)


class FolderMixin(object):

    def get_folder(self, data_folder):
        base_folder = self.get_base_folder(data_folder)
        return check_absolute_path(str(self.id), base_folder)

    @classmethod
    def make_unique_record(Class, data_folder):
        base_folder = Class.get_base_folder(data_folder)
        record = Class()
        try:
            id_length = getattr(Class, 'id_length')
        except AttributeError:
            record.folder = make_enumerated_folder(base_folder)
        else:
            record.folder = make_random_folder(base_folder, id_length)
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
