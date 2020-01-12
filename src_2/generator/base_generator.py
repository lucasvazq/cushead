
from src.configuration import configuration
from src.generator import files

class BaseGenerator(configuration.IconsFormatConfig, files.FilesGenerator):
    def __init__(self, config):
        self.config = configuration.parse_config(config)
        super().__init__(self.config)

        self.generate_non_media_files()
        self.generate_media_files()
