# database/ventas.py
import pymysql
from database.conexion import conectar
from database.productos import productos
from sesion import Sesion

# --- ESTADO GLOBAL EN MEMORIA DEL CARRITO ---
carrito = {}

def obtener_productos():
    """Retorna el catálogo de productos disponible."""
    return productos()

def obtener_modos_pago():
    """Consulta los modos de pago habilitados desde la tabla 'modopago'."""
    conexion = conectar()
    modos_default = [
        {"idmodopago": 1, "nombre": "Efectivo"},
        {"idmodopago": 2, "nombre": "Tarjeta / Posnet"},
        {"idmodopago": 3, "nombre": "Transferencia / MP"}
    ]
    
    if not conexion:
        return modos_default

    try:
        cursor = conexion.cursor(pymysql.cursors.DictCursor)
        # Consulta explícita a la tabla 'modopago' con la columna 'modo'
        cursor.execute("SELECT idmodopago, modo FROM modopago")
        filas = cursor.fetchall()
        
        if not filas:
            return modos_default

        modos_limpios = []
        for f in filas:
            id_val = f.get("idmodopago") or f.get("id") or 1
            nombre_val = f.get("modo") or f.get("nombre") or "Método Pago"
            
            modos_limpios.append({
                "idmodopago": int(id_val),
                "nombre": str(nombre_val)
            })
            
        return modos_limpios

    except Exception as e:
        print(f"⚠️ Error al obtener modos de pago desde 'modopago': {e}")
        return modos_default
    finally:
        if conexion:
            conexion.close()

def agregar_al_carrito(producto):
    """Agrega un producto o incrementa su cantidad."""
    nombre = producto["nombre"]
    precio = producto["importe"]
    idproducto = producto.get("idproductos") or producto.get("idproducto") or producto.get("id")
    
    if nombre in carrito:
        carrito[nombre]["cantidad"] += 1
    else:
        carrito[nombre] = {
            "idproducto": idproducto,
            "precio": precio,
            "cantidad": 1,
            "cortesia": False,
            "autorizado": None
        }

def modificar_cantidad(nombre, cambio):
    """Incrementa o decrementa la cantidad de un ítem."""
    if nombre in carrito:
        carrito[nombre]["cantidad"] += cambio
        if carrito[nombre]["cantidad"] <= 0:
            del carrito[nombre]

def obtener_total_carrito():
    """Calcula el monto total acumulado en el carrito (omite cortesías)."""
    total = 0.0
    for item in carrito.values():
        if not item.get("cortesia", False):
            total += item["precio"] * item["cantidad"]
    return total

def vaciar_carrito():
    """Limpia todos los productos del carrito."""
    carrito.clear()

def obtener_id_sesion(clave, valor_defecto=1):
    """Auxiliar para obtener IDs numéricos de la sesión activa."""
    if hasattr(Sesion, "datos") and isinstance(Sesion.datos, dict):
        if clave in Sesion.datos and Sesion.datos[clave]:
            return Sesion.datos[clave]
    if hasattr(Sesion, clave):
        val = getattr(Sesion, clave)
        val = val() if callable(val) else val
        if val: return val
    return valor_defecto

def obtener_recaudacion_acumulada_jornada():
    """
    Suma todas las ventas OK de la jornada activa para el usuario/punto actual.
    Evita que el monto acumulado vuelva a $0 si se reinicia la aplicación.
    """
    conexion = conectar()
    if not conexion:
        return 0.0

    try:
        cursor = conexion.cursor()
        
        # ✅ Usamos la función corregida que contiene los IDs reales
        sesion = obtener_datos_sesion_actual()
        idjornada = sesion.get("idjornada", 1)
        idusuario = sesion.get("idusuario", 1)

        print(f"🔍 Consultando recaudación para idjornada: {idjornada}, idusuario: {idusuario}")

        sql = """
            SELECT COALESCE(SUM(total), 0.00) 
            FROM ventas 
            WHERE idjornada = %s AND idusuario = %s AND estado = 'OK'
        """
        cursor.execute(sql, (idjornada, idusuario))
        resultado = cursor.fetchone()
        
        monto = float(resultado[0]) if resultado and resultado[0] is not None else 0.0
        print(f"💰 Recaudación acumulada hallada: ${monto}")
        return monto

    except Exception as e:
        print(f"❌ Error al consultar recaudación acumulada: {e}")
        return 0.0
    finally:
        conexion.close()

