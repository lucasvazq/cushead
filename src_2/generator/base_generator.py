
from src.configuration import configuration

class BaseGenerator:
    def __init__(self, config):
        self.config = configuration.parse_config(config)
