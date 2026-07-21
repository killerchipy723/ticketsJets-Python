import pymysql
from database.conexion import conectar

def iniciar_sesion(usuario, password):

    conexion = conectar()

    # Cursor que devuelve diccionarios
    cursor = conexion.cursor(pymysql.cursors.DictCursor)

    sql = """
        SELECT *
        FROM usuarios
        WHERE usuario=%s
        AND password=%s
        AND estado=1
    """

    cursor.execute(sql, (usuario, password))

    datos = cursor.fetchone()

    cursor.close()
    conexion.close()

    return datos