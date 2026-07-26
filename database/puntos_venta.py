# database/puntos_venta.py
from database.conexion import conectar


class ModelPuntosVenta:

    @staticmethod
    def obtener_puntos_venta():
        """Retorna todos los puntos de venta registrados en la base de datos."""
        conn = conectar()
        if not conn:
            return []
        try:
            with conn.cursor() as cursor:
                sql = """
                    SELECT idpunto, nombre, idequipo, estado 
                    FROM puntos_venta 
                    ORDER BY idpunto DESC
                """
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener puntos de venta: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def crear_punto_venta(nombre, idequipo, estado="Activo"):
        """Inserta un nuevo punto de venta en la base de datos."""
        conn = conectar()
        if not conn:
            return False, "Error de conexión a la base de datos."

        try:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO puntos_venta (nombre, idequipo, estado) 
                    VALUES (%s, %s, %s)
                """
                cursor.execute(sql, (nombre, idequipo, estado))
                conn.commit()
                return True, "Punto de Venta registrado correctamente."
        except Exception as e:
            conn.rollback()
            return False, f"Error al registrar punto de venta: {e}"
        finally:
            conn.close()

    @staticmethod
    def actualizar_punto_venta(idpunto, nombre, idequipo, estado):
        """Actualiza los datos de un punto de venta existente."""
        conn = conectar()
        if not conn:
            return False, "Error de conexión a la base de datos."

        try:
            with conn.cursor() as cursor:
                sql = """
                    UPDATE puntos_venta 
                    SET nombre = %s, idequipo = %s, estado = %s 
                    WHERE idpunto = %s
                """
                cursor.execute(sql, (nombre, idequipo, estado, idpunto))
                conn.commit()
                return True, "Punto de Venta actualizado correctamente."
        except Exception as e:
            conn.rollback()
            return False, f"Error al actualizar punto de venta: {e}"
        finally:
            conn.close()

    @staticmethod
    def cambiar_estado(idpunto, nuevo_estado):
        """Cambia rápidamente el estado (Activo/Inactivo) de un equipo."""
        conn = conectar()
        if not conn:
            return False, "Error de conexión a la base de datos."

        try:
            with conn.cursor() as cursor:
                sql = "UPDATE puntos_venta SET estado = %s WHERE idpunto = %s"
                cursor.execute(sql, (nuevo_estado, idpunto))
                conn.commit()
                return True, f"Estado actualizado a {nuevo_estado}."
        except Exception as e:
            conn.rollback()
            return False, f"Error al cambiar estado: {e}"
        finally:
            conn.close()

    @staticmethod
    def eliminar_punto_venta(idpunto):
        """Elimina un punto de venta de la base de datos."""
        conn = conectar()
        if not conn:
            return False, "Error de conexión a la base de datos."

        try:
            with conn.cursor() as cursor:
                sql = "DELETE FROM puntos_venta WHERE idpunto = %s"
                cursor.execute(sql, (idpunto,))
                conn.commit()
                return True, "Punto de Venta eliminado correctamente."
        except Exception as e:
            conn.rollback()
            return False, f"Error al eliminar punto de venta: {e}"
        finally:
            conn.close()

    @staticmethod
    def verificar_equipo_autorizado(mac_equipo):
        """
        Verifica si la MAC del equipo actual está registrada y en estado 'Activo'.
        Retorna los datos del punto de venta si está autorizado, o None si no.
        """
        conn = conectar()
        if not conn:
            return None

        try:
            with conn.cursor() as cursor:
                sql = """
                    SELECT idpunto, nombre, estado 
                    FROM puntos_venta 
                    WHERE idequipo = %s AND estado = 'Activo'
                """
                cursor.execute(sql, (mac_equipo,))
                return cursor.fetchone()
        except Exception as e:
            print(f"Error al verificar equipo: {e}")
            return None
        finally:
            conn.close()