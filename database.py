import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Optional

# Configuración de la conexión a la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'indicado_pandillas_db'
}

def create_connection():
    """
    Establece y devuelve una conexión a la base de datos MariaDB/MySQL.
    Retorna None si falla la conexión.
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# --- CONSULTAS RELACIONADAS CON PANDILLAS ---

def get_pandillas_por_zona(zona: str) -> List[Dict]:
    """
    Obtiene una lista de pandillas filtradas por su zona geográfica.
    """
    conn = create_connection()
    if conn is None: return []

    query = "SELECT Nombre, Description, Peligrosidad FROM Pandillas WHERE Zona = %s"
    
    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, (zona,))
            return cursor.fetchall()
    except Error as e:
        print(f"Error en get_pandillas_por_zona: {e}")
        return []
    finally:
        if conn.is_connected(): conn.close()

def get_pandillas_por_peligrosidad(nivel: str) -> List[Dict]:
    """
    Obtiene pandillas filtradas por su nivel de peligrosidad (Alta, Media, Baja).
    """
    conn = create_connection()
    if conn is None: return []

    query = "SELECT Nombre, Description, Zona FROM Pandillas WHERE Peligrosidad = %s"
    
    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, (nivel,))
            return cursor.fetchall()
    except Error as e:
        print(f"Error en get_pandillas_por_peligrosidad: {e}")
        return []
    finally:
        if conn.is_connected(): conn.close()

def get_reporte_global(nombre_pandilla: str) -> List[Dict]:
    """
    Obtiene la ficha técnica completa de una pandilla específica por nombre.
    """
    conn = create_connection()
    if conn is None: return []
    
    termino = f"%{nombre_pandilla}%"
    query = "SELECT * FROM Pandillas WHERE Nombre LIKE %s"
    
    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, (termino,))
            return cursor.fetchall()
    except Error as e:
        print(f"Error en get_reporte_global: {e}")
        return []
    finally:
        if conn.is_connected(): conn.close()

def get_pandillas_por_delito(tipo_delito: str) -> List[Dict]:
    """
    Busca pandillas que hayan cometido un tipo de delito específico.
    """
    conn = create_connection()
    if conn is None: return []
    
    query = """
    SELECT p.Nombre, p.Zona, d.Tipo_Delito, dp.Fecha_Evento
    FROM Pandillas p
    JOIN Delitos_Pandillas dp ON p.ID_Pandilla = dp.ID_Pandilla
    JOIN Delitos d ON dp.ID_Delito = d.ID_Delito
    WHERE d.Tipo_Delito LIKE %s
    """
    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, (f"%{tipo_delito}%",))
            return cursor.fetchall()
    except Error as e:
        print(f"Error en get_pandillas_por_delito: {e}")
        return []
    finally:
        if conn.is_connected(): conn.close()

def get_rivalidades_pandilla(nombre_pandilla: str) -> List[Dict]:
    """
    Busca las rivalidades de una pandilla (bidireccional: pandilla 1 o 2).
    """
    conn = create_connection()
    if conn is None: return []
    
    termino = f"%{nombre_pandilla}%"
    query = """
    SELECT p1.Nombre as Pandilla1, p2.Nombre as Pandilla2
    FROM Pandillas_Rivales pr
    JOIN Pandillas p1 ON pr.ID_Pandilla1 = p1.ID_Pandilla
    JOIN Pandillas p2 ON pr.ID_Pandilla2 = p2.ID_Pandilla
    WHERE p1.Nombre LIKE %s OR p2.Nombre LIKE %s
    """
    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, (termino, termino))
            return cursor.fetchall()
    except Error as e:
        print(f"Error en get_rivalidades_pandilla: {e}")
        return []
    finally:
        if conn.is_connected(): conn.close()

# --- CONSULTAS RELACIONADAS CON INTEGRANTES ---

def get_integrante_por_nombre(busqueda: str) -> List[Dict]:
    """
    Busca integrantes por nombre o alias (coincidencia parcial).
    """
    conn = create_connection()
    if conn is None: return []
    
    termino = f"%{busqueda}%"
    query = """
    SELECT i.Nombre_Completo, i.Alias, i.Datos_Importantes, p.Nombre as Nombre_Pandilla
    FROM Integrantes i
    JOIN Pandillas_Integrantes pi ON i.ID_Integrante = pi.ID_Integrante
    JOIN Pandillas p ON pi.ID_Pandilla = p.ID_Pandilla
    WHERE i.Nombre_Completo LIKE %s OR i.Alias LIKE %s
    """
    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, (termino, termino))
            return cursor.fetchall()
    except Error as e:
        print(f"Error en get_integrante_por_nombre: {e}")
        return []
    finally:
        if conn.is_connected(): conn.close()

def get_integrantes_por_delito(tipo_delito: str) -> List[Dict]:
    """
    Busca integrantes que hayan cometido un delito específico.
    """
    conn = create_connection()
    if conn is None: return []
    
    query = """
    SELECT i.Nombre_Completo, i.Alias, d.Tipo_Delito, di.Fecha_Evento
    FROM Integrantes i
    JOIN Delitos_Integrantes di ON i.ID_Integrante = di.ID_Integrante
    JOIN Delitos d ON di.ID_Delito = d.ID_Delito
    WHERE d.Tipo_Delito LIKE %s
    """
    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, (f"%{tipo_delito}%",))
            return cursor.fetchall()
    except Error as e:
        print(f"Error en get_integrantes_por_delito: {e}")
        return []
    finally:
        if conn.is_connected(): conn.close()

def get_integrantes_por_falta(tipo_falta: str) -> List[Dict]:
    """
    Busca integrantes que hayan cometido faltas administrativas.
    """
    conn = create_connection()
    if conn is None: return []
    
    query = """
    SELECT i.Nombre_Completo, i.Alias, f.Tipo_Falta, fi.Fecha_Evento, fi.Colonia
    FROM Integrantes i
    JOIN Faltas_Integrantes fi ON i.ID_Integrante = fi.ID_Integrante
    JOIN Faltas f ON fi.ID_Falta = f.ID_Falta
    WHERE f.Tipo_Falta LIKE %s
    """
    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, (f"%{tipo_falta}%",))
            return cursor.fetchall()
    except Error as e:
        print(f"Error en get_integrantes_por_falta: {e}")
        return []
    finally:
        if conn.is_connected(): conn.close()

# --- CONSULTAS DE EVENTOS (RIÑAS) ---

def get_rinas_por_pandilla(nombre_pandilla: str) -> List[Dict]:
    """
    Obtiene el historial de riñas donde participó una pandilla.
    """
    conn = create_connection()
    if conn is None: return []
    
    termino = f"%{nombre_pandilla}%"
    query = """
    SELECT r.Descripcion, r.Fecha, r.Lugar, p1.Nombre as Pandilla1, p2.Nombre as Pandilla2
    FROM Rinas r
    JOIN Pandillas p1 ON r.ID_Pandilla1 = p1.ID_Pandilla
    JOIN Pandillas p2 ON r.ID_Pandilla2 = p2.ID_Pandilla
    WHERE p1.Nombre LIKE %s OR p2.Nombre LIKE %s
    ORDER BY r.Fecha DESC
    """
    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, (termino, termino))
            return cursor.fetchall()
    except Error as e:
        print(f"Error en get_rinas_por_pandilla: {e}")
        return []
    finally:
        if conn.is_connected(): conn.close()

if __name__ == '__main__':
    print("Prueba de conexión exitosa. Ejecuta el bot principal.")