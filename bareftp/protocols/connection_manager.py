from gi.repository import GObject
import sys
if sys.version[0] == '2':
    import thread as _thread
    import Queue as queue
else:
    import _thread
    import queue

import threading
from protocols.ftp import FTPClient
from protocols.local import LocalClient


class TaskRunner(threading.Thread):
    def __init__(self):
        super(TaskRunner, self).__init__()
        self.connections = []
        self.cv = threading.Condition()
        self.taskqueue = queue.Queue()
        self.stopsignal = False

    def append_task(self, job):
        self.taskqueue.put(job)

    def run(self):
        while True:
            if self.stopsignal:
                return
            self.cv.acquire()
            while self.taskqueue.empty():
                self.cv.wait()
                if self.stopsignal:
                    self.cv.release()
                    return
            self.do_task()
            self.cv.release()

    def do_task(self):
        if self.taskqueue.empty():
            return False
        j = self.taskqueue.get()
        for (conn, job, args) in j:
            conn.available = False
            result = job(*args)
            conn.available = True
            if not result:
                break
        self.taskqueue.task_done()


class ConnectionManager(GObject.GObject):

    def __init__(self):
        super(ConnectionManager, self).__init__()
        self._lock = threading.Lock()
        self.tr = TaskRunner()
        self.tr.start()

    def abort_all(self):
        self.tr.cv.acquire()
        self.tr.stopsignal = True
        self.tr.cv.notify()
        self.tr.cv.release()
        self.tr.join()

    def get_num_connections(self):
        return len(self.connections)

    def get_connection(self):
        if len(self.tr.connections) == 0:
            c = self.create_connection()
            self.tr.connections.append(c)
            return c
        else:
            c = self.find_available_connection()
            if c:
                return c

            c = self.create_connection()
            c._open("xxx", 21, "xxx", "xxx")
            c._cwd(self.tr.connections[0].current_dir)
            self.tr.connections.append(c)
            return c

    def create_connection(self):
        c = None
        if self.type == 'FTP':
            c = FTPClient()
            c.out.connect('log-event', self.log_event)

        elif self.type == "LOCAL":
            c = LocalClient()

        c.connect('log-event', self.log_event)
        c.connect('list-received', self.list_received)
        c.connect('pwd-received', self.pwd_received)
        return c

    def find_available_connection(self):
        #TODO: Check all connections and return an avaiable one..
        for conn in self.tr.connections:
            if not conn.xfer_in_progress:
                return conn
        return None

    # The following is convenience functions to do frequently used
    # sequences of commands in one threaded funtion call

    def _cwd_pwd_xdir(self, _path):
        tasks = []
        if _path:
            tasks.append(self._cwd(_path, True))
        tasks.append(self._pwd(True))
        tasks.append(self._xdir(True))
        self.append_tasks(tasks)

    # End of convenience functions

    def _open(self, returntask=False):
        c = self.get_connection()
        task = [c._open, ("host", 21, "user", "passwd")]
        if returntask:
            return task
        self.append_task(task)

    def _pwd(self, returntask=False):
        c = self.get_connection()
        task = [c, c._pwd, ()]
        if returntask:
            return task
        self.append_task(task)

    def _cwd(self, _path, returntask=False):
        c = self.get_connection()
        task = [c, c._cwd, (_path,)]
        if returntask:
            return task
        self.append_task(task)

    def _xdir(self, returntask=False):
        c = self.get_connection()
        task = [c, c._xdir, ()]
        if returntask:
            return task
        self.append_task(task)

    def _mkdir(self, _dirname, returntask=False):
        c = self.get_connection()
        task = [c, c._mkdir, (_dirname,)]
        if returntask:
            return task
        self.append_task(task)
        self._xdir(False)

    def _delete(self, files):
        c = self.get_connection()
        for f in files:
            task = [c, c._delete, (f.filename,)]
            self.append_task(task)
        self._xdir(False)

    def _rmdir(self, files):
        c = self.get_connection()
        for f in files:
            task = [c, c._rmdir, (f.filename,)]
            self.append_task(task)
        self._xdir(False)

    def _rename(self, src, dst, returntask=False):
        c = self.get_connection()
        task = [c, c._rename, (src, dst)]
        if returntask:
            return task
        self.append_task(task)
        self._xdir(False)

    def _chmod(self, files, permissions):
        c = self.get_connection()
        for f in files:
            task = [c, c._chmod, (f.filename, permissions)]
            self.append_task(task)
        self._xdir(False)

    def _close(self):
        c = self.get_connection()
        self.append_task([c, c._close, ()])

    def append_task(self, task):
        self.append_tasks([task])

    def append_tasks(self, tasks):
        self.tr.cv.acquire()
        self.tr.append_task(tasks)
        self.tr.cv.notify()
        self.tr.cv.release()

    def log_event(self, sender, message):
        self.emit('message-received', message)

    def list_received(self, sender, filelist):
        self.emit('list-received', filelist)

    def pwd_received(self, sender, pwd):
        self.emit('pwd-received', pwd)
