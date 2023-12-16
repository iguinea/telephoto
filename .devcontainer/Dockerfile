FROM ubuntu:20.04
RUN apt-get update 
RUN ln -fs /usr/share/zoneinfo/Europe/Madrid /etc/localtime
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata
RUN dpkg-reconfigure --frontend noninteractive tzdata
RUN apt-get install -y python3.9 python3.9-dev pip git python3-cups cups curl
RUN pip3 install --upgrade pip

RUN echo "root:root" | chpasswd 