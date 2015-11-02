from invisibleroads.scripts import ConfigurableScript
from invisibleroads_macros.disk import make_folder, remove_path
from pyramid.paster import get_appsettings


class InitializePostsScript(ConfigurableScript):

    priority = 10

    def configure(self, argument_subparser):
        super(ConfigurableScript, self).configure(argument_subparser)
        argument_subparser.add_argument('--restart', action='store_true')

    def run(self, args):
        settings = get_appsettings(args.configuration_path)
        if args.restart and 'data.folder' in settings:
            remove_path(settings['data.folder'])
        for key, value in settings.items():
            if key.endswith('.folder'):
                make_folder(value)
