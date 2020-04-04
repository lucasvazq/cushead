import src_2.base.configuration
import src_2.base.generator.files


class BaseGenerator(src_2.base.generator.files.FilesGenerator):
    def generate(self):
        return {
            "text_files": self.generate_non_media_files(),
            "image_files": self.generate_media_files(),
        }
