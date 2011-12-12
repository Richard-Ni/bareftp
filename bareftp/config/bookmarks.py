import xml.dom.minidom
import os

class BookmarkItem(object):
    pass

class BookmarkFolder(object):
    def __init__(self):
        self.items = []

class Bookmarks(object):
    def __init__(self):
        _home = os.environ.get('HOME', '/')
        xdg_data_home = os.environ.get('XDG_DATA_HOME', os.path.join(_home, '.local', 'share'))
        _file = os.path.join(xdg_data_home, "bareftp", "bookmarks.xml")
        if os.path.exists(_file):
            bookmarks_xml = xml.dom.minidom.parse(_file)
            b = bookmarks_xml.documentElement
        else:
            b = None
        
        self.bookmarks = BookmarkFolder()
        self.bookmarks.name = 'rootfolder'
        if b:
            self.traversexml(b, self.bookmarks)
        
    def traversexml(self, refitem, folder):
        for node in refitem.childNodes:
            if node.nodeType == node.ELEMENT_NODE:
                if node.tagName == 'bookmark':
                    b = BookmarkItem()
                    b.name = node.getAttribute('name')
                    b.protocol = self.getText(node.getElementsByTagName('protocol')[0].childNodes)
                    b.host = self.getText(node.getElementsByTagName('host')[0].childNodes)
                    b.port = self.getText(node.getElementsByTagName('port')[0].childNodes)
                    b.user = self.getText(node.getElementsByTagName('user')[0].childNodes)
                    
                    # TODO: GnomeKeyring
                    b.pwd_store = node.getElementsByTagName('password')[0].getAttribute('store')
                    b.pwd_keyid = node.getElementsByTagName('password')[0].getAttribute('keyid')
                    b.password = self.getText(node.getElementsByTagName('password')[0].childNodes)
                    
                    x = self.getText(node.getElementsByTagName('showhidden')[0].childNodes)
                    b.showhidden = {"true":True,"false":False}.get(x.lower()) 
                    b.encryptdata = self.getText(node.getElementsByTagName('encryptdata')[0].childNodes)
                    b.charset = self.getText(node.getElementsByTagName('charset')[0].childNodes)
                    b.remotepath = self.getText(node.getElementsByTagName('remotepath')[0].childNodes)
                    b.localpath = self.getText(node.getElementsByTagName('localpath')[0].childNodes)
                    folder.items.append(b)
                if node.tagName == 'folder':
                    f = BookmarkFolder()
                    f.name = node.getAttribute('name')
                    folder.items.append(f)
                    self.traversexml(node, f)
    
    def getText(self, nodelist):
        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return ''.join(rc)
