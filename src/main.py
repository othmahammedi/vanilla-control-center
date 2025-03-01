# main.py
#
# Copyright 2022 Mirko Brombin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-only

import sys
import logging
import gi
from gettext import gettext as _

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw
from .window import VanillaWindow


logging.basicConfig(level=logging.INFO)


class VanillaControlCenterApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='org.vanillaos.ControlCenter',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.create_action('quit', self.quit, ['<primary>q'])
        self.create_action('about', self.on_about_action)

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = VanillaWindow(application=self)
        win.present()

    def on_about_action(self, widget, *args):
        """Callback for the app.about action."""
        about = Adw.AboutWindow(transient_for=self.props.active_window,
                                application_name=_('Vanilla OS Control Center'),
                                application_icon='org.vanillaos.ControlCenter',
                                developer_name='Mirko Brombin',
                                version='0.1.1',
                                developers=['Mirko Brombin'],
                                copyright='© 2022 Mirko Brombin')
        about.add_credit_section(
            _("Translators"),
            [
                "0xMRTT https://github.com/0xMRTT",
                "rffontenelle https://github.com/rffontenelle",
                "alinpr18 https://github.com/alinpr18"
            ]
        )
        about.present()

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point."""
    app = VanillaControlCenterApplication()
    return app.run(sys.argv)
