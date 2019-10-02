
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
        print(source_file_path)
        class_instance.copy_file()

    @staticmethod
    def format_sizes(icon_brand_config):
        sizes_square = getattr(icon_brand_config, 'sizes_square', [])
        sizes_square = [[size, size] for size in sizes_square]
        sizes_rectangular = getattr(icon_brand_config, 'sizes_rectangular', [])
        max_min_sizes = getattr(icon_brand_config, 'sizes_max_min', [])
        max_min_sizes = [[size[1], size[1]] for size in max_min_sizes]
        return sizes_square + sizes_rectangular + max_min_sizes
