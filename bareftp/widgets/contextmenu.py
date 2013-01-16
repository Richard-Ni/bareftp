from gi.repository import Gtk
from lib.icon_loader import load_icon
from i18n import _

class ContextMenu(Gtk.Menu):
    def __init__(self):
        super(ContextMenu, self).__init__()

        m0 = Gtk.ImageMenuItem(_('Open Directory'))
        m0.set_image(load_icon(Gtk.STOCK_GO_UP))

        self.append(m0)
