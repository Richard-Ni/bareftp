from gi.repository import Gtk, GObject
from widgets.bookmark import BookmarkMenuItem
from config.bookmarks import Bookmarks, BookmarkFolder, BookmarkItem


class BookmarkUtils(GObject.GObject):

    def __init__(self):
        super(BookmarkUtils, self).__init__()
        GObject.signal_new("bookmark_clicked", BookmarkUtils, GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (object,))

        self.menu1 = Gtk.Menu()
        self.menu2 = Gtk.Menu()
        self.menubar = None

    def build_menus(self):
        b = Bookmarks()
        self.create_bookmark_menu(b.bookmarks, self.menu1, self.menu2)
        self.set_menubar_bookmark_items()

    def create_bookmark_menu(self, bookmark_entry, bookmarkmenu, bookmarkmenu2):
        if bookmark_entry.items:
            for item in bookmark_entry.items:
                b = BookmarkMenuItem(item.name)
                b2 = BookmarkMenuItem(item.name)
                if isinstance(item, BookmarkFolder):
                    b.set_image(Gtk.Image.new_from_icon_name(Gtk.STOCK_DIRECTORY, Gtk.IconSize.MENU))
                    b2.set_image(Gtk.Image.new_from_icon_name(Gtk.STOCK_DIRECTORY, Gtk.IconSize.MENU))
                    bookmarkmenu.append(b)
                    bookmarkmenu2.append(b2)
                    m1 = Gtk.Menu()
                    m2 = Gtk.Menu()
                    b.set_submenu(m1)
                    b2.set_submenu(m2)
                    self.create_bookmark_menu(item, m1, m2)
                elif isinstance(item, BookmarkItem):
                    b.set_image(Gtk.Image.new_from_icon_name(Gtk.STOCK_FILE, Gtk.IconSize.MENU))
                    b.connect('activate', self.bookmark_activated, item)
                    bookmarkmenu.append(b)
                    b2 = BookmarkMenuItem(item.name)
                    b2.connect('activate', self.bookmark_activated, item)
                    b2.set_image(Gtk.Image.new_from_icon_name(Gtk.STOCK_FILE, Gtk.IconSize.MENU))
                    bookmarkmenu2.append(b2)

    def set_menubar_bookmark_items(self):
        if self.menubar == None:
            return

        for w in self.menubar.get_children():
            if w.props.name == 'BookmarkMenu':
                for w2 in w.get_submenu():
                    if w2.props.name == 'Bookmarks':
                        w2.set_submenu(None)
                        w2.set_submenu(self.menu2)
                        w2.get_submenu().show_all()

    def get_bookmarks_menu(self):
        self.menu1.show_all()
        return self.menu1

    def get_bookmarks_menuaction(self):
        return self.menu2

    def bookmark_activated(self, sender, bookmark_item):
        self.emit('bookmark_clicked', bookmark_item)
