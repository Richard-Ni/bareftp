from __future__ import division
from gi.repository import GObject
import datetime

class FtpFile(object):
    def __init__(self, filename=''):
        super(FtpFile, self).__init__()
        self.filename = filename
        self.icon = None
        self.size = 0.0
        self.lastmodified = None
        self.owner = ''
        self.group = ''
        self.permissions = ''
        self.isdir = False
        self.islink = False
        self.linkdest = ''
        self.abs_path = ''
        self.rel_path = ''
        
    def expand(self):
        return [self, self.icon, self.filename, self.format_size(),
                self.format_date(), self.owner, self.group, self.permissions]
    
    def format_date(self):
        if self.lastmodified:
            return self.lastmodified.strftime("%m/%d/%Y %I:%M:%S %p")
        return ''

    def format_size(self):
        return self.pretty_size(self.size)

    def pretty_size(self, _size):
        if self.isdir:
            return ''
        suffixes = [("bytes",2**10), ("KB",2**20), ("MB",2**30), ("GB",2**40), ("TB",2**50)]
        for suf, lim in suffixes:
            if _size > lim:
                continue
            else:
                return round(_size/float(lim/2**10),1).__str__() + ' ' + suf
        return "%.1f bytes" % _size
    
