from gi.repository import Gtk, GObject
from mainwin import MainWindow
import sys
import traceback


class BareFtpApp(object):
    def __init__(self):
        super(BareFtpApp, self).__init__()

        # TODO: Some fancy splash screen here?..

        #while Gtk.events_pending():
        #    Gtk.main_iteration_do(False)

        try:
            GObject.threads_init()

            MainWindow()
            Gtk.main()
        except:
            traceback.print_exc(file=sys.stdout)
            self._quit()

    def _quit(self, *args):
        sys.exit(0)

if __name__ == '__main__':
    app = BareFtpApp()
