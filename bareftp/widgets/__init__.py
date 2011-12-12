from gi.repository import GObject
from widgets.filelist import BareFTPFileList

GObject.signal_new("cwd-event", BareFTPFileList, GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (object,))
GObject.signal_new("newdirnamed-event", BareFTPFileList, GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (str,))
GObject.signal_new("file-renamed-event", BareFTPFileList, GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (object, str,))
GObject.signal_new("delete-files-event", BareFTPFileList, GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (object, ))
GObject.signal_new("chmod-event", BareFTPFileList, GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (object, str))