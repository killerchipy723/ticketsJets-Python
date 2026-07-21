import pymysql

def conectar():

    conexion = pymysql.connect(
        host="localhost",
        user="root",
        password="admin123",
        database="ticketsjets"
    )

    return conexion