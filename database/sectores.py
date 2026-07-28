# database/sectores.py
import pymysql
from database.conexion import conectar


def obtener_sectores_y_jornadas():
    """
    Obtiene la lista de sectores con el nombre de su jornada asignada
    y el listado de todas las jornadas para los desplegables.
    """
    conexion = conectar()
    if not conexion:
        return None, None, "Error de conexión con la base de datos."

    cursor = conexion.cursor(pymysql.cursors.DictCursor)

    try:
        # 1. Obtener todos los sectores junto con su jornada
        cursor.execute("""
            SELECT s.idsector, s.idjornada, s.nombre, s.precio, s.estado, j.nombre AS jornada
            FROM sectores_entradas s
            INNER JOIN jornadas j ON j.idjornada = s.idjornada
            ORDER BY s.idsector DESC
        """)
        sectores = cursor.fetchall()

        # 2. Obtener jornadas activas/disponibles para selección
        cursor.execute("""
            SELECT idjornada, nombre 
            FROM jornadas 
            ORDER BY idjornada DESC
        """)
        jornadas = cursor.fetchall()

        return sectores, jornadas, None

    except Exception as e:
        print(f"❌ Error en obtener_sectores_y_jornadas: {e}")
        return None, None, str(e)
    finally:
        cursor.close()
        conexion.close()


def guardar_sector_entrada_db(idjornada, nombre, precio, estado):
    """
    Registra un nuevo sector vinculado a una jornada.
    """
    conexion = conectar()
    if not conexion:
        return False, "Error de conexión."

    cursor = conexion.cursor()

    try:
        nombre_clean = nombre.strip().upper()
        
        cursor.execute("""
            INSERT INTO sectores_entradas (idjornada, nombre, precio, estado)
            VALUES (%s, %s, %s, %s)
        """, (idjornada, nombre_clean, precio, estado))

        conexion.commit()
        return True, "Sector registrado correctamente."

    except Exception as e:
        print(f"❌ Error en guardar_sector_entrada_db: {e}")
        if conexion:
            conexion.rollback()
        return False, str(e)
    finally:
        cursor.close()
        conexion.close()


def actualizar_sector_entrada_db(idsector, idjornada, nombre, precio, estado):
    """
    Actualiza la vinculación de un sector con su jornada, nombre, precio y estado.
    """
    conexion = conectar()
    if not conexion:
        return False, "Error de conexión."

    cursor = conexion.cursor()

    try:
        nombre_clean = nombre.strip().upper()

        cursor.execute("""
            UPDATE sectores_entradas
            SET idjornada = %s, nombre = %s, precio = %s, estado = %s
            WHERE idsector = %s
        """, (idjornada, nombre_clean, precio, estado, idsector))

        conexion.commit()
        return True, "Sector actualizado correctamente."

    except Exception as e:
        print(f"❌ Error en actualizar_sector_entrada_db: {e}")
        if conexion:
            conexion.rollback()
        return False, str(e)
    finally:
        cursor.close()
        conexion.close()


def eliminar_sector_entrada_db(idsector):
    """
    Elimina un sector de entrada por su ID.
    """
    conexion = conectar()
    if not conexion:
        return False, "Error de conexión."

    cursor = conexion.cursor()

    try:
        cursor.execute("DELETE FROM sectores_entradas WHERE idsector = %s", (idsector,))
        conexion.commit()
        return True, "Sector eliminado correctamente."

    except Exception as e:
        print(f"❌ Error en eliminar_sector_entrada_db: {e}")
        if conexion:
            conexion.rollback()
        return False, str(e)
    finally:
        cursor.close()
        conexion.close()