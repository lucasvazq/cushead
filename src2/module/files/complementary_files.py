class ComplementaryFiles:
    icons_config = {}
    config = {}

    def browserconfig(self):
        """browserconfig.xml"""
        if not 'browserconfig' in self.icons_config:
            return ''

        config = self.icons_config['browserconfig']
        icon = config.get('filename', '')
        square_sizes = config.get('square_sizes', [])
        non_square_sizes = config.get('non_square_sizes', [])
        static_url = self.config.get('static_url', '')

        browserconfig = ("<?xml version='1.0' encoding='utf-8'?><browserconfig>"
                         "<msapplication><tile>")
        browserconfig += ''.join([
            "<square{0}x{0}logo src='{1}{2}-{0}x{0}.png' />".format(
                size,
                static_url,
                icon
            )
            for size in square_sizes
        ])
        browserconfig += ''.join([
            "<wide{0}x{1}logo src='{2}{3}-{0}x{1}.png' />".format(
                size[0],
                size[1],
                static_url,
                icon
            )
            for size in non_square_sizes
        ])
        color = self.config.get('background_color', '')
        browserconfig += (f"<TileColor>{color}</TileColor></tile></msapplication>"
                           "</browserconfig>")
        browserconfig = browserconfig.replace('\'', '"')
        return browserconfig
