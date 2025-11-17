from telegram import Update
from telegram.ext import ContextTypes

# Importamos los teclados y el NUEVO estado
from keyboards import back_keyboard, CONTACTO

async def start_contacto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Inicia el flujo de Contacto."""
    
    await update.message.reply_text(
        "--- MÓDULO DE CONTACTO ---\n\n"
        "Aquí pondremos un formulario para enviar un email al administrador.\n\n"
        "Escribe 'menú' para volver.",
        reply_markup=back_keyboard()
    )
    
    return CONTACTO