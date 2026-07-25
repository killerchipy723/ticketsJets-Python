# database/jornadas.py
from database.conexion import conectar

class ModelJornadas:
    @staticmethod
    def obtener_jornadas():
        """Retorna todas las jornadas registradas en la base de datos."""
        conn = conectar()
        if not conn:
            return []
        try:
            with conn.cursor() as cursor:
                sql = """
                    SELECT idjornada, nombre, clave, finicio, ffinal, estado 
                    FROM jornadas 
                    ORDER BY idjornada DESC
                """
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener jornadas: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def obtener_puntos_venta():
        """Obtiene el listado de puntos de venta para los checkboxes."""
        conn = conectar()
        if not conn:
            return []
        try:
            with conn.cursor() as cursor:
                # Ajusta la consulta según el nombre real de tu tabla
                cursor.execute("SELECT idpunto, nombre FROM puntos_venta ORDER BY nombre")
                return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener puntos de venta: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def obtener_productos():
        """Obtiene el listado de productos para los checkboxes."""
        conn = conectar()
        if not conn:
            return []
        try:
            with conn.cursor() as cursor:
                # Ajusta la consulta según el nombre real de tu tabla
                cursor.execute("SELECT idproductos, nombre, importe FROM productos ORDER BY nombre")
                return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener productos: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def crear_jornada(nombre, clave, finicio, ffin, equipos_ids, productos_ids):
        """Inserta una jornada completa en estado Activo."""
        conn = conectar()
        if not conn:
            return False, "Error de conexión a la base de datos."

        try:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO jornadas (nombre, clave, finicio, ffinal, estado) 
                    VALUES (%s, %s, %s, %s, 'Activo')
                """
                cursor.execute(sql, (nombre, clave, finicio, ffin))
                
                # Si necesitas guardar la relación en tablas intermedias de MySQL:
                # id_jornada = cursor.lastrowid
                # ... guardar en jornadas_puntos o jornadas_productos ...

                conn.commit()
                return True, "Jornada registrada correctamente."
        except Exception as e:
            conn.rollback()
            return False, f"Error al registrar jornada: {e}"
        finally:
            conn.close()

    @staticmethod
    def actualizar_jornada(idjornada, nombre, clave, finicio, ffin):
        """Actualiza los datos de la jornada seleccionada."""
        conn = conectar()
        if not conn:
            return False, "Error de conexión a la base de datos."

        try:
            with conn.cursor() as cursor:
                sql = """
                    UPDATE jornadas 
                    SET nombre = %s, clave = %s, finicio = %s, ffinal = %s 
                    WHERE idjornada = %s
                """
                cursor.execute(sql, (nombre, clave, finicio, ffin, idjornada))
                conn.commit()
                return True, "Jornada actualizada correctamente."
        except Exception as e:
            conn.rollback()
            return False, f"Error al actualizar jornada: {e}"
        finally:
            conn.close()

    @staticmethod
    def eliminar_jornada(idjornada):
        """Elimina la jornada de la base de datos."""
        conn = conectar()
        if not conn:
            return False, "Error de conexión a la base de datos."

        try:
            with conn.cursor() as cursor:
                sql = "DELETE FROM jornadas WHERE idjornada = %s"
                cursor.execute(sql, (idjornada,))
                conn.commit()
                return True, "Jornada eliminada correctamente."
        except Exception as e:
            conn.rollback()
            return False, f"Error al eliminar jornada: {e}"
        finally:
            conn.close()