# database/boleteria.py
import pymysql
from database.conexion import conectar
from sesion import Sesion





def _extraer_idjornada(idjornada=None):
    """
    Extrae de forma limpia y segura el idjornada (entero).
    Revisa el parámetro recibido, o en su defecto examina Sesion.datos / Sesion._datos.
    """
    # 1. Si ya nos pasaron algo directo en la llamada
    if idjornada is not None:
        if isinstance(idjornada, dict):
            idjornada = idjornada.get("idjornada") or idjornada.get("id") or idjornada.get("id_jornada")
        
        try:
            if idjornada is not None:
                return int(idjornada)
        except (ValueError, TypeError):
            pass

    # 2. Si es None o falló, recurrimos a la estructura de Sesion (igual que en ventas.py)
    datos = {}
    if hasattr(Sesion, "datos") and isinstance(Sesion.datos, dict):
        datos = Sesion.datos
    elif hasattr(Sesion, "_datos") and isinstance(Sesion._datos, dict):
        datos = Sesion._datos
    elif hasattr(Sesion, "obtener") and callable(Sesion.obtener):
        res = Sesion.obtener()
        if isinstance(res, dict): 
            datos = res

    # Buscar la clave idjornada (o id) en los datos de la sesión
    val = datos.get("idjornada") or datos.get("id_jornada") or datos.get("id")

    # Intentar como atributo de la clase o instancia
    if val is None and hasattr(Sesion, "idjornada"):
        attr = getattr(Sesion, "idjornada")
        val = attr() if callable(attr) else attr

    if val is not None:
        try:
            return int(val)
        except (ValueError, TypeError):
            return None

    return None


def obtener_datos_boleteria_home(idjornada, idpunto=None):
    """
    Obtiene la información inicial para la pantalla de Boletería:
    sectores activos, modos de pago, total recaudado, cantidad de entradas y estado de la caja.
    """
    idjornada_int = _extraer_idjornada(idjornada)
    if idjornada_int is None:
        return None, "No se pudo determinar el ID de la jornada."

    conexion = conectar()
    if not conexion:
        return None, "Error de conexión con la base de datos."

    cursor = conexion.cursor(pymysql.cursors.DictCursor)

    try:
        # 1. Verificar estado de la caja (cerrada / abierta)
        cerrado_boleteria = False
        if idpunto:
            cursor.execute("""
                SELECT estado FROM jornadas_puntos 
                WHERE idjornada = %s AND idpunto = %s
                ORDER BY idjornada DESC LIMIT 1
            """, (idjornada_int, idpunto))
            row_estado = cursor.fetchone()
            if row_estado and row_estado["estado"].lower() == "cerrado":
                cerrado_boleteria = True

        # 2. Modos de Pago
        cursor.execute("""
            SELECT idmodopago, modo
            FROM modopago
            ORDER BY idmodopago ASC
        """)
        modopago = cursor.fetchall()

        # 3. Sectores de Entradas para la Jornada
        cursor.execute("""
            SELECT idsector, nombre, precio
            FROM sectores_entradas
            WHERE idjornada = %s
              AND LOWER(estado) = 'activo'
            ORDER BY nombre
        """, (idjornada_int,))
        sectores = cursor.fetchall()

        # 4. Recaudación Total en Entradas
        cursor.execute("""
            SELECT COALESCE(SUM(total), 0) AS total
            FROM ventas_entradas
            WHERE idjornada = %s
              AND estado = 'OK'
        """, (idjornada_int,))
        row_recaudacion = cursor.fetchone()
        recaudacion = row_recaudacion["total"] if row_recaudacion else 0

        # 5. Total de Entradas Vendidas (Cantidad)
        cursor.execute("""
            SELECT COALESCE(SUM(d.cantidad), 0) AS total
            FROM ventas_entradas_detalle d
            JOIN ventas_entradas v ON v.idventa = d.idventa
            WHERE v.idjornada = %s
              AND v.estado = 'OK'
        """, (idjornada_int,))
        row_entradas = cursor.fetchone()
        entradas_vendidas = row_entradas["total"] if row_entradas else 0

        return {
            "modopago": modopago,
            "sectores": sectores,
            "recaudacion": float(recaudacion),
            "entradas_vendidas": int(entradas_vendidas),
            "cerrado_boleteria": cerrado_boleteria
        }, None

    except Exception as e:
        print(f"❌ Error en obtener_datos_boleteria_home: {e}")
        return None, f"Error en base de datos: {e}"
    finally:
        cursor.close()
        conexion.close()


