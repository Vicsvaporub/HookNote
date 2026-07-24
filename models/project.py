import json
from pathlib import Path
from datetime import datetime


class Project:

    def __init__(self, folder, title="Untitled Project"):

        self.folder = Path(folder)
        self.title = title

        self.project_file = self.folder / "project.json"
        self.pattern_file = self.folder / "pattern.md"
        self.notes_file = self.folder / "notes.md"

        self.images_folder = self.folder / "images"
        self.references_folder = self.folder / "references"
        self.charts_folder = self.folder / "charts"


    def create(self):

        self.folder.mkdir(
            parents=True,
            exist_ok=True
        )

        self.images_folder.mkdir(
            exist_ok=True
        )

        self.references_folder.mkdir(
            exist_ok=True
        )

        self.charts_folder.mkdir(
            exist_ok=True
        )

        self.pattern_file.touch()
        self.notes_file.touch()

        data = {
            "title": self.title,
            "created": str(datetime.now()),
            "modified": str(datetime.now()),
            "tags": [],
            "cover_image": None
        }

        with open(
            self.project_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )
