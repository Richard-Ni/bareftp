from protocols.protocol import Protocol
from ftplib import FTP
from ftplib import error_perm
from lib.listparser import parse_list
from lib.stdoutwrapper import StdOutWrapper, redirect_stdout
import re
import sys


class FTPClient(Protocol):
    def __init__(self):
        super(FTPClient, self).__init__()
        self.out = StdOutWrapper()

        self.ftp = None
        self.features = []
        self.system = ''
        self.connected = False
        self.xfer = False
        self.current_dir = ''
        self.datasocket = None
        self.unicodeerror = False

        if sys.version[0] == '3':
            self.encode_cmd = self.encode_cmd_py3
            self.encode_resp = self.encode_resp_py3
        else:
            self.encode_cmd = self.encode_cmd_py2
            self.encode_resp = self.encode_resp_py2
        self.available = True

    def _open(self, remote_host, remote_port, user, passwd):
        self.ftp = FTP()
        self.ftp.set_debuglevel(1)

        with redirect_stdout(self.out):
            try:
                self.ftp.connect(remote_host, remote_port, 20)
            except:
                self.out.write('*ERROR*' + str(sys.exc_info()[1]))
                self.ftp = None
                return False
            try:
                self.ftp.login(user, passwd)
                self.connected = True
            except:
                self.ftp = None
                return False
            try:
                #self.ftp.sendcmd('cd []')
                self.system = self.ftp.sendcmd('SYST')
            except:
                pass
            try:
                self.features = self.parseFeatures(self.ftp.sendcmd('FEAT'), '211')
            except:
                pass
            return True

    def _is_connected(self):
        return self.connected

    def _transfer_in_progress(self):
        return self.xfer

    def _is_available(self):
        return self.available

    def _cwd(self, _path):
        if self.ftp is None:
            self.send_log_message('Not connected')
            return False
        with redirect_stdout(self.out):
            try:
                self.ftp.cwd(self.encode_cmd(_path))
                return True
            except error_perm as err:
                #self.out.write(str(err))
                return False
            except:
                self.send_log_message(['error', 'ftp.py: %s' % sys.exc_info()[1] + '\n'])
                return False

    def _pwd(self):
        if self.ftp is None:
            self.send_log_message('Not connected')
            return False

        with redirect_stdout(self.out):
            try:
                pwd = self.ftp.pwd()
                pwd = self.encode_resp(pwd)
                self.current_dir = pwd
                self.pwd_received(pwd)
                return True
            except error_perm as err:
                self.out.write(str(err))
                return False

    def _delete(self, filename):
        with redirect_stdout(self.out):
            try:
                self.ftp.delete(self.encode_cmd(filename))
            except error_perm as err:
                return False

    def _rmdir(self, dirname):
        with redirect_stdout(self.out):
            try:
                _files = []
                self.traverse(dirname, _files)
                _files.reverse()
                self._cwd(self.current_dir)
                for f in _files:
                    #print(f.rel_path + '/' + f.filename)
                    if f.isdir:
                        self.ftp.rmd(self.encode_cmd(f.filename))
                    else:
                        self.ftp.delete(self.encode_cmd(f.filename))
                self.ftp.rmd(self.encode_cmd(dirname))
            except error_perm as err:
                return False

    def _mkdir(self, _path):
        with redirect_stdout(self.out):
            try:
                self.ftp.mkd(self.encode_cmd(_path))
            except error_perm as err:
                return False

    def _rename(self, src, dst):
        with redirect_stdout(self.out):
            try:
                self.ftp.rename(self.encode_cmd(src), self.encode_cmd(dst))
                return True
            except error_perm as err:
                return False

    def _chmod(self, path, mode):
        with redirect_stdout(self.out):
            try:
                self.parseFeatures(self.ftp.sendcmd('SITE CHMOD %s %s' % (mode, self.encode_cmd(path))), '200')
                return True
            except error_perm as err:
                return False

    def _xdir(self, returnlist=False):
        if self.ftp == None:
            self.send_log_message('Not connected')
            return False

        list_command = "LIST"

        if self.system.find("VMS") >= 0 or self.system.find("MultiNet Unix Emulation") >= 0:
            list_command = "LIST"

        lines = []
        with redirect_stdout(self.out):
            try:
                ret = self.ftp.retrlines(list_command, lines.append)
                lines = self.encode_lines(lines)
                files = parse_list(lines)
                if returnlist:
                    return files
                if files:
                    self.update_file_list(files)
                #if 'MLSD' in self.features:
                #    self.ftp.retrlines('MLSD', self.dump)
            except error_perm as err:
                self.out.write(str(err))
                return False

    def _get_init(self, filename):
        with redirect_stdout(self.out):
            try:
                self.ftp.voidcmd('TYPE I')
                self.datasocket = self.ftp.transfercmd('RETR ' + self.encode_cmd(filename))
                return True
            except error_perm as err:
                return False

    def _get_packet(self):
        return self.datasocket.recv(2048)

    def _get_end(self):
        with redirect_stdout(self.out):
            try:
                self.datasocket.close()
                self.ftp.voidresp()
                self.datasocket = None
                self._xdir()
                return True
            except error_perm as err:
                return False

    def _put_init(self, filename):
        #self.filehandle = open(os.path.join(self.currentdir, filename), 'w')
        with redirect_stdout(self.out):
            try:
                self.ftp.voidcmd('TYPE I')
                self.datasocket = self.ftp.transfercmd('STOR ' + self.encode_cmd(filename))
                return True
            except error_perm as err:
                return False

    def _put_packet(self, packet):
        self.datasocket.send(packet)
        #self.filehandle.write(packet)
        pass

    def _put_end(self):
        with redirect_stdout(self.out):
            try:
                self.datasocket.close()
                self.ftp.voidresp()
                self.datasocket = None
                self._xdir()
                return True
            except error_perm as err:
                return False

    def traverse(self, _path, _files):
        self._cwd(self.current_dir + "/" + _path)
        for f in self._xdir(True):
            if f.filename != '.' and f.filename != '..':
                f.abs_path = self.current_dir + '/' + _path
                f.rel_path = _path
                _files.append(f)
                if f.isdir:
                    self.traverse(_path + '/' + f.filename, _files)

    def encode_cmd_py3(self, cmd):
        #TODO encode to whatever configured - use a sane default
        if not self.unicodeerror:
            return cmd.encode('utf8').decode('latin1')
        else:
            return cmd

    def encode_cmd_py2(self, cmd):
        #TODO encode to whatever configured - use a sane default
        return cmd.encode('utf8')

    def encode_resp_py3(self, strdata):
        #TODO decode to whatever configured - use a sane default
        conf_value = 'utf-8'
        try:
            return strdata.encode('latin1').decode(conf_value)
        except UnicodeDecodeError:
            self.unicodeerror = True
            return strdata

    def encode_resp_py2(self, strdata):
        #TODO decode to whatever configured - use a sane default
        try:
            return strdata.decode('utf-8')
        except UnicodeDecodeError:
            return strdata

    def encode_lines(self, lines):
        _lines = []
        for line in lines:
            _lines.append(self.encode_resp(line))
        return _lines

    def parseFeatures(self, reply, code):
        lines = re.split(r'[\n\r]+', reply)
        features = []
        if lines[0].strip().startswith(code):
            for line in lines:
                if line.find(code) < 0 and line.find('Features') < 0 and line.find('End') < 0:
                    features.append(line.strip())
        return features

    def _close(self):
        self.connected = False
        self.ftp.quit()

    def dump(self, l):
        return
        sys.__stdout__.write(l)
        sys.__stdout__.write('\n')
        sys.__stdout__.flush()
