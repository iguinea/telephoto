# TelePhoto

Bot de telegram que imprimirá las fotografías que se lancen e un canal de telegram

## Configuratión de Telegram
Tenemos que pedir un TOKEN para acceder a Telegram, para ellos hablaremos con el @Botfather

## Configuración de TelePicture

Tenemos que 


## Instalación de CUPS

Instalamos el servidor de impresión CUPS

```bash
$ apt update
$ apt install -y cups
```

Podemos levantar el servicio
```bash
$ systemctl enable cups.service
$ systemctl start cups.service
```
## Configuración de Canon Selphy CP1200 y CUPS

Averiguar la IP de Canon Selphy CP1200 --> Se puede hacer desde el panel de control de la impresora


### Instalación de Canon Selphy CP1200

Acceder al panel de control de CUPS: http://ip-cups:631/
* Administration --> Add Printer
* Other Network Printers: Internet Printing Protocol (ipp)
* Connection: ipp://[CANON_PRINTER_IP]/ipp/print   ex: ipp://192.168.1.136/ipp/print
* Name: Canon
* Or Provide a PPD File: Canon_Selphy_CP1200/Canon_SELPHY_CP1300.ppd
* Add Printer
* Set Printer Options: Por defecto como viene ...

Lo que nos tiene que quedar!
- Driver:	Canon SELPHY CP1300 HTTP-AirPrint (color)
- Connection:	ipp://192.168.1.136/ipp/print
- Defaults:	job-sheets=none, none media=jpn_hagaki_100x148mm sides=one-sided


```bash
root@b3d93782b833:/workspaces/telephoto# lpoptions -p Canon -l
ColorModel/Color Mode: Gray *RGB
cupsPrintQuality/Quality: *Normal
PageSize/Media Size: 54x86mm 54x86mm.Fullbleed 89x119mm 89x119mm.Fullbleed *Postcard Postcard.Fullbleed Custom.WIDTHxHEIGHT
MediaType/MediaType: *photographic any
root@b3d93782b833:/workspaces/telephoto# 
```


## Access development environment

python3 -m venv telephoto
source telephoto/bin/activate



## GUTENPRINT 5.3

Hay problemas con las impresoras selphy y el gutenprint 5.4, por lo qu tendremos que descargarnos la versión 5.3 y compilarla.

Antes hay que instalar las cabeceras de libusb-1.0-dev




# Links

https://github.com/abelits/canon-selphy-print


https://www.techradar.com/how-to/computing/how-to-turn-the-raspberry-pi-into-a-wireless-printer-server-1312717

https://github.com/reuterbal/photobooth/issues/40

Mucha info de comandos lp
https://github.com/pibooth/pibooth/issues/268


https://github.com/python-telegram-bot/python-telegram-bot

Canon Selphy CP1200 Web Page
http://192.168.1.136:8008/lpadm