from gi.repository import Gtk, Gdk, GdkPixbuf
from lib.ftpfile import FtpFile
from widgets.chmod_dialog import ChmodDialog
from i18n import _
import lib


class BareFTPFileList(Gtk.TreeView):
    def __init__(self):
        super(BareFTPFileList, self).__init__()

        self.col_filename = Gtk.TreeViewColumn(_("Filename"))
        self.col_filename.props.sort_column_id = 0
        self.col_filename.props.sort_indicator = True
        self.col_filename.props.resizable = True
        #self.col_filename.props.sort_order = 'gtk-sort-ascending'

        self.cr_filename = Gtk.CellRendererText()
        renderer = Gtk.CellRendererText()
        iconrenderer = Gtk.CellRendererPixbuf()

        self.col_filename.pack_start(iconrenderer, False)
        self.col_filename.pack_start(self.cr_filename, False)
        self.col_filename.add_attribute(iconrenderer, "pixbuf", 1)
        self.col_filename.add_attribute(self.cr_filename, "text", 2)

        self.col_size = Gtk.TreeViewColumn(_("Size"), renderer, text=3)
        self.col_size.props.sort_column_id = 2
        self.col_size.props.sort_indicator = True
        self.col_size.props.resizable = True

        self.col_date = Gtk.TreeViewColumn(_("Date"), renderer, text=4)
        self.col_date.props.sort_column_id = 3
        self.col_date.props.sort_indicator = True
        self.col_date.props.resizable = True

        self.col_user = Gtk.TreeViewColumn(_("User"), renderer, text=5)
        self.col_user.props.sort_column_id = 4
        self.col_user.props.sort_indicator = True
        self.col_user.props.resizable = True

        self.col_group = Gtk.TreeViewColumn(_("Group"), renderer, text=6)
        self.col_group.props.sort_column_id = 5
        self.col_group.props.sort_indicator = True
        self.col_group.props.resizable = True

        self.col_perm = Gtk.TreeViewColumn(_("Permissions"), renderer, text=7)
        self.col_perm.props.sort_column_id = 6
        self.col_perm.props.sort_indicator = True
        self.col_perm.props.resizable = True

        self.append_column(self.col_filename)
        self.append_column(self.col_size)
        self.append_column(self.col_date)
        self.append_column(self.col_user)
        self.append_column(self.col_group)
        self.append_column(self.col_perm)

        self.get_selection().props.mode = Gtk.SelectionMode.MULTIPLE

        self.connect('row-activated', self.row_activated)
        self.connect('key-press-event', self.key_pressed)
        self.connect('button-release-event', self.showmenu)

        self.props.model = BareFTPListStore()

    def refresh_model(self, model):
        model.set_sort_func(0, self.sort_name)
        model.set_sort_func(2, self.sort_size)
        model.set_sort_func(3, self.sort_date)
        model.set_sort_func(4, self.sort_user)
        model.set_sort_func(5, self.sort_group)
        model.set_sort_func(6, self.sort_permissions)

        # TODO: What is the correct enum for ascending??
        model.set_sort_column_id(0, 0)
        self.props.model = model

    def sort_name(self, model, iter1, iter2, data):
        file1 = model.get_value(iter1, 0)
        file2 = model.get_value(iter2, 0)

        if file1.filename == '..':
            return 0
        if file1.isdir and not file2.isdir:
            return 0
        elif not file1.isdir and file2.isdir:
            return 1

        if file1.filename.lower() > file2.filename.lower():
            return 1
        else:
            return -1

        #items = [str1, str2]
        #items.sort(lambda x, y: cmp(x.lower(),y.lower()))
        #if items[0] == str1:
        #    return 0
        #else:
        #    return 1

    def sort_size(self, model, iter1, iter2, data):
        file1 = model.get_value(iter1, 0)
        file2 = model.get_value(iter2, 0)

        if file1.filename == '..':
            return 0
        elif file1.isdir and not file2.isdir:
            return 0
        elif not file1.isdir and file2.isdir:
            return 1
        else:
            if file1.size < file2.size:
                return -1
            else:
                return 1

    def sort_date(self, model, iter1, iter2, data):
        file1 = model.get_value(iter1, 0)
        file2 = model.get_value(iter2, 0)

        if file1.filename == '..':
            return 0
        elif file1.isdir and not file2.isdir:
            return 0
        elif not file1.isdir and file2.isdir:
            return 1
        else:
            if file1.lastmodified < file2.lastmodified:
                return -1
            else:
                return 1

    def sort_user(self, model, iter1, iter2, data):
        file1 = model.get_value(iter1, 0)
        file2 = model.get_value(iter2, 0)

        if file1.filename == '..':
            return 0
        elif file1.isdir and not file2.isdir:
            return 0
        elif not file1.isdir and file2.isdir:
            return 1
        else:
            if file1.owner < file2.owner:
                return -1
            else:
                return 1

    def sort_group(self, model, iter1, iter2, data):
        file1 = model.get_value(iter1, 0)
        file2 = model.get_value(iter2, 0)

        if file1.filename == '..':
            return 0
        elif file1.isdir and not file2.isdir:
            return 0
        elif not file1.isdir and file2.isdir:
            return 1
        else:
            if file1.group < file2.group:
                return -1
            else:
                return 1

    def sort_permissions(self, model, iter1, iter2, data):
        file1 = model.get_value(iter1, 0)
        file2 = model.get_value(iter2, 0)

        if file1.filename == '..':
            return 0
        elif file1.isdir and not file2.isdir:
            return 0
        elif not file1.isdir and file2.isdir:
            return 1
        else:
            if file1.permissions < file2.permissions:
                return -1
            else:
                return 1

    def edit_permissions(self, *args):
        files = self.get_selected_files()
        chmoddialog = ChmodDialog(self.get_toplevel())
        if len(files) == 1:
            chmoddialog.set_permissions(files[0].permissions)
        chmoddialog.show_all()
        dr = chmoddialog.run()
        if dr == Gtk.ResponseType.OK:
            self.emit('chmod-event', files, chmoddialog.get_permissions())
        chmoddialog.destroy()

    def showmenu(self, sender, evt):
        if evt.button == 3:
            # TODO: Make proper menus and events
            self.menu = Gtk.Menu()

            ftpfiles = self.get_selected_files()
            if not ftpfiles:
                return
            if len(ftpfiles) == 1 and ftpfiles[0].isdir:
                m0 = Gtk.ImageMenuItem(_('Open Directory'))
                img = Gtk.Image()
                img.set_from_pixbuf(lib.icon_loader.load_icon(Gtk.STOCK_GO_UP))
                m0.set_image(img)
                self.menu.append(m0)

            m1 = Gtk.MenuItem(_('Permissions'))
            m1.connect('activate', self.edit_permissions)
            self.menu.append(m1)

            m2 = Gtk.MenuItem(_('Delete'))
            m2.connect('activate', self.delete_file)
            self.menu.append(m2)

            self.menu.popup(None, None, None, None, evt.button, evt.time)
            self.menu.show_all()

    def get_selected_files(self):
        files = []
        (liststore, paths) = self.get_selection().get_selected_rows()

        for p in paths:
            _iter = self.props.model.get_iter(p)
            _file = liststore.get_value(_iter, 0)
            files.append(_file)
        return files

    def delete_file(self, *args):
        self.emit('delete-files-event', self.get_selected_files())

    def row_activated(self, *args):
        files = self.get_selected_files()
        if files and len(files) == 1:
            self.emit('cwd-event', files[0])

    def is_clicked_node_selected(self, x, y):
        paths = self.get_path_at_pos(x, y)
        if paths:
            path = paths[0]
            if path:
                return self.get_selection().path_is_selected(path)
        return False

    def is_multiple_nodes_selected(self):
        (store, paths) = self.get_selection().get_selected_rows()
        return len(paths) > 1

    def key_pressed(self, sender, evt):
        if evt.keyval == Gdk.KEY_F2:
            if self.is_multiple_nodes_selected():
                return
            (store, paths) = self.get_selection().get_selected_rows()
            cr = self.cr_filename
            cr.props.editable = True
            self.signal_edit = cr.connect('edited', self.file_renamed)
            self.signal_canceledit = cr.connect('editing-canceled', self.filename_editing_canceled)
            self.set_cursor_on_cell(paths[0], self.get_column(0), cr, True)
        if evt.keyval == Gdk.KEY_Delete:
            self.delete_file()

    def file_renamed(self, sender, _path, newname):
        _store = self.props.model
        _iter = _store.get_iter(_path)
        f = _store.get_value(_iter, 0)

        self.disconnect_edit_signals()
        self.emit('file-renamed-event', f, newname)

    def makedir(self):
        _store = self.props.model
        _newiter = _store.insert(1)
        f = FtpFile(_('New Directory'))
        f.isdir = True
        f.icon = lib.icon_loader.load_icon(Gtk.STOCK_DIRECTORY)
        _store.set_value(_newiter, 0, f)
        _store.set_value(_newiter, 1, f.icon)
        _store.set_value(_newiter, 2, f.filename)

        _path = _store.get_path(_newiter)
        cr = self.cr_filename
        cr.props.editable = True
        self.signal_edit = cr.connect('edited', self.newdir_edited)
        self.signal_canceledit = cr.connect('editing-canceled', self.filename_editing_canceled)
        self.set_cursor_on_cell(_path, self.get_column(0), cr, True)

    def newdir_edited(self, sender, _path, dirname):
        _store = self.props.model
        _iter = _store.get_iter(_path)
        f = _store.get_value(_iter, 0)
        f.filename = dirname
        _store.set_value(_iter, 0, f)
        _store.set_value(_iter, 2, dirname)

        self.disconnect_edit_signals()
        self.emit('newdirnamed-event', dirname)

    def filename_editing_canceled(self, *args):
        print('editing-canceled')
        self.refresh_model(self.props.model)

    def disconnect_edit_signals(self):
        self.cr_filename.props.editable = False
        if self.signal_edit:
            self.cr_filename.disconnect(self.signal_edit)
            self.signal_edit = None
        if self.signal_canceledit:
            self.cr_filename.disconnect(self.signal_canceledit)
            self.signal_canceledit = None


class BareFTPListStore(Gtk.ListStore):
    def __init__(self):
        super(BareFTPListStore, self).__init__(object, GdkPixbuf.Pixbuf, str, str, str, str, str, str)

    def appendfile(self, ftpfile):
        return self.append(ftpfile.expand())

    def insertfile(self, ftpfile):
        pass
