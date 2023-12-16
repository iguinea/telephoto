import logging
import requests
import cups
import os
import yaml

from time import sleep
from PIL import Image

from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler



# Reemplaza 'TOKEN' con el token de tu bot de Telegram
#TOKEN = '6706683235:AAEEm67phupYfOYOGNOP55zanSvKySmdJcw'
#CHANNEL_ID = '-100YYYYYYYYYYYYY'  # Reemplaza 'Y' con el id de tu canal

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def print_job_details(job_id):
    conn = cups.Connection()
    job_attributes = conn.getJobAttributes(job_id)

    for attribute, value in job_attributes.items():
        print(f"{attribute}: {value}")
        
async def print_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    
    im=Image.open(filename)
    im.resize((1200,1800))                  # resize image to 1200*1800
    im.save(filename+"resized.jpg","JPEG")  # save image to file
    
    print_id = conn.printFile(printer_name, filename+"resized.jpg", "Python Print Job", {})
    #while conn.getJobs().get(print_id, None):
    #    sleep(1)
    
    # delete files
    os.remove(filename)
    os.remove(filename+"resized.jpg")

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
    #print("Photo URL:", photo_file.file_path)
    print(photo_file)
    download_file(photo_file.file_path,'photo.jpg') 
    print_file('photo.jpg')
    
    
#async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def load_config(ruta_archivo):
    try:
        # Cargar el contenido del archivo YAML
        with open(ruta_archivo, 'r') as archivo:
            configuracion = yaml.safe_load(archivo)
        return configuracion
    except FileNotFoundError:
        print(f"Error: El archivo {ruta_archivo} no fue encontrado.")
        return None
    except yaml.YAMLError as e:
        print(f"Error al cargar el archivo YAML: {e}")
        return None
    
    
archivo_configuracion = 'config.yaml'
config = {}

if __name__ == '__main__':
    
    config = load_config(archivo_configuracion)
    print (config)

    application = ApplicationBuilder().token(config['TOKEN']).build()
   
    #echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    #application.add_handler(echo_handler)

    #start_handler = CommandHandler('start', start)
    #application.add_handler(start_handler)
     
    print_stats_handler = CommandHandler('stats', print_stats)
    application.add_handler(print_stats_handler)
    
    photo_handler = MessageHandler(filters.PHOTO, handle_photo)
    application.add_handler(photo_handler)


    application.run_polling()
    
    
    