def registrar_venta(
    desgloses_pago, 
    idcliente=None, 
    observaciones="", 
    es_cortesia=False, 
    autoriza_cortesia="",
    idjornada=None,    # <-- NUEVO
    idpunto=None,      # <-- NUEVO
    idusuario=None     # <-- NUEVO
):
    """
    Procesa el cobro insertando en 'ventas', 'ventas_detalle' y 'ventas_pago'.
    Acepta pagos simples, combinados y cortesías.
    """
    if not carrito:
        return False, "El carrito está vacío.", None

    total_venta = 0.0 if es_cortesia else obtener_total_carrito()

    if not es_cortesia:
        if not desgloses_pago:
            return False, "Por favor, especifique al menos un método de pago.", None

        total_pagado = sum(float(pago["importe"]) for pago in desgloses_pago)
        if round(total_venta, 2) > round(total_pagado, 2):
            return False, f"Monto insuficiente. Total a cobrar: ${total_venta:,.2f} | Ingresado: ${total_pagado:,.2f}", None

    conexion = conectar()
    if not conexion:
        return False, "Error al conectar con la base de datos.", None

    try:
        cursor = conexion.cursor()

        # Si no nos pasan los IDs explícitos, los buscamos con el fallback habitual
        if not idjornada:
            idjornada = obtener_id_sesion("idjornada", 1)
        if not idpunto:
            idpunto = obtener_id_sesion("idpunto", 1)
        if not idusuario:
            idusuario = obtener_id_sesion("idusuario", obtener_id_sesion("id", 1))

        idmodopago_cabecera = None
        if not es_cortesia and len(desgloses_pago) == 1:
            idmodopago_cabecera = desgloses_pago[0]["idmodopago"]

        obs_final = f"CORTESIA - Auth: {autoriza_cortesia}" if es_cortesia else observaciones

        # 1. INSERT EN 'ventas'
        sql_venta = """
            INSERT INTO ventas (
                idjornada, idusuario, idpunto, idclientes, idmodopago, 
                total, descuento_total, estado, observaciones, qr_token, estado_ticket
            ) VALUES (%s, %s, %s, %s, %s, %s, 0.00, 'OK', %s, '', 'VALIDO')
        """
        cursor.execute(sql_venta, (
            idjornada, idusuario, idpunto, idcliente, idmodopago_cabecera, 
            total_venta, obs_final
        ))
        idventa = cursor.lastrowid

        # 2. INSERT EN 'ventas_detalle'
        sql_detalle = """
            INSERT INTO ventas_detalle (
                idventa, idproductos, cantidad, precio_unitario, descuento, 
                subtotal, cortesia, autorizado
            ) VALUES (%s, %s, %s, %s, 0.00, %s, %s, %s)
        """
        for item in carrito.values():
            cortesia_flag = 1 if es_cortesia else 0
            precio_u = float(item["precio"])
            subtotal = 0.0 if es_cortesia else (precio_u * int(item["cantidad"]))
            autorizado_por = autoriza_cortesia if es_cortesia else None

            cursor.execute(sql_detalle, (
                idventa, item.get("idproducto", 1), item["cantidad"], 
                precio_u, subtotal, cortesia_flag, autorizado_por
            ))

        # 3. INSERT EN 'ventas_pagos' (Si no es cortesía)
        if not es_cortesia:
            sql_pago = """
                INSERT INTO ventas_pagos (idventa, idmodopago, importe)
                VALUES (%s, %s, %s)
            """
            for pago in desgloses_pago:
                if float(pago["importe"]) > 0:
                    cursor.execute(sql_pago, (idventa, pago["idmodopago"], pago["importe"]))

        conexion.commit()

        mensaje = f"¡Venta #{idventa} procesada con éxito!\nTotal: ${total_venta:,.2f}"
        vaciar_carrito()
        
        return True, mensaje, idventa

    except Exception as e:
        conexion.rollback()
        print(f"❌ Error al guardar venta en BD: {e}")
        return False, f"Error en base de datos: {e}", None
    finally:
        cursor.close()
        conexion.close()

def obtener_datos_sesion_actual():
    """Extrae de forma limpia y segura cada campo de la Sesión activa (incluyendo IDs numéricos)."""
    datos = {}
    if hasattr(Sesion, "datos") and isinstance(Sesion.datos, dict):
        datos = Sesion.datos
    elif hasattr(Sesion, "_datos") and isinstance(Sesion._datos, dict):
        datos = Sesion._datos
    elif hasattr(Sesion, "obtener") and callable(Sesion.obtener):
        res = Sesion.obtener()
        if isinstance(res, dict): datos = res

    def obtener_valor(clave, metodo_fallback=None, valor_defecto=""):
        if clave in datos and datos[clave] is not None:
            val = datos[clave]
            if not isinstance(val, dict):
                return str(val)
        
        if metodo_fallback and hasattr(Sesion, metodo_fallback):
            attr = getattr(Sesion, metodo_fallback)
            val = attr() if callable(attr) else attr
            if val is not None and not isinstance(val, dict):
                return str(val)
                
        return valor_defecto

    def obtener_id(clave, atributo_fallback=None, valor_defecto=1):
        """Extrae un ID numérico entero de la sesión."""
        if clave in datos and datos[clave] is not None:
            try:
                return int(datos[clave])
            except (ValueError, TypeError):
                pass

        if atributo_fallback and hasattr(Sesion, atributo_fallback):
            attr = getattr(Sesion, atributo_fallback)
            val = attr() if callable(attr) else attr
            if val is not None:
                try:
                    return int(val)
                except (ValueError, TypeError):
                    pass

        return valor_defecto

    # Nombres descriptivos para la interfaz y tickets
    usuario = obtener_valor("nombre", "nombre", "Invitado")
    operador = obtener_valor("operador", "operador", usuario)
    rol = obtener_valor("rol", "rol", "Vendedor").strip().title()
    punto = obtener_valor("punto", "punto", "Punto 1")
    jornada = obtener_valor("nombre_jornada", "jornada", "Jornada Activa")
    equipo = obtener_valor("equipo", "equipo", "LOCAL")

    # ✅ IDs NUMÉRICOS PARA LA BASE DE DATOS
    idusuario = obtener_id("idusuarios", "id", 1)
    if idusuario == 1:
        idusuario = obtener_id("idusuario", "id", 1)

    idjornada = obtener_id("idjornada", "idjornada", 1)
    idpunto = obtener_id("idpunto", "idpunto", 1)

    return {
        # Cadenas de texto para visualización
        "usuario": usuario,
        "operador": operador,
        "rol": rol,
        "punto": punto,
        "jornada": jornada,
        "equipo": equipo,
        "estado_caja": "ABIERTA",
        # IDs numéricos para consultas e INSERTs en MySQL
        "idusuario": idusuario,
        "idjornada": idjornada,
        "idpunto": idpunto
    }