# reports/impresion_boleteria.py
from io import BytesIO
import win32con
import win32print
import win32ui
from PIL import Image, ImageWin
import qrcode


def obtener_impresora_activa():
    """Obtiene la impresora predeterminada o la primera disponible en el sistema."""
    try:
        nombre = win32print.GetDefaultPrinter()
        if nombre:
            return nombre
    except Exception:
        pass

    try:
        impresoras = win32print.EnumPrinters(
            win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
        )
        if impresoras:
            return impresoras[0][2]
    except Exception:
        pass

    return None


def formatear_moneda(monto):
    """Convierte un número a formato de moneda ($18.000)."""
    val = float(monto or 0)
    return f"${val:,.0f}".replace(",", ".")


def imprimir_ticket_boleteria_silencioso(datos_ticket, nombre_impresora_custom=None):
    """
    Imprime el ticket de entrada de boletería copiando el formato exacto de tipografías 
    y DPI del ticket de bebidas.
    """
    hprinter = None
    hdc = None
    doc_iniciado = False
    fonts = []

    try:
        nombre_impresora = nombre_impresora_custom or obtener_impresora_activa()

        if not nombre_impresora:
            print("❌ No se encontró ninguna impresora instalada en el sistema.")
            return False

        hprinter = win32print.OpenPrinter(nombre_impresora)
        hdc = win32ui.CreateDC()
        hdc.CreatePrinterDC(nombre_impresora)

        hdc.StartDoc("TicketEntrada_TicketJets")
        doc_iniciado = True
        hdc.StartPage()

        # Escala según el DPI de la impresora (Idéntico a Bebidas)
        dpi_x = hdc.GetDeviceCaps(win32con.LOGPIXELSX) or 203
        dpi_y = hdc.GetDeviceCaps(win32con.LOGPIXELSY) or 203

        scale_x = dpi_x / 203.0
        scale_y = dpi_y / 203.0

        # Ancho imprimible
        ancho_imprimible = hdc.GetDeviceCaps(win32con.HORZRES) or int(520 * scale_x)

        # Configuración de Fuentes escaladas
        height_normal = int(32 * scale_y)
        height_destacado = int(38 * scale_y)
        height_titulo = int(46 * scale_y)

        font_normal = win32ui.CreateFont({"name": "Arial", "height": height_normal, "weight": 700})
        font_destacado = win32ui.CreateFont({"name": "Arial", "height": height_destacado, "weight": 700})
        font_titulo = win32ui.CreateFont({"name": "Arial", "height": height_titulo, "weight": 700})
        fonts = [font_normal, font_destacado, font_titulo]

        y = int(15 * scale_y)
        line_height_normal = int(38 * scale_y)
        line_height_destacado = int(44 * scale_y)
        line_height_titulo = int(54 * scale_y)

        margin_x = int(10 * scale_x)

        def escribir_linea(texto, destacado=False, titulo=False, centrado=False):
            nonlocal y
            texto_str = str(texto or "")
            if titulo:
                hdc.SelectObject(font_titulo)
                lh = line_height_titulo
            elif destacado:
                hdc.SelectObject(font_destacado)
                lh = line_height_destacado
            else:
                hdc.SelectObject(font_normal)
                lh = line_height_normal

            if centrado:
                size_x, _ = hdc.GetTextExtent(texto_str)
                x = max(margin_x, (ancho_imprimible - size_x) // 2)
            else:
                x = margin_x

            hdc.TextOut(x, y, texto_str)
            y += lh

        linea_separadora = "------------------------------------------------------------"

        cab = datos_ticket.get("cabecera", {}) if isinstance(datos_ticket, dict) else {}
        detalles = datos_ticket.get("detalles", []) if isinstance(datos_ticket, dict) else []
        pagos = datos_ticket.get("pagos", []) if isinstance(datos_ticket, dict) else []

        f_fecha = (
            cab.get("fecha_emision").strftime("%d/%m/%Y %H:%M:%S")
            if cab.get("fecha_emision")
            else ""
        )
        cliente_nombre = cab.get("cliente_nombre") or "CONSUMIDOR FINAL"
        cliente_dni = cab.get("cliente_dni") or "00000000"

        # --- CABECERA ---
        escribir_linea("TicketJets", titulo=True, centrado=True)
        escribir_linea("ENTRADA DE BOLETERIA", destacado=True, centrado=True)
        escribir_linea(linea_separadora)

        # --- DATOS ENTRADA ---
        escribir_linea(f"Jornada: {cab.get('jornada', '')}")
     
        id_v = cab.get("idventa", 0)
        escribir_linea(f"Ticket N°: #{id_v:06d}", destacado=True)
        escribir_linea(f"Fecha: {f_fecha}")
        escribir_linea(f"Operador: {cab.get('operador', '')}")
        escribir_linea(linea_separadora)

        # --- DATOS CLIENTE ---
        escribir_linea(f"Cliente: {cliente_nombre[:25]}")
        escribir_linea(f"DNI/Doc: {cliente_dni}")
        escribir_linea(linea_separadora)

        # --- DETALLE DE SECTORES ---
        for d in detalles:
            escribir_linea(f"Sector: {d.get('sector', '')[:25]}", destacado=True)
            subtotal_str = formatear_moneda(d.get("subtotal", 0))
            p_unit_str = formatear_moneda(d.get("precio_unitario", 0))
            escribir_linea(f"  {d.get('cantidad', 1)} x {p_unit_str} = {subtotal_str}")

        escribir_linea(linea_separadora)
        total_str = formatear_moneda(cab.get("total", 0))
        escribir_linea(f"TOTAL: {total_str}", titulo=True)
        escribir_linea(linea_separadora)

        # --- FORMAS DE PAGO ---
        escribir_linea("Forma de Pago:", destacado=True)
        for pago in pagos:
            pago_str = formatear_moneda(pago.get("importe", 0))
            escribir_linea(f" - {pago.get('modo', '')}: {pago_str}")

        escribir_linea(linea_separadora)

        # --- CÓDIGO QR ---
        qr_texto = f"TICKET:{cab.get('idventa')}|DNI:{cliente_dni}|JORNADA:{cab.get('jornada','')}|TOTAL:{cab.get('total')}"
        qr = qrcode.make(qr_texto)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        buffer.seek(0)

        tamano_qr_px = int(220 * scale_x)
        img_qr = Image.open(buffer).resize((tamano_qr_px, tamano_qr_px))

        qr_x1 = max(margin_x, (ancho_imprimible - tamano_qr_px) // 2)
        qr_y1 = y
        qr_x2 = qr_x1 + tamano_qr_px
        qr_y2 = qr_y1 + tamano_qr_px

        dibujo_qr = ImageWin.Dib(img_qr)
        dibujo_qr.draw(hdc.GetHandleOutput(), (qr_x1, qr_y1, qr_x2, qr_y2))
        y += tamano_qr_px + int(20 * scale_y)

        # --- PIE DE PÁGINA ---
        escribir_linea("¡Gracias por su compra!", destacado=True, centrado=True)
        escribir_linea("Conserve este ticket", centrado=True)

        y += int(80 * scale_y)
        escribir_linea(".", centrado=False)

        hdc.EndPage()
        hdc.EndDoc()
        doc_iniciado = False
        return True

    except Exception as e:
        print(f"❌ Error al imprimir ticket de boletería: {e}")
        if hdc and doc_iniciado:
            try:
                hdc.AbortDoc()
            except Exception:
                pass
        return False

    finally:
        for f in fonts:
            try:
                f.DeleteObject()
            except Exception:
                pass
        if hdc:
            try:
                hdc.DeleteDC()
            except Exception:
                pass
        if hprinter:
            try:
                win32print.ClosePrinter(hprinter)
            except Exception:
                pass


def imprimir_ticket_cierre_silencioso(idjornada, session_data=None, *args, **kwargs):
    """
    Imprime el resumen de cierre de caja leyendo la base de datos con el mismo 
    formato de fuentes y DPI del ticket de ventas. Utiliza session_data como 
    respaldo directo para los datos del operador y la jornada.
    """
    hprinter = None
    hdc = None
    doc_iniciado = False
    fonts = []

    try:
        from database.boleteria_db import obtener_datos_ticket_cierre

        if isinstance(idjornada, dict):
            # Si idjornada es un diccionario de sesión pasado como primer argumento
            if not session_data:
                session_data = idjornada
            idjornada = idjornada.get('idjornada') or idjornada.get('id')

        datos_cierre, err = obtener_datos_ticket_cierre(idjornada)
        if err or not datos_cierre:
            print(f"❌ Error al obtener datos de cierre: {err}")
            return False

        nombre_impresora = obtener_impresora_activa()

        if not nombre_impresora:
            print("❌ No se encontró ninguna impresora instalada en el sistema.")
            return False

        hprinter = win32print.OpenPrinter(nombre_impresora)
        hdc = win32ui.CreateDC()
        hdc.CreatePrinterDC(nombre_impresora)

        hdc.StartDoc("CierreBoleteria_TicketJets")
        doc_iniciado = True
        hdc.StartPage()

        dpi_x = hdc.GetDeviceCaps(win32con.LOGPIXELSX) or 203
        dpi_y = hdc.GetDeviceCaps(win32con.LOGPIXELSY) or 203

        scale_x = dpi_x / 203.0
        scale_y = dpi_y / 203.0

        ancho_imprimible = hdc.GetDeviceCaps(win32con.HORZRES) or int(520 * scale_x)

        height_normal = int(32 * scale_y)
        height_destacado = int(38 * scale_y)
        height_titulo = int(46 * scale_y)

        font_normal = win32ui.CreateFont({"name": "Arial", "height": height_normal, "weight": 700})
        font_destacado = win32ui.CreateFont({"name": "Arial", "height": height_destacado, "weight": 700})
        font_titulo = win32ui.CreateFont({"name": "Arial", "height": height_titulo, "weight": 700})
        fonts = [font_normal, font_destacado, font_titulo]

        y = int(15 * scale_y)
        line_height_normal = int(38 * scale_y)
        line_height_destacado = int(44 * scale_y)
        line_height_titulo = int(54 * scale_y)

        margin_x = int(10 * scale_x)

        def escribir_linea(texto, destacado=False, titulo=False, centrado=False):
            nonlocal y
            texto_str = str(texto or "")
            if titulo:
                hdc.SelectObject(font_titulo)
                lh = line_height_titulo
            elif destacado:
                hdc.SelectObject(font_destacado)
                lh = line_height_destacado
            else:
                hdc.SelectObject(font_normal)
                lh = line_height_normal

            if centrado:
                size_x, _ = hdc.GetTextExtent(texto_str)
                x = max(margin_x, (ancho_imprimible - size_x) // 2)
            else:
                x = margin_x

            hdc.TextOut(x, y, texto_str)
            y += lh

        linea_separadora = "------------------------------------------------------------"

        # --- EXTRACCIÓN ROBUSTA DE SESIÓN Y BASE DE DATOS ---
        sess = session_data if isinstance(session_data, dict) else {}

        # 1. Obtención de Jornada (Busca en BD primero, luego en session_data)
        nombre_jornada = (
            datos_cierre.get("jornada")
            or datos_cierre.get("nombre_jornada")
            or sess.get("jornada")
            or sess.get("nombre_jornada")
            or sess.get("jornada_nombre")
            or (f"Jornada #{idjornada}" if idjornada else "General")
        )

        # 2. Obtención de Operador (Busca en BD primero, luego en session_data)
        operador = (
            datos_cierre.get("operador")
            or datos_cierre.get("usuario")
            or sess.get("operador")
            or sess.get("usuario")
            or sess.get("nombre_usuario")
            or sess.get("nombre")
            or "S/D"
        )

        # 3. Fecha y hora de emisión
        fecha_emision = datos_cierre.get("fecha_cierre") or datos_cierre.get("fecha")
        if hasattr(fecha_emision, "strftime"):
            f_fecha = fecha_emision.strftime("%d/%m/%Y %H:%M:%S")
        else:
            from datetime import datetime
            f_fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        sectores = datos_cierre.get("sectores", [])
        pagos = datos_cierre.get("pagos", [])
        total_general = datos_cierre.get("total_general", 0)

        # --- CABECERA ENCABEZADO ---
        escribir_linea("TicketJets", titulo=True, centrado=True)
        escribir_linea("CIERRE DE BOLETERIA", destacado=True, centrado=True)
        escribir_linea(linea_separadora)

        # DATOS DE LA JORNADA Y OPERADOR
        escribir_linea(f"Jornada: {nombre_jornada}", destacado=True)
        escribir_linea(f"Operador: {operador}")
        escribir_linea(f"Fecha: {f_fecha}")
        escribir_linea(linea_separadora)

        # --- RESUMEN POR SECTOR ---
        escribir_linea("RESUMEN POR SECTOR:", destacado=True)
        if sectores:
            for s in sectores:
                sector_nom = str(s.get("sector", ""))[:20]
                cant = s.get("cantidad", 0)
                tot_sec = formatear_moneda(s.get("total", 0))
                escribir_linea(f" - {sector_nom} (x{cant}): {tot_sec}")
        else:
            escribir_linea(" Sin ventas registradas.")

        escribir_linea(linea_separadora)

        # --- RESUMEN POR MEDIO DE PAGO ---
        escribir_linea("RESUMEN POR MEDIO DE PAGO:", destacado=True)
        if pagos:
            for p in pagos:
                modo_nom = str(p.get("modo", ""))
                tot_pago = formatear_moneda(p.get("total", 0))
                escribir_linea(f" - {modo_nom}: {tot_pago}")
        else:
            escribir_linea(" Sin pagos registrados.")

        escribir_linea(linea_separadora)

        # --- TOTAL GENERAL ---
        total_general_str = formatear_moneda(total_general)
        escribir_linea(f"TOTAL GENERAL: {total_general_str}", titulo=True)
        escribir_linea(linea_separadora)

        # --- PIE DE PÁGINA ---
        escribir_linea("Cierre de caja completado", centrado=True)
        y += int(80 * scale_y)
        escribir_linea(".", centrado=False)

        hdc.EndPage()
        hdc.EndDoc()
        doc_iniciado = False
        return True

    except Exception as e:
        print(f"❌ Error al imprimir ticket de cierre de boletería: {e}")
        if hdc and doc_iniciado:
            try:
                hdc.AbortDoc()
            except Exception:
                pass
        return False

    finally:
        for f in fonts:
            try:
                f.DeleteObject()
            except Exception:
                pass
        if hdc:
            try:
                hdc.DeleteDC()
            except Exception:
                pass
        if hprinter:
            try:
                win32print.ClosePrinter(hprinter)
            except Exception:
                pass