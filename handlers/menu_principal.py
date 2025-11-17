import logging
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    filters, 
    ContextTypes, 
    ConversationHandler
)

# Importamos los teclados y estados 
from keyboards import main_menu_keyboard, back_keyboard, MENU, CONSULTAS, AYUDA, CONTACTO

# Importamos las funciones "placeholder"
from .consultas import start_consultas
from .ayuda import start_ayuda
from .contacto import start_contacto

# --- Funciones del Menú ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Comando /start. Muestra bienvenida y menú principal."""
    user = update.effective_user
    welcome_message = (
        f"¡Hola, {user.first_name}\n\n"
        "Soy el bot de asistencia para el sistema de información de pandillas.\n\n"
        "Selecciona una opción del menú para comenzar."
    )
    
    await update.message.reply_text(welcome_message, reply_markup=main_menu_keyboard())
    
    return MENU

async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Maneja la selección del usuario en el menú principal."""
    text = update.message.text
    
    if "consultas" in text.lower():
        return await start_consultas(update, context)
        
    elif "preguntas frecuentes" in text.lower():
        return await start_ayuda(update, context)

    elif "contacto" in text.lower():
        return await start_contacto(update, context)
        
    else:
        await update.message.reply_text("Opción no reconocida, por favor usa los botones.", reply_markup=main_menu_keyboard())
        return MENU

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancela y termina la conversación."""
    await update.message.reply_text(
        "Operación cancelada. ¡Hasta luego!", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

# --- Creamos el ConversationHandler ---

def get_main_conv_handler() -> ConversationHandler:
    """
    Crea el manejador de conversación principal con todos los estados.
    """
    back_to_menu_handler = MessageHandler(filters.Regex(r'(?i)menú|volver|atrás'), start)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MENU: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu)
            ],
            
            CONSULTAS: [
                MessageHandler(filters.Regex(r'(?i)menú|volver|atrás'), start)
            ],
            AYUDA: [
                MessageHandler(filters.Regex(r'(?i)menú|volver|atrás'), start)
            ],
            CONTACTO: [
                MessageHandler(filters.Regex(r'(?i)menú|volver|atrás'), start)
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    return conv_handler