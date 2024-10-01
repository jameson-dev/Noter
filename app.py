from notes import Notes
from database import Database
import logger
from config import Config


def main():
    config = Config()
    config.load_config()

    logger.init_logger(config)
    db = Database(config)
    notes = Notes()


if __name__ == "__main__":
    main()

