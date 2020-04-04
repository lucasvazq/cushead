import src.base.configuration
import src.base.generator.files


class BaseGenerator(src.base.generator.files.FilesGenerator):
    def generate(self):
        return {
            "text_files": self.generate_non_media_files(),
            "image_files": self.generate_media_files(),
        }
