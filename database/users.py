# database/users.py
from database.conexion import conectar

class ModelUsuarios:
    @staticmethod
    def obtener_usuarios():
        """Obtiene la lista de usuarios para la tabla de la vista."""
        conn = conectar()
        if not conn:
            return []
        
        try:
            with conn.cursor() as cursor:
                # Selecciona en el orden exacto que espera el Treeview:
                # (idusuarios, nombre, rol, estado, operador)
                sql = """
                    SELECT idusuarios, nombre, rol, estado, operador 
                    FROM usuarios 
                    ORDER BY idusuarios DESC
                """
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener usuarios: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def crear_usuario(nombre, clave, rol, estado, operador):
        """Inserta un nuevo usuario en la base de datos."""
        conn = conectar()
        if not conn:
            return False, "Error de conexión a la base de datos."

        try:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO usuarios (nombre, clave, rol, estado, operador) 
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (nombre, clave, rol, estado, operador))
                conn.commit()
                return True, "Usuario registrado correctamente."
        except Exception as e:
            conn.rollback()
            return False, f"Error al registrar usuario: {e}"
        finally:
            conn.close()

    @staticmethod
    def actualizar_usuario(idusuarios, nombre, clave, rol, estado, operador):
        """Actualiza un usuario existente por su idusuarios."""
        conn = conectar()
        if not conn:
            return False, "Error de conexión a la base de datos."

        try:
            with conn.cursor() as cursor:
                if clave:
                    # Si ingresó clave nueva, se actualiza también la contraseña
                    sql = """
                        UPDATE usuarios 
                        SET nombre = %s, clave = %s, rol = %s, estado = %s, operador = %s 
                        WHERE idusuarios = %s
                    """
                    cursor.execute(sql, (nombre, clave, rol, estado, operador, idusuarios))
                else:
                    # Si dejó la clave en blanco, se conservan los datos sin alterar la clave
                    sql = """
                        UPDATE usuarios 
                        SET nombre = %s, rol = %s, estado = %s, operador = %s 
                        WHERE idusuarios = %s
                    """
                    cursor.execute(sql, (nombre, rol, estado, operador, idusuarios))

                conn.commit()
                return True, "Usuario actualizado correctamente."
        except Exception as e:
            conn.rollback()
            return False, f"Error al actualizar usuario: {e}"
        finally:
            conn.close()

    @staticmethod
    def eliminar_usuario(idusuarios):
        """Elimina un usuario por su idusuarios."""
        conn = conectar()
        if not conn:
            return False, "Error de conexión a la base de datos."

        try:
            with conn.cursor() as cursor:
                sql = "DELETE FROM usuarios WHERE idusuarios = %s"
                cursor.execute(sql, (idusuarios,))
                conn.commit()
                return True, "Usuario eliminado correctamente."
        except Exception as e:
            conn.rollback()
            return False, f"Error al eliminar usuario: {e}"
        finally:
            conn.close()