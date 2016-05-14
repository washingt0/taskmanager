#!/usr/bin/python
import os, sys, signal, gtk, psutil, time


class Manager:
	def getProcess(self):
		uso_CPU = psutil.cpu_percent(percpu=True)
		return uso_CPU

	def getMemory(self):
		uso_MEM = psutil.virtual_memory()
		return usoMEM


class mainWindow:
	def __init__(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_title("Fodendo Gerenciador")
		self.window.set_size_request(500, 500)
		self.window.set_position(gtk.WIN_POS_CENTER)
		self.window.box = VBox()
		self.window.show()
		self.window.connect("destroy", self.destroy)


	def main(self):
		gtk.main()


	def destroy(self, widget):
		gtk.main_quit()


if __name__ == "__main__":
	window = mainWindow()
	window.main()
