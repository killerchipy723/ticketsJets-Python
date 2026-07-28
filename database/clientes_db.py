# database/clientes_db.py
import pymysql
from database.conexion import conectar  # 👈 Usamos conectar() del Pool


def obtener_todos_clientes_db():
    """Obtiene la lista completa de clientes."""
    conexion = None
    cursor = None
    try:
        conexion = conectar()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""
            SELECT idclientes, apenomb, dni, cuil, correo, fecha_nacimiento
            FROM clientes
            ORDER BY apenomb ASC
        """)
        clientes = cursor.fetchall()
        return clientes, None
    except Exception as e:
        print("ERROR OBTENER CLIENTES:", e)
        return [], str(e)
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()  # Al usar PooledDB, .close() devuelve la conexión al pool


def buscar_clientes_db(criterio=""):
    """Busca clientes filtrando por Apellido/Nombre o DNI."""
    conexion = None
    cursor = None
    try:
        conexion = conectar()
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        query = """
            SELECT idclientes, apenomb, dni, cuil, correo, fecha_nacimiento
            FROM clientes
            WHERE apenomb LIKE %s OR dni LIKE %s
            ORDER BY apenomb ASC
            LIMIT 20
        """
        filtro = f"%{criterio}%"
        cursor.execute(query, (filtro, filtro))
        clientes = cursor.fetchall()
        return clientes, None
    except Exception as e:
        print("ERROR BUSCAR CLIENTES:", e)
        return [], str(e)
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()


def guardar_cliente_db(apenomb, dni, cuil, correo, fecha_nacimiento=None):
    """Inserta un nuevo cliente y retorna su ID."""
    conexion = None
    cursor = None
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        query = """
            INSERT INTO clientes (apenomb, dni, cuil, correo, fecha_nacimiento)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (apenomb.upper(), dni, cuil, correo, fecha_nacimiento or None),
        )
        conexion.commit()
        id_nuevo = cursor.lastrowid
        return True, id_nuevo, "Cliente registrado correctamente."
    except Exception as e:
        if conexion:
            conexion.rollback()
        print("ERROR GUARDAR CLIENTE:", e)
        return False, None, f"Error al guardar cliente: {str(e)}"
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()


def actualizar_cliente_db(
    idclientes, apenomb, dni, cuil, correo, fecha_nacimiento=None
):
    """Actualiza los datos de un cliente existente."""
    conexion = None
    cursor = None
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        query = """
            UPDATE clientes
            SET apenomb=%s, dni=%s, cuil=%s, correo=%s, fecha_nacimiento=%s
            WHERE idclientes=%s
        """
        cursor.execute(
            query,
            (
                apenomb.upper(),
                dni,
                cuil,
                correo,
                fecha_nacimiento or None,
                idclientes,
            ),
        )
        conexion.commit()
        return True, "Cliente actualizado correctamente."
    except Exception as e:
        if conexion:
            conexion.rollback()
        print("ERROR UPDATE CLIENTE:", e)
        return False, f"Error al actualizar cliente: {str(e)}"
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()


def eliminar_cliente_db(idclientes):
    """Elimina un cliente por su ID."""
    conexion = None
    cursor = None
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute(
            "DELETE FROM clientes WHERE idclientes=%s", (idclientes,)
        )
        conexion.commit()
        return True, "Cliente eliminado correctamente."
    except Exception as e:
        if conexion:
            conexion.rollback()
        print("ERROR DELETE CLIENTE:", e)
        return False, f"Error al eliminar cliente: {str(e)}"
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()