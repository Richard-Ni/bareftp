from __future__ import division
from gi.repository import Gtk, GObject
from lib.xferpool import Xfer
from i18n import _


class ProgressList(Gtk.TreeView):
    def __init__(self):
        super(ProgressList, self).__init__()

        self.xid2iter = dict()
        self.piter = None
        self.props.show_expanders = True
        self.get_selection().props.mode = Gtk.SelectionMode.SINGLE

        self.col_file = Gtk.TreeViewColumn(_("File"))
        self.col_file.props.sort_column_id = 0
        self.col_file.props.sort_indicator = True

        self.cr_file = Gtk.CellRendererText()
        iconrenderer = Gtk.CellRendererPixbuf()
        textrenderer = Gtk.CellRendererText()
        progressrenderer = Gtk.CellRendererProgress()

        self.col_file.pack_start(iconrenderer, False)
        self.col_file.pack_start(self.cr_file, False)
        self.col_file.set_cell_data_func(self.cr_file, self.on_filename_data)
        self.col_file.set_cell_data_func(iconrenderer, self.on_icon_data)

        self.col_direction = Gtk.TreeViewColumn("<->", textrenderer)
        self.col_direction.set_cell_data_func(textrenderer, self.on_direction_data)

        self.col_status = Gtk.TreeViewColumn(_("Status"), textrenderer)
        self.col_status.set_cell_data_func(textrenderer, self.on_status_data)

        self.col_progress = Gtk.TreeViewColumn(_("Progress"), progressrenderer)
        self.col_progress.set_cell_data_func(progressrenderer, self.on_progress_data)

        self.col_transferred = Gtk.TreeViewColumn(_("Transferred bytes"), textrenderer)
        self.col_transferred.set_cell_data_func(textrenderer, self.on_transferred_data)

        self.col_transfer_rate = Gtk.TreeViewColumn(_("Transfer rate"), textrenderer)
        self.col_transfer_rate.set_cell_data_func(textrenderer, self.on_transfer_rate_data)

        self.col_time = Gtk.TreeViewColumn(_("Time"), textrenderer)
        self.col_time.set_cell_data_func(textrenderer, self.on_time_data)

        self.append_column(self.col_file)
        self.append_column(self.col_direction)
        self.append_column(self.col_status)
        self.append_column(self.col_progress)
        self.append_column(self.col_transferred)
        self.append_column(self.col_transfer_rate)
        self.append_column(self.col_time)

        self.props.model = Gtk.TreeStore(object)

    def append_xfer(self, xfer):
        if not self.piter:
            self.parentxfer = Xfer()
            #self.parentxfer.children = [xfer,]
            self.piter = self.props.model.append(None)
            #self.xid2iter[self.parentxfer.xid] = self.piter
            self.props.model.set_value(self.piter, 0, self.parentxfer)
        GObject.idle_add(self.append_file, xfer)

    def append_file(self, xfer):
        citer = self.props.model.append(self.piter)
        self.xid2iter[xfer.xid] = citer
        self.props.model.set_value(citer, 0, xfer)
        xfer.connect('xfer-event', self.update_xfer)
        self.expand_all()

    def update_xfer(self, xfer):
        citer = self.xid2iter[xfer.xid]
        #piter = self.xid2iter[-1]
        self.props.model.set_value(citer, 0, xfer)
        #self.props.model.set_value(piter, 0, self.parentxfer)

    def on_filename_data(self, column, renderer, treemodel, treeiter, data):
        f = self.props.model.get_value(treeiter, 0)
        renderer.props.text = f.filename

    def on_icon_data(self, column, renderer, treemodel, treeiter, data):
        f = self.props.model.get_value(treeiter, 0)
        renderer.props.pixbuf = f.icon

    def on_direction_data(self, column, renderer, treemodel, treeiter, data):
        x = self.props.model.get_value(treeiter, 0)
        if x.direction:
            renderer.props.text = x.direction
        else:
            renderer.props.text = ''

    def on_status_data(self, column, renderer, treemodel, treeiter, data):
        f = self.props.model.get_value(treeiter, 0)
        renderer.props.text = f.status

    def on_progress_data(self, column, renderer, treemodel, treeiter, data):
        f = self.props.model.get_value(treeiter, 0)
        if f.transferred_bytes > 0:
            factor = (f.transferred_bytes / f.size) * 100
            renderer.props.text = '%s%%' % str(int(factor))
            renderer.props.value = int(factor)
        else:
            renderer.props.text = '0%'
            renderer.props.value = 0

    def on_transferred_data(self, column, renderer, treemodel, treeiter, data):
        x = self.props.model.get_value(treeiter, 0)
        renderer.props.text = str(x.format_transferred_bytes())

    def on_transfer_rate_data(self, column, renderer, treemodel, treeiter, data):
        x = self.props.model.get_value(treeiter, 0)
        renderer.props.text = x.transfer_rate

    def on_time_data(self, column, renderer, treemodel, treeiter, data):
        x = self.props.model.get_value(treeiter, 0)
        renderer.props.text = str(x.elapsed_time)
