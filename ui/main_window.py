import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk, Gio
from services.project_manager import ProjectManager
from models.project import Project

class MainWindow(Gtk.ApplicationWindow):

    def __init__(self, app):

        super().__init__(
            application=app
        )

        self.project_manager = ProjectManager()

        self.set_title(
            "🧶 HookNote"
        )

        self.set_default_size(
            900,
            600
        )

        # ==========================================
        # MENU ACTIONS
        # ==========================================

        new_project_action = Gio.SimpleAction.new(
            "new_project",
            None
        )

        new_project_action.connect(
            "activate",
            self.menu_new_project
        )

        self.add_action(
            new_project_action
        )

        quit_action=Gio.SimpleAction.new(
            "quit",
            None
        )

        quit_action.connect(
            "activate",
            self.menu_quit
        )

        self.add_action(
            quit_action
        )

        # ==========================================
        # MENU BAR
        # ==========================================

        menu_bar = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=5
        )

        file_button = Gtk.MenuButton(
            label="File"
        )

        file_menu = Gio.Menu()

        file_menu.append(
            "New Project",
            "win.new_project"
        )

        file_menu.append(
            "Quit",
            "win.quit"
        )

        file_button.set_menu_model(
            file_menu
        )

        menu_bar.append(
            file_button
        )


        # ==========================================
        # MAIN LAYOUT
        # ==========================================

        main_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=0
        )

        # ==========================================
        # SIDEBAR
        # ==========================================

        sidebar = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=10
        )

        sidebar.set_size_request(
            220,
            -1
        )

        sidebar.set_margin_top(
            20
        )

        sidebar.set_margin_bottom(
            20
        )

        sidebar.set_margin_start(
            15
        )

        sidebar.set_margin_end(
            15
        )

        # Sidebar title

        projects_label = Gtk.Label(
            label="🧺 Projects"
        )

        sidebar.append(
            projects_label
        )

        self.project_list = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=5
        )

        sidebar.append(
            self.project_list
        )

        # ==========================================
        # NEW PROJECT BUTTON
        # ==========================================

        new_project_button = Gtk.Button(
            label="➕ New Project"
        )

        new_project_button.connect(
            "clicked",
            self.show_new_project_dialog
        )

        sidebar.append(
            new_project_button
        )

        # ==========================================
        # MAIN CONTENT
        # ==========================================

        content = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=10
        )

        content.set_hexpand(
            True
        )

        content.set_vexpand(
            True
        )

        content.set_margin_top(
            30
        )

        content.set_margin_start(
            30
        )

        content.set_margin_end(
            30
        )

        self.project_title_label = Gtk.Label(
            label="Welcome to HookNote 🧶"
        )

        content.append(
            self.project_title_label
        )

        # ==========================================
        # PUT SIDEBAR AND CONTENT TOGETHER
        # ==========================================

        main_box.append(
            sidebar
        )

        main_box.append(
            content
        )

        # ==========================================
        # PUT LAYOUT IN WINDOW
        # ==========================================

        root_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=0
        )

        root_box.append(
            menu_bar
        )

        root_box.append(
            main_box
        )

        root_box.set_vexpand(
            True
        )

        self.set_child(
            root_box
        )

        self.refresh_project_list()

    def refresh_project_list(self):

        # Remove old project buttons
        while child := self.project_list.get_first_child():

            self.project_list.remove(
                child
            )

        # Find all existing projects
        projects = (
            self.project_manager.get_projects()
        )

        # Create a button for each project
        for project_folder in projects:

            project_button = Gtk.Button(
                label=f"📁 {project_folder.name}"
            )

            project_button.connect(
                "clicked",
                self.load_project,
                project_folder
            )

            right_click = Gtk.GestureClick(
                button=3
            )

            right_click.connect(
                "pressed",
                self.show_project_context_menu,
                project_folder
            )

            project_button.add_controller(
                right_click
            )

            self.project_list.append(
                project_button
            )

    def menu_new_project(
            self,
            action,
            parameter
        ):

            self.show_new_project_dialog(
                None
            )

    def menu_quit(
            self,
            action,
            parameter
        ):

            self.get_application().quit()

    def load_project(
            self,
            button,
            project_folder
        ):

            project = Project.load(
                project_folder
            )

            self.current_project = project

            print(
                f"Loaded project: {project.title}"
            )

            self.project_title_label.set_label(
                f"🧶 {project.title}"
            )

    def show_project_context_menu(
            self,
            gesture,
            n_press,
            x,
            y,
            project_folder
        ):

            popover = Gtk.Popover()

            delete_button = Gtk.Button(
                label="🗑️ Delete Project"
            )

            delete_button.connect(
                "clicked",
                self.confirm_delete_project,
                project_folder,
                popover
            )

            popover.set_child(
                delete_button
            )

            button = gesture.get_widget()

            popover.set_parent(
                button
            )

            popover.popup()

    def confirm_delete_project(
            self,
            button,
            project_folder,
            popover
        ):

            popover.popdown()
            popover.unparent()

            dialog = Gtk.Dialog(
                title="Delete Project?",
                transient_for=self,
                modal=True
            )

            dialog.add_button(
                "Cancel",
                Gtk.ResponseType.CANCEL
            )

            dialog.add_button(
                "Delete",
                Gtk.ResponseType.ACCEPT
            )

            content_area = (
                dialog.get_content_area()
            )

            label = Gtk.Label(
                label=(
                    f'Are you sure you want to delete '
                    f'"{project_folder.name}"?'
                )
            )

            label.set_margin_top(20)
            label.set_margin_bottom(20)
            label.set_margin_start(20)
            label.set_margin_end(20)

            content_area.append(
                label
            )

            dialog.connect(
                "response",
                self.delete_project_response,
                project_folder
            )

            dialog.present()

    def delete_project_response(
            self,
            dialog,
            response,
            project_folder
        ):

        if response == Gtk.ResponseType.ACCEPT:

            self.project_manager.delete_project(
                project_folder
            )

            # Check if the deleted project
            # was the currently open project
            if (
                hasattr(self, "current_project")
                and self.current_project.folder
                == project_folder
            ):

                self.current_project = None

                self.project_title_label.set_label(
                    "Welcome to HookNote 🧶"
                )

            self.refresh_project_list()

            print(
                f"Deleted project: "
                f"{project_folder.name}"
            )

        dialog.destroy()

    # ==============================================
    # NEW PROJECT DIALOG
    # ==============================================

    def show_new_project_dialog(
        self,
        button
    ):

        dialog = Gtk.Dialog(
            title="New Crochet Project",
            transient_for=self,
            modal=True
        )

        dialog.add_button(
            "Cancel",
            Gtk.ResponseType.CANCEL
        )

        dialog.add_button(
            "Create",
            Gtk.ResponseType.ACCEPT
        )

        content_area = (
            dialog.get_content_area()
        )

        box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=10
        )

        box.set_margin_top(
            20
        )

        box.set_margin_bottom(
            20
        )

        box.set_margin_start(
            20
        )

        box.set_margin_end(
            20
        )

        label = Gtk.Label(
            label="Project title:"
        )

        entry = Gtk.Entry()

        entry.set_placeholder_text(
            "e.g. Forest Dragon"
        )

        box.append(
            label
        )

        box.append(
            entry
        )

        content_area.append(
            box
        )

        dialog.connect(
            "response",
            self.new_project_response,
            entry
        )

        dialog.present()


    # ==============================================
    # NEW PROJECT RESPONSE
    # ==============================================

    def new_project_response(
        self,
        dialog,
        response,
        entry
    ):

        if response == Gtk.ResponseType.ACCEPT:

            title = (
                entry.get_text().strip()
            )

            if title:

                project = self.project_manager.create_project(
                    title
                )

                print(
                    f"Created project: {project.title}"
                )

                self.refresh_project_list()

        dialog.destroy()
