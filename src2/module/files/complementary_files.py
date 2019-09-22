
import json
from os import path

class ComplementaryFiles:
    config: dict
    icons_config: dict

    def full_complementary_files(self):
        return {
            'browserconfig': self._browserconfig(),
            'manifest': self._manifest(),
            'opensearch': self._opensearch(),
            'robots': self._robots(),
            'sitemap': self._sitemap(),
        }

    def _browserconfig(self):
        """browserconfig.xml"""
        browserconfig_config = self.icons_config.get('browserconfig', {})
        icon = browserconfig_config.get('filename', '')
        square_sizes = browserconfig_config.get('square_sizes', [])
        non_square_sizes = browserconfig_config.get('non_square_sizes', [])
        static_url = self.config.get('static_url', '')
        browserconfig = ("<?xml version='1.0' encoding='utf-8'?>"
                         "<browserconfig><msapplication><tile>")
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
        browserconfig += ( "<TileColor>"
                          f"{self.config.get('background_color', '')}"
                           "</TileColor></tile></msapplication>"
                           "</browserconfig>").replace('\'', '"')
        destination_path = path.join(self.config.get('static_folder_path', ''),
                                    'browserconfig.xml')
        return {
            'content': browserconfig,
            'destination_path': destination_path,
        }

    def _manifest(self):
        """manifest.json"""
        manifest_config = self.icons_config.get('manifest', {})
        manifest = {}
        if 'title' in self.config:
            manifest['name'] = self.config['title']
            manifest['short_name'] = self.config['title']
        if 'description' in self.config:
            manifest['description'] = self.config['description']
        if 'dir' in self.config:
            manifest['dir'] = self.config['dir']
        if 'start_url' in self.config:
            manifest['start_url'] = self.config['start_url']
        if 'orientation' in self.config:
            manifest['orientation'] = self.config['orientation']
        if 'background_color' in self.config:
            manifest['background_color'] = self.config['background_color']
            manifest['theme_color'] = self.config['background_color']
        if 'language' in self.config:
            manifest['default_locale'] = self.config['language']
        if 'scope' in self.config:
            manifest['scope'] = self.config['scope']
        if 'display' in self.config:
            manifest['display'] = self.config['display']
        if 'platform' in self.config:
            manifest['platform'] = self.config['platform']
        if 'applications' in self.config:
            manifest['related_applications'] = self.config['applications']
        manifest['icons'] = [
            {
                'src': "{0}{1}-{2}x{2}".format(
                    self.config.get('static_url', ''),
                    manifest_config.get('filename', ''), size
                ),
                'sizes': f"{size}x{size}",
                'type': 'image/png',
                'density': str(size / 48)
            }
            for size in manifest_config.get('square_sizes', [])
        ]
        manifest = json.dumps(manifest)
        destination_path = path.join(self.config.get('static_folder_path', ''),
                                     'manifest.json')
        return {
            'content': manifest,
            'destination_path': destination_path,
        }

    def _opensearch(self):
        """opensearch.xml"""
        opensearch = (
            ("<?xml version='1.0' encoding='utf-8'?>"
             "<OpenSearchDescription xmlns:moz='"
             "http://www.mozilla.org/2006/browser/search/' "
             "xmlns='http://a9.com/-/spec/opensearch/1.1/'>"
             "</OpenSearchDescription>"
             "<ShortName>{0}</ShortName>"
             "<Description>Search {0}</Description>"
             "<InputEncoding>UTF-8</InputEncoding>"
             "<Url method='get' type='text/html' "
             "template='http://www.google.com/search?q="
             "{{searchTerms}}+site%3A{1}' />"
             "<Image height='16' width='16' type='image/png'>"
             "{2}/opensearch-16x16.png"
             "</Image>")
            .format(
                self.config.get('title', ''),
                self.config.get('url', ''),
                self.config.get('static_url', ''),
            ).replace('\'', '"')
        )
        destination_path = path.join(self.config.get('static_folder_path', ''),
                                     'opensearch.xml')
        return {
            'content': opensearch,
            'destination_path': destination_path,
        }

    def _robots(self):
        """robots.txt"""
        # clean_url
        sitemap_reference = (
            "\n"
            f"Sitemap: {self.config.get('protocol', '')}"
            f"{self.config.get('clean_url', '')}/sitemap.xml"
            if 'sitemap' in self.config else ''
        )
        robots = ( "User-agent: *\n"
                   "Allow: /\n"
                  f"{sitemap_reference}")
        destination_path = path.join(self.config.get('output_folder_path', ''),
                                     'robots.txt')
        return {
            'content': robots,
            'destination_path': destination_path
        }

    def _sitemap(self):
        """sitemap.xml"""
        # clean_url
        sitemap = ( "<?xml version='1.0' encoding='uft-8'?>"
                    "<urlset xmlns="
                    "'http://www.sitemaps.org/schemas/sitemap/0.9' "
                    "xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' "
                    "xsi:schemaLocation="
                    "'http://www.sitemaps.org/schemas/sitemap/0.9 "
                    "http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd'>"
                   f"<url><loc>{self.config.get('protocol', '')}"
                   f"{self.config.get('clean_url', '')}/</loc>"
                    "</url></urlset>").replace('\'', '"')
        destination_path = path.join(self.config.get('output_folder_path', ''),
                                     'sitemap.xml')
        return {
            'content': sitemap,
            'destination_path': destination_path,
        }
