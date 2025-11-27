from telegram import Update
from telegram.ext import ContextTypes
from keyboards import ayuda_menu_keyboard, back_keyboard, AYUDA

async def start_ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Selecciona un tema sobre el cual necesites ayuda:",
        reply_markup=ayuda_menu_keyboard()
    )
    return AYUDA

async def ayuda_sobre_sistema(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
🧩 *Sobre el Sistema*
El sistema permite:
- Consultar pandillas por zona.
- Revisar peligrosidad.
- Buscar integrantes.
- Generar reportes.

Escribe 'menú' para volver.
"""
    await update.message.reply_text(text, reply_markup=back_keyboard())
    return AYUDA

async def ayuda_roles(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
👤 *Roles del Sistema*

• *Ciudadano:* Consulta básica sin login.
• *Capturista:* Puede registrar información, no modificar.
• *Administrador:* Control total del sistema.

Escribe 'menú' para volver.
"""
    await update.message.reply_text(text, reply_markup=back_keyboard())
    return AYUDA

async def ayuda_interfaz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
🖥️ *Uso de la Interfaz*

- Menú principal siempre visible
- Consultas por zona, delito o integrante
- Botones sencillos y navegación guiada

Escribe 'menú' para volver.
"""
    await update.message.reply_text(text, reply_markup=back_keyboard())
    return AYUDA

async def ayuda_pandillas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
📍 *Información de Pandillas*

Aquí puedes consultar:
- Dirección
- Peligrosidad
- Integrantes
- Actividades asociadas
- Rivalidades

Escribe 'menú' para volver.
"""
    await update.message.reply_text(text, reply_markup=back_keyboard())
    return AYUDA
