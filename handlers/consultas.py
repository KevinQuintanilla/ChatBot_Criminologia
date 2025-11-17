from telegram import Update
from telegram.ext import ContextTypes

# Importamos los teclados y estados
from keyboards import back_keyboard, main_menu_keyboard, MENU, CONSULTAS

async def start_consultas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Inicia el flujo de consultas."""
    
    await update.message.reply_text(
        "--- MÓDULO DE CONSULTAS ---\n\n"
        "Aquí irán las opciones de búsqueda (por zona, peligrosidad, etc.).\n\n"
        "Escribe 'menú' para volver.",
        reply_markup=back_keyboard()
    )
    return CONSULTAS
