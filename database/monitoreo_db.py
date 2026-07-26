# database/monitoreo_db.py
import pymysql
from database.conexion import conectar

def obtener_datos_monitoreo():
    """
    Retorna la jornada activa y la lista de cajas con su estado actual y recaudación.
    """
    conexion = conectar()
    
    # Refresca el estado de la transacción para ver los cambios recientes
    conexion.commit() 
    
    cursor = conexion.cursor(pymysql.cursors.DictCursor)
    try:
        # 1. Obtener la jornada activa
        cursor.execute("SELECT idjornada, nombre FROM jornadas WHERE estado = 'Activo' LIMIT 1")
        jornada = cursor.fetchone()
        
        if not jornada:
            return None, []

        idjornada = jornada['idjornada']

        # 2. Obtener los puntos de venta y cruzarlos con la jornada activa
        query_cajas = """
            SELECT 
                pv.idpunto,
                pv.nombre AS nombre_caja,
                jp.estado AS estado_caja,
                COALESCE(SUM(v.total), 0) AS recaudacion
            FROM puntos_venta pv
            LEFT JOIN jornadas_puntos jp ON pv.idpunto = jp.idpunto AND jp.idjornada = %s
            LEFT JOIN ventas v ON v.idpunto = pv.idpunto 
                               AND v.idjornada = %s 
                               AND v.estado = 'OK'
            GROUP BY pv.idpunto, pv.nombre, jp.estado
            ORDER BY pv.nombre
        """
        cursor.execute(query_cajas, (idjornada, idjornada))
        cajas_db = cursor.fetchall()

        # 3. Formatear los datos para la interfaz
        cajas_formateadas = []
        for c in cajas_db:
            es_activa = (c['estado_caja'] == 'Abierto')
            cajas_formateadas.append({
                "nombre": c['nombre_caja'],
                "activa": es_activa,
                "operador": "Asignado" if es_activa else "Sin Asignar",
                "recaudacion": float(c['recaudacion'])
            })

        return jornada, cajas_formateadas

    except Exception as e:
        print(f"❌ Error en obtener_datos_monitoreo: {e}")
        return None, []
    finally:
        cursor.close()
        conexion.close()


def finalizar_jornada_activa(idjornada):
    """Cierra la jornada en la base de datos."""
    conexion = conectar()
    cursor = conexion.cursor()
    try:
        cursor.execute("UPDATE jornadas SET estado = 'Finalizado' WHERE idjornada = %s", (idjornada,))
        conexion.commit()
        return True
    except Exception as e:
        conexion.rollback()
        print(f"❌ Error al finalizar jornada: {e}")
        return False
    finally:
        cursor.close()
        conexion.close()