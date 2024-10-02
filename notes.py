import json
import os

from loguru import logger


class Notes:
    def __init__(self, filename='notes.json'):
        self.filename = filename
        self.notes = self.load_notes()

    def load_notes(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                return json.load(file)

        return []

    def save_notes(self):
        with open(self.filename, "w") as file:
            json.dump(self.notes, file)

    def add_note(self, note):
        self.notes.append(note)
        self.save_notes()

    def view_notes(self):
        if not self.notes:
            logger.info("No notes found.")
        else:
            for i, note in enumerate(self.notes, 1):
                logger.info(f"{i}: {note}")
