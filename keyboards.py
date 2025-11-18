from telegram import ReplyKeyboardMarkup

# --- Definición de Estados de la Conversación ---
(
    MENU, 
    CONSULTAS,           
    SUBMENU_DELITO,      
    SELECCION_CRITERIO,  
    AYUDA,
    CONTACTO
) = range(6)

def main_menu_keyboard():
    """Genera el teclado del menú principal."""
    keyboard = [
        ["Consultas"],
        ["Ayuda (Preguntas Frecuentes)"],
        ["Contacto / Solicitar Ayuda"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

def back_keyboard():
    """Genera un botón simple para volver al menú principal."""
    keyboard = [["Volver al Menu Principal"]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# --- TECLADOS DEL MÓDULO DE CONSULTAS ---

def consultas_menu_keyboard():
    """Menú principal de tipos de búsquedas disponibles."""
    keyboard = [
        ["Reporte Global", "Por Zona"],
        ["Por Integrante", "Por Peligrosidad"],
        ["Por Delito", "Faltas Administrativas"],
        ["Rivalidades", "Historial Rinas"],
        ["Volver al Menu Principal"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def zonas_keyboard():
    """Opciones de zonas geográficas."""
    keyboard = [
        ["Norte", "Sur"],
        ["Oriente", "Poniente"],
        ["Centro"],
        ["Atras"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def peligrosidad_keyboard():
    """Niveles de peligrosidad."""
    keyboard = [
        ["Alta", "Media", "Baja"],
        ["Atras"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def tipo_busqueda_delito_keyboard():
    """Submenú para elegir entidad al buscar delitos."""
    keyboard = [
        ["Por Pandilla", "Por Integrante"],
        ["Atras"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def delitos_keyboard():
    """Lista de delitos comunes registrados."""
    keyboard = [
        ["Robo a Transeunte", "Robo de Vehiculo"],
        ["Narcomenudeo", "Extorsion"],
        ["Homicidio", "Danos a Propiedad"],
        ["Atras"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def faltas_keyboard():
    """Lista de faltas administrativas comunes."""
    keyboard = [
        ["Tomar en via publica", "Grafiti ilegal"],
        ["Escandalizar", "Rina sin heridos"],
        ["Violencia familiar", "Orinar en via publica"],
        ["Atras"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)