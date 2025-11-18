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

# Importación de recursos locales
from keyboards import (
    main_menu_keyboard, 
    MENU, 
    CONSULTAS, 
    SUBMENU_DELITO, 
    SELECCION_CRITERIO, 
    AYUDA, 
    CONTACTO
)
from .consultas import (
    start_consultas, 
    handle_tipo_consulta, 
    handle_submenu_delito, 
    handle_criterio_seleccionado
)
from .ayuda import start_ayuda
from .contacto import start_contacto

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Manejador del comando /start.
    Inicia la conversación y muestra el menú principal.
    """
    user = update.effective_user
    welcome_message = (
        f"Hola, {user.first_name}.\n\n"
        "Soy el bot de asistencia para el sistema de informacion de pandillas.\n\n"
        "Selecciona una opcion del menu para comenzar."
    )
    
    await update.message.reply_text(welcome_message, reply_markup=main_menu_keyboard())
    return MENU

async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Procesa la opción seleccionada en el menú principal y redirige al módulo correspondiente.
    """
    text = update.message.text.lower()
    
    if "consultas" in text:
        return await start_consultas(update, context)
        
    elif "preguntas" in text:
        return await start_ayuda(update, context)

    elif "contacto" in text:
        return await start_contacto(update, context)
        
    else:
        await update.message.reply_text(
            "Opcion no reconocida, por favor usa los botones.", 
            reply_markup=main_menu_keyboard()
        )
        return MENU

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Finaliza la conversación actual y elimina el teclado.
    """
    await update.message.reply_text(
        "Operacion cancelada. Hasta luego.", 
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def get_main_conv_handler() -> ConversationHandler:
    """
    Configura y devuelve el ConversationHandler principal con todos los estados y transiciones.
    """
    # Filtro común para botones de regreso
    back_filter = filters.Regex(r'(?i)menú|volver|atrás|principal')
    back_handler = MessageHandler(back_filter, start)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MENU: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu)
            ],
            CONSULTAS: [
                back_handler,
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_tipo_consulta)
            ],
            SUBMENU_DELITO: [
                back_handler,
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_submenu_delito)
            ],
            SELECCION_CRITERIO: [
                back_handler,
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_criterio_seleccionado)
            ],
            AYUDA: [
                back_handler
            ],
            CONTACTO: [
                back_handler,
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    return conv_handler