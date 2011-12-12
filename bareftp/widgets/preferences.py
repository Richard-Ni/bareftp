from gi.repository import Gtk
from i18n import _
from config.settings import Config
from widgets.bareftpwidgets import ProtocolComboBox


class PreferencesDialog(Gtk.Dialog):
    def __init__(self, parent, config):
        super(PreferencesDialog, self).__init__(_('Preferences'),
                            parent, Gtk.DialogFlags.MODAL |
                            Gtk.DialogFlags.DESTROY_WITH_PARENT,
                            (Gtk.STOCK_CLOSE, Gtk.ResponseType.CANCEL))

        self.settings = config

        content_area = self.get_content_area()
        notebook = Gtk.Notebook()
        notebook.props.border_width = 10
        content_area.pack_start(notebook, False, False, 0)

        #vbox2 = Gtk.VBox()
        #self.pack_start(vbox2, False, False, 0)

        frame = Gtk.Frame()
        label = Gtk.Label()
        label.props.use_markup = True
        label.set_markup(_('<b>Character encoding</b>'))

        vbox = Gtk.VBox(False, 6)
        vbox.props.border_width = 5

        frame.props.label_widget = label
        frame.props.shadow_type = Gtk.ShadowType.NONE

        alignment = Gtk.Alignment()
        alignment.props.left_padding = 15

        frame.add(alignment)

        hbox = Gtk.HBox(False, 6)
        hbox.props.border_width = 3
        hbox.pack_start(Gtk.Label(_('Remote Charset')), False, False, 0)

        self.cb_remote_charset = Gtk.ComboBoxText.new()
        encs = sorted(Config.encodings.keys())

        idx = 0
        rmcs = self.settings.get_remote_charset()
        for enc in encs:
            self.cb_remote_charset.append_text(enc)
            if enc == rmcs:
                self.cb_remote_charset.set_active(idx)
            idx += 1

        self.cb_remote_charset.connect('changed', self.remote_charset_changed)

        hbox.pack_start(self.cb_remote_charset, False, False, 0)
        alignment.add(hbox)

        vbox.pack_start(frame, False, False, 5)

        frame = Gtk.Frame()
        label = Gtk.Label()
        label.props.use_markup = True
        label.set_markup(_('<b>File view</b>'))
        frame.props.label_widget = label
        frame.props.shadow_type = Gtk.ShadowType.NONE

        alignment = Gtk.Alignment()
        alignment.props.left_padding = 15

        frame.add(alignment)

        _vbox = Gtk.VBox(False, 6)

        self.cb_show_hidden_files = Gtk.CheckButton(_('Show hidden files'))
        self.cb_show_hidden_files.set_active(self.settings.get_show_hidden_files())
        self.cb_show_hidden_files.connect('toggled', self.show_hidden_files_changed)
        _vbox.pack_start(self.cb_show_hidden_files, False, False, 0)

        self.cb_enable_directory_cache = Gtk.CheckButton(_('Enable directory cache'))
        self.cb_enable_directory_cache.set_active(self.settings.get_enable_directory_cache())
        self.cb_enable_directory_cache.connect('toggled', self.enable_directory_cache_changed)
        _vbox.pack_start(self.cb_enable_directory_cache, False, False, 0)

        alignment.add(_vbox)
        vbox.pack_start(frame, False, False, 5)

        frame = Gtk.Frame()
        label = Gtk.Label()
        label.props.use_markup = True
        label.set_markup(_('<b>File transfer</b>'))
        frame.props.label_widget = label
        frame.props.shadow_type = Gtk.ShadowType.NONE

        alignment = Gtk.Alignment()
        alignment.props.left_padding = 15

        frame.add(alignment)

        _vbox = Gtk.VBox(False, 6)
        self.cb_preserve_file_permissions = Gtk.CheckButton(_('Preserve file permissions'))
        self.cb_preserve_file_permissions.set_active(self.settings.get_preserve_file_permissions())
        self.cb_preserve_file_permissions.connect('toggled', self.preserve_file_permissions_changed)
        _vbox.pack_start(self.cb_preserve_file_permissions, False, False, 0)

        alignment.add(_vbox)
        vbox.pack_start(frame, False, False, 5)

        frame = Gtk.Frame()
        label = Gtk.Label()
        label.props.use_markup = True
        label.set_markup('<b>%s</b>' % _('Bookmarks'))
        frame.props.label_widget = label
        frame.props.shadow_type = Gtk.ShadowType.NONE

        alignment = Gtk.Alignment()
        alignment.props.left_padding = 15

        frame.add(alignment)

        _vbox = Gtk.VBox(False, 6)
        self.cb_use_gnome_keyring = Gtk.CheckButton(_('Use Gnome Keyring for passwords'))
        self.cb_use_gnome_keyring.set_active(self.settings.get_use_gnome_keyring())
        self.cb_use_gnome_keyring.connect('toggled', self.use_gnome_keyring_changed)
        _vbox.pack_start(self.cb_use_gnome_keyring, False, False, 0)

        alignment.add(_vbox)
        vbox.pack_start(frame, False, False, 5)

        notebook.append_page(vbox, Gtk.Label(_('General')))

        # Connection tab..

        frame = Gtk.Frame()
        label = Gtk.Label()
        label.props.use_markup = True
        label.set_markup(_('<b>Protocol</b>'))

        vbox = Gtk.VBox(False, 6)
        vbox.props.border_width = 5

        frame.props.label_widget = label
        frame.props.shadow_type = Gtk.ShadowType.NONE

        alignment = Gtk.Alignment()
        alignment.props.left_padding = 15

        frame.add(alignment)
        vbox.pack_start(frame, False, False, 5)

        _hbox = Gtk.HBox(False, 6)
        alignment.add(_hbox)
        _hbox.pack_start(Gtk.Label(_('Default protocol:')), False, False, 0)

        ls = Gtk.ListStore(int, str)
        ls.append([1, 'FTP'])
        ls.append([2, 'FTPS'])
        ls.append([3, 'SSH (SFTP)'])
        self.cb_default_protocol = ProtocolComboBox()
        self.cb_default_protocol.set_model(ls)
        self.cb_default_protocol.set_value(self.settings.get_default_protocol())
        self.cb_default_protocol.connect('changed', self.default_protocol_changed)

        _hbox.pack_start(self.cb_default_protocol, False, False, 0)

        frame = Gtk.Frame()
        label = Gtk.Label()
        label.props.use_markup = True
        label.set_markup(_('<b>Network</b>'))

        frame.props.label_widget = label
        frame.props.shadow_type = Gtk.ShadowType.NONE

        alignment = Gtk.Alignment()
        alignment.props.left_padding = 15

        frame.add(alignment)

        vbox.pack_start(frame, False, False, 5)

        _hbox = Gtk.HBox(False, 6)
        alignment.add(_hbox)
        _hbox.pack_start(Gtk.Label(_('Network timeout (s):')), False, False, 0)

        self.entry_network_timeout = Gtk.Entry()
        self.entry_network_timeout.set_width_chars(6)
        self.entry_network_timeout.set_text(str(self.settings.get_network_timeout()))
        _hbox.pack_start(self.entry_network_timeout, False, False, 0)
        self.entry_network_timeout.connect('changed', self.network_timeout_changed)

        frame = Gtk.Frame()
        label = Gtk.Label()
        label.props.use_markup = True
        label.set_markup(_('<b>File transfer</b>'))

        frame.props.label_widget = label
        frame.props.shadow_type = Gtk.ShadowType.NONE

        alignment = Gtk.Alignment()
        alignment.props.left_padding = 15

        frame.add(alignment)

        vbox.pack_start(frame, False, False, 5)

        _vbox = Gtk.VBox(False, 6)
        alignment.add(_vbox)

        self.cb_single_transfer = Gtk.CheckButton(_('Do one transfer at a time'))
        self.cb_single_transfer.set_active(self.settings.get_single_transfer())
        self.cb_single_transfer.connect('toggled', self.single_transfer_changed)

        _vbox.pack_start(self.cb_single_transfer, False, False, 0)

        _hbox = Gtk.HBox(False, 6)
        _hbox.pack_start(Gtk.Label(_('Maximum number of connections:')), False, False, 0)

        self.sb_max_connections = Gtk.SpinButton()
        self.sb_max_connections.props.numeric = True
        self.sb_max_connections.props.digits = 0
        self.sb_max_connections.props.climb_rate = 1
        self.sb_max_connections.props.adjustment.props.upper = 100
        self.sb_max_connections.props.adjustment.props.lower = 1
        self.sb_max_connections.props.adjustment.props.step_increment = 1
        self.sb_max_connections.set_value(self.settings.get_max_connections())
        if self.cb_single_transfer.get_active():
            self.sb_max_connections.props.sensitive = False
        self.sb_max_connections.connect('changed', self.max_connections_changed)
        _hbox.pack_start(self.sb_max_connections, False, False, 0)
        _vbox.pack_start(_hbox, False, False, 0)

        notebook.append_page(vbox, Gtk.Label(_('Connection')))

        # FTP tab

        frame = Gtk.Frame()
        label = Gtk.Label()
        label.props.use_markup = True
        label.set_markup('<b>%s %s</b>' % (_('FTP'), _('Connection')))

        vbox = Gtk.VBox(False, 6)
        vbox.props.border_width = 5

        frame.props.label_widget = label
        frame.props.shadow_type = Gtk.ShadowType.NONE

        alignment = Gtk.Alignment()
        alignment.props.left_padding = 15

        frame.add(alignment)
        vbox.pack_start(frame, False, False, 5)

        _hbox = Gtk.HBox(False, 6)
        alignment.add(_hbox)
        _hbox.pack_start(Gtk.Label(_('Default port:')), False, False, 0)

        self.entry_ftp_default_port = Gtk.Entry()
        self.entry_ftp_default_port.set_width_chars(4)
        self.entry_ftp_default_port.set_text(str(self.settings.get_ftp_default_port()))
        self.entry_ftp_default_port.connect('changed', self.ftp_default_port_changed)
        _hbox.pack_start(self.entry_ftp_default_port, False, False, 0)

        frame = Gtk.Frame()
        label = Gtk.Label()
        label.props.use_markup = True
        label.set_markup(_('<b>File transfer</b>'))

        frame.props.label_widget = label
        frame.props.shadow_type = Gtk.ShadowType.NONE

        alignment = Gtk.Alignment()
        alignment.props.left_padding = 15

        frame.add(alignment)

        vbox.pack_start(frame, False, False, 5)

        _hbox = Gtk.HBox(False, 6)
        alignment.add(_hbox)

        self.cb_passive_ftp = Gtk.CheckButton(_('Passive file transfers'))
        self.cb_passive_ftp.set_active(self.settings.get_ftp_passive())
        self.cb_passive_ftp.connect('toggled', self.ftp_passive_mode_changed)
        _hbox.pack_start(self.cb_passive_ftp, False, False, 0)

        frame = Gtk.Frame()
        label = Gtk.Label()
        label.props.use_markup = True
        label.set_markup(_('<b>Anonymous login</b>'))

        frame.props.label_widget = label
        frame.props.shadow_type = Gtk.ShadowType.NONE

        alignment = Gtk.Alignment()
        alignment.props.left_padding = 15

        frame.add(alignment)

        vbox.pack_start(frame, False, False, 5)

        _vbox = Gtk.VBox(False, 6)
        alignment.add(_vbox)

        self.cb_tr_empty_anon = Gtk.CheckButton(_("Translate empty user to 'anonymous'"))
        self.cb_tr_empty_anon.set_active(self.settings.get_translate_empty_anon())
        self.cb_tr_empty_anon.connect('toggled', self.tr_empty_anon_changed)
        _vbox.pack_start(self.cb_tr_empty_anon, False, False, 0)

        self.cb_use_email_pass = Gtk.CheckButton(_("Use email as anonymous password"))
        self.cb_use_email_pass.set_active(self.settings.get_empty_anon_pass_email())
        self.cb_use_email_pass.connect('toggled', self.use_email_pass_changed)
        _vbox.pack_start(self.cb_use_email_pass, False, False, 0)

        _hbox = Gtk.HBox(False, 6)
        _hbox.pack_start(Gtk.Label(_('Email address:')), False, False, 0)

        self.entry_email = Gtk.Entry()
        self.entry_email.set_text(self.settings.get_email())
        self.entry_email.connect('changed', self.email_changed)
        _hbox.pack_start(self.entry_email, False, False, 0)

        _vbox.pack_start(_hbox, False, False, 0)

        notebook.append_page(vbox, Gtk.Label(_('FTP')))

        # FTPS tab

        frame = Gtk.Frame()
        label = Gtk.Label()
        label.props.use_markup = True
        label.set_markup(_('<b>Protection level</b>'))

        vbox = Gtk.VBox(False, 6)
        vbox.props.border_width = 5

        frame.props.label_widget = label
        frame.props.shadow_type = Gtk.ShadowType.NONE

        alignment = Gtk.Alignment()
        alignment.props.left_padding = 15

        frame.add(alignment)
        vbox.pack_start(frame, False, False, 5)

        _hbox = Gtk.HBox(False, 6)
        alignment.add(_hbox)

        self.cb_ftps_protection_level = Gtk.CheckButton(_('Encrypt Data Channel'))
        self.cb_ftps_protection_level.set_active(self.settings.get_ftps_protection_level() == 'C')
        self.cb_ftps_protection_level.connect('toggled', self.ftps_protection_level_changed)
        _hbox.pack_start(self.cb_ftps_protection_level, False, False, 0)

        frame = Gtk.Frame()
        label = Gtk.Label()
        label.props.use_markup = True
        label.set_markup(_('<b>Certificates</b>'))

        frame.props.label_widget = label
        frame.props.shadow_type = Gtk.ShadowType.NONE

        alignment = Gtk.Alignment()
        alignment.props.left_padding = 15

        frame.add(alignment)
        vbox.pack_start(frame, False, False, 5)

        _hbox = Gtk.HBox(False, 6)
        alignment.add(_hbox)

        self.cb_verify_cert = Gtk.CheckButton(_('Verify server certificate'))
        self.cb_verify_cert.set_active(self.settings.get_verify_server_cert())
        self.cb_verify_cert.connect('toggled', self.verify_server_cert_changed)
        _hbox.pack_start(self.cb_verify_cert, False, False, 0)

        notebook.append_page(vbox, Gtk.Label(_('FTPS')))

        # SSH

        frame = Gtk.Frame()
        label = Gtk.Label()
        label.props.use_markup = True
        label.set_markup('<b>%s %s</b>' % (_('SFTP'), _('Connection')))

        vbox = Gtk.VBox(False, 6)
        vbox.props.border_width = 5

        frame.props.label_widget = label
        frame.props.shadow_type = Gtk.ShadowType.NONE

        alignment = Gtk.Alignment()
        alignment.props.left_padding = 15

        frame.add(alignment)
        vbox.pack_start(frame, False, False, 5)

        _hbox = Gtk.HBox(False, 6)
        alignment.add(_hbox)

        _hbox.pack_start(Gtk.Label(_('Default port:')), False, False, 0)

        self.entry_ssh_default_port = Gtk.Entry()
        self.entry_ssh_default_port.set_width_chars(4)
        self.entry_ssh_default_port.set_text(str(self.settings.get_ssh_default_port()))
        self.entry_ssh_default_port.connect('changed', self.ssh_default_port_changed)
        _hbox.pack_start(self.entry_ssh_default_port, False, False, 0)

        notebook.append_page(vbox, Gtk.Label(_('SSH')))

        self.show_all()

    def remote_charset_changed(self, *args):
        self.settings.set_remote_charset(self.cb_remote_charset.get_active_text())

    def show_hidden_files_changed(self, *args):
        self.settings.set_show_hidden_files(self.cb_show_hidden_files.get_active())

    def enable_directory_cache_changed(self, *args):
        self.settings.set_enable_directory_cache(self.cb_enable_directory_cache.get_active())

    def preserve_file_permissions_changed(self, *args):
        self.settings.set_preserve_file_permissions(self.cb_preserve_file_permissions.get_active())

    def use_gnome_keyring_changed(self, *args):
        self.settings.set_use_gnome_keyring(self.cb_use_gnome_keyring.get_active())

    def default_protocol_changed(self, *args):
        self.settings.set_default_protocol(self.cb_default_protocol.get_value())

    def network_timeout_changed(self, *args):
        try:
            timeout = int(self.entry_network_timeout.get_text())
            self.settings.set_network_timeout(timeout)
        except:
            pass

    def single_transfer_changed(self, *args):
        single_transfer = self.cb_single_transfer.get_active()
        self.sb_max_connections.props.sensitive = not single_transfer
        self.settings.set_single_transfer(self.cb_single_transfer.get_active())

    def max_connections_changed(self, *args):
        self.settings.set_max_connections(self.sb_max_connections.get_value())

    def ftp_default_port_changed(self, *args):
        try:
            ftp_port = int(self.entry_ftp_default_port.get_text())
            self.settings.set_ftp_default_port(ftp_port)
        except:
            pass

    def ftp_passive_mode_changed(self, *args):
        self.settings.set_ftp_passive(self.cb_passive_ftp.get_active())

    def tr_empty_anon_changed(self, *args):
        self.settings.set_translate_empty_anon(self.cb_tr_empty_anon.get_active())

    def use_email_pass_changed(self, *args):
        self.settings.set_empty_anon_pass_email(self.cb_use_email_pass.get_active())

    def email_changed(self):
        self.settings.set_email(self.entry_email.get_text())

    def ftps_protection_level_changed(self, *args):
        plevel = 'P'
        if self.cb_ftps_protection_level.get_active():
            plevel = 'C'
        self.settings.set_ftps_protection_level(plevel)

    def verify_server_cert_changed(self):
        self.settings.set_verify_server_cert(self.cb_verify_cert.get_active())

    def ssh_default_port_changed(self):
        try:
            sshport = int(self.entry_ssh_default_port.get_text())
            self.settings.set_ssh_default_port(sshport)
        except:
            pass
