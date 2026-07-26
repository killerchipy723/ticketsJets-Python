# database/productos.py
import pymysql
from database.conexion import conectar

# ==============================================================================
# 1. FUNCIÓN EXISTENTE (Para el módulo de Ventas)
# ==============================================================================
def productos():
    """
    Retorna la lista de productos como una lista de diccionarios (DictCursor).
    Se mantiene intacta para no romper la sección de Ventas.
    """
    conexion = conectar()
    if not conexion:
        return []

    try:
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM productos"
        cursor.execute(sql)
        prod = cursor.fetchall()
        cursor.close()
        return prod
    except Exception as e:
        print(f"Error en funcion productos(): {e}")
        return []
    finally:
        conexion.close()


# ==============================================================================
# 2. CLASE MODELPRODUCTOS (Para el módulo de Gestión de Productos / ABM)
# ==============================================================================
class ModelProductos:
    @staticmethod
    def obtener_productos():
        """Obtiene la lista de productos en formato tupla para llenar la Treeview."""
        conn = conectar()
        puntos = []
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT idproductos, nombre, importe, estado, stock FROM productos ORDER BY idproductos DESC")
                puntos = cursor.fetchall()
                cursor.close()
            except Exception as e:
                print(f"Error al obtener productos: {e}")
            finally:
                conn.close()
        return puntos

    @staticmethod
    def crear_producto(nombre, importe, estado, stock):
        conn = conectar()
        if conn:
            try:
                cursor = conn.cursor()
                query = "INSERT INTO productos (nombre, importe, estado, stock) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (nombre, importe, estado, stock))
                conn.commit()
                cursor.close()
                return True, "Producto registrado exitosamente."
            except Exception as e:
                return False, f"Error al guardar producto: {e}"
            finally:
                conn.close()
        return False, "Error de conexión con la base de datos."

    @staticmethod
    def actualizar_producto(idproductos, nombre, importe, estado, stock):
        conn = conectar()
        if conn:
            try:
                cursor = conn.cursor()
                query = "UPDATE productos SET nombre=%s, importe=%s, estado=%s, stock=%s WHERE idproductos=%s"
                cursor.execute(query, (nombre, importe, estado, stock, idproductos))
                conn.commit()
                cursor.close()
                return True, "Producto actualizado correctamente."
            except Exception as e:
                return False, f"Error al actualizar producto: {e}"
            finally:
                conn.close()
        return False, "Error de conexión con la base de datos."

    @staticmethod
    def eliminar_producto(idproductos):
        conn = conectar()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM productos WHERE idproductos=%s", (idproductos,))
                conn.commit()
                cursor.close()
                return True, "Producto eliminado correctamente."
            except Exception as e:
                return False, f"Error al eliminar producto: {e}"
            finally:
                conn.close()
        return False, "Error de conexión con la base de datos."