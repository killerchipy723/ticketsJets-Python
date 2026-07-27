# database/modopago_db.py
from database.conexion import conectar


class ModelModoPago:

    @staticmethod
    def obtener_modos_pago():
        """Retorna todos los modos de pago registrados."""
        conn = conectar()
        if not conn:
            return []
        try:
            with conn.cursor() as cursor:
                sql = """
                    SELECT idmodopago, modo, estado 
                    FROM modopago 
                    ORDER BY idmodopago DESC
                """
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener modos de pago: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def crear_modo_pago(modo, estado="Activo"):
        """Registra un nuevo modo de pago."""
        conn = conectar()
        if not conn:
            return False, "Error de conexión a la base de datos."

        try:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO modopago (modo, estado)
                    VALUES (%s, %s)
                """
                cursor.execute(sql, (modo, estado))
                conn.commit()
                return True, "Modo de pago registrado correctamente."
        except Exception as e:
            conn.rollback()
            return False, f"Error al registrar modo de pago: {e}"
        finally:
            conn.close()

    @staticmethod
    def actualizar_modo_pago(idmodo, modo, estado):
        """Actualiza un modo de pago existente capturando idmodo."""
        conn = conectar()
        if not conn:
            return False, "Error de conexión a la base de datos."

        try:
            with conn.cursor() as cursor:
                sql = """
                    UPDATE modopago 
                    SET modo = %s, estado = %s 
                    WHERE idmodopago = %s
                """
                cursor.execute(sql, (modo, estado, idmodo))
                conn.commit()
                return True, "Modo de pago actualizado correctamente."
        except Exception as e:
            conn.rollback()
            return False, f"Error al actualizar modo de pago: {e}"
        finally:
            conn.close()

    @staticmethod
    def eliminar_modo_pago(idmodo):
        """Elimina un modo de pago por idmodo."""
        conn = conectar()
        if not conn:
            return False, "Error de conexión a la base de datos."

        try:
            with conn.cursor() as cursor:
                sql = "DELETE FROM modopago WHERE idmodopago = %s"
                cursor.execute(sql, (idmodo,))
                conn.commit()
                return True, "Modo de pago eliminado correctamente."
        except Exception as e:
            conn.rollback()
            return False, f"Error al eliminar modo de pago: {e}"
        finally:
            conn.close()