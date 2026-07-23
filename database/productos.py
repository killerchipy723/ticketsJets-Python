import pymysql
from database.conexion import conectar

def productos():

    conexion = conectar()

    # Cursor que devuelve diccionarios
    cursor = conexion.cursor(pymysql.cursors.DictCursor)

    sql = """
        SELECT *
        FROM productos
    """

    cursor.execute(sql)

    prod = cursor.fetchall()

    cursor.close()
    conexion.close()

    return prod