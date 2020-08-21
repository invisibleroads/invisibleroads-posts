from invisibleroads.scripts import ConfigurableScript
from invisibleroads_macros_disk import make_folder, remove_folder

from .routines.configuration import load_filled_settings


class InitializePostsScript(ConfigurableScript):

    priority = 10

    def configure(self, argument_subparser):
        super(InitializePostsScript, self).configure(argument_subparser)
        argument_subparser.add_argument('--restart', action='store_true')

    def run(self, args, argv):
        settings = load_filled_settings(args.configuration_path)
        if args.restart and 'data.folder' in settings:
            remove_folder(settings['data.folder'])
        for key, value in settings.items():
            if key.endswith('.folder'):
                make_folder(value)
