# -*- coding: utf-8 -*-
from gi.repository import Gtk
import lib.icon_loader
from widgets.filelist import BareFTPListStore
from widgets.fileview import BareFTPFileView
from widgets.bookmark import BookmarkMenuButton
from widgets.progresslist import ProgressList
from utils.bookmarkutils import BookmarkUtils
from config.settings import Config
from lib.xferpool import XferManager, Xfer
import version
from i18n import _


class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__(type=Gtk.WindowType.TOPLEVEL)

        self.set_title('bareFTP')
        self.connect("delete_event", self._on_delete)
        self.connect_after('destroy', self._on_delete)
        self.set_default_size(1200, 800)
        self.progresslist = ProgressList()
        self.xferman = XferManager()
        self.xferman.progresslist = self.progresslist
        vbox = Gtk.VBox()
        self.add(vbox)

        action_entries = (
            # name, stock id, label, accelerator, tooltip
            ("FileMenu", None, _("_File")),
            ("HelpMenu", None, _("_Help")),
            ("EditMenu", None, _("_Edit")),
            ("BookmarkMenu", None, _("Bookmarks")),
            ("Bookmarks", Gtk.STOCK_DIRECTORY, _("Bookmarks")),
            ("AddBookmark", Gtk.STOCK_ADD, _("Add bookmark")),
            ("EditBookmarks", Gtk.STOCK_EDIT, _("Edit bookmarks")),
            ("Preferences", Gtk.STOCK_PREFERENCES, _("Preferences"),
                None, None, self.open_prefs),
            ("About", Gtk.STOCK_ABOUT, _("_About"), None, None, self.about_cb),
            ("Quit", Gtk.STOCK_QUIT, _("_Quit"),
            "<control>Q", None, self._quit),
        )

        action_group = Gtk.ActionGroup(name='AppWindowActions')
        action_group.add_actions(action_entries)

        merge = Gtk.UIManager()
        merge.insert_action_group(action_group, 0)
        self.add_accel_group(merge.get_accel_group())

        # Add the top menu bar
        merge.add_ui_from_string(self.get_menu_xml())
        bar = merge.get_widget('/MenuBar')
        vbox.pack_start(bar, False, False, 0)
        #bar.show()

        hbox = Gtk.HBox(False, 6)
        vbox.pack_start(hbox, False, False, 4)

        icon = Gtk.Image.new_from_icon_name(Gtk.STOCK_DIRECTORY,
                                                    Gtk.IconSize.MENU)
        bookmarkbtn = BookmarkMenuButton(icon, _('Bookmarks'))

        bu = BookmarkUtils()
        bu.connect('bookmark_clicked', self.activate_bookmark)
        bu.menubar = bar
        bu.build_menus()

        bookmarkbtn.set_menu(bu.get_bookmarks_menu())

        hbox.pack_start(bookmarkbtn, False, False, 0)
        hbox.pack_start(Gtk.Label(_('Host:')), False, False, 0)
        self.entry_host = Gtk.Entry()
        hbox.pack_start(self.entry_host, False, False, 0)
        hbox.pack_start(Gtk.Label(_('Port:')), False, False, 0)
        self.entry_port = Gtk.Entry()
        hbox.pack_start(self.entry_port, False, False, 0)
        hbox.pack_start(Gtk.Label(_('Username:')), False, False, 0)
        self.entry_username = Gtk.Entry()
        hbox.pack_start(self.entry_username, False, False, 0)
        hbox.pack_start(Gtk.Label(_('Password:')), False, False, 0)
        self.entry_password = Gtk.Entry()
        hbox.pack_start(self.entry_password, False, False, 0)

        self.btn_connect = Gtk.Button('Connect')
        self.btn_connect.connect('clicked', self.conn_clicked)
        hbox.pack_start(self.btn_connect, False, False, 0)

        self.vpaned = Gtk.VPaned()

        self.hpaned = Gtk.HPaned()
        self.vpaned.add(self.hpaned)

        vbox.pack_start(self.vpaned, True, True, 0)

        self.liststore = BareFTPListStore()
        self.fileview = BareFTPFileView(True)
        self.fileview.conn_manager.type = 'LOCAL'
        self.fileview.conn_manager.side = 'LEFT'
        self.liststore2 = BareFTPListStore()
        self.fileview2 = BareFTPFileView(True)
        self.fileview2.conn_manager.type = 'FTP'
        self.fileview2.conn_manager.side = 'RIGHT'
        #fileview.set_model(liststore)

        _hbox = Gtk.HBox()
        _hbox.pack_start(self.fileview, True, True, 0)

        b1 = Gtk.Button()
        b1.props.relief = Gtk.ReliefStyle.NONE
        b2 = Gtk.Button()
        b2.props.relief = Gtk.ReliefStyle.NONE

        img1 = Gtk.Image()
        img1.set_from_pixbuf(lib.icon_loader.load_icon('stock_right'))

        b1.add(img1)
        b1.props.label = None
        b1.connect('clicked', self.upload_click)
        
        img2 = Gtk.Image()
        img2.set_from_pixbuf(lib.icon_loader.load_icon('stock_left'))

        b2.add(img2)
        b2.props.label = None
        b2.connect('clicked', self.download_click)
        _vbox = Gtk.VBox(True, 12)
        _vbox2 = Gtk.VBox(True, 12)
        _vbox2.pack_start(b1, False, False, 6)
        _vbox2.pack_start(b2, False, False, 6)
        _vbox.pack_start(_vbox2, False, False, 0)
        _vbox.reorder_child(_vbox2, 1)
        _hbox.pack_start(_vbox, False, False, 4)
        self.hpaned.pack1(_hbox, True, True)
        self.hpaned.pack2(self.fileview2, True, True)

        notebook = Gtk.Notebook()
        notebook.props.tab_pos = Gtk.PositionType.BOTTOM

        sw_xfer = Gtk.ScrolledWindow()
        sw_xfer.props.shadow_type = Gtk.ShadowType.ETCHED_IN
        sw_xfer.add(self.progresslist)
        notebook.append_page(sw_xfer, Gtk.Label(_('Transfers')))

        _sw2 = Gtk.ScrolledWindow()
        #_sw2.props.vscrollbar_policy = Gtk.GTK_POLICY_AUTOMATIC
        #_sw2.props.hscrollbar_policy = Gtk.GTK_POLICY_AUTOMATIC

        self.log = Gtk.TextView()

        tag = Gtk.TextTag.new("default")
        tag.props.font = 'Monospace 8'
        self.log.props.buffer.props.tag_table.add(tag)

        tag = Gtk.TextTag.new("welcome")
        tag.props.foreground = "dark green"
        tag.props.font = 'Monospace 8'
        self.log.props.buffer.props.tag_table.add(tag)

        tag = Gtk.TextTag.new("error")
        tag.props.foreground = "red"
        tag.props.font = 'Monospace 8'
        self.log.props.buffer.props.tag_table.add(tag)

        tag = Gtk.TextTag.new("client")
        tag.props.foreground = "dark blue"
        tag.props.font = 'Monospace 8'
        self.log.props.buffer.props.tag_table.add(tag)

        _sw2.add(self.log)
        self.fileview.log = self.log
        self.fileview2.log = self.log
        notebook.append_page(_sw2, Gtk.Label(_('Messages')))

        self.vpaned.add(notebook)
        self.statusbar = Gtk.Statusbar()
        vbox.pack_start(self.statusbar, False, False, 0)

        self.settings = Config()
        self.vpaned.set_position(self.settings.get_vpaned_pos())
        self.hpaned.set_position(self.settings.get_hpaned_pos())

        #self.connect('exposeevent', self.winexposed)
        self.fileview.init()
        self.show_all()

    def download_click(self, *args):
        for f in self.fileview2.filelist.get_selected_files():
            x = Xfer(f, self.fileview2.conn_manager, self.fileview.conn_manager)
            self.xferman.append_xfer(x)
    
    def upload_click(self, *args):
        for f in self.fileview.filelist.get_selected_files():
            x = Xfer(f, self.fileview.conn_manager, self.fileview2.conn_manager)
            self.xferman.append_xfer(x)

    def cleanup(self):
        self.xferman.abort_all()
        self.fileview2.conn_manager.abort_all()
        self.fileview.conn_manager.abort_all()
        self.settings.set_vpaned_pos(self.vpaned.get_position())
        self.settings.set_hpaned_pos(self.hpaned.get_position())

        # TODO: Abort transfers..

    def get_menu_xml(self):
        m = """
        <ui>
         <menubar name='MenuBar'>
          <menu action='FileMenu'>
           <separator/>
           <menuitem action='Quit'/>
          </menu>
          <menu action='EditMenu'>
           <menuitem action='Preferences'/>
          </menu>
          <menu action='BookmarkMenu'>
           <menuitem action='AddBookmark'/>
           <menuitem action='EditBookmarks'/>
           <separator/>
           <menuitem action='Bookmarks'/>
          </menu>
          <menu action='HelpMenu'>
           <menuitem action='About'/>
          </menu>
         </menubar>
        </ui>
        """
        return m

    def conn_clicked(self, *args):
        self.fileview2.init()

    def activate_bookmark(self, sender, bookmark_item):
        print(bookmark_item.name)

    def open_prefs(self, *args):
        from widgets.preferences import PreferencesDialog
        pd = PreferencesDialog(self, self.settings)
        pd.run()
        pd.destroy()

    def about_cb(self, widget):
        authors = ['Christian Eide <christian@eide-itc.no>']
        artists = ["Kalle Persson (bareFTP icon) <kalle@nemus.se>"]
        about = Gtk.AboutDialog(program_name='bareFTP',
            version=version.version,
            copyright='Copyright (C) 2011 Christian Eide',
            website='http://www.bareftp.org',
            website_label='http://www.bareftp.org',
            comments=_('File Transfer Client'),
            authors=authors,
            artists=artists,
            translator_credits=_("translator-credits"),
            logo=lib.icon_loader.load_bareftp_pixbuf(version.bareftp_datadir,
                            'bareftp2.png'),
            title=_('About bareFTP'))
        about.set_transient_for(self)
        about.connect('response', self.widget_destroy)
        about.show()

    def widget_destroy(self, widget, button):
        widget.destroy()

    def _quit(self, *args):
        print("Good bye...")
        self.cleanup()
        Gtk.main_quit()

    def _on_delete(self, *args):
        self.cleanup()
        Gtk.main_quit()
