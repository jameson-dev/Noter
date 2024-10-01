import os

from loguru import logger


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = "logs"


def init_logger(config):
    """ Add logging using loguru """
    logger.add(sink=f"{LOG_DIR}/app.log",
               level=config.get('General', 'log_level'),
               rotation="6 hours",
               format="{time} {level} {message}"
               )
