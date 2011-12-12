from gi.repository import GObject
import re
import sys

class StdOutWrapper(GObject.GObject):
    def __init__(self):
        super(StdOutWrapper, self).__init__()
        self.lines = []

    def write(self, _str):
        if  _str.strip() == '' or _str.find('*resp*') >= 0 or _str.find('*cmd*') >= 0 or _str.find('*welcome*') >= 0:
            return
        if _str.startswith('\'') and _str.endswith('\'') or _str.startswith('\"') and _str.endswith('\"'):
            _str =  _str[1:-1]

        if sys.version[0] == '3':
            _str = _str.encode('latin1').decode('utf-8')
        else:
            _str = _str.decode('unicode_escape').encode('latin1')

        for l in _str.split('\\n'):
            if l == '':
                continue
            _type = 'default'
            if not l[0].isdigit() and not l[0] == ' ':
                _type = 'client'
            if l.startswith('4') or l.startswith('5'):
                _type = 'error'
            if l.startswith('*ERROR*'):
                _type = 'error'
                l = l[7:]
            if l.startswith('220'):
                _type = 'welcome'

            self.lines.append([_type, l + '\n'])

    def flush(self):
        for l in self.lines:
            self.emit('log-event', l)
            self.lines = []
