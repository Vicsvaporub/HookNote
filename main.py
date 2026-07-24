import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk

from ui.main_window import MainWindow


class HookNote(Gtk.Application):

    def __init__(self):
        super().__init__(
            application_id="com.vic.hooknote"
        )

    def do_activate(self):

        window = MainWindow(
            self
        )

        window.present()


app = HookNote()

app.run()
