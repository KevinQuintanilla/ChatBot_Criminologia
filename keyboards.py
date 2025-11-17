from telegram import ReplyKeyboardMarkup

# --- Estados para la conversación ---
(
    MENU, 
    CONSULTAS, 
    AYUDA,
    CONTACTO
) = range(4)


def main_menu_keyboard():
    """Crea el teclado del menú principal"""
    
    keyboard = [
        ["🔍 Consultas"],
        ["❓ Ayuda (Preguntas Frecuentes)"],
        ["📧 Contacto / Solicitar Ayuda"]
    ]
    
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

def back_keyboard():
    """Crea un teclado para volver al menú"""
    keyboard = [["🔙 Menú Principal"]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)