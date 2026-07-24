import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk


class MainWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        super().__init__(
            application=app
        )

        self.set_title(
            "🧶 HookNote"
        )

        self.set_default_size(
            900,
            600
        )

        label = Gtk.Label(
            label="Welcome to HookNote 🧶"
        )

        self.set_child(
            label
        )
