from dbutils.pooled_db import PooledDB
import pymysql

# Creamos el Pool una sola vez al cargar el módulo
pool = PooledDB(
    creator=pymysql,  # Driver que estás usando
    maxconnections=30,  # Máximo de conexiones abiertas simultáneas (para tus 20+ cajas)
    mincached=5,  # Mantiene al menos 5 conexiones vivas listas para usar
    maxcached=10,  # Máximo de conexiones inactivas en espera
    blocking=True,  # Si se acaban las 30, la caja espera unos milisegundos a que se libere una
    host="localhost",
    user="root",
    password="admin123",
    database="inclub_offline",
    autocommit=False,  # Mantener control manual de transacciones
)


def conectar():
    """
    Devuelve una conexión desde el Pool.
    Para tus modelos e interfaces, esta función hace exactamente lo mismo que antes:
    retorna una conexión con .cursor(), .commit(), .close(), etc.
    """
    return pool.connection()