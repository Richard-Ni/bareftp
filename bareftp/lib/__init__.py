from gi.repository import GObject
from lib.stdoutwrapper import StdOutWrapper
from lib.xferpool import Xfer

GObject.signal_new('log-event', StdOutWrapper, GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (object,))
GObject.signal_new('xfer-event', Xfer, GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, ())
GObject.signal_new('xfer-finished', Xfer, GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (object,int,))