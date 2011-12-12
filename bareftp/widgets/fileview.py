from gi.repository import Gtk, Gdk, GObject
from widgets.filelist import BareFTPFileList, BareFTPListStore
from protocols.connection_manager import ConnectionManager
import lib.icon_loader
import sys
from i18n import _


class BareFTPFileView(Gtk.VBox):
    def __init__(self, start=False):
        super(BareFTPFileView, self).__init__(False, 1)

        self.conn_manager = ConnectionManager()
        self.conn_manager.connect('message-received', self.messageReceived)
        self.conn_manager.connect('list-received', self.updateView)
        self.conn_manager.connect('pwd-received', self.updatePath)

        hbox = Gtk.HBox(False, 1)
        self.entry_path = Gtk.Entry()
        self.entry_path.connect('activate', self.entry_path_activated)
        hbox.pack_start(self.entry_path, True, True, 0)

        self.btnup = Gtk.Button()
        self.btnup.props.relief = Gtk.ReliefStyle.NONE
        self.btnup.props.can_focus = True

        img = Gtk.Image()
        img.set_from_pixbuf(lib.icon_loader.load_icon(Gtk.STOCK_GO_UP))
        self.btnup.add(img)
        self.btnup.props.label = None
        self.btnup.props.tooltip_text = _('Parent Directory')
        self.btnup.connect('clicked', self.cwd, '..')
        hbox.pack_start(self.btnup, False, False, 0)

        self.btnnewdir = Gtk.Button()
        self.btnnewdir.props.relief = Gtk.ReliefStyle.NONE
        self.btnnewdir.props.can_focus = True

        img2 = Gtk.Image()
        if Gtk.IconTheme.get_default().has_icon('stock_new-dir'):
            img2.set_from_pixbuf(lib.icon_loader.load_icon('stock_new-dir'))
        else:
            img2.set_from_pixbuf(lib.icon_loader.load_icon(Gtk.STOCK_DIRECTORY))

        self.btnnewdir.add(img2)
        self.btnnewdir.props.label = None
        self.btnnewdir.props.tooltip_text = _('New Directory')
        self.btnnewdir.connect('clicked', self.init_newdir)
        hbox.pack_start(self.btnnewdir, False, False, 0)

        self.pack_start(hbox, False, False, 0)

        self.filelist = BareFTPFileList()
        self.filelist.connect('cwd-event', self.cwd)
        self.filelist.connect('newdirnamed-event', self.newdir_named)
        self.filelist.connect('file-renamed-event', self.file_renamed)
        self.filelist.connect('delete-files-event', self.delete_files)
        self.filelist.connect('chmod-event', self.chmod)

        sw = Gtk.ScrolledWindow()
        sw.props.shadow_type = Gtk.ShadowType.ETCHED_IN
        sw.add(self.filelist)
        self.pack_start(sw, True, True, 0)
        self.filelist.connect('button-press-event', self.btnpress)
        self.filelist.show()
        #GObject.idle_add(self.set_sensitive, False)

    def btnpress(self, sender, evt):
        if evt.button == 3:
            with_modifier = (evt.state & Gdk.ModifierType.SHIFT_MASK) or (evt.state & Gdk.ModifierType.CONTROL_MASK)
            if not with_modifier and self.filelist.is_clicked_node_selected(evt.x, evt.y) and self.filelist.is_multiple_nodes_selected():
                return True
        return False

    def init_newdir(self, *args):
        self.filelist.makedir()

    def entry_path_activated(self, *args):
        _path = self.entry_path.get_text()
        if _path.strip():
            self.cwd(None, _path)

    def cwd(self, sender, _file):
        if isinstance(_file, str):
            self.conn_manager._cwd_pwd_xdir(_file)
        else:
            self.conn_manager._cwd_pwd_xdir(_file.filename)

    def chmod(self, sender, files, permissions):
        self.conn_manager._chmod(files, permissions)

    def newdir_named(self, sender, newdirname):
        self.conn_manager._mkdir(newdirname)

    def file_renamed(self, sender, _file, newname):
        self.conn_manager._rename(_file.filename, newname)

    def delete_files(self, sender, files):
        diag = Gtk.MessageDialog(self.get_toplevel(),
                                 Gtk.DialogFlags.MODAL,
                                 Gtk.MessageType.QUESTION,
                                 Gtk.ButtonsType.YES_NO,
                                 _('Are you sure you want to delete the selected files?'))
        if diag.run() == Gtk.ResponseType.YES:
            _files = []
            _dirs = []
            for f in files:
                if f.isdir and not f.islink:
                    _dirs.append(f)
                else:
                    _files.append(f)
            if _files:
                self.conn_manager._delete(_files)
            if _dirs:
                self.conn_manager._rmdir(_dirs)

        diag.destroy()

    def set_model(self, model):
        self.filelist.refresh_model(model)

    def messageReceived(self, sender, message):
        if self.log:
            GObject.idle_add(self.printLog, message)

    def printLog(self, message):
        logbuffer = self.log.get_buffer()
        enditer = logbuffer.get_end_iter()
        try:
            logbuffer.insert_with_tags_by_name(enditer, message[1], message[0])
            self.log.scroll_mark_onscreen(logbuffer.get_insert())
        except:
            sys.__stdout__.write(message)
            sys.__stdout__.flush()

    def updateView(self, sender, files):
        liststore = BareFTPListStore()
        for f in files:
            if f.isdir:
                f.icon = lib.icon_loader.load_icon(Gtk.STOCK_DIRECTORY)
            else:
                f.icon = lib.icon_loader.load_icon_from_filename(f.filename)
            if f.islink:
                f.icon = lib.icon_loader.load_icon('stock_right')

            liststore.appendfile(f)
        GObject.idle_add(self.set_model, liststore)

    def updatePath(self, sender, path):
        GObject.idle_add(self.entry_path.set_text, path)

    def init(self):
        self.conn_manager._open()
        self.conn_manager._cwd_pwd_xdir(None)
