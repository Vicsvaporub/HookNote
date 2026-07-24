import tempfile
from pathlib import Path

from models.project import Project


def test_project_creation():

    with tempfile.TemporaryDirectory() as temp_folder:

        project_folder = (
            Path(temp_folder) / "Test Project"
        )

        project = Project(
            project_folder,
            "Test Project"
        )

        project.create()

        assert project_folder.exists()
        assert (project_folder / "project.json").exists()
        assert (project_folder / "pattern.md").exists()
        assert (project_folder / "notes.md").exists()
        assert (project_folder / "images").exists()
        assert (project_folder / "references").exists()
        assert (project_folder / "charts").exists()
