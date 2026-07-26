# database/jornadas_admin.py
import pymysql
from database.conexion import conectar

class ModelJornadasAdmin:
    @staticmethod
    def obtener_jornadas_activas():
        """Obtiene las jornadas para listar en la administración."""
        conn = conectar()
        jornadas = []
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT idjornada, nombre, estado FROM jornadas ORDER BY idjornada DESC")
                jornadas = cursor.fetchall()
                cursor.close()
            except Exception as e:
                print(f"Error al obtener jornadas: {e}")
            finally:
                conn.close()
        return jornadas

    @staticmethod
    def obtener_puntos_con_estado(id_jornada):
        """Retorna todos los puntos de venta indicando si están asignados a la jornada."""
        conn = conectar()
        puntos = []
        if conn:
            try:
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                # Consulta LEFT JOIN con la tabla intermedia (ej. jornada_punto)
                sql = """
                    SELECT p.idpunto, p.nombre, 
                           IF(jp.idjornada IS NOT NULL, 1, 0) AS asignado
                    FROM puntos_venta p
                    LEFT JOIN jornadas_puntos jp 
                        ON p.idpunto = jp.idpunto AND jp.idjornada = %s
                    WHERE p.estado = 'Activo'
                """
                cursor.execute(sql, (id_jornada,))
                puntos = cursor.fetchall()
                cursor.close()
            except Exception as e:
                print(f"Error al obtener puntos para la jornada: {e}")
            finally:
                conn.close()
        return puntos

    @staticmethod
    def obtener_productos_con_estado(id_jornada):
        """Retorna todos los productos indicando si están asignados a la jornada."""
        conn = conectar()
        productos = []
        if conn:
            try:
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                # Consulta LEFT JOIN con la tabla intermedia (ej. jornada_producto)
                sql = """
                    SELECT pr.idproductos, pr.nombre, pr.importe, 
                           IF(jp.idjornada IS NOT NULL, 1, 0) AS asignado
                    FROM productos pr
                    LEFT JOIN jornadas_productos jp 
                        ON pr.idproductos = jp.idproducto AND jp.idjornada = %s
                    WHERE pr.estado = 'Activo'
                """
                cursor.execute(sql, (id_jornada,))
                productos = cursor.fetchall()
                cursor.close()
            except Exception as e:
                print(f"Error al obtener productos para la jornada: {e}")
            finally:
                conn.close()
        return productos

    @staticmethod
    def toggle_punto_jornada(id_jornada, id_punto, asignado_actualmente):
        """Asigna o remueve un punto de venta de la jornada."""
        conn = conectar()
        if conn:
            try:
                cursor = conn.cursor()
                if asignado_actualmente:
                    cursor.execute("DELETE FROM jornadas_puntos WHERE idjornada=%s AND idpunto=%s", (id_jornada, id_punto))
                else:
                    cursor.execute("INSERT INTO jornadas_puntos (idjornada, idpunto) VALUES (%s, %s)", (id_jornada, id_punto))
                conn.commit()
                cursor.close()
                return True, "Cambio aplicado"
            except Exception as e:
                return False, f"Error: {e}"
            finally:
                conn.close()
        return False, "Error de conexión"

    @staticmethod
    def toggle_producto_jornada(id_jornada, id_producto, asignado_actualmente):
        """Asigna o remueve un producto de la jornada."""
        conn = conectar()
        if conn:
            try:
                cursor = conn.cursor()
                if asignado_actualmente:
                    cursor.execute("DELETE FROM jornadas_productos WHERE idjornada=%s AND idproducto=%s", (id_jornada, id_producto))
                else:
                    cursor.execute("INSERT INTO jornadas_productos (idjornada, idproducto) VALUES (%s, %s)", (id_jornada, id_producto))
                conn.commit()
                cursor.close()
                return True, "Cambio aplicado"
            except Exception as e:
                return False, f"Error: {e}"
            finally:
                conn.close()
        return False, "Error de conexión"