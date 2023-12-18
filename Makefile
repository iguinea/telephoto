
all:

	@echo "make install"
	@echo "make run"
activate:
	. venv/bin/activate
deactivate:
	deactivate

install:

	pip3 install requests
	pip3 install pycups
	pip3 install pyyaml
	pip3 install Pillow
	pip3 install ipaddress
	pip3 install python-telegram-bot --upgrade
	pip3 install -r requirements.txt

run: 
	 python3 main.py

freeze:
	pip freeze > requirements.txt