from gi.repository import Gtk, GdkPixbuf, Gio
#from bareftp.version import version
from os import path
import mimetypes


def load_icon(stock_id):

    icontheme = Gtk.IconTheme.get_default()
    pixbuf = icontheme.load_icon(stock_id, 16, 0)

    return pixbuf


def load_icon_from_filename(filename):

    m = mimetypes.guess_type(filename)[0]
    icontheme = Gtk.IconTheme.get_default()
    pixbuf = None
    if m:
        icon = Gio.content_type_get_icon(m)
        iconinfo = icontheme.lookup_by_gicon(icon, 16, 0)
        if iconinfo:
            pixbuf = iconinfo.load_icon()

    if not pixbuf:
        pixbuf = load_icon(Gtk.STOCK_FILE)

    return pixbuf


def load_bareftp_pixbuf(datadir, filename):
    pixbufpath = path.join(datadir, 'pixmaps', filename)
    return GdkPixbuf.Pixbuf.new_from_file(pixbufpath)
