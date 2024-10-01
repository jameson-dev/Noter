import os

from notes import Notes
from database import Database
from loguru import logger

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = "logs"

# Add logging using loguru
logger.add(f"{LOG_DIR}/app.log", rotation="6 hours", format="{time} {level} {message}")


def main():
    db = Database()
    notes = Notes()


if __name__ == "__main__":
    main()

