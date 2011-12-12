from gi.repository import Gtk
from i18n import _


class ChmodDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, _('Permissions'), parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 200)

        box = self.get_content_area()

        frame = Gtk.Frame()
        box.pack_start(frame, False, False, 0)

        label = Gtk.Label()
        label.props.use_markup = True
        label.set_markup('<b>' + _('Permissions') + '</b>')
        frame.props.label_widget = label

        alignment = Gtk.Alignment()
        alignment.props.left_padding = 15
        alignment.props.top_padding = 15

        frame.add(alignment)

        hbox = Gtk.HBox()
        alignment.add(hbox)

        frame1 = Gtk.Frame()
        label = Gtk.Label()
        label.props.use_markup = True
        label.set_markup('<b>' + _('User') + '</b>')

        frame1.props.label_widget = label
        frame1.props.shadow_type = Gtk.ShadowType.NONE

        alignment = Gtk.Alignment()
        alignment.props.left_padding = 15

        frame1.add(alignment)

        vbox = Gtk.VBox()
        self.u_r = Gtk.CheckButton(_('Read'))
        vbox.pack_start(self.u_r, False, False, 0)
        self.u_w = Gtk.CheckButton(_('Write'))
        vbox.pack_start(self.u_w, False, False, 0)
        self.u_x = Gtk.CheckButton(_('Execute'))
        vbox.pack_start(self.u_x, False, False, 0)
        alignment.add(vbox)

        hbox.pack_start(frame1, False, False, 0)

        frame1 = Gtk.Frame()
        label = Gtk.Label()
        label.props.use_markup = True
        label.set_markup('<b>' + _('Group') + '</b>')

        frame1.props.label_widget = label
        frame1.props.shadow_type = Gtk.ShadowType.NONE

        alignment = Gtk.Alignment()
        alignment.props.left_padding = 15

        frame1.add(alignment)

        vbox = Gtk.VBox()
        self.g_r = Gtk.CheckButton(_('Read'))
        vbox.pack_start(self.g_r, False, False, 0)
        self.g_w = Gtk.CheckButton(_('Write'))
        vbox.pack_start(self.g_w, False, False, 0)
        self.g_x = Gtk.CheckButton(_('Execute'))
        vbox.pack_start(self.g_x, False, False, 0)
        alignment.add(vbox)

        hbox.pack_start(frame1, False, False, 0)

        frame1 = Gtk.Frame()
        label = Gtk.Label()
        label.props.use_markup = True
        label.set_markup('<b>' + _('Others') + '</b>')

        frame1.props.label_widget = label
        frame1.props.shadow_type = Gtk.ShadowType.NONE

        alignment = Gtk.Alignment()
        alignment.props.left_padding = 15

        frame1.add(alignment)

        vbox = Gtk.VBox()
        self.o_r = Gtk.CheckButton(_('Read'))
        vbox.pack_start(self.o_r, False, False, 0)
        self.o_w = Gtk.CheckButton(_('Write'))
        vbox.pack_start(self.o_w, False, False, 0)
        self.o_x = Gtk.CheckButton(_('Execute'))
        vbox.pack_start(self.o_x, False, False, 0)
        alignment.add(vbox)

        hbox.pack_start(frame1, False, False, 0)

    def get_permissions(self):
        u = 0
        g = 0
        o = 0

        if self.u_r.get_active():
            u = u | 4
        if self.u_w.get_active():
            u = u | 2
        if self.u_x.get_active():
            u = u | 1

        if self.g_r.get_active():
            g = g | 4
        if self.g_w.get_active():
            g = g | 2
        if self.g_x.get_active():
            g = g | 1

        if self.o_r.get_active():
            o = o | 4
        if self.o_w.get_active():
            o = o | 2
        if self.o_x.get_active():
            o = o | 1

        return '%d%d%d' % (u, g, o)

    def set_permissions(self, permissions):
        if not permissions:
            return

        if len(permissions) > 9:
            permissions = permissions[1:]
        if len(permissions) != 9:
            print("Couldn't parse permissions: %s" % permissions)
            return

        us = permissions[:3]
        gs = permissions[3:6]
        os = permissions[6:9]

        self.u_r.set_active(us.find('r') >= 0)
        self.u_w.set_active(us.find('w') >= 0)
        self.u_x.set_active(us.find('x') >= 0)
        self.g_r.set_active(gs.find('r') >= 0)
        self.g_w.set_active(gs.find('w') >= 0)
        self.g_x.set_active(gs.find('x') >= 0)
        self.o_r.set_active(os.find('r') >= 0)
        self.o_w.set_active(os.find('w') >= 0)
        self.o_x.set_active(os.find('x') >= 0)
