# database/repo_jornadas_db.py
from database.conexion import conectar
from datetime import datetime

class ModelReportesJornadas:

    @staticmethod
    def obtener_jornadas():
        """Obtiene la lista de jornadas ordenadas descendentemente."""
        conn = conectar()
        if not conn:
            return []
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT idjornada, nombre FROM jornadas ORDER BY idjornada DESC")
                return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener jornadas: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def obtener_puntos_venta():
        """Obtiene la lista de puntos de venta."""
        conn = conectar()
        if not conn:
            return []
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT idpunto, nombre FROM puntos_venta ORDER BY nombre")
                return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener puntos de venta: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def obtener_productos():
        """Obtiene la lista de productos."""
        conn = conectar()
        if not conn:
            return []
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT idproductos, nombre FROM productos ORDER BY nombre")
                return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener productos: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def obtener_resumen_cajas(idjornada=None):
        """
        Migrado de /reporte (reporte_cajas)
        Recaudación acumulada por punto de venta para una jornada.
        """
        conn = conectar()
        if not conn:
            return [], "Sin Conexión", 0

        try:
            with conn.cursor() as cursor:
                # Si no se indica jornada, tomar la última activa o más reciente
                if not idjornada:
                    cursor.execute("SELECT idjornada, nombre FROM jornadas ORDER BY idjornada DESC LIMIT 1")
                    jornada = cursor.fetchone()
                    if not jornada:
                        return [], "Sin Jornada", 0
                    idjornada = jornada[0] if isinstance(jornada, tuple) else jornada["idjornada"]
                    jornada_nombre = jornada[1] if isinstance(jornada, tuple) else jornada["nombre"]
                else:
                    cursor.execute("SELECT nombre FROM jornadas WHERE idjornada = %s", (idjornada,))
                    j = cursor.fetchone()
                    jornada_nombre = (j[0] if isinstance(j, tuple) else j["nombre"]) if j else "Desconocida"

                # Consulta de Recaudación Real por Caja
                sql = """
                    SELECT 
                        p.nombre AS punto,
                        COALESCE(SUM(d.subtotal), 0) AS total
                    FROM ventas v
                    JOIN ventas_detalle d ON d.idventa = v.idventa
                    JOIN puntos_venta p ON p.idpunto = v.idpunto
                    WHERE v.idjornada = %s
                    GROUP BY p.nombre
                    ORDER BY p.nombre
                """
                cursor.execute(sql, (idjornada,))
                cajas = cursor.fetchall()

                # Calcular total general
                total_general = sum(c[1] if isinstance(c, tuple) else c["total"] for c in cajas)
                return cajas, jornada_nombre, total_general

        except Exception as e:
            print(f"Error en obtener_resumen_cajas: {e}")
            return [], "Error", 0
        finally:
            conn.close()

    @staticmethod
    def obtener_reporte_detalle(idjornada=None, idcaja=None, idproducto=None, desde=None, hasta=None):
        """
        Migrado de /admin/reportes (admin_reportes)
        Detalle exhaustivo de ventas según filtros aplicados.
        """
        conn = conectar()
        if not conn:
            return [], 0, "Sin Conexión"

        try:
            with conn.cursor() as cursor:
                condiciones = []
                valores = []

                if idjornada:
                    condiciones.append("v.idjornada = %s")
                    valores.append(idjornada)
                if idcaja:
                    condiciones.append("v.idpunto = %s")
                    valores.append(idcaja)
                if idproducto:
                    condiciones.append("d.idproductos = %s")
                    valores.append(idproducto)
                if desde and hasta:
                    condiciones.append("DATE(v.fecha_hora) BETWEEN %s AND %s")
                    valores.extend([desde, hasta])

                where_sql = ""
                if condiciones:
                    where_sql = "WHERE " + " AND ".join(condiciones)

                # CORRECCIÓN EN LA CONSULTA SQL:
                # - mp.modo AS modo_pago (según tu DESCRIBE)
                # - ON mp.idmodopago = vp.idmodopago (según tu clave primaria)
                query = f"""
                    SELECT
                        v.idventa,
                        v.fecha_hora,
                        j.nombre   AS jornada,
                        pto.nombre AS caja,
                        mp.modo    AS modo_pago,
                        pr.nombre  AS producto,
                        d.cortesia,
                        d.autorizado,
                        d.cantidad,
                        d.subtotal,
                        vp.importe AS importe_pago
                    FROM ventas v
                    JOIN jornadas j        ON j.idjornada = v.idjornada
                    JOIN puntos_venta pto ON pto.idpunto = v.idpunto
                    JOIN ventas_detalle d ON d.idventa = v.idventa
                    JOIN productos pr      ON pr.idproductos = d.idproductos
                    LEFT JOIN ventas_pagos vp  ON vp.idventa = v.idventa
                    LEFT JOIN modopago mp      ON mp.idmodopago = vp.idmodopago
                    {where_sql}
                    ORDER BY v.fecha_hora DESC
                """
                cursor.execute(query, valores)
                ventas = cursor.fetchall()

                total_general = sum(v[10] if isinstance(v, tuple) else (v["importe_pago"] or 0) for v in ventas)

                jornada_nombre = "Todas"
                if idjornada:
                    cursor.execute("SELECT nombre FROM jornadas WHERE idjornada = %s", (idjornada,))
                    j = cursor.fetchone()
                    if j:
                        jornada_nombre = j[0] if isinstance(j, tuple) else j["nombre"]

                return ventas, total_general, jornada_nombre

        except Exception as e:
            print(f"Error en obtener_reporte_detalle: {e}")
            return [], 0, "Error"
        finally:
            conn.close()