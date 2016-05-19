#!/usr/bin/python
import gtk
import psutil
import gobject
import datetime
import os


class mainWindow:
    def __init__(self):
        # cria um mapa para armazenar os processos
        self.processos = {}
        # instancia a Janela do gerenciador e define o titulo, tamanho, posicao e nao permite redimensionamento
        self.window = gtk.Dialog()
        self.window.set_title("Fodendo Gerenciador")
        self.window.set_size_request(950, 600)
        self.window.set_resizable(False)
        self.window.set_position(gtk.WIN_POS_CENTER)
        # instancia uma subjanela com scroll e define tamanho, borda e politicas
        self.scrolled_window = gtk.ScrolledWindow()
        self.scrolled_window.set_size_request(750, 500)
        self.scrolled_window.set_border_width(10)
        self.scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        # cria um box na janela e adiciona a subjanela com scroll
        self.window.vbox.pack_start(self.scrolled_window, True, True, 0)
        self.scrolled_window.show()
        # cria a lista que vai ser exibida e define os tipos dos campos
        self.store = gtk.ListStore(str, str, int, str, str, str, str, str)
        # preenche a lista com as informacoes do processos atuais
        for i in psutil.pids():
            self.processos[i] = psutil.Process(i)
        for i, j in self.processos.iteritems():
            if i in psutil.pids():
                self.store.append([j.name(), j.username(), i, (str(int(j.cpu_percent()))+"%"),
                                   self.form_ram(j.memory_percent()), self.get_time(j.create_time()), j.status(),
                                   j.nice()])
        # cria a arvore de visualizacao e define o modelo como sendo a lista criada
        self.tree = gtk.TreeView(self.store)
        self.tree.set_model(self.store)
        # instancia renderador
        renderer = gtk.CellRendererText()
        # cria as colunas
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
        self.tree.append_column(column)
        # instancia botoes e os conecta a suas funcoes
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
        self.new_proc = gtk.Button("Novo Processo")
        self.new_proc.connect("clicked", self.newproc)
        # instancia os buffers para os campos de texto
        self.tusocpu = gtk.TextBuffer()
        self.tusorma = gtk.TextBuffer()
        self.tusoswp = gtk.TextBuffer()
        # configura o texto a ser exibido
        self.tusocpu.set_text("CPU: ")
        self.tusorma.set_text("RAM: ")
        self.tusoswp.set_text("SWAP: ")
        # adiciona o texto ao campo e define o campo como nao editavel
        self.uso_cpu = gtk.TextView()
        self.uso_cpu.set_editable(False)
        self.uso_cpu.set_buffer(self.tusocpu)
        self.uso_ram = gtk.TextView()
        self.uso_ram.set_editable(False)
        self.uso_ram.set_buffer(self.tusorma)
        self.uso_swp = gtk.TextView()
        self.uso_swp.set_editable(False)
        self.uso_swp.set_buffer(self.tusoswp)
        # instancia container
        self.fix = gtk.Fixed()
        # adiciona botoes e textos no container que foi instanciado
        self.fix.put(self.matar_processo, 10, 15)
        self.fix.put(self.parar_processo, 90, 15)
        self.fix.put(self.continuar_proc, 150, 15)
        self.fix.put(self.nice_more, 250, 15)
        self.fix.put(self.nice_less, 420, 15)
        self.fix.put(self.uso_cpu, 600, 20)
        self.fix.put(self.uso_ram, 690, 20)
        self.fix.put(self.uso_swp, 780, 20)
        self.fix.put(self.new_proc, 400, 50)
        # adiciona o container na janela
        self.window.vbox.pack_start(self.fix)
        # instancia o seletor e define selecao unica
        self.selected = self.tree.get_selection()
        self.selected.set_mode(gtk.SELECTION_SINGLE)
        # configura a arvore como visivel
        self.tree.show()
        # adiciona a arvore na janela com scroll
        self.scrolled_window.add(self.tree)
        self.window.show_all()
        self.window.connect("destroy", self.destroy)
        # define timeout para atualizar a lista
        gobject.timeout_add(1000, self.get_info)

    # metodo para formatar o tempo de execucao do processo
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

    # metodo que formata o uso de RAM
    def form_ram(self, uso):
        uso = round(uso, 2)
        ram = str(uso).split('.')
        return "{},{}%".format(int(ram[0]), int(ram[1]))

    # metodo que inicia a GUI
    def main(self):
        gtk.main()

    # metodo que destroi a GUI
    def destroy(self, widget):
        gtk.main_quit()

    # metodo que faz a atualizacao dos dados
    def get_info(self):
        # obtem e atualiza os valores de uso geral
        swp = psutil.swap_memory()
        ram = psutil.virtual_memory()
        self.tusocpu.set_text("CPU: {}%".format(str(psutil.cpu_percent(percpu=False))))
        self.tusorma.set_text("RAM: {}%".format(str(ram[2])))
        self.tusoswp.set_text("SWAP: {}%".format(str(swp[3])))
        # verifica se ha um novo processo e adiciona no mapa
        for i in psutil.pids():
            if i not in self.processos:
                self.processos[i] = psutil.Process(i)
                self.store.append([self.processos[i].name(), self.processos[i].username(), i,
                                   (str(int(self.processos[i].cpu_percent()))+"%"),
                                   self.form_ram(self.processos[i].memory_percent()),
                                   self.get_time(self.processos[i].create_time()), self.processos[i].status(),
                                   self.processos[i].nice()])
        # obtem iterador para primeiro elemento da lista
        z = self.store.get_iter_first()
        # verifica ate o final da lista
        while z is not None:
            # se o processo da lista ainda esta em execucao
            if self.store.get_value(z, 2) in psutil.pids():
                # se o processo esta no mapa
                if self.store.get_value(z, 2) in self.processos:
                    j = self.processos[self.store.get_value(z, 2)]
                    self.store.set_value(z, 3, (str(int(j.cpu_percent()))+"%"))
                    self.store.set_value(z, 4, self.form_ram(j.memory_percent()))
                    self.store.set_value(z, 5, self.get_time(j.create_time()))
                    self.store.set_value(z, 6, j.status())
                    self.store.set_value(z, 7, j.nice())
                else:
                    self.store.remove(z)
            # se o processo nao estiver em execucao e removido do mapa e da lista
            else:
                del self.processos[self.store.get_value(z, 2)]
                self.store.remove(z)
            # obtem iterador para o proximo registro
            z = self.store.iter_next(z)
        return True

    # metodo que mata um processo
    def killproc(self, widget):
        select = self.selected.get_selected()
        proc = psutil.Process(self.store.get_value(select[1], 2))
        proc.terminate()
        return True

    # metodo que para um processo
    def stopproc(self, widget):
        select = self.selected.get_selected()
        proc = psutil.Process(self.store.get_value(select[1], 2))
        proc.suspend()
        return True

    # metodo que continua um processo
    def contproc(self, widget):
        select = self.selected.get_selected()
        proc = psutil.Process(self.store.get_value(select[1], 2))
        proc.resume()
        return True

    # metodo que aumenta a prioridade do processo
    def nicemore(self, widget):
        select = self.selected.get_selected()
        proc = psutil.Process(self.store.get_value(select[1], 2))
        this = psutil.Process(os.getpid())
        if this.username() != 'root':
            d = gtk.Dialog()
            label = gtk.Label('Apenas super usuario pode executar essa acao!')
            label.show()
            d.set_title("Alerta")
            d.set_size_request(350, 50)
            d.set_resizable(False)
            d.vbox.pack_start(label)
            d.run()
        else:
            proc.nice(proc.nice() - 1)
        return True

    # metodo que diminui a prioridade do processo
    def niceless(self, widget):
        select = self.selected.get_selected()
        proc = psutil.Process(self.store.get_value(select[1], 2))
        proc.resume()
        proc.nice(proc.nice() + 1)
        return True

    # metodo que abre a GUI para criar novo processo
    def newproc(self, widget):
        win = gtk.Dialog()
        win.set_title("Novo Processo")
        win.set_size_request(300, 150)
        win.set_resizable(False)
        fix = gtk.Fixed()
        self.comando = gtk.Entry()
        self.nice = gtk.Entry()
        tcomando = gtk.TextBuffer()
        tcomando.set_text("Comando: ")
        tnice = gtk.TextBuffer()
        tnice.set_text("Prioridade: ")
        textc = gtk.TextView()
        textc.set_editable(False)
        textn = gtk.TextView()
        textn.set_editable(False)
        textc.set_buffer(tcomando)
        textn.set_buffer(tnice)
        create = gtk.Button("Criar")
        create.connect("clicked", self.createproc)
        fix.put(textc, 30, 25)
        fix.put(textn, 30, 65)
        fix.put(self.comando, 120, 20)
        fix.put(self.nice, 120, 60)
        fix.put(create, 120, 100)
        win.vbox.pack_start(fix)
        win.show_all()

    # metodo que cria novo processo
    def createproc(self, widget):
        comando = self.comando.get_text()
        nice = self.comando.get_text()
        arg = [str("nice -n {}".format(str(nice)))]
        if os.fork() == 0:
            os.execvp(comando, arg)
            exit()

if __name__ == "__main__":
    window = mainWindow()
    window.main()