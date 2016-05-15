#!/usr/bin/python
import gtk, psutil, gobject, datetime


class mainWindow:
    def __init__(self):
        self.window = gtk.Dialog()
        self.window.set_title("Fodendo Gerenciador")
        self.window.set_size_request(950, 600)
        self.window.set_resizable(False)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.scrolled_window = gtk.ScrolledWindow()
        self.scrolled_window.set_size_request(750, 500)
        self.scrolled_window.set_border_width(10)
        self.scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        self.window.vbox.pack_start(self.scrolled_window, True, True, 0)
        self.scrolled_window.show()
        self.store = gtk.ListStore(str, str, int, str, str, str, int)
        self.get_info()
        self.tree = gtk.TreeView(self.store)
        self.tree.set_model(self.store)
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Nome do Processo", renderer, text=0)
        column.set_sort_column_id(0)
        self.tree.append_column(column)
        column = gtk.TreeViewColumn("Usuario", renderer, text=1)
        column.set_sort_column_id(1)
        self.tree.append_column(column)
        column = gtk.TreeViewColumn("PID", renderer, text=2)
        column.set_sort_column_id(2)
        self.tree.append_column(column)
        column = gtk.TreeViewColumn("CPU", renderer, text=3)
        column.set_sort_column_id(3)
        self.tree.append_column(column)
        column = gtk.TreeViewColumn("Tempo", renderer, text=4)
        column.set_sort_column_id(4)
        self.tree.append_column(column)
        column = gtk.TreeViewColumn("Status", renderer, text=5)
        column.set_sort_column_id(5)
        self.tree.append_column(column)
        column = gtk.TreeViewColumn("Nice", renderer, text=6)
        column.set_sort_column_id(6)
        self.tree.append_column(column)
        self.tree.show()
        self.scrolled_window.add(self.tree)
        self.window.show()
        self.window.connect("destroy", self.destroy)
        gobject.timeout_add(1000, self.get_info)

    def get_time(self, time):
        c = datetime.datetime.now() - datetime.datetime.fromtimestamp(time)
        a = divmod(c.total_seconds(), 60)
        h = 0
        m = 0
        s = 0
        if a[0] > 60:
            h = int(a[0]/60)
            m = a[0] - (h*60)
            s = a[1]
        else:
            m = a[0]
            s = a[1]
        b = "{}:{}:{}".format(str(h).zfill(2), str(int(m)).zfill(2), str(int(s)).zfill(2))
        return b

    def main(self):
        gtk.main()

    def destroy(self, widget):
        gtk.main_quit()

    def get_info(self):
        self.store.clear()
        for i in psutil.pids():
            if i in psutil.pids():
                processo = psutil.Process(i)
                self.store.append([processo.name(), processo.username(), i, processo.cpu_percent(),
                                   self.get_time(processo.create_time()), processo.status(), processo.nice()])
        return True


if __name__ == "__main__":
    window = mainWindow()
    window.main()
