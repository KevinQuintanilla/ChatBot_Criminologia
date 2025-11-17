import os
import logging
from telegram.ext import Application
from dotenv import load_dotenv

# Importamos el "cerebro" desde nuestro handler
from handlers.menu_principal import get_main_conv_handler

# Configura un log básico para ver errores en la terminal
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Cargar las variables de entorno (buscará el .env)
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

if not TOKEN:
    raise ValueError("No se encontró el BOT_TOKEN. Revisa tu archivo .env")

def main():
    print("Iniciando bot...")
    app = Application.builder().token(TOKEN).build()
    main_handler = get_main_conv_handler()
    app.add_handler(main_handler)
    print("Bot iniciado y escuchando...")
    app.run_polling()

if __name__ == '__main__':
    main()