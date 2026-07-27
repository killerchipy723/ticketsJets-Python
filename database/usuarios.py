# database/usuarios.py
import pymysql
from database.conexion import conectar
from utils.network import obtener_mac_local


def iniciar_sesion(usuario, password):
    """Valida credenciales, asignación de equipo (MAC), permisos,

    jornada activa y estado de caja en la tabla jornadas_puntos.
    """
    conexion = conectar()
    if not conexion:
        return None, "Error al conectar con la base de datos."

    cursor = conexion.cursor(pymysql.cursors.DictCursor)

    try:
        equipo_mac = obtener_mac_local()

        # ==========================================================
        # 1️⃣ VALIDAR USUARIO Y CONTRASEÑA
        # ==========================================================
        sql_usuario = """
            SELECT idusuarios, nombre, rol, estado, operador
            FROM usuarios
            WHERE LOWER(nombre) = LOWER(%s) 
              AND clave = %s
        """
        cursor.execute(sql_usuario, (usuario, password))
        user = cursor.fetchone()

        if not user:
            return None, "Usuario o contraseña incorrectos."

        if (user["estado"] or "").strip().lower() != "activo":
            return None, "El usuario se encuentra inactivo."

        # ==========================================================
        # CASO ADMINISTRADOR (Acceso directo)
        # ==========================================================
        rol_limpio = (user["rol"] or "").strip().lower()
        if rol_limpio in ["administrador", "admin"]:
            datos_sesion = {
                "id": user["idusuarios"],
                "nombre": user["nombre"],
                "rol": user["rol"],
                "equipo": equipo_mac,
                "operador": user["operador"],
                "idpunto": None,
                "punto": None,
                "idjornada": None,
            }
            return datos_sesion, None

        # ==========================================================
        # 2️⃣ VALIDAR PUNTO DE VENTA (POR MAC)
        # ==========================================================
        sql_punto = """
            SELECT idpunto, nombre
            FROM puntos_venta
            WHERE LOWER(idequipo) = LOWER(%s) 
              AND LOWER(estado) = 'activo'
        """
        cursor.execute(sql_punto, (equipo_mac,))
        punto = cursor.fetchone()

        if not punto:
            return (
                None,
                f"Este equipo (MAC: {equipo_mac}) no está habilitado como"
                " punto de venta.",
            )

        # ==========================================================
        # 3️⃣ VALIDAR PERMISO USUARIO ↔ PUNTO DE VENTA
        # ==========================================================
        sql_permiso = """
            SELECT 1
            FROM usuarios_puntos
            WHERE idusuario = %s 
              AND idpunto = %s
            LIMIT 1
        """
        cursor.execute(sql_permiso, (user["idusuarios"], punto["idpunto"]))

        if not cursor.fetchone():
            return (
                None,
                "Usuario no autorizado para operar en este punto de venta.",
            )

        # ==========================================================
        # 4️⃣ VALIDAR JORNADA ACTIVA GENERAL
        # ==========================================================
        sql_jornada = """
            SELECT idjornada, nombre 
            FROM jornadas 
            WHERE LOWER(estado) = 'activo' 
            LIMIT 1
        """
        cursor.execute(sql_jornada)
        jornada = cursor.fetchone()

        if not jornada:
            return (
                None,
                (
                    "No hay ninguna jornada activa en el sistema. Contacte a"
                    " un Administrador."
                ),
            )

        idjornada = jornada["idjornada"]

        # ==========================================================
        # 5️⃣ VALIDAR ESTADO DE CAJA EN 'jornadas_puntos'
        # ==========================================================
        sql_caja = """
            SELECT estado
            FROM jornadas_puntos
            WHERE idjornada = %s AND idpunto = %s
            LIMIT 1
        """
        cursor.execute(sql_caja, (idjornada, punto["idpunto"]))
        caja = cursor.fetchone()

        if not caja:
            return (
                None,
                (
                    "El punto de venta no tiene un estado asignado para la"
                    " jornada actual."
                ),
            )

        estado_caja = (caja["estado"] or "").strip().lower()

        if estado_caja == "cerrado":
            return (
                None,
                (
                    "❌ La caja ya fue cerrada para esta jornada. No puede volver"
                    " a operar."
                ),
            )

        # ==========================================================
        # SESIÓN COMPLETADA EXITOSAMENTE
        # ==========================================================
        datos_sesion = {
            "id": user["idusuarios"],
            "nombre": user["nombre"],
            "rol": user["rol"],
            "idpunto": punto["idpunto"],
            "punto": punto["nombre"],
            "equipo": equipo_mac,
            "operador": user["operador"],
            "idjornada": idjornada,
            "nombre_jornada": jornada["nombre"],
        }

        return datos_sesion, None

    except Exception as e:
        print(f"❌ Error en iniciar_sesion: {e}")
        return None, f"Error de base de datos: {e}"

    finally:
        cursor.close()
        conexion.close()