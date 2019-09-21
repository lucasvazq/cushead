
from os import path

from PIL import Image
from resizeimage import resizeimage

def resize_images(config, icon_brand_config, size):
    main_path = config.get('main_path', '')
    filesource = icon_brand_config.get('source', '')
    filesource = path.join(main_path, filesource)
    filename = icon_brand_config.get('filename', '')
    filename = (f"{filename}-{size[0]}x{size[1]}.png")
    static_url = config.get('static_url_path', '')
    filedest = path.join(static_url, filename)
    with open(filesource, 'r+b') as bytefile, \
        Image.open(bytefile) as image:
        cover = resizeimage.resize_contain(image, [size[0], size[1]])
        cover.save(filedest, image.format)


def format_sizes(icon_brand_config):
    """Structure
    square_sizes = [1, 2]
    non_square_sizes = [[1, 2], [3, 4]]
    """
    square_sizes = icon_brand_config.get('square_sizes', [])
    square_sizes = [[size, size] for size in square_sizes]
    non_square_sizes = icon_brand_config.get('non_square_sizes', [])
    max_min = icon_brand_config.get('squares_sizes', [])
    max_min = [size[0] for size in max_min]
    return square_sizes + non_square_sizes + max_min
