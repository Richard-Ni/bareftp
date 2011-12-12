from gi.repository import GObject


class LogMessage(object):
    pass


class Protocol(GObject.GObject):
    def __init__(self):
        super(Protocol, self).__init__()

        self.available = False
        self.xfer_in_progress = False

    def _open(self, remote_host, remote_port, user, passwd):
        pass

    def _close(self):
        pass

    def _is_connected(self):
        return False

    def _dir(self):
        return None

    def _xdir(self):
        return None

    def _get(self, _file):
        pass

    def _put(self, _file):
        pass

    def _delete(self, filename):
        pass

    def _move(self, src, dst):
        pass

    def _rename(self, src, dst):
        pass

    def _cwd(self, path):
        pass

    def _pwd(self):
        return None

    def _mkdir(self, path):
        pass

    def _rmdir(self, path):
        pass

    def _chmod(self, path, mode):
        pass

    def _abort(self):
        pass

    def _isdir(self, path, directory):
        return False

    def send_log_message(self, message):
        self.emit('log-event', message)

    def update_file_list(self, files):
        self.emit('list-received', files)

    def pwd_received(self, pwd):
        self.emit('pwd-received', pwd)
