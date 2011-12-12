from gi.repository import Gtk


class ProtocolComboBox(Gtk.ComboBox):
    def __init__(self):
        super(ProtocolComboBox, self).__init__()

        cr_text = Gtk.CellRendererText()
        self.pack_start(cr_text, False)
        self.add_attribute(cr_text, "text", 1)

    def set_value(self, value):
        if self.props.model == None or value == None or value == -1:
            self.reset()

        myiter = self.props.model.get_iter_first()
        v = self.props.model.get_value(myiter, 0)
        if v == value:
                self.set_active_iter(myiter)
                return

        found = False
        while not found:
            myiter = self.props.model.iter_next(myiter)
            if iter == None:
                break
            v = self.props.model.get_value(myiter, 0)
            if v == value:
                self.set_active_iter(myiter)
                found = True
                break

        if not found:
            self.reset()

    def get_value(self):
        myiter = self.get_active_iter()
        value = self.props.model.get_value(myiter, 0)
        if value == -1:
            return None
        return value
