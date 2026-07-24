from pathlib import Path

from models.project import Project


class ProjectManager:

    def __init__(self):

        self.projects_folder = (
            Path.home()
            / "Documents"
            / "HookNote Projects"
        )

        self.projects_folder.mkdir(
            parents=True,
            exist_ok=True
        )


    def create_project(self, title):

        project_folder = (
            self.projects_folder / title
        )

        project = Project(
            project_folder,
            title
        )

        project.create()

        return project


    def get_projects(self):

        projects = []

        for folder in self.projects_folder.iterdir():

            if not folder.is_dir():
                continue

            project_file = (
                folder / "project.json"
            )

            if project_file.exists():

                projects.append(
                    folder
                )

        return sorted(
            projects,
            key=lambda folder: folder.name.lower()
        )

    def delete_project(self, project_folder):

        project_folder = Path(project_folder)

        if not project_folder.exists():
            return False

        if not project_folder.is_dir():
            return False

        import shutil

        shutil.rmtree(
            project_folder
        )

        return True
