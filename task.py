#!/usr/bin/python
import gtk, psutil, gobject, datetime, os


class mainWindow:
    def __init__(self):
        self.processos = {}
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
        self.store = gtk.ListStore(str, str, int, str, float, str, str, int)
        for i in psutil.pids():
            self.processos[i] = psutil.Process(i)

        for i, j in self.processos.iteritems():
            if i in psutil.pids():
                self.store.append([j.name(), j.username(), i, (str(int(j.cpu_percent()))+"%"), round(j.memory_percent(), 3),
                                   self.get_time(j.create_time()), j.status(), j.nice()])
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
        column.set_sort_order(gtk.SORT_DESCENDING)
        self.tree.append_column(column)
        column = gtk.TreeViewColumn("Memoria", renderer, text=4)
        column.set_sort_column_id(4)
        self.tree.append_column(column)
        column = gtk.TreeViewColumn("Tempo", renderer, text=5)
        column.set_sort_column_id(5)
        self.tree.append_column(column)
        column = gtk.TreeViewColumn("Status", renderer, text=6)
        column.set_sort_column_id(6)
        self.tree.append_column(column)
        column = gtk.TreeViewColumn("Nice", renderer, text=7)
        column.set_sort_column_id(7)
        self.matar_processo = gtk.Button("Finalizar")
        self.matar_processo.connect("clicked", self.killproc)
        self.parar_processo = gtk.Button("Parar")
        self.parar_processo.connect("clicked", self.stopproc)
        self.continuar_proc = gtk.Button("Continuar")
        self.continuar_proc.connect("clicked", self.contproc)
        self.nice_more = gtk.Button("Aumentar Prioridade")
        self.nice_more.connect("clicked", self.nicemore)
        self.nice_less = gtk.Button("Diminuir Prioridade")
        self.nice_less.connect("clicked", self.niceless)
        self.fix = gtk.Fixed()
        self.fix.put(self.matar_processo, 10, 10)
        self.fix.put(self.parar_processo, 90, 10)
        self.fix.put(self.continuar_proc, 150, 10)
        self.fix.put(self.nice_more, 250, 10)
        self.fix.put(self.nice_less, 420, 10)
        self.window.vbox.pack_start(self.fix)
        self.selected = self.tree.get_selection()
        self.selected.set_mode(gtk.SELECTION_SINGLE)
        self.tree.append_column(column)
        self.tree.show()
        self.scrolled_window.add(self.tree)
        self.window.show_all()
        self.window.connect("destroy", self.destroy)
        gobject.timeout_add(1000, self.get_info)

    def get_time(self, time):
        c = datetime.datetime.now() - datetime.datetime.fromtimestamp(time)
        a = divmod(c.total_seconds(), 60)
        h = 0
        if a[0] > 60:
            h = int(a[0] / 60)
            m = a[0] - (h * 60)
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
        for i in psutil.pids():
            if i not in self.processos:
                self.processos[i] = psutil.Process(i)
                self.store.append([self.processos[i].name(), self.processos[i].username(), i,
                                   (str(int(self.processos[i].cpu_percent()))+"%"),
                                   (self.processos[i].memory_percent(), 3),
                                   self.get_time(self.processos[i].create_time()), self.processos[i].status(),
                                   self.processos[i].nice()])
        z = self.store.get_iter_first()
        while z is not None:
            if self.store.get_value(z, 2) in psutil.pids():
                if self.store.get_value(z, 2) in self.processos:
                    j = self.processos[self.store.get_value(z, 2)]
                    self.store.set_value(z, 3, (str(int(j.cpu_percent()))+"%"))
                    self.store.set_value(z, 4, round(j.memory_percent(), 3))
                    self.store.set_value(z, 5, self.get_time(j.create_time()))
                    self.store.set_value(z, 6, j.status())
                    self.store.set_value(z, 7, j.nice())
                else:
                    self.store.remove(z)
            else:
                del self.processos[self.store.get_value(z, 2)]
                self.store.remove(z)
            z = self.store.iter_next(z)
        return True

    def killproc(self, widget):
        select = self.selected.get_selected()
        proc = psutil.Process(self.store.get_value(select[1], 2))
        proc.terminate()
        return True

    def stopproc(self, widget):
        select = self.selected.get_selected()
        proc = psutil.Process(self.store.get_value(select[1], 2))
        proc.suspend()
        return True

    def contproc(self, widget):
        select = self.selected.get_selected()
        proc = psutil.Process(self.store.get_value(select[1], 2))
        proc.resume()
        return True

    def nicemore(self, widget):
        select = self.selected.get_selected()
        proc = psutil.Process(self.store.get_value(select[1], 2))
        this = psutil.Process(os.getpid())
        if this.username() != 'root':
            d = gtk.Dialog()
            label = gtk.Label('Apenas super usuario pode executar essa acao')
            label.show()
            d.vbox.pack_start(label)
            d.run()
        else:
            proc.nice(proc.nice() - 1)
        return True

    def niceless(self, widget):
        select = self.selected.get_selected()
        proc = psutil.Process(self.store.get_value(select[1], 2))
        proc.resume()
        proc.nice(proc.nice() + 1)
        return True


if __name__ == "__main__":
    window = mainWindow()
    window.main()
