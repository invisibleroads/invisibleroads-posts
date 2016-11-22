from invisibleroads_macros.descriptor import classproperty
from invisibleroads_macros.disk import (
    make_enumerated_folder, make_unique_folder, resolve_relative_path)
from invisibleroads_macros.table import normalize_key
from os.path import basename, exists, join
from pyramid.httpexceptions import HTTPNotFound


class DummyBase(object):

    def __init__(self, **kw):
        self.__dict__.update(kw)


class FolderMixin(object):

    @classmethod
    def get_from(Class, request):
        key = Class._singular + '_id'
        matchdict = request.matchdict
        data_folder = request.data_folder
        instance = Class(id=matchdict[key])
        instance_folder = instance.get_folder(data_folder)
        if not exists(instance_folder):
            raise HTTPNotFound
        return instance

    @classmethod
    def spawn(Class, data_folder, random_length=None, *args, **kw):
        instance = Class()
        instance.folder = Class.spawn_folder(
            data_folder, random_length, *args, **kw)
        instance.id = basename(instance.folder)
        return instance

    @classmethod
    def spawn_folder(Class, data_folder, random_length=None):
        parent_folder = Class.get_parent_folder(data_folder)
        return make_unique_folder(
            parent_folder, length=random_length,
        ) if random_length else make_enumerated_folder(parent_folder)

    @classmethod
    def get_parent_folder(Class, data_folder):
        return join(data_folder, Class._plural)

    @classproperty
    def _plural(Class):
        return Class._singular + 's'

    @classproperty
    def _singular(Class):
        key = getattr(Class, '__name__', Class.__class__.__name__)
        return normalize_key(key, word_separator='_', separate_camel_case=True)

    def get_folder(self, data_folder):
        parent_folder = self.get_parent_folder(data_folder)
        return resolve_relative_path(str(self.id), parent_folder)
