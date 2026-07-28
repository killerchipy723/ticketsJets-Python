# utils/impresion_reportes.py
import os
import tempfile
import sys
from datetime import datetime

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    REPORTLAB_DISPONIBLE = True
except ImportError:
    REPORTLAB_DISPONIBLE = False


class GeneradorReportes:

    @staticmethod
    def generar_pdf_a4(titulo, jornada, datos_tabla, columnas, total, ruta_guardado):
        """Genera un archivo PDF en formato A4 profesional (para Resumen o Detalle)."""
        if not REPORTLAB_DISPONIBLE:
            return False, "La librería 'reportlab' no está instalada. Ejecuta: pip install reportlab"

        try:
            # Orientación vertical con márgenes estrechos para maximizar espacio
            doc = SimpleDocTemplate(
                ruta_guardado, 
                pagesize=A4, 
                rightMargin=20, 
                leftMargin=20, 
                topMargin=25, 
                bottomMargin=25
            )
            elements = []
            styles = getSampleStyleSheet()

            # Encabezado
            elements.append(Paragraph(f"<b>TICKETSJETS - {titulo.upper()}</b>", styles['Title']))
            elements.append(Paragraph(
                f"<b>Jornada:</b> {jornada} | <b>Fecha Reporte:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}", 
                styles['Normal']
            ))
            elements.append(Spacer(1, 12))

            # Estructura de la Tabla
            content = [columnas]
            for row in datos_tabla:
                content.append([str(cell) for cell in row])

            t = Table(content, repeatRows=1)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#212529")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F8F9FA")),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#DEE2E6")),
            ]))
            elements.append(t)
            elements.append(Spacer(1, 12))
            
            # Total
            elements.append(Paragraph(f"<b>TOTAL RECAUDADO: ${total:,.2f}</b>", styles['Heading2']))

            doc.build(elements)
            return True, "PDF A4 generado correctamente."
        except Exception as e:
            return False, f"Error generando PDF: {e}"

    @staticmethod
    def generar_ticket_resumen_cajas(jornada_nombre, resumen_cajas, total_general):
        """
        Genera el ticket térmico de 80mm con desglose por cada caja:
        - Jornada, Fecha y Hora
        - Caja / Punto de Venta
        - Cantidad de productos vendidos
        - Desglose por Medio de Pago (Efectivo, Transferencia, QR, etc.)
        - Total por Caja y Total General
        """
        lineas = []
        lineas.append("=" * 40)
        lineas.append("        RESUMEN RECAUDACION CAJAS       ")
        lineas.append("=" * 40)
        lineas.append(f"Jornada : {jornada_nombre[:28]}")
        lineas.append(f"Fecha   : {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        lineas.append("=" * 40)

        for caja in resumen_cajas:
            # Datos de la caja
            nombre_caja = caja.get("caja", "Caja N/A")
            operador = caja.get("operador", "Sin Asignar")
            cant_prods = caja.get("cant_productos", 0)
            desglose_pagos = caja.get("pagos", {})  # Ej: {"Efectivo": 5000, "Transferencia": 3000, "QR": 1500}
            total_caja = caja.get("total_caja", 0.0)

            lineas.append(f"CAJA    : {nombre_caja.upper()[:28]}")
            lineas.append(f"Operador: {operador[:28]}")
            lineas.append(f"Productos Vendidos: {cant_prods}")
            lineas.append("-" * 40)
            lineas.append("  Desglose de Medios de Pago:")

            if desglose_pagos:
                for modo, importe in desglose_pagos.items():
                    lineas.append(f"    - {modo[:18]:<18}: ${importe:>12,.2f}")
            else:
                lineas.append("    (Sin movimientos)")

            lineas.append(f"  TOTAL CAJA{'':<12}: ${total_caja:>12,.2f}")
            lineas.append("-" * 40)

        lineas.append("=" * 40)
        lineas.append(f"TOTAL RECAUDADO GENERAL: ${total_general:>13,.2f}")
        lineas.append("=" * 40)
        lineas.append("\n\n\n")

        return "\n".join(lineas)

    @staticmethod
    def imprimir_con_dialogo(contenido_o_archivo, es_pdf=False):
        """Abre el diálogo o spooler de impresión del sistema operativo."""
        try:
            if sys.platform == "win32":
                import win32api
                if es_pdf:
                    win32api.ShellExecute(0, "print", contenido_o_archivo, None, ".", 0)
                else:
                    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt") as f:
                        f.write(contenido_o_archivo)
                        temp_path = f.name
                    win32api.ShellExecute(0, "printui", f'/p /n "{temp_path}"', None, ".", 0)
                return True, "Enviado al servicio de impresión."
            else:
                with tempfile.NamedTemporaryFile("w", delete=False) as f:
                    f.write(contenido_o_archivo)
                    temp_path = f.name
                os.system(f"lpr '{temp_path}'")
                return True, "Enviado al sistema de impresión."
        except Exception as e:
            return False, f"Error al imprimir: {e}"