from telegram import Update
from telegram.ext import ContextTypes

# Importamos los teclados y estados
from keyboards import back_keyboard, main_menu_keyboard, MENU, AYUDA

async def start_ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Inicia el flujo de Ayuda (Preguntas Frecuentes)."""
    
    faq_text = """
--- MÓDULO DE AYUDA (FAQ) ---

Aquí puedes poner las preguntas frecuentes:

1. ¿Cómo busco una pandilla?
   - Ve a 🔍 Consultas > Buscar por Zona.

2. ¿Qué significa la peligrosidad Alta?
   - Significa que...

Escribe 'menú' para volver.
    """
    
    await update.message.reply_text(faq_text, reply_markup=back_keyboard())
    return AYUDA
