
from PIL import Image
from resizeimage import resizeimage

from src.helpers.fso import FilesHelper


class ImageService:
    image_instance: object

    @staticmethod
    def resize_image(destination_file_path, source_file_path, size):
        with open(source_file_path, 'rb') as file_instance, \
                Image.open(file_instance) as image_instance:
            cover = resizeimage.resize_contain(image_instance,
                                               [size[0], size[1]])
            cover.save(destination_file_path, image_instance.format)

    @staticmethod
    def move_svg(destination_file_path, source_file_path):
        FilesHelper.copy_file(destination_file_path=destination_file_path,
                              source_file_path=source_file_path)

    @staticmethod
    def format_sizes(icon_brand_config):
        """Structure
        square_sizes = [1, 2]
        non_square_sizes = [[1, 2], [3, 4]]
        """
        square_sizes = icon_brand_config.get('square_sizes', [])
        square_sizes = [[size, size] for size in square_sizes]
        non_square_sizes = icon_brand_config.get('non_square_sizes', [])
        max_min = icon_brand_config.get('max_min', [])
        if max_min:
            max_min = [[size[0], size[0]] for size in max_min]
        return square_sizes + non_square_sizes + max_min
