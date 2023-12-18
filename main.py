import logging
import requests
import cups
import os
import yaml
import ipaddress
import subprocess

from time import sleep
from PIL import Image
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def print_job_details(job_id):
    conn = cups.Connection()
    job_attributes = conn.getJobAttributes(job_id)

    for attribute, value in job_attributes.items():
        print(f"{attribute}: {value}")
        
async def handle_print_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = cups.Connection()
    printers = conn.getPrinters()

    for printer in printers:
        print(printer)
        print(printers[printer])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=printer)

        
    for job in conn.getJobs(which_jobs='all'):
        print(job)
        print_job_details(job)
        #print(conn.getJobs(which_jobs='all')[jobs])
        completed_jobs = conn.getJobs(which_jobs='all')
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Completed Jobs: "+str(len(completed_jobs)))
    
def print_file(filename):
    conn = cups.Connection()
    printers = conn.getPrinters()

    #for printer in printers:
    #
    #    print(printer)
    #    print(printers[printer])

    printer_name = list(printers.keys())[0]  # Usa el primer impresor disponible
    print(printer_name)
    
    #im=Image.open(filename)
    #im.resize((1200,1800))                  # resize image to 1200*1800
    #im.save(filename+"resized.jpg","JPEG")  # save image to file
    
    #print_id = conn.printFile(printer_name, filename+"resized.jpg", "Python Print Job", {})
    print_id = conn.printFile(printer_name, filename, "Python Print Job", {})
    return print_id
    #while conn.getJobs().get(print_id, None):
    #    sleep(1)
    
    # delete files
    #os.remove(filename)
    #os.remove(filename+"resized.jpg")

def download_file(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
    else:
        print("Failed to download file, status code:", response.status_code)


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_file = await context.bot.get_file(update.message.photo[-1].file_id)
    cutom_name = '/opt/telePhoto/temp/'+str(update.message.from_user.id)+"_"+str(update.message.message_id)+'.jpg'
    cutom_resized_name = '/opt/telePhoto/temp/'+str(update.message.from_user.id)+"_"+str(update.message.message_id)+'_resized.jpg'
    # Descargar la imagen
    download_file(photo_file.file_path,cutom_name) 

    # resize the image
    im=Image.open(cutom_name)
    im.resize((1200,1800))                  # resize image to 1200*1800
    im.save(cutom_resized_name,"JPEG")  # save image to file
    os.Remove(cutom_name)
    
    #print_id = print_file(cutom_resized_name)
    conn = cups.Connection()
    print_id = conn.printFile(config['PRINTER_NAME'], cutom_resized_name, "Python Print Job", {})
    
    await context.bot.deleteMessage (message_id = update.message.message_id, chat_id = update.message.chat_id)
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{print_id}")
    os.Remove(cutom_resized_name)

    
#async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
async def handle_configure(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Comprueba si se ha proporcionado algún argumento
    if context.args:
        ip_str = context.args[0]
        # borramos la impresora
        if ip_str=="delete":
            command = f"lpadmin -x {config['PRINTER_NAME']}"
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output, error = process.communicate()
            if process.returncode != 0:
                print(f"Hubo un error: {error.decode('utf-8')}")
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Error al borrar la impresora:  {error.decode('utf-8')}")
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Impresora borrada: {output.decode('utf-8')}")
            return
        # pasamos a configurar la impresora
        try:
            
            ip = ipaddress.ip_address(ip_str)   # Intenta convertir el argumento en una dirección IP
            context.user_data['ip'] = ip        # Almacena la dirección IP para su uso posterior
            
            # comando para configurar la dirección IP en CUPS como nueva impresora
            command = f"lpadmin -p {config['PRINTER_NAME']} -v ipp://{ip}/ipp/print -E -L {config['PRINTER_LOCATION']} -D {config['PRINTER_DESCRIPTION']} -i Canon_Selphy_CP1200/Canon_SELPHY_CP1300.ppd"
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output, error = process.communicate()
            if process.returncode != 0:
                print(f"Hubo un error: {error.decode('utf-8')}")
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Error al configurar la impresora: {output.decode('utf-8')}")
                return
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Impresora configurada: {output.decode('utf-8')}")
            
            # comando para establecer la impresora por defecto    
            command = f"lpoptions -d {config['PRINTER_NAME']}"
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output, error = process.communicate()
            if process.returncode != 0:
                print(f"Hubo un error: {error.decode('utf-8')}")
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Error al configurar la impresora por defecto: {output.decode('utf-8')}")
                return
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Impresora por defecto configurada: {output.decode('utf-8')}")
                
            # Envía un mensaje de confirmación
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"IP configurada a {ip}")
            return
           
            
        except ValueError:
            # Si el argumento no es una dirección IP válida, envía un mensaje de error
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{ip_str} no es una dirección IP válida.")
            return
    else:
        # Envía un mensaje de error
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Por favor, proporciona una dirección IP o el comando delete")
   
        
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #print(update)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def load_config(ruta_archivo):
    try:
        with open(ruta_archivo, 'r') as archivo: # Cargar el contenido del archivo YAML
            configuracion = yaml.safe_load(archivo)
        return configuracion
    except FileNotFoundError:
        print(f"Error: El archivo {ruta_archivo} no fue encontrado.")
        return None
    except yaml.YAMLError as e:
        print(f"Error al cargar el archivo YAML: {e}")
        return None
    
    
archivo_configuracion = '/opt/telePhoto/config.yaml'
config = {}

if __name__ == '__main__':
    
    config = load_config(archivo_configuracion)
    #print (config)

    application = ApplicationBuilder().token(config['TOKEN']).build()
   
    #echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    #application.add_handler(echo_handler)

    #start_handler = CommandHandler('start', start)
    #application.add_handler(start_handler)
     
    configure_handler = CommandHandler('config', handle_configure)
    application.add_handler(configure_handler)
    
    print_stats_handler = CommandHandler('stats', handle_print_stats)
    application.add_handler(print_stats_handler)
    
    photo_handler = MessageHandler(filters.PHOTO, handle_photo)
    application.add_handler(photo_handler)

    application.run_polling()
