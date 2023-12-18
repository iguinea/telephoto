
all:

	@echo "make install_dependencies"
	@echo "make run"

install_dependencies:
	pip3 install requests
	pip3 install pycups
	pip3 install pyyaml
	pip3 install Pillow
	pip3 install ipaddress
	pip3 install python-telegram-bot --upgrade

run: 
	 python3 main.py


run_pi: 
	. .venv/bin/activate
	python3 main.py

install_pi:
	sudo mkdir -p /opt/telePhoto/tmp /opt/telePhoto/temp /opt/telePhoto/resources
	sudo chmod -R 777 /opt/telePhoto
	cp Canon_Selphy_CP1200/Generic_Gray_Gamma_2.2_Profile.icc /opt/telePhoto/resources
	cp Canon_Selphy_CP1200/sRGB_Profile.icc /opt/telePhoto/resources
	cp Canon_Selphy_CP1200/Canon_SELPHY_CP1200_custom.ppd /opt/telePhoto/resources

	
#	sudo apt install -y python3-full python3-venv libcups2-dev imagemagick python3-pip
	sudo apt install -y              python3-venv libcups2-dev imagemagick python3-pip
	python3 -m venv .venv
	. .venv/bin/activate
	make install_dependencies
	
	@echo "Please, execute ./addConfig.sh to configure TOKEN and Channel ID"

install_pi_service: 
	sudo cp resources/telephoto.service /etc/systemd/system
	sudo systemctl enable telephoto.service
	sudo systemctl start telephoto.service
	