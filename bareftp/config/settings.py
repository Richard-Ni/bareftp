from gi.repository import Gio
import getpass, socket

class Config(object):

    BASE_KEY = 'apps.bareftp'

    def __init__(self):
        self.settings = Gio.Settings.new(self.BASE_KEY)

    def get_vpaned_pos(self):
        return self.settings.get_int('vpaned-pos')

    def set_vpaned_pos(self, pos):
        self.settings.set_int('vpaned-pos', pos)

    def get_hpaned_pos(self):
        return self.settings.get_int('hpaned-pos')

    def set_hpaned_pos(self, pos):
        self.settings.set_int('hpaned-pos', pos)

    def get_remote_charset(self):
        return self.settings.get_string('remote-charset')

    def set_remote_charset(self, charset):
        self.settings.set_string('remote-charset', charset)

    def get_show_hidden_files(self):
        return self.settings.get_boolean('show-hidden-files')

    def set_show_hidden_files(self, show_hidden):
        self.settings.set_boolean('show-hidden-files', show_hidden)

    def get_enable_directory_cache(self):
        return self.settings.get_boolean('enable-directory-cache')

    def set_enable_directory_cache(self, cache_enabled):
        self.settings.set_boolean('enable-directory-cache', cache_enabled)

    def get_preserve_file_permissions(self):
        return self.settings.get_boolean('preserve-file-permissions')

    def set_preserve_file_permissions(self, preserve_file_permissions):
        self.settings.set_boolean('preserve-file-permissions', preserve_file_permissions)

    def get_use_gnome_keyring(self):
        return self.settings.get_boolean('use-gnome-keyring')

    def set_use_gnome_keyring(self, use_gnome_keyring):
        self.settings.set_boolean('use-gnome-keyring', use_gnome_keyring)

    def get_default_protocol(self):
        return self.settings.get_int('default-protocol')

    def set_default_protocol(self, default_protocol):
        self.settings.set_int('default-protocol', default_protocol)

    def get_network_timeout(self):
        return self.settings.get_int('network-timeout')

    def set_network_timeout(self, timeout):
        self.settings.set_int('network-timeout', timeout)

    def get_single_transfer(self):
        return not self.settings.get_boolean('simultaneous-transfers')

    def set_single_transfer(self, single_transfer):
        self.settings.set_boolean('simultaneous-transfers', not single_transfer)

    def get_max_connections(self):
        return self.settings.get_int('max-connections')

    def set_max_connections(self, max_connections):
        self.settings.set_int('max-connections', max_connections)

    def get_ftp_default_port(self):
        return self.settings.get_int('ftp-default-port')

    def set_ftp_default_port(self, ftp_default_port):
        self.settings.set_int('ftp-default-port', ftp_default_port)

    def get_ftp_passive(self):
        return self.settings.get_boolean('passive-mode')

    def set_ftp_passive(self, passive_mode):
        self.settings.set_boolean('passive-mode', passive_mode)

    def get_translate_empty_anon(self):
        return self.settings.get_boolean('translate-empty-user-anon')

    def set_translate_empty_anon(self, tr_empty_anon):
        self.settings.set_boolean('translate-empty-user-anon', tr_empty_anon)

    def get_empty_anon_pass_email(self):
        return self.settings.get_boolean('empty-anon-pass-email')

    def set_empty_anon_pass_email(self, empty_anon_pass_email):
        self.settings.set_boolean('empty-anon-pass-email', empty_anon_pass_email)

    def get_email(self):
        email = self.settings.get_string('email')
        if not email:
            return '%s@%s' % (getpass.getuser(), socket.gethostname())
        return email

    def set_email(self, email):
        self.settings.set_string('email', email)

    def get_ftps_protection_level(self):
        return self.settings.get_string('data-protection-level')

    def set_ftps_protection_level(self, protection_level):
        self.settings.set_string('data-protection-level', protection_level)

    def get_verify_server_cert(self):
        return self.settings.get_boolean('verify-server-certificate')

    def set_verify_server_cert(self, verify_server_cert):
        self.settings.set_boolean('verify-server-certificate', verify_server_cert)

    def get_ssh_default_port(self):
        return self.settings.get_int('sftp-default-port')

    def set_ssh_default_port(self, ssh_default_port):
        self.settings.set_int('sftp-default-port', ssh_default_port)

    encodings = {
            'ascii': 'ascii',
            'big5-tw': 'big5',
            'big5-hkscs': 'big5hkscs',
            'cp037': 'cp037',
            'cp154': 'ptcp154',
            'cp424': 'cp424',
            'cp437': 'cp437',
            'cp500': 'cp500',
            'cp720': 'cp720',
            'cp737': 'cp737',
            'cp775': 'cp775',
            'cp850': 'cp850',
            'cp852': 'cp852',
            'cp855': 'cp855',
            'cp856': 'cp856',
            'cp857': 'cp857',
            'cp860': 'cp860',
            'cp861': 'cp861',
            'cp862': 'cp862',
            'cp863': 'cp863',
            'cp864': 'cp864',
            'cp865': 'cp865',
            'cp866': 'cp866',
            'cp869': 'cp869',
            'cp874': 'cp874',
            'cp875': 'cp875',
            'cp932': 'cp932',
            'cp936': 'gbk',
            'cp949': 'cp949',
            'cp950': 'cp950',
            'cp1006': 'cp1006',
            'cp1026': 'cp1026',
            'cp1140': 'cp1140',
            'cp1361': 'johab',
            'windows-1250': 'cp1250',
            'windows-1251': 'cp1251',
            'windows-1252': 'cp1252',
            'windows-1253': 'cp1253',
            'windows-1254': 'cp1254',
            'windows-1255': 'cp1255',
            'windows-1256': 'cp1256',
            'windows-1257': 'cp1257',
            'windows-1258': 'cp1258',
            'eucjp': 'euc_jp',
            'eucjis2004': 'euc_jis_2004',
            'eucjisx0213': 'euc_jisx0213',
            'euckr': 'euc_kr',
            'euccn chinese': 'gb2312',
            'gb18030': 'gb18030',
            'hz-gb': 'hz',
            'iso-2022jp': 'iso2022_jp',
            'iso-2022jp-1': 'iso2022_jp_1',
            'iso-2022jp-2': 'iso2022_jp_2',
            'iso-2022jp-2004': 'iso2022_jp_2004',
            'iso-2022jp-3': 'iso2022_jp_3',
            'iso-2022jp-ext': 'iso2022_jp_ext',
            'iso-2022-kr': 'iso2022_kr',
            'iso-8859-1': 'latin_1',
            'iso-8859-2': 'iso8859_2',
            'iso-8859-3': 'iso8859_3',
            'iso-8859-4': 'iso8859_4',
            'iso-8859-5': 'iso8859_5',
            'iso-8859-6': 'iso8859_6',
            'iso-8859-7': 'iso8859_7',
            'iso-8859-8': 'iso8859_8',
            'iso-8859-9': 'iso8859_9',
            'iso-8859-10': 'iso8859_10',
            'iso-8859-13': 'iso8859_13',
            'iso-8859-14': 'iso8859_14',
            'iso-8859-15': 'iso8859_15',
            'iso-8859-16': 'iso8859_16',
            'koi8_r': 'koi8_r',
            'koi8_u': 'koi8_u',
            'maccyrillic': 'mac_cyrillic',
            'macgreek': 'mac_greek',
            'maciceland': 'mac_iceland',
            'maclatin2': 'mac_latin2',
            'macroman': 'mac_roman',
            'macturkish': 'mac_turkish',
            'shiftjis': 'shift_jis',
            'shiftjis2004': 'shift_jis_2004',
            'shiftjisx0213': 'shift_jisx0213',
            'utf-32': 'utf_32',
            'utf-32be': 'utf_32_be',
            'utf-32le': 'utf_32_le',
            'utf-16': 'utf_16',
            'utf-16be': 'utf_16_be',
            'utf-16le': 'utf_16_le',
            'utf-7': 'utf_7',
            'utf-8': 'utf_8'
        }
