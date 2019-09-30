from os import path
from typing import Dict, List, Union

from src.services.images import ImageService


class ImageFilesCreation(ImageService):
    """Class to handle the default configuration used for images creation

    Methods:
        default_icons_creation_config
            -> List[Dict[str, Union[List[int], bool, str]]]:
    """
    config = {}
    icons_config = {}

    def _default_png_icons_creation(self, brand) -> List[Dict[str, Union[List[int], bool, str]]]:
        images_format = []
        favicon_png = self.config.get('favicon_png', '')
        if not favicon_png:
            return images_format
        destination_file_path_unformatted = path.join(
            self.config.get('static_folder_path', ''), "{}-{}x{}.png"
        )
        source_file_path = path.join(self.config.get('main_folder_path', ''),
                                     favicon_png)
        for brand_icon_config in self.icons_config.get(brand, []):
            file_name = getattr(brand_icon_config, 'file_name', '')
            for size in self.format_sizes(brand_icon_config):
                destination_file_path = (
                    destination_file_path_unformatted.format(file_name,
                                                             size[0], size[1])
                )
                images_format.append({
                    'destination_file_path': destination_file_path,
                    'resize': True,
                    'size': size,
                    'source_file_path': source_file_path,
                })
        return images_format

    def _favicon_ico_icons_creation(self) -> List[Dict[str, Union[List[int], bool, str]]]:
        favicon_ico = self.config.get('favicon_ico', '')
        if not favicon_ico:
            return []
        destination_file_path = path.join(
            self.config.get('output_folder_path'),
            'favicon.ico',
        )
        source_file_path = path.join(self.config.get('main_folder_path', ''),
                                     favicon_ico)
        return [{
            'destination_file_path': destination_file_path,
            'resize': False,
            'size': [],
            'source_file_path': source_file_path,
        }]

    def _favicon_png_icons_creation(self):
        return self._default_png_icons_creation('favicon_png')

    def _favicon_svg_icons_creation(self) -> List[Dict[str, Union[List[int], bool, str]]]:
        favicon_svg = self.config.get('favicon_svg', '')
        if not favicon_svg:
            return []
        destination_file_path = path.join(
            self.config.get('static_folder_path'),
            'favicon.svg',
        )
        source_file_path = path.join(self.config.get('main_folder_path'),
                                     favicon_svg)
        return [{
            'destination_file_path': destination_file_path,
            'resize': False,
            'size': [],
            'source_file_path': source_file_path,
        }]

    def _preview_png_icons_creation(self) -> List[Dict[str, Union[List[int], bool, str]]]:
        preview_png = self.config.get('preview_png', '')
        if not preview_png:
            return []
        destination_file_path = path.join(
            self.config.get('static_folder_path'),
            'preview-500x500.png',
        )
        source_file_path = path.join(self.config.get('main_folder_path'),
                                     preview_png)
        return [{
            'destination_file_path': destination_file_path,
            'resize': True,
            'size': [500, 500],
            'source_file_path': source_file_path,
        }]

    def _browserconfig_icons_creation(self):
        return self._default_png_icons_creation('browserconfig')

    def _manifest_icons_creation(self):
        return self._default_png_icons_creation('manifest')

    def _opensearch_icons_creation(self):
        return self._default_png_icons_creation('opensearch')

    def get_icons_creation_config(self) \
            -> List[Dict[str, Union[List[int], bool, str]]]:
        """Return a list with default images creation configuration

        It's include configurations for the images listed in the assets folder

        Default structure of the dicts in the return is:
        {
            'destination_file_path': str,
            'resize': bool,
            'size': list,
            'source_file_path': str,
        }
        """
        icons_creation_config = [
            self._favicon_ico_icons_creation(),
            self._favicon_png_icons_creation(),
            self._favicon_svg_icons_creation(),
            self._preview_png_icons_creation(),

            self._browserconfig_icons_creation(),
            self._manifest_icons_creation(),
            self._opensearch_icons_creation(),
        ]
        return [
            element for group in icons_creation_config
            for element in group
        ]
