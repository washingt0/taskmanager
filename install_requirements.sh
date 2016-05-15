#!/bin/bash
echo "Require Python GTK2 and Python PSUtil"
read -p "Contine?[y/n]" var
if [[($var = 'Y') || ($var = 'y')]]; then
  	sudo apt-get install python-gtk2 python-psutil -y
  	./task.py
fi
