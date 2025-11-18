from telegram import Update
from telegram.ext import ContextTypes

from keyboards import (
    consultas_menu_keyboard, 
    zonas_keyboard, 
    peligrosidad_keyboard,
    tipo_busqueda_delito_keyboard,
    delitos_keyboard,
    faltas_keyboard,
    back_keyboard,
    main_menu_keyboard,
    MENU, CONSULTAS, SUBMENU_DELITO, SELECCION_CRITERIO
)
from database import (
    get_pandillas_por_zona, 
    get_pandillas_por_peligrosidad,
    get_integrante_por_nombre,
    get_pandillas_por_delito,
    get_integrantes_por_delito,
    get_rivalidades_pandilla,
    get_reporte_global,
    get_integrantes_por_falta,
    get_rinas_por_pandilla
)

async def start_consultas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Inicia el flujo de consultas mostrando el menú de opciones.
    """
    await update.message.reply_text(
        "SISTEMA DE CONSULTAS\nSelecciona una opcion:",
        reply_markup=consultas_menu_keyboard()
    )
    return CONSULTAS

async def handle_tipo_consulta(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Maneja la selección del tipo de búsqueda (Zona, Peligrosidad, etc.)
    y muestra el siguiente teclado correspondiente.
    """
    text = update.message.text
    
    # Configuración de la búsqueda según el botón presionado
    if "Reporte Global" in text:
        context.user_data['tipo_busqueda'] = 'reporte_global'
        await update.message.reply_text(
            "REPORTE GLOBAL\nEscribe el nombre de la pandilla para ver su ficha tecnica:",
            reply_markup=back_keyboard()
        )
        return SELECCION_CRITERIO

    elif "Faltas" in text:
        context.user_data['tipo_busqueda'] = 'falta'
        await update.message.reply_text("Selecciona la falta administrativa:", reply_markup=faltas_keyboard())
        return SELECCION_CRITERIO

    elif "Rinas" in text: # Sin ñ en el código para evitar problemas
        context.user_data['tipo_busqueda'] = 'rinas'
        await update.message.reply_text(
            "HISTORIAL DE RINAS\nEscribe el nombre de la pandilla para ver sus eventos:",
            reply_markup=back_keyboard()
        )
        return SELECCION_CRITERIO

    elif "Zona" in text:
        context.user_data['tipo_busqueda'] = 'zona'
        await update.message.reply_text("Selecciona la zona:", reply_markup=zonas_keyboard())
        return SELECCION_CRITERIO
        
    elif "Peligrosidad" in text:
        context.user_data['tipo_busqueda'] = 'peligrosidad'
        await update.message.reply_text("Selecciona el nivel:", reply_markup=peligrosidad_keyboard())
        return SELECCION_CRITERIO
        
    elif "Integrante" in text:
        context.user_data['tipo_busqueda'] = 'integrante'
        await update.message.reply_text("Escribe el NOMBRE o ALIAS:", reply_markup=back_keyboard())
        return SELECCION_CRITERIO
        
    elif "Delito" in text:
        # Redirige al submenú para especificar si busca por pandilla o integrante
        await update.message.reply_text("Buscar pandillas o integrantes?", reply_markup=tipo_busqueda_delito_keyboard())
        return SUBMENU_DELITO
        
    elif "Rivalidad" in text:
        context.user_data['tipo_busqueda'] = 'rivalidad'
        await update.message.reply_text("Escribe el nombre de la pandilla:", reply_markup=back_keyboard())
        return SELECCION_CRITERIO
        
    elif "Menu" in text or "Principal" in text:
        await update.message.reply_text("Menu Principal", reply_markup=main_menu_keyboard())
        return MENU
        
    else:
        await update.message.reply_text("Opcion no valida.", reply_markup=consultas_menu_keyboard())
        return CONSULTAS

