# impresion.py
import win32print
import win32ui
import win32con
from PIL import Image, ImageWin
import qrcode
from io import BytesIO
import subprocess
import platform

def obtener_impresora_activa():
    """Obtiene la impresora predeterminada o la primera disponible en el sistema."""
    try:
        nombre = win32print.GetDefaultPrinter()
        if nombre:
            return nombre
    except Exception:
        pass

    impresoras = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
    if impresoras:
        return impresoras[0][2]
    
    return None

def formatear_moneda(monto):
    """Convierte un número a formato de moneda argentina/latam ($18.000)."""
    val = float(monto or 0)
    return f"${val:,.0f}".replace(",", ".")

def imprimir_ticket_silencioso(datos_ticket, nombre_impresora_custom=None):
    """
    Imprime el ticket para 80mm con márgenes naturales y formato de moneda $18.000.
    """
    try:
        nombre_impresora = nombre_impresora_custom or obtener_impresora_activa()

        if not nombre_impresora:
            print("❌ No se encontró ninguna impresora instalada en el sistema.")
            return False

        print(f"🖨️ Enviando ticket a la impresora: '{nombre_impresora}'")

        hprinter = win32print.OpenPrinter(nombre_impresora)
        hdc = win32ui.CreateDC()
        hdc.CreatePrinterDC(nombre_impresora)

        hdc.StartDoc("TicketVenta_TicketJets")
        hdc.StartPage()

        # Escala según el DPI de la impresora
        dpi_x = hdc.GetDeviceCaps(win32con.LOGPIXELSX) or 203
        dpi_y = hdc.GetDeviceCaps(win32con.LOGPIXELSY) or 203

        scale_x = dpi_x / 203.0
        scale_y = dpi_y / 203.0

        # Ancho imprimible
        ancho_imprimible = hdc.GetDeviceCaps(win32con.HORZRES) or int(520 * scale_x)

        # Fuentes
        height_normal = int(32 * scale_y)
        height_destacado = int(38 * scale_y)
        height_titulo = int(46 * scale_y)

        font_normal = win32ui.CreateFont({"name": "Arial", "height": height_normal, "weight": 700})
        font_destacado = win32ui.CreateFont({"name": "Arial", "height": height_destacado, "weight": 700})
        font_titulo = win32ui.CreateFont({"name": "Arial", "height": height_titulo, "weight": 700})

        y = int(15 * scale_y)
        line_height_normal = int(38 * scale_y)
        line_height_destacado = int(44 * scale_y)
        line_height_titulo = int(54 * scale_y)

        # Margen izquierdo fijo para evitar desalineaciones con el borde físico
        margin_x = int(10 * scale_x)

        def escribir_linea(texto, destacado=False, titulo=False, centrado=False):
            nonlocal y
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
                size_x, _ = hdc.GetTextExtent(texto)
                x = max(margin_x, (ancho_imprimible - size_x) // 2)
            else:
                x = margin_x

            hdc.TextOut(x, y, texto)
            y += lh

        linea_separadora = "------------------------------------------------------------"

        # --- CABECERA ---
        escribir_linea("TicketJets", titulo=True, centrado=True)
        escribir_linea("NO VALIDO COMO FACTURA", destacado=True, centrado=True)
        escribir_linea(linea_separadora)

        # --- DATOS VENTA ---
        escribir_linea(f"Jornada: {datos_ticket['jornada']}")
        escribir_linea(f"Venta N: {datos_ticket['idventa']}", destacado=True)
        escribir_linea(f"Fecha: {datos_ticket['fecha_hora']}")
        escribir_linea(f"Operador: {datos_ticket['operador']}")

        if datos_ticket.get("es_cortesia"):
            escribir_linea(linea_separadora)
            escribir_linea("*** VENTA DE CORTESIA ***", destacado=True, centrado=True)
            escribir_linea(f"Auth: {datos_ticket.get('autorizado_cortesia')}")

        escribir_linea(linea_separadora)
        escribir_linea(f"Cliente: {datos_ticket['cliente']}")
        escribir_linea(linea_separadora)

        # --- PRODUCTOS ---
        for prod in datos_ticket['detalle']:
            escribir_linea(f"{prod['producto'][:28]}", destacado=True)
            subtotal_str = formatear_moneda(prod['subtotal'])
            escribir_linea(f"  {prod['cantidad']} x {subtotal_str}")

        escribir_linea(linea_separadora)
        total_str = formatear_moneda(datos_ticket['total'])
        escribir_linea(f"TOTAL: {total_str}", titulo=True)
        escribir_linea(linea_separadora)

        # --- FORMAS DE PAGO ---
        escribir_linea("Forma de Pago:", destacado=True)
        for pago in datos_ticket['pagos']:
            pago_str = formatear_moneda(pago['importe'])
            escribir_linea(f" - {pago['modo']}: {pago_str}")

        escribir_linea(linea_separadora)

        # --- CÓDIGO QR ---
        qr_texto = f"TicketJets | Venta:{datos_ticket['idventa']} | Total:{total_str}"
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

        # Avance de papel para facilitar el corte
        y += int(80 * scale_y)
        escribir_linea(".", centrado=False)

        # Finalizar Trabajo
        hdc.EndPage()
        hdc.EndDoc()
        win32print.ClosePrinter(hprinter)
        print("✅ Ticket impreso con formato limpio $18.000 y guiones.")
        return True

    except Exception as e:
        print(f"❌ Error al imprimir en segundo plano: {e}")
        return False

# Impresion de tickets de cierre de caja


def imprimir_ticket_cierre_silencioso(datos_cierre, operador_nombre="OPERADOR"):
    """
    Genera e imprime el ticket de Cierre de Caja en impresoras térmicas de 80mm.
    Ancho de línea estándar: 42 caracteres.
    """
    ANCHO = 42
    LINEA = "-" * ANCHO
    DOBLE_LINEA = "=" * ANCHO

    lineas = [
        "TicketsJets".center(ANCHO),
        "CIERRE DE CAJA".center(ANCHO),
        DOBLE_LINEA,
        f" FECHA: {datos_cierre['fecha_impresion']}",
        f" PUNTO: {datos_cierre['punto'][:28]}",
        f" OPERADOR: {operador_nombre[:25]}",
        LINEA,
        " RESUMEN DE VENTAS POR PRODUCTO".center(ANCHO),
        f"{'CANT':<5} {'DESCRIPCION':<25} {'TOTAL':>10}",
        LINEA
    ]

    # Detalle de productos vendidos
    for p in datos_cierre.get("productos", []):
        cant = f"x{int(p['cantidad'])}"
        nombre = str(p["producto"])[:24]
        total = f"${float(p['total_producto']):,.2f}"
        lineas.append(f"{cant:<5} {nombre:<25} {total:>10}")

    lineas.append(LINEA)
    lineas.append(" TOTALES POR MÉTODOS DE PAGO".center(ANCHO))
    lineas.append(LINEA)

    # Totales por método de pago
    for tp in datos_cierre.get("totales_pago", []):
        modo = str(tp["modo"])[:25]
        monto = f"${float(tp['total']):,.2f}"
        lineas.append(f" {modo:<25} {monto:>14}")

    lineas.append(DOBLE_LINEA)
    
    # Total General
    total_str = f"${datos_cierre['total_general']:,.2f}"
    lineas.append(f" TOTAL GENERAL:{total_str:>27}")
    lineas.append(DOBLE_LINEA)
    lineas.append("\n\n\n\n")  # Avance de papel para corte manual o automático

    texto_ticket = "\n".join(lineas)

    # Imprimir según el sistema operativo
    sistema = platform.system()
    try:
        if sistema == "Windows":
            import win32print
            import win32ui

            printer_name = win32print.GetDefaultPrinter()
            hprinter = win32print.OpenPrinter(printer_name)
            try:
                # Envío directo RAW a la impresora térmica
                win32print.StartDocPrinter(hprinter, 1, ("Ticket_Cierre", None, "RAW"))
                win32print.StartPagePrinter(hprinter)
                win32print.WritePrinter(hprinter, texto_ticket.encode("latin-1", errors="replace"))
                win32print.EndPagePrinter(hprinter)
                win32print.EndDocPrinter(hprinter)
            finally:
                win32print.ClosePrinter(hprinter)

        else:
            # En Linux / macOS usa 'lpr'
            process = subprocess.Popen(["lpr"], stdin=subprocess.PIPE)
            process.communicate(texto_ticket.encode("latin-1", errors="replace"))

        return True, "Ticket de Cierre impreso correctamente."

    except Exception as e:
        print(f"❌ Error al imprimir ticket de cierre: {e}")
        return False, f"Error al imprimir: {e}"