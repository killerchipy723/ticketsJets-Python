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
                cursor.execute(
                    "SELECT idpunto, nombre FROM puntos_venta ORDER BY nombre"
                )
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
                cursor.execute(
                    "SELECT idproductos, nombre, importe FROM productos ORDER BY nombre"
                )
                return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener productos: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def hay_jornada_activa():
        """Verifica si existe alguna jornada en estado 'Activo'."""
        conn = conectar()
        if not conn:
            return False
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(*) FROM jornadas WHERE estado = 'Activo'"
                )
                res = cursor.fetchone()
                count = (
                    res[0]
                    if isinstance(res, (tuple, list))
                    else list(res.values())[0]
                )
                return count > 0
        except Exception as e:
            print(f"Error al verificar jornada activa: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def crear_jornada(
        nombre,
        clave,
        finicio,
        ffin,
        equipos_ids,
        productos_ids,
        forzar_cierre=False,
    ):
        """
        Inserta una jornada y guarda la relación con puntos de venta y productos habilitados.
        Si forzar_cierre=True, cambia el estado de las jornadas activas previas a 'Finalizado'.
        """
        conn = conectar()
        if not conn:
            return False, "Error de conexión a la base de datos.", False

        try:
            with conn.cursor() as cursor:
                # 1. Verificar si hay jornada activa
                cursor.execute(
                    "SELECT COUNT(*) FROM jornadas WHERE estado = 'Activo'"
                )
                res = cursor.fetchone()
                activa_count = (
                    res[0]
                    if isinstance(res, (tuple, list))
                    else list(res.values())[0]
                )

                if activa_count > 0:
                    if not forzar_cierre:
                        return (
                            False,
                            "Ya existe una jornada ACTIVA actualmente.\n\n¿Desea cerrarla ahora para crear la nueva?",
                            True,
                        )

                    # Si el usuario aceptó cerrar la anterior:
                    cursor.execute(
                        "UPDATE jornadas SET estado = 'Finalizado' WHERE estado = 'Activo'"
                    )

                # 2. Insertar la nueva jornada en la tabla cabecera
                sql = """
                    INSERT INTO jornadas (nombre, clave, finicio, ffinal, estado) 
                    VALUES (%s, %s, %s, %s, 'Activo')
                """
                cursor.execute(sql, (nombre, clave, finicio, ffin))

                # Obtenemos el ID de la jornada que se acaba de crear
                idjornada = cursor.lastrowid

                # 3. Guardar Puntos de Venta (Equipos) habilitados
                for id_punto in equipos_ids:
                    cursor.execute(
                        """
                        INSERT INTO jornadas_puntos (idjornada, idpunto)
                        VALUES (%s, %s)
                    """,
                        (idjornada, id_punto),
                    )

                # 4. Guardar Productos habilitados
                for id_producto in productos_ids:
                    cursor.execute(
                        """
                        INSERT INTO jornadas_productos (idjornada, idproducto)
                        VALUES (%s, %s)
                    """,
                        (idjornada, id_producto),
                    )

                conn.commit()
                return True, "Jornada registrada correctamente.", False
        except Exception as e:
            conn.rollback()
            return False, f"Error al registrar jornada: {e}", False
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
                # Opcional: si la BD no tiene ON DELETE CASCADE, eliminamos relaciones primero
                cursor.execute(
                    "DELETE FROM jornadas_puntos WHERE idjornada = %s",
                    (idjornada,),
                )
                cursor.execute(
                    "DELETE FROM jornadas_productos WHERE idjornada = %s",
                    (idjornada,),
                )

                sql = "DELETE FROM jornadas WHERE idjornada = %s"
                cursor.execute(sql, (idjornada,))
                conn.commit()
                return True, "Jornada eliminada correctamente."
        except Exception as e:
            conn.rollback()
            return False, f"Error al eliminar jornada: {e}"
        finally:
            conn.close()