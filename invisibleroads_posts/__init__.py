def includeme(config):
    configure_settings(config)


def configure_settings(config):
    settings = config.get_settings()
    # Define data_folder
    if 'data.folder' in settings:
        config.add_request_method(
            lambda request: settings['data.folder'], 'data_folder', reify=True)
