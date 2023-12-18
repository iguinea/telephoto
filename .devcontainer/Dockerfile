FROM ubuntu:20.04
RUN apt-get update 
RUN ln -fs /usr/share/zoneinfo/Europe/Madrid /etc/localtime
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata
RUN dpkg-reconfigure --frontend noninteractive tzdata
RUN apt-get install -y python3.9 python3.9-dev pip git python3-cups cups curl python3.9-venv libcups2-dev
RUN pip3 install --upgrade pip
RUN echo "root:root" | chpasswd


RUN mkdir -p /opt/telePhoto/resources
RUN mkdir -p /opt/telePhoto/temp
COPY Canon_Selphy_CP1200/Generic_Gray_Gamma_2.2_Profile.icc /opt/telePhoto/resources/
COPY Canon_Selphy_CP1200/sRGB_Profile.icc /opt/telePhoto/resources/