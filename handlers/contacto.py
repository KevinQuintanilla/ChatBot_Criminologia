from telegram import Update
from telegram.ext import ContextTypes
from keyboards import back_keyboard, main_menu_keyboard, CONTACTO, MENU
from .correo import send_email

async def start_contacto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "--- MÓDULO DE CONTACTO ---\n\n"
        "Escribe el mensaje que deseas enviar al administrador.\n"
        "Cuando termines, mándalo tal cual.\n\n"
        "Escribe 'menú' para volver.",
        reply_markup=back_keyboard()
    )
    return CONTACTO

async def recibir_mensaje_contacto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    texto = update.message.text

    
    if texto.lower() == "menú" or texto.lower() == "menu":
        await update.message.reply_text(
            "Volviendo al menú...", 
            reply_markup=main_menu_keyboard() 
        )
        return MENU 

    # ENVIAR CORREO
    enviado = send_email(
        asunto="Mensaje solicitando ayuda",
        cuerpo=f"Mensaje del usuario {update.effective_user.username}:\n\n{texto}"
    )

    if enviado:
        await update.message.reply_text(
            "Tu mensaje fue enviado con éxito.\n\nVolviendo al menú principal...",
            reply_markup=main_menu_keyboard() 
        )
    else:
        await update.message.reply_text(
            "Ocurrió un error al enviar el mensaje.\nIntenta más tarde.",
            reply_markup=main_menu_keyboard() 
        )

    return MENU 