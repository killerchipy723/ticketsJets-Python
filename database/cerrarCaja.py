# database/cerrarCaja.py
from datetime import datetime
import pymysql
from database.conexion import conectar


def obtener_datos_cierre_caja(idjornada, idpunto):
    """Obtiene los datos consolidados para el ticket de cierre de caja."""
    conexion = conectar()
    if not conexion:
        return None, "Error al conectar con la base de datos."

    cursor = conexion.cursor(pymysql.cursors.DictCursor)

    try:
        # 1. Nombre del Punto de Venta
        cursor.execute(
            """
            SELECT nombre
            FROM puntos_venta
            WHERE idpunto = %s
        """,
            (idpunto,),
        )
        punto = cursor.fetchone()
        nombre_punto = punto["nombre"] if punto else "PUNTO DE VENTA"

        # 2. Resumen por Producto
        cursor.execute(
            """
            SELECT
                p.nombre AS producto,
                SUM(d.cantidad) AS cantidad,
                SUM(d.subtotal) AS total_producto
            FROM ventas v
            JOIN ventas_detalle d ON d.idventa = v.idventa
            JOIN productos p ON p.idproductos = d.idproductos
            WHERE v.idjornada = %s
              AND v.idpunto = %s
              AND d.cortesia = 0
            GROUP BY p.nombre
            ORDER BY p.nombre
        """,
            (idjornada, idpunto),
        )
        productos = cursor.fetchall() or []

        # 3. Totales por Forma de Pago
        cursor.execute(
            """
            SELECT mp.modo,
                   SUM(d.subtotal) AS total
            FROM ventas v
            JOIN ventas_detalle d ON d.idventa = v.idventa
            JOIN modopago mp ON mp.idmodopago = v.idmodopago
            WHERE v.idjornada = %s
              AND v.idpunto = %s
            GROUP BY mp.modo
            ORDER BY mp.modo
        """,
            (idjornada, idpunto),
        )
        totales_pago = cursor.fetchall() or []

        # 4. Total General
        cursor.execute(
            """
            SELECT COALESCE(SUM(d.subtotal), 0) AS total
            FROM ventas v
            JOIN ventas_detalle d ON d.idventa = v.idventa
            WHERE v.idjornada = %s
              AND v.idpunto = %s
        """,
            (idjornada, idpunto),
        )
        fila_total = cursor.fetchone()
        total_general = (
            float(fila_total["total"]) if fila_total and fila_total["total"] else 0.0
        )

        datos_ticket = {
            "punto": nombre_punto,
            "productos": productos,
            "totales_pago": totales_pago,
            "total_general": total_general,
            "fecha_impresion": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        }

        return datos_ticket, None

    except Exception as e:
        print(f"❌ Error al obtener datos de cierre: {e}")
        return None, str(e)
    finally:
        cursor.close()
        conexion.close()


def cerrar_caja_bd(idjornada, idpunto):
    """Actualiza el estado de la caja a 'Cerrado' en jornadas_puntos."""
    conexion = conectar()
    if not conexion:
        return False, "Error al conectar con la base de datos."

    cursor = conexion.cursor()

    try:
        sql = """
            UPDATE jornadas_puntos
            SET estado = 'Cerrado'
            WHERE idjornada = %s AND idpunto = %s
        """
        cursor.execute(sql, (idjornada, idpunto))
        conexion.commit()

        return True, "Caja cerrada correctamente en el sistema."

    except Exception as e:
        conexion.rollback()
        print(f"❌ Error al cerrar caja: {e}")
        return False, f"Error al actualizar la caja: {e}"
    finally:
        cursor.close()
        conexion.close()