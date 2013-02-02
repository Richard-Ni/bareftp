from __future__ import division
from gi.repository import GObject, GLib
import sys
from lib.repeat_timer import RepeatTimer
import threading
import time
import datetime

if sys.version[0] == '2':
    import thread as _thread
    import Queue as queue
else:
    import _thread
    import queue


class XferRunner(threading.Thread):
    def __init__(self):
        super(XferRunner, self).__init__()
        self.xfers = []
        self.cv = threading.Condition()
        self.xferqueue = queue.Queue()
        self.stopsignal = False

    def append_xfer(self, xfer):
        self.xferqueue.put(xfer)

    def run(self):
        while True:
            if self.stopsignal:
                return
            self.cv.acquire()
            while self.xferqueue.empty():
                self.cv.wait()
                if self.stopsignal:
                    self.cv.release()
                    return
            self.do_xfer()
            self.cv.release()

    def do_xfer(self):
        if self.xferqueue.empty():
            return False
        xfer = self.xferqueue.get()
        # TODO: run start here for threaded multiple transfers..
        xfer.run()
        self.xferqueue.task_done()


class Xfer(GObject.GObject, threading.Thread):
    def __init__(self, ftpfile=None, sender=None, receiver=None):
        super(Xfer, self).__init__()
        threading.Thread.__init__(self)
        # sender and receiver is a connection_manager

        self.status = ''
        self.transferred_bytes = 0
        self.transfer_rate = ''
        self.bytes_since_speed_calc = 0
        self.elapsed_time = ''
        self.bps = 0
        self.timestamp = None
        self.direction = ''
        self.sleeptime = 0.0
        self.lock = threading.Lock()

        if not ftpfile:
            self.xid = -1
            self.filename = 'Connection'
            self.icon = None
            self.size = 0
            self.ftpfile = None
            return

        self.filename = ftpfile.filename
        self.icon = ftpfile.icon
        self.size = ftpfile.size
        self.conn_r = receiver.get_connection()
        self.conn_s = sender.get_connection()
        if sender.side == 'RIGHT':
            self.direction = '<-'
        else:
            self.direction = '->'
        self.ftpfile = ftpfile
        self.repeater = RepeatTimer(0.5, self.xfer_event)

    def run(self):
        if self.xid < 0:
            return
        self.conn_s.xfer_in_progress = True
        self.conn_r.xfer_in_progress = True

        # Prepare both ends
        if not self.conn_s._get_init(self.filename) or not self.conn_r._put_init(self.filename):
            self.conn_s.xfer_in_progress = False
            self.conn_r.xfer_in_progress = False
            return

        # Do the actual transfer

        self.repeater.start()
        self.start_time = time.time()
        self.timestamp = time.time()
        self.status = 'Transfering'

        while 1:
            data = self.conn_s._get_packet()
            if not data:
                break
            tr_size = len(data)
            self.lock.acquire()
            self.transferred_bytes += tr_size
            self.bytes_since_speed_calc += tr_size
            self.conn_r._put_packet(data)

            if self.sleeptime > 0:
                time.sleep(self.sleeptime)
            self.lock.release()

        self.repeater.cancel()
        self.status = 'Finished'
        self.emit('xfer-event')

        # Clean up on both ends
        self.conn_s._get_end()
        self.conn_r._put_end()

        self.conn_s.xfer_in_progress = False
        self.conn_r.xfer_in_progress = False

    def format_transferred_bytes(self):
        if self.xid < 0:
            return ''
        return '%s of %s' % (self.ftpfile.pretty_size(self.transferred_bytes), self.ftpfile.pretty_size(self.size))

    def xfer_event(self):
        self.lock.acquire()
        if self.xid >= 0:

            t2 = time.time()
            t3 = datetime.timedelta(0, int(round(t2 - self.start_time)))
            time_since_speed_calc = t2 - self.timestamp
            if time_since_speed_calc >= 1.2:
                tr_bytes = self.bytes_since_speed_calc
                self.timestamp = time.time()
                self.bytes_since_speed_calc = 0
                self.bps = tr_bytes / time_since_speed_calc
                self.transfer_rate = self.ftpfile.pretty_size(int(round(self.bps))) + '/s'
            if self.bps > 0:
                eta = datetime.timedelta(0, int(round(self.size / self.bps)))
                tminus = eta - t3
                if tminus.total_seconds() > 0:
                    self.elapsed_time = str(t3) + ' (ETA: ' + str(tminus) + ')'
                else:
                    self.elapsed_time = str(t3)
            else:
                self.elapsed_time = str(t3)

            #limit = 409600
            #if self.bps > 0:
            #    delta = (self.bps - limit) / 1000000 / 1000
            #    self.sleeptime += delta

            self.emit('xfer-event')
        self.lock.release()


class XferManager(GObject.GObject):
    def __init__(self):
        super(XferManager, self).__init__()
        self.xfer_count = 0
        self.progresslist = None
        self._lock = threading.Lock()
        self.xferrunner = XferRunner()
        self.xferrunner.start()

    def abort_all(self):
        self.xferrunner.cv.acquire()
        self.xferrunner.stopsignal = True
        self.xferrunner.cv.notify()
        self.xferrunner.cv.release()
        self.xferrunner.join()

    def append_xfer(self, xfer):
        self.xferrunner.cv.acquire()
        xfer.xid = self.xfer_count
        self.xfer_count += 1
        self.progresslist.append_xfer(xfer)
        self.xferrunner.append_xfer(xfer)
        self.xferrunner.cv.notify()
        self.xferrunner.cv.release()