async def handle_submenu_delito(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Maneja el submenú específico para consultas de delitos (Por Pandilla o Por Integrante).
    """
    text = update.message.text
    
    if "Pandilla" in text:
        context.user_data['tipo_busqueda'] = 'delito_pandilla'
        await update.message.reply_text("Selecciona el delito:", reply_markup=delitos_keyboard())
        return SELECCION_CRITERIO
        
    elif "Integrante" in text:
        context.user_data['tipo_busqueda'] = 'delito_integrante'
        await update.message.reply_text("Selecciona el delito:", reply_markup=delitos_keyboard())
        return SELECCION_CRITERIO
        
    elif "Atras" in text:
        return await start_consultas(update, context)
        
    else:
        await update.message.reply_text("Opcion no valida.", reply_markup=tipo_busqueda_delito_keyboard())
        return SUBMENU_DELITO

async def handle_criterio_seleccionado(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Ejecuta la consulta a la base de datos basándose en el criterio seleccionado (texto o botón)
    y devuelve los resultados formateados.
    """
    criterio = update.message.text
    tipo = context.user_data.get('tipo_busqueda')
    
    # Manejo de botón "Atrás"
    if "Atras" in criterio or "Menu" in criterio or "Volver" in criterio:
        return await start_consultas(update, context)

    lista_resultados = []
    mensaje = ""
    
    # --- EJECUCIÓN DE CONSULTAS ---
    
    if tipo == 'reporte_global':
        lista_resultados = get_reporte_global(criterio)
        if lista_resultados:
            p = lista_resultados[0]
            mensaje = (
                f"REPORTE GLOBAL: {p['Nombre']}\n\n"
                f"Lider: {p['Lider']}\n"
                f"Integrantes: {p['No_Integrantes']} aprox.\n"
                f"Rango de Edades: {p['Edades_Integrantes']}\n"
                f"Peligrosidad: {p['Peligrosidad']}\n"
                f"Zona: {p['Zona']}\n"
                f"Base: {p['Calle']} #{p['Numero']}, {p['Colonia']}\n\n"
                f"Descripcion:\n{p['Description']}\n"
            )
            # Respuesta inmediata para este caso
            await update.message.reply_text(mensaje, reply_markup=consultas_menu_keyboard())
            return CONSULTAS

    elif tipo == 'falta':
        lista_resultados = get_integrantes_por_falta(criterio)
        mensaje = f"Faltas de tipo '{criterio}':\n\n"
        for i in lista_resultados:
            mensaje += f"- {i['Nombre_Completo']} ({i['Alias']})\n"
            mensaje += f"  Fecha: {i['Fecha_Evento']} en {i['Colonia']}\n"

    elif tipo == 'rinas':
        lista_resultados = get_rinas_por_pandilla(criterio)
        mensaje = f"Historial de Rinas de '{criterio}':\n\n"
        for r in lista_resultados:
            mensaje += f"Fecha: {r['Fecha']}\n"
            mensaje += f"VS: {r['Pandilla1']} vs {r['Pandilla2']}\n"
            mensaje += f"Lugar: {r['Lugar']}\n"
            mensaje += f"Detalle: {r['Descripcion']}\n"
            mensaje += "-------------------\n"

    elif tipo == 'zona':
        lista_resultados = get_pandillas_por_zona(criterio)
        mensaje = f"Pandillas en zona {criterio}:\n\n"
        for p in lista_resultados:
            mensaje += f"- {p['Nombre']} (Peligrosidad: {p['Peligrosidad']})\n"
            
    elif tipo == 'peligrosidad':
        lista_resultados = get_pandillas_por_peligrosidad(criterio)
        mensaje = f"Pandillas de peligrosidad {criterio}:\n\n"
        for p in lista_resultados:
            mensaje += f"- {p['Nombre']} ({p['Zona']})\n"
            
    elif tipo == 'integrante':
        lista_resultados = get_integrante_por_nombre(criterio)
        mensaje = f"Resultados para '{criterio}':\n\n"
        for i in lista_resultados:
            mensaje += f"Nombre: {i['Nombre_Completo']}\nAlias: {i['Alias']}\nPandilla: {i['Nombre_Pandilla']}\n\n"
            
    elif tipo == 'delito_pandilla':
        lista_resultados = get_pandillas_por_delito(criterio)
        mensaje = f"Pandillas vinculadas a '{criterio}':\n\n"
        for d in lista_resultados:
            mensaje += f"- {d['Nombre']} (Zona {d['Zona']})\n"
            
    elif tipo == 'delito_integrante':
        lista_resultados = get_integrantes_por_delito(criterio)
        mensaje = f"Integrantes vinculados a '{criterio}':\n\n"
        for i in lista_resultados:
            mensaje += f"- {i['Nombre_Completo']} (Alias: {i['Alias']})\n"
            
    elif tipo == 'rivalidad':
        lista_resultados = get_rivalidades_pandilla(criterio)
        mensaje = f"Rivalidades encontradas:\n\n"
        for r in lista_resultados:
            mensaje += f"{r['Pandilla1']} VS {r['Pandilla2']}\n"

    # --- MANEJO DE RESULTADOS ---
    
    if not lista_resultados:
        # Si es búsqueda libre (texto), permitimos reintentar
        if tipo in ['integrante', 'rivalidad', 'reporte_global', 'rinas']:
             await update.message.reply_text(
                f"No encontre informacion sobre: '{criterio}'. Intenta de nuevo.", 
                reply_markup=back_keyboard()
            )
             return SELECCION_CRITERIO
        else:
            # Si fue selección de botón y no hubo datos
            await update.message.reply_text(
                f"No hay registros para: '{criterio}'.", 
                reply_markup=consultas_menu_keyboard()
            )
            return CONSULTAS
    else:
        await update.message.reply_text(mensaje, reply_markup=consultas_menu_keyboard())
        return CONSULTAS