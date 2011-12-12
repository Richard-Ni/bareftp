from gi.repository import Gtk


class BookmarkMenuButton(Gtk.MenuToolButton):
    def __init__(self, icon, label):
        super(BookmarkMenuButton, self).__init__()

        hbox = self.get_child()
        self.button = hbox.get_children()[0]
        self.togglebutton = hbox.get_children()[1]
        hbox.remove(self.button)

        self.arr = self.togglebutton.get_child()
        self.togglebutton.remove(self.arr)

        hbox = Gtk.HBox()
        hbox.pack_start(icon, False, False, 2)
        hbox.pack_start(Gtk.Label(label), False, False, 2)
        hbox.add(self.arr)
        self.togglebutton.add(hbox)


class BookmarkMenuItem(Gtk.ImageMenuItem):
    def __init__(self, name):
        super(BookmarkMenuItem, self).__init__(name)
        self.item = None
