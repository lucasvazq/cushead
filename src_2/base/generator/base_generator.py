import src_2.base.configuration
import src_2.base.generator.files


class BaseGenerator(src_2.base.configuration.IconsFormatConfig, src_2.base.generator.files.FilesGenerator):
    def __init__(self, config):
        self.config = src_2.base.configuration.parse_config(config)
        super().__init__(self.config)

        self.generate_non_media_files()
        self.generate_media_files()
