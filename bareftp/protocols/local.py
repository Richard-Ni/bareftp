from protocols.protocol import Protocol
import lib.file_permission
from lib.ftpfile import FtpFile
import os
import sys
import stat
import time
import shutil
import pwd
import grp


class LocalClient(Protocol):
    def __init__(self):
        super(LocalClient, self).__init__()
        self.currentdir = ''
        self.filehandle = None
        self.available = True
        self.connected = True
        
    def _open(self, remote_host, remote_port, user, passwd):
        self.available = False
        self.currentdir = os.path.expanduser('~')
        self.available = True

    def _is_connected(self):
        return True

    def _cwd(self, _path):
        if _path:
            if _path == '..':
                self.currentdir = os.path.split(self.currentdir)[0]
            else:
                self.currentdir = os.path.join(self.currentdir, _path)
        return True

    def _pwd(self):
        self.pwd_received(self.currentdir)
        return True

    def _xdir(self):
        try:
            files = []
            for line in os.listdir(self.currentdir):
                filename = os.path.join(self.currentdir, line)
                if not os.path.exists(filename):
                    continue
                file_stats = os.stat(filename)
                if sys.version[0] == '3':
                    size = int(file_stats[stat.ST_SIZE])
                else:
                    size = long(file_stats[stat.ST_SIZE])
                date = time.strftime("%m/%d/%Y %I:%M:%S %p", time.localtime(file_stats[stat.ST_MTIME]))
                perms = lib.file_permission.str_from_mode(file_stats[stat.ST_MODE])

                uid = file_stats[stat.ST_UID]
                gid = file_stats[stat.ST_GID]

                user = pwd.getpwuid(uid)[0]
                group = grp.getgrgid(gid)[0]

                f = FtpFile()
                f.filename = line
                f.size = size
                f.lastmodified = date
                f.permissions = perms
                f.owner = user
                f.group = group

                if stat.S_ISDIR(file_stats[stat.ST_MODE]):
                    f.isdir = True
                if stat.S_ISLNK(file_stats[stat.ST_MODE]):
                    f.islink = True
                files.append(f)

            self.update_file_list(files)
        except OSError as err:
            self.send_log_message(['error', 'LOCAL: %s' % str(err) + '\n'])
            return False
        except:
            self.send_log_message(['error', 'LOCAL: %s' % sys.exc_info()[1] + '\n'])
            return False
        return True

    def _delete(self, filename):
        try:
            os.remove(os.path.join(self.currentdir, filename))
        except OSError as err:
            self.send_log_message(['error', 'LOCAL: %s' % str(err) + '\n'])
            return False
        except:
            self.send_log_message(['error', 'LOCAL: %s' % sys.exc_info()[1] + '\n'])
            return False
        return True

    def _rmdir(self, dirname):
        try:
            shutil.rmtree(os.path.join(self.currentdir, dirname), False, self.shutil_error)
        except OSError as err:
            self.send_log_message(['error', 'LOCAL: %s' % str(err) + '\n'])
            return False
        except:
            self.send_log_message(['error', 'LOCAL: %s' % sys.exc_info()[1] + '\n'])
            return False
        return True

    def shutil_error(self, _func, _path, _excinfo):
        #TODO: Log something here?
        pass

    def _mkdir(self, _path):
        try:
            os.mkdir(os.path.join(self.currentdir, _path))
        except OSError as err:
            self.send_log_message(['error', 'LOCAL: %s' % str(err) + '\n'])
            return False
        except:
            self.send_log_message(['error', 'LOCAL: %s' % sys.exc_info()[1] + '\n'])
            return False
        return True

    def _rename(self, src, dst):
        try:
            os.rename(os.path.join(self.currentdir, src), os.path.join(self.currentdir, dst))
        except OSError as err:
            self.send_log_message(['error', 'LOCAL: %s' % str(err) + '\n'])
            return False
        except:
            self.send_log_message(['error', 'LOCAL: %s' % sys.exc_info()[1] + '\n'])
            return False
        return True

    def _chmod(self, path, mode):
        try:
            os.chmod(os.path.join(self.currentdir, path), int(mode, 8))
        except OSError as err:
            self.send_log_message(['error', 'LOCAL: %s' % str(err) + '\n'])
            return False
        except:
            self.send_log_message(['error', 'LOCAL: %s' % sys.exc_info()[1] + '\n'])
            return False
        return True

    def _put_init(self, filename):
        self.filehandle = open(os.path.join(self.currentdir, filename), 'w')

    def _put_packet(self, packet):
        self.filehandle.write(packet)

    def _put_end(self):
        self.filehandle.close()
        self.filehandle = None
    
    def _get_init(self, filename):
        self.filehandle = open(os.path.join(self.currentdir, filename), 'r')

    def _get_packet(self):
        return self.filehandle.read(2048)

    def _get_end(self):
        self.filehandle.close()
        self.filehandle = None

    def encode_lines(self, lines):
        _lines = []
        for line in lines:
            self.dump(line)
            # python3: string is latin1 (wtf?)
            l = line.encode('latin1')
            # TODO: Convert to whatever configured encoding
            l = l.decode('utf-8')
            _lines.append(l)
        return _lines
