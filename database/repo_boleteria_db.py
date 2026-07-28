from database.conexion import conectar
import pymysql

class ModelReportesBoleteria:

    @staticmethod
    def obtener_jornadas():
        """Obtiene todas las jornadas ordenadas de la más reciente a la más antigua."""
        conexion = None
        cursor = None
        try:
            conexion = conectar()
            cursor = conexion.cursor(pymysql.cursors.DictCursor)
            cursor.execute("""
                SELECT idjornada, nombre
                FROM jornadas
                ORDER BY idjornada DESC
            """)
            return cursor.fetchall()
        except Exception as e:
            print("ERROR AL OBTENER JORNADAS:", e)
            return []
        finally:
            if cursor: cursor.close()
            if conexion: conexion.close()

    @staticmethod
    def obtener_jornada_por_id(idjornada):
        """Obtiene el nombre de una jornada específica."""
        conexion = None
        cursor = None
        try:
            conexion = conectar()
            cursor = conexion.cursor(pymysql.cursors.DictCursor)
            cursor.execute("""
                SELECT nombre
                FROM jornadas
                WHERE idjornada = %s
            """, (idjornada,))
            return cursor.fetchone()
        except Exception as e:
            print("ERROR AL OBTENER JORNADA:", e)
            return None
        finally:
            if cursor: cursor.close()
            if conexion: conexion.close()

    @staticmethod
    def obtener_usuarios_boleteria():
        """Obtiene los usuarios con rol 'Boleteria'."""
        conexion = None
        cursor = None
        try:
            conexion = conectar()
            cursor = conexion.cursor(pymysql.cursors.DictCursor)
            cursor.execute("""
                SELECT idusuarios, nombre
                FROM usuarios
                WHERE rol = 'Boleteria'
                ORDER BY nombre
            """)
            return cursor.fetchall()
        except Exception as e:
            print("ERROR AL OBTENER USUARIOS BOLETERIA:", e)
            return []
        finally:
            if cursor: cursor.close()
            if conexion: conexion.close()

    @staticmethod
    def obtener_operadores_boletería():
        """Alias para compatibilidad con la vista."""
        return ModelReportesBoleteria.obtener_usuarios_boleteria()

    @staticmethod
    def obtener_sectores():
        """Obtiene todos los sectores de entradas."""
        conexion = None
        cursor = None
        try:
            conexion = conectar()
            cursor = conexion.cursor(pymysql.cursors.DictCursor)
            cursor.execute("""
                SELECT idsector, nombre
                FROM sectores_entradas
                ORDER BY nombre
            """)
            return cursor.fetchall()
        except Exception as e:
            print("ERROR AL OBTENER SECTORES:", e)
            return []
        finally:
            if cursor: cursor.close()
            if conexion: conexion.close()

    @staticmethod
    def obtener_reporte_boleteria_compacto(idjornada):
        """Obtiene la recaudación agrupada por punto/usuario para una jornada."""
        conexion = None
        cursor = None
        try:
            conexion = conectar()
            cursor = conexion.cursor(pymysql.cursors.DictCursor)
            
            cursor.execute("""
                SELECT 
                    u.nombre AS punto,
                    COALESCE(SUM(v.total), 0) AS total
                FROM ventas_entradas v
                INNER JOIN usuarios u ON u.idusuarios = v.idusuario
                WHERE v.idjornada = %s
                  AND v.estado = 'OK'
                GROUP BY u.idusuarios
                ORDER BY u.nombre
            """, (idjornada,))
            cajas = cursor.fetchall()

            cursor.execute("""
                SELECT COALESCE(SUM(total), 0) AS total
                FROM ventas_entradas
                WHERE idjornada = %s
                  AND estado = 'OK'
            """, (idjornada,))
            resultado_total = cursor.fetchone()
            total_general = resultado_total["total"] if resultado_total else 0

            return cajas, total_general
        except Exception as e:
            print("ERROR REPORTE BOLETERIA COMPACTO:", e)
            return [], 0
        finally:
            if cursor: cursor.close()
            if conexion: conexion.close()

    @staticmethod
    def obtener_reporte_boleteria_detallado(idjornada=None, idusuario=None, idsector=None):
        """
        Obtiene las ventas y calcula tanto el total general como el desglose por medio de pago.
        Retorna: (ventas, total_general, desglose_pagos)
        """
        conexion = None
        cursor = None
        try:
            conexion = conectar()
            cursor = conexion.cursor(pymysql.cursors.DictCursor)

            query = """
                SELECT
                    COALESCE(v.fecha_emision, '') AS fecha,
                    COALESCE(c.apenomb, 'Consumidor Final') AS cliente,
                    COALESCE(m.modo, 'Efectivo') AS modo_pago,
                    COALESCE(v.total, 0) AS importe,
                    COALESCE(j.nombre, '') AS jornada,
                    COALESCE(u.nombre, '') AS usuario
                FROM ventas_entradas v
                LEFT JOIN jornadas j ON j.idjornada = v.idjornada
                LEFT JOIN usuarios u ON u.idusuarios = v.idusuario
                JOIN clientes c ON c.idclientes = v.cliente
                JOIN modopago m ON m.idmodopago = v.idmodopago
                WHERE v.estado = 'OK'
            """

            params = []

            if idjornada:
                query += " AND v.idjornada = %s"
                params.append(int(idjornada))

            if idusuario:
                query += " AND v.idusuario = %s"
                params.append(int(idusuario))

            query += " ORDER BY v.fecha_emision DESC"

            cursor.execute(query, params)
            ventas = cursor.fetchall()

            total_general = 0.0
            desglose_pagos = {}

            if ventas:
                for v in ventas:
                    imp = float(v.get("importe", 0))
                    modo = str(v.get("modo_pago", "Efectivo")).strip() or "Efectivo"
                    
                    total_general += imp
                    desglose_pagos[modo] = desglose_pagos.get(modo, 0.0) + imp

            return ventas, total_general, desglose_pagos
        except Exception as e:
            print("ERROR REPORTE BOLETERIA DETALLADO:", e)
            return [], 0, {}
        finally:
            if cursor: cursor.close()
            if conexion: conexion.close()

    @staticmethod
    def obtener_reporte_detalle_boleteria(idjornada=None, idusuario=None, idsector=None, **kwargs):
        """
        Alias compatible con la vista view_reporte_boleteria.py.
        """
        return ModelReportesBoleteria.obtener_reporte_boleteria_detallado(
            idjornada=idjornada, 
            idusuario=idusuario, 
            idsector=idsector
        )

# Alias para la clase por si se importa con otro nombre
RepoBoleteria = ModelReportesBoleteria