from os.path import basename, splitext
from titlecase import titlecase


def render_title(path):
    nickname = splitext(basename(path.rstrip('/')))[0]
    return titlecase(nickname.replace('-', ' '))