def registrar_venta_entrada_db(idusuario, idjornada, idcliente, idsector, cantidad, total, pagos):
    """
    Registra la venta de entradas de forma transaccional.
    pagos es una lista de diccionarios con el desglose de pago(s):
    [{'idmodopago': int, 'importe': float}]
    """
    idjornada_int = _extraer_idjornada(idjornada)
    if idjornada_int is None:
        return False, "No se pudo determinar el ID de la jornada."

    conexion = conectar()
    if not conexion:
        return False, "Error de conexión con la base de datos."

    cursor = conexion.cursor(pymysql.cursors.DictCursor)

    try:
        conexion.begin()

        # 1. Validar coincidencia de suma de pagos contra el total
        suma_pagos = round(sum(float(p["importe"]) for p in pagos), 2)
        if round(float(total), 2) != suma_pagos:
            raise Exception("La suma de los pagos no coincide con el total de la venta.")

        idmodopago_venta = pagos[0]["idmodopago"] if len(pagos) == 1 else None

        # 2. Insertar Cabecera en ventas_entradas
        sql_cabecera = """
            INSERT INTO ventas_entradas
            (idjornada, idusuario, cliente, idmodopago, total, estado)
            VALUES (%s, %s, %s, %s, %s, 'OK')
        """
        cursor.execute(sql_cabecera, (idjornada_int, idusuario, idcliente, idmodopago_venta, total))
        idventa = cursor.lastrowid

        # 3. Obtener precio unitario del sector
        cursor.execute("""
            SELECT precio
            FROM sectores_entradas
            WHERE idsector = %s AND LOWER(estado) = 'activo'
            LIMIT 1
        """, (idsector,))
        sector = cursor.fetchone()

        if not sector:
            raise Exception("El sector seleccionado no existe o está inactivo.")

        precio = float(sector["precio"])
        subtotal = round(precio * cantidad, 2)

        # 4. Insertar Detalle
        sql_detalle = """
            INSERT INTO ventas_entradas_detalle
            (idventa, idsector, cantidad, precio_unitario, subtotal)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql_detalle, (idventa, idsector, cantidad, precio, subtotal))

        # 5. Insertar Desglose de Pagos
        sql_pago = """
            INSERT INTO ventas_entradas_pagos
            (idventa, idmodopago, importe)
            VALUES (%s, %s, %s)
        """
        for p in pagos:
            cursor.execute(sql_pago, (idventa, p["idmodopago"], p["importe"]))

        conexion.commit()
        return True, {"idventa": idventa, "msg": "Entrada emitida correctamente"}

    except Exception as e:
        print(f"❌ Error al registrar venta de entrada: {e}")
        if conexion:
            conexion.rollback()
        return False, str(e)
    finally:
        cursor.close()
        conexion.close()


def cerrar_caja_boleteria_db(idjornada, idusuario, idpunto=None):
    idjornada_int = _extraer_idjornada(idjornada)
    if idjornada_int is None:
        return False, "No se pudo determinar el ID de la jornada."

    conexion = conectar()
    if not conexion:
        return False, "Error de conexión con la base de datos."

    cursor = conexion.cursor(pymysql.cursors.DictCursor)

    try:
        # Extraer idpunto seguro sin instanciar la clase de forma imprevista
        if not idpunto:
            if hasattr(Sesion, "idpunto"):
                idpunto = getattr(Sesion, "idpunto")
            elif hasattr(Sesion, "datos") and isinstance(Sesion.datos, dict):
                idpunto = Sesion.datos.get("idpunto")

        conexion.begin()

        if idpunto:
            sql = """
                UPDATE jornadas_puntos 
                SET estado = 'Cerrado',
                    fecha_cierre = NOW()
                WHERE idjornada = %s 
                  AND idpunto = %s 
                  AND estado = 'Abierto'
            """
            cursor.execute(sql, (idjornada_int, idpunto))
        else:
            sql = """
                UPDATE jornadas_puntos
                SET estado = 'Cerrado',
                    fecha_cierre = NOW()
                WHERE idjornada = %s 
                  AND estado = 'Abierto'
            """
            cursor.execute(sql, (idjornada_int,))

        if cursor.rowcount == 0:
            conexion.rollback()
            return False, "La caja de boletería ya se encontraba cerrada o no existe una apertura activa."

        conexion.commit()
        return True, "Caja de boletería cerrada correctamente."

    except Exception as e:
        print(f"❌ Error al cerrar caja de boletería: {e}")
        if conexion:
            conexion.rollback()
        return False, f"Error al cerrar la caja: {str(e)}"
    finally:
        cursor.close()
        conexion.close()


#--------------------------------------------- Tickets de Venta de Entrada -------------------------

def obtener_datos_ticket_venta_db(idventa):
    """
    Obtiene los datos completos de una venta de entrada para imprimir/visualizar el ticket.
    """
    conexion = conectar()
    if not conexion:
        return None, "Error de conexión con la base de datos."

    cursor = conexion.cursor(pymysql.cursors.DictCursor)

    try:
        cursor.execute("""
            SELECT 
                v.idventa,
                v.fecha_emision,
                v.total,
                j.nombre AS jornada,
                u.operador AS operador,
                c.apenomb AS cliente_nombre,
                c.dni AS cliente_dni,
                c.cuil AS cliente_cuil
            FROM ventas_entradas v
            JOIN jornadas j ON j.idjornada = v.idjornada
            JOIN usuarios u ON u.idusuarios = v.idusuario
            LEFT JOIN clientes c ON c.idclientes = v.cliente
            WHERE v.idventa = %s
        """, (idventa,))
        cabecera = cursor.fetchone()

        if not cabecera:
            return None, "No se encontró la venta especificada."

        cursor.execute("""
            SELECT 
                s.nombre AS sector,
                d.cantidad,
                d.precio_unitario,
                d.subtotal
            FROM ventas_entradas_detalle d
            JOIN sectores_entradas s ON s.idsector = d.idsector
            WHERE d.idventa = %s
        """, (idventa,))
        detalles = cursor.fetchall()

        cursor.execute("""
            SELECT 
                m.modo,
                p.importe
            FROM ventas_entradas_pagos p
            JOIN modopago m ON m.idmodopago = p.idmodopago
            WHERE p.idventa = %s
        """, (idventa,))
        pagos = cursor.fetchall()

        return {
            "cabecera": cabecera,
            "detalles": detalles,
            "pagos": pagos
        }, None

    except Exception as e:
        print(f"❌ Error en obtener_datos_ticket_venta_db: {e}")
        return None, str(e)
    finally:
        cursor.close()
        conexion.close()


#--------------------------------------------- Tickets de CIERRE ----------------------------------

def obtener_datos_ticket_cierre(idjornada):
    """
    Obtiene el resumen por sector y por forma de pago para la jornada activa.
    """
    idjornada_int = _extraer_idjornada(idjornada)
    if idjornada_int is None:
        return None, "ID de jornada no válido o ausente."

    conexion = conectar()
    if not conexion:
        return None, "Error de conexión."

    cursor = conexion.cursor(pymysql.cursors.DictCursor)

    try:
        # Resumen por Sector
        cursor.execute("""
            SELECT s.nombre AS sector,
                   SUM(d.cantidad) AS cantidad,
                   SUM(d.subtotal) AS total
            FROM ventas_entradas v
            JOIN ventas_entradas_detalle d ON d.idventa = v.idventa
            JOIN sectores_entradas s ON s.idsector = d.idsector
            WHERE v.idjornada = %s
              AND v.estado = 'OK'
            GROUP BY s.nombre
            ORDER BY s.nombre
        """, (idjornada_int,))
        sectores = cursor.fetchall()

        # Resumen por Forma de Pago
        cursor.execute("""
            SELECT m.modo,
                   SUM(p.importe) AS total
            FROM ventas_entradas_pagos p
            JOIN ventas_entradas v ON v.idventa = p.idventa
            JOIN modopago m ON m.idmodopago = p.idmodopago
            WHERE v.idjornada = %s
              AND v.estado = 'OK'
            GROUP BY m.modo
            ORDER BY m.modo
        """, (idjornada_int,))
        pagos = cursor.fetchall()

        # Total General
        cursor.execute("""
            SELECT COALESCE(SUM(total), 0) AS total
            FROM ventas_entradas
            WHERE idjornada = %s
              AND estado = 'OK'
        """, (idjornada_int,))
        row_total = cursor.fetchone()
        total_general = row_total["total"] if row_total else 0

        return {
            "sectores": sectores,
            "pagos": pagos,
            "total_general": float(total_general)
        }, None

    except Exception as e:
        print(f"❌ Error en obtener_datos_ticket_cierre: {e}")
        return None, str(e)
    finally:
        cursor.close()
        conexion.close()


def obtener_reporte_boleteria_detallado(idjornada=None, idusuario=None, idsector=None):
    """
    Permite filtrar por jornada, usuario y sector de boletería.
    """
    conexion = conectar()
    if not conexion:
        return None, "Error de conexión."

    cursor = conexion.cursor(pymysql.cursors.DictCursor)

    try:
        query = """
            SELECT
                v.fecha_emision,
                j.nombre  AS jornada,
                u.nombre  AS usuario,
                s.nombre  AS sector,
                d.cantidad,
                d.precio_unitario,
                d.subtotal
            FROM ventas_entradas v
            JOIN ventas_entradas_detalle d ON d.idventa = v.idventa
            JOIN jornadas j ON j.idjornada = v.idjornada
            JOIN sectores_entradas s ON s.idsector = d.idsector
            JOIN usuarios u ON u.idusuarios = v.idusuario
            WHERE v.estado = 'OK'
        """
        params = []

        if idjornada:
            idjornada_int = _extraer_idjornada(idjornada)
            if idjornada_int:
                query += " AND v.idjornada = %s"
                params.append(idjornada_int)

        if idusuario:
            query += " AND v.idusuario = %s"
            params.append(int(idusuario))

        if idsector:
            query += " AND d.idsector = %s"
            params.append(int(idsector))

        query += " ORDER BY v.fecha_emision DESC"

        cursor.execute(query, params)
        ventas = cursor.fetchall()

        total_general = sum(float(v["subtotal"]) for v in ventas) if ventas else 0.0

        return {
            "ventas": ventas,
            "total_general": total_general
        }, None

    except Exception as e:
        print(f"❌ Error en obtener_reporte_boleteria_detallado: {e}")
        return None, str(e)
    finally:
        cursor.close()
        conexion.close()