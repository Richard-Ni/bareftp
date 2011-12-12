from gi.repository import GObject

from protocols.protocol import Protocol
from protocols.ftp import FTPClient 
from protocols.connection_manager import ConnectionManager

# Signals from the protocols, consumed by the connection manager
GObject.signal_new("log-event", Protocol, GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (object,))
GObject.signal_new("pwd-received", Protocol, GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (str,))
GObject.signal_new('list-received', Protocol, GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (object,))

# Signals from the connection manager, consumed by GUI
GObject.signal_new('message-received', ConnectionManager, GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (object,))
GObject.signal_new('error', ConnectionManager, GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (object,))
GObject.signal_new('updated', ConnectionManager, GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (object,))
GObject.signal_new("pwd-received", ConnectionManager, GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (str,))
GObject.signal_new('list-received', ConnectionManager, GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (object,))

#GObject.signal_new('updated', ConnectionManager, GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (object,))

GObject.signal_new('error', FTPClient, GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (object,))