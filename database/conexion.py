import pymysql

def conectar():

    conexion = pymysql.connect(
        host="192.168.1.34",
        user="tickets",
        password="123456",
        database="inclub_offline"
    )

    return conexion