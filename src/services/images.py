
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
        class_instance = FilesHelper(destination_file_path=destination_file_path,
                              source_file_path=source_file_path)
        print(
            destination_file_path
        )
        print(source_file_path)
        class_instance.copy_file()

    @staticmethod
    def format_sizes(icon_brand_config):
        """Structure
        square_sizes = [1, 2]
        non_square_sizes = [[1, 2], [3, 4]]
        """
        square_sizes = getattr(icon_brand_config, 'sizes_square', [])
        square_sizes = [[size, size] for size in square_sizes]
        rectangular_sizes = getattr(icon_brand_config, 'sizes_rectangular', [])
        return square_sizes + rectangular_sizes
