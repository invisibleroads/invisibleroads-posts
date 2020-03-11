from invisibleroads_macros.descriptor import classproperty
from invisibleroads_macros.disk import (
    get_absolute_path, make_enumerated_folder, make_unique_folder)
from invisibleroads_macros.table import normalize_key
from os.path import basename, exists, join
from pyramid.httpexceptions import HTTPNotFound


class FolderMixin(object):

    @classmethod
    def get_from(Class, request, record_id=None):
        key = Class._singular + '_id'
        if not record_id:
            record_id = get_record_id(request, key)
        data_folder = request.data_folder
        instance = Class(id=record_id)
        instance_folder = instance.get_folder(data_folder)
        if not exists(instance_folder):
            raise HTTPNotFound({key: 'bad'})
        return instance

    @classmethod
    def spawn(Class, data_folder, id_length=None, *args, **kw):
        instance = Class()
        instance.folder = Class.spawn_folder(
            data_folder, id_length, *args, **kw)
        instance.id = basename(instance.folder)
        return instance

    @classmethod
    def spawn_folder(Class, data_folder, id_length=None):
        parent_folder = Class.get_parent_folder(data_folder)
        return make_unique_folder(
            parent_folder, length=id_length,
        ) if id_length else make_enumerated_folder(parent_folder)

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
        return get_absolute_path(
            str(self.id), parent_folder, resolve_links=False)
