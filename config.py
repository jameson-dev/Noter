import configparser
import os

from loguru import logger


class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        root_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_file_path = os.path.join(root_dir, 'config.ini')

    def check_config(self):
        logger.info(f"Checking for config at {self.config_file_path}")

        if not os.path.exists(self.config_file_path):
            self.create_config()
        else:
            logger.info("Configuration file found.")

    def create_config(self):
        self.config['General'] = {
            'log_level': 'INFO',
        }

        self.config['Database'] = {
            'db_host': 'localhost',
            'db_user': '',
            'db_password': ''
        }

        with open(self.config_file_path, 'w') as configfile:
            self.config.write(configfile)

        logger.info(f"Configuration file created at {self.config_file_path}")

    def load_config(self):
        self.check_config()

        logger.info("Loading configuration file")
        self.config.read(self.config_file_path)

    def get(self, section, option):
        return self.config.get(section, option)

    def getint(self, section, option):
        return self.config.getint(section, option)

    def getboolean(self, section, option):
        return self.config.getboolean(section, option)


