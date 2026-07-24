import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk


class HookNote(Gtk.Application):

    def __init__(self):
        super().__init__(
            application_id="com.vic.hooknote"
        )

    def do_activate(self):

        window = Gtk.ApplicationWindow(
            application=self
        )

        window.set_title(
            "🧶 HookNote"
        )

        window.set_default_size(
            900,
            600
        )

        label = Gtk.Label(
            label="Welcome to HookNote 🧶"
        )

        window.set_child(
            label
        )

        window.present()


app = HookNote()

app.run()
