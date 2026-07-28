import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta

# Librerías de ReportLab
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

from database.repo_boleteria_db import ModelReportesBoleteria


class NumberedCanvas(canvas.Canvas):
    """
    Canvas personalizado para calcular y dibujar 'Página X de Y' 
    y añadir un pie de página profesional en todas las hojas.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#7E8299"))
        
        # Línea divisoria de pie de página
        self.setStrokeColor(colors.HexColor("#E4E6EF"))
        self.setLineWidth(0.5)
        self.line(36, 35, letter[0] - 36, 35)

        # Texto del pie de página
        texto_pie = "Sistema de Gestión de Boletería — Documento Oficial de Recaudación"
        self.drawString(36, 22, texto_pie)
        
        paginacion = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(letter[0] - 36, 22, paginacion)
        self.restoreState()


class ViewReporteBoleteria(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        self.ventas_actuales = []
        self.total_actual = 0.0
        self.desglose_actual = {}

        # Estilos visuales GUI
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure("Treeview", 
                        background="#1e1e2d", 
                        foreground="#ffffff", 
                        fieldbackground="#1e1e2d",
                        rowheight=28)
        style.map("Treeview", background=[("selected", "#009ef7")])
        style.configure("Treeview.Heading", 
                        background="#151521", 
                        foreground="#ffffff", 
                        font=("Segoe UI", 9, "bold"))

        self.init_ui()
        self.cargar_filtros_iniciales()
        self.buscar_reporte()

    def init_ui(self):
        # --- ENCABEZADO ---
        lbl_titulo = tk.Label(
            self, 
            text="🎟️ Reporte General de Boletería", 
            font=("Segoe UI", 16, "bold"), 
            bg="#0f0f17", 
            fg="#ffffff"
        )
        lbl_titulo.pack(anchor="w", pady=(0, 15))

        # --- FILTROS DE BÚSQUEDA ---
        frame_filtros = tk.LabelFrame(
            self, 
            text=" Filtros de Búsqueda ", 
            font=("Segoe UI", 10, "bold"), 
            bg="#1e1e2d", 
            fg="#a2a3b7", 
            bd=1, 
            padx=10, 
            pady=10
        )
        frame_filtros.pack(fill="x", pady=(0, 15))

        def crear_label(parent, texto):
            return tk.Label(parent, text=texto, bg="#1e1e2d", fg="#ffffff", font=("Segoe UI", 9))

        crear_label(frame_filtros, "Jornada:").grid(row=0, column=0, sticky="w", padx=5)
        self.combo_jornada = ttk.Combobox(frame_filtros, state="readonly", width=18)
        self.combo_jornada.grid(row=1, column=0, padx=5, pady=(0, 5))

        crear_label(frame_filtros, "Boletero:").grid(row=0, column=1, sticky="w", padx=5)
        self.combo_operador = ttk.Combobox(frame_filtros, state="readonly", width=18)
        self.combo_operador.grid(row=1, column=1, padx=5, pady=(0, 5))

        crear_label(frame_filtros, "Sector:").grid(row=0, column=2, sticky="w", padx=5)
        self.combo_sector = ttk.Combobox(frame_filtros, state="readonly", width=18)
        self.combo_sector.grid(row=1, column=2, padx=5, pady=(0, 5))

        crear_label(frame_filtros, "Desde (YYYY-MM-DD):").grid(row=0, column=3, sticky="w", padx=5)
        self.ent_desde = ttk.Entry(frame_filtros, width=12)
        self.ent_desde.insert(0, (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"))
        self.ent_desde.grid(row=1, column=3, padx=5, pady=(0, 5))

        crear_label(frame_filtros, "Hasta (YYYY-MM-DD):").grid(row=0, column=4, sticky="w", padx=5)
        self.ent_hasta = ttk.Entry(frame_filtros, width=12)
        self.ent_hasta.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.ent_hasta.grid(row=1, column=4, padx=5, pady=(0, 5))

        btn_buscar = tk.Button(
            frame_filtros, text="🔍 Buscar", bg="#009ef7", fg="white", 
            font=("Segoe UI", 9, "bold"), bd=0, padx=12, pady=3, cursor="hand2",
            command=self.buscar_reporte
        )
        btn_buscar.grid(row=1, column=5, padx=5, pady=(0, 5))

        btn_limpiar = tk.Button(
            frame_filtros, text="🧹 Limpiar", bg="#2b2b40", fg="white", 
            font=("Segoe UI", 9), bd=0, padx=12, pady=3, cursor="hand2",
            command=self.limpiar_filtros
        )
        btn_limpiar.grid(row=1, column=6, padx=5, pady=(0, 5))

        # --- TARJETAS KPI (GUI) ---
        self.frame_kpi = tk.Frame(self, bg="#0f0f17")
        self.frame_kpi.pack(fill="x", pady=(0, 15))

        # --- TABLA TREEVIEW ---
        frame_tabla = tk.Frame(self, bg="#0f0f17")
        frame_tabla.pack(fill="both", expand=True)

        columnas = ("fecha", "cliente", "modo_pago", "importe")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", selectmode="browse")
        
        headers = ["Fecha / Hora", "Cliente", "Modo de Pago", "Importe"]
        anchos = [180, 250, 150, 120]

        for col, h, w in zip(columnas, headers, anchos):
            self.tabla.heading(col, text=h)
            self.tabla.column(col, width=w, anchor="center" if col != "cliente" else "w")

        scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll_y.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

    def cargar_filtros_iniciales(self):
        try:
            self.map_jornadas = {"-- Todas las Jornadas --": None}
            for j in ModelReportesBoleteria.obtener_jornadas():
                id_j = j[0] if isinstance(j, tuple) else j["idjornada"]
                nom_j = j[1] if isinstance(j, tuple) else j["nombre"]
                self.map_jornadas[nom_j] = id_j
            self.combo_jornada["values"] = list(self.map_jornadas.keys())
            self.combo_jornada.current(0)

            self.map_operadores = {"-- Todos los Boleteros --": None}
            for op in ModelReportesBoleteria.obtener_operadores_boletería():
                id_u = op[0] if isinstance(op, tuple) else op["idusuarios"]
                nom_u = op[1] if isinstance(op, tuple) else op["nombre"]
                self.map_operadores[nom_u] = id_u
            self.combo_operador["values"] = list(self.map_operadores.keys())
            self.combo_operador.current(0)

            self.map_sectores = {"-- Todos los Sectores --": None}
            for sec in ModelReportesBoleteria.obtener_sectores():
                id_s = sec[0] if isinstance(sec, tuple) else sec["idsector"]
                nom_s = sec[1] if isinstance(sec, tuple) else sec["nombre"]
                self.map_sectores[nom_s] = id_s
            self.combo_sector["values"] = list(self.map_sectores.keys())
            self.combo_sector.current(0)
        except Exception as e:
            print(f"Error al cargar filtros: {e}")

    def actualizar_tarjetas_kpi(self):
        for child in self.frame_kpi.winfo_children():
            child.destroy()

        f_tot = tk.Frame(self.frame_kpi, bg="#1e1e2d", padx=15, pady=10, highlightbackground="#2b2b40", highlightthickness=1)
        f_tot.pack(side="left", padx=(0, 15))
        tk.Label(f_tot, text="TOTAL RECAUDADO", font=("Segoe UI", 8, "bold"), bg="#1e1e2d", fg="#a2a3b7").pack(anchor="w")
        tk.Label(f_tot, text=f"${self.total_actual:,.2f}", font=("Segoe UI", 16, "bold"), bg="#1e1e2d", fg="#50cd89").pack(anchor="w")

        colores_pagos = ["#009ef7", "#7239ea", "#ffc700", "#f1416c"]
        for idx, (modo, monto) in enumerate(self.desglose_actual.items()):
            color = colores_pagos[idx % len(colores_pagos)]
            f_modo = tk.Frame(self.frame_kpi, bg="#1e1e2d", padx=15, pady=10, highlightbackground="#2b2b40", highlightthickness=1)
            f_modo.pack(side="left", padx=(0, 15))
            tk.Label(f_modo, text=f"TOTAL {modo.upper()}", font=("Segoe UI", 8, "bold"), bg="#1e1e2d", fg="#a2a3b7").pack(anchor="w")
            tk.Label(f_modo, text=f"${monto:,.2f}", font=("Segoe UI", 16, "bold"), bg="#1e1e2d", fg=color).pack(anchor="w")

        btn_exportar = tk.Button(
            self.frame_kpi, text="📄 Exportar PDF Profesional", bg="#f1416c", fg="white", 
            font=("Segoe UI", 9, "bold"), bd=0, padx=15, pady=8, cursor="hand2",
            command=self.exportar_pdf
        )
        btn_exportar.pack(side="right", anchor="se")

    def buscar_reporte(self):
        idjornada = self.map_jornadas.get(self.combo_jornada.get())
        idusuario = self.map_operadores.get(self.combo_operador.get())
        idsector = self.map_sectores.get(self.combo_sector.get())

        ventas, total_general, desglose = ModelReportesBoleteria.obtener_reporte_detalle_boleteria(
            idjornada=idjornada, idusuario=idusuario, idsector=idsector
        )

        self.ventas_actuales = ventas
        self.total_actual = total_general
        self.desglose_actual = desglose or {}

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for v in ventas:
            fec = str(v.get("fecha", ""))
            cli = str(v.get("cliente", "Consumidor Final"))
            pago = str(v.get("modo_pago", "Efectivo"))
            imp = float(v.get("importe", 0))

            self.tabla.insert("", "end", values=(
                fec, cli, pago, f"${imp:,.2f}"
            ))

        self.actualizar_tarjetas_kpi()

    def limpiar_filtros(self):
        self.combo_jornada.current(0)
        self.combo_operador.current(0)
        self.combo_sector.current(0)
        self.ent_desde.delete(0, tk.END)
        self.ent_desde.insert(0, (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"))
        self.ent_hasta.delete(0, tk.END)
        self.ent_hasta.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.buscar_reporte()

    def exportar_pdf(self):
        """Genera un reporte PDF con diseño ejecutivo avanzado."""
        if not self.ventas_actuales:
            messagebox.showwarning("Atención", "No hay datos disponibles para exportar.")
            return

        nombre_jornada = self.combo_jornada.get()
        if "--" in nombre_jornada:
            nombre_jornada = "General"

        nombre_boletero = self.combo_operador.get()
        if "--" in nombre_boletero:
            nombre_boletero = "Todos"

        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")],
            title="Guardar Reporte de Boletería PDF",
            initialfile=f"Reporte_Boleteria_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        )

        if not filepath:
            return

        try:
            doc = SimpleDocTemplate(
                filepath,
                pagesize=letter,
                rightMargin=36, leftMargin=36, topMargin=40, bottomMargin=50
            )
            elementos = []
            estilos = getSampleStyleSheet()

            # Estilos personalizados
            estilo_banner_titulo = ParagraphStyle(
                'BannerTitulo',
                fontName='Helvetica-Bold',
                fontSize=16,
                textColor=colors.white,
                leading=20
            )
            
            estilo_banner_sub = ParagraphStyle(
                'BannerSub',
                fontName='Helvetica',
                fontSize=9,
                textColor=colors.HexColor("#A2A3B7"),
                leading=12
            )

            estilo_banner_meta = ParagraphStyle(
                'BannerMeta',
                fontName='Helvetica',
                fontSize=8,
                textColor=colors.white,
                alignment=2,
                leading=12
            )

            estilo_seccion = ParagraphStyle(
                'TituloSeccion',
                fontName='Helvetica-Bold',
                fontSize=12,
                textColor=colors.HexColor("#1E1E2D"),
                spaceAfter=8
            )

            estilo_celda = ParagraphStyle(
                'CeldaTabla',
                fontName='Helvetica',
                fontSize=8,
                textColor=colors.HexColor("#3F4254"),
                leading=10
            )

            estilo_celda_header = ParagraphStyle(
                'CeldaHeader',
                fontName='Helvetica-Bold',
                fontSize=8,
                textColor=colors.white,
                leading=10
            )

            # --- 1. BANNER / ENCABEZADO ---
            fecha_impresion = datetime.now().strftime("%d/%m/%Y %H:%M")
            txt_header_izq = Paragraph(
                f"REPORTE DE RECAUDACIÓN<br/><font size=8 color='#A2A3B7'>Jornada: {nombre_jornada} | Boletero: {nombre_boletero}</font>", 
                estilo_banner_titulo
            )
            txt_header_der = Paragraph(
                f"<b>Fecha Emisión:</b> {fecha_impresion}<br/><b>Estado:</b> OFICIAL", 
                estilo_banner_meta
            )

            tabla_header = Table([[txt_header_izq, txt_header_der]], colWidths=[360, 180])
            tabla_header.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#1E1E2D")),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('PADDING', (0, 0), (-1, -1), 12),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ]))
            elementos.append(tabla_header)
            elementos.append(Spacer(1, 15))

            # --- 2. TARJETAS DE RESUMEN EJECUTIVO (KPI) ---
            elementos.append(Paragraph("Resumen de Recaudación por Medio de Pago", estilo_seccion))
            
            kpi_cells = []
            
            # Celda Total General
            txt_kpi_tot = Paragraph(
                f"<font size=7 color='#7E8299'><b>TOTAL GENERAL</b></font><br/><font size=12 color='#50CD89'><b>${self.total_actual:,.2f}</b></font>",
                ParagraphStyle('KpiTot', parent=estilos['Normal'], alignment=1)
            )
            kpi_cells.append(txt_kpi_tot)

            # Celdas por Forma de Pago
            colores_kpi = ["#009EF7", "#7239EA", "#FFC700", "#F1416C"]
            for idx, (modo, monto) in enumerate(self.desglose_actual.items()):
                c_hex = colores_kpi[idx % len(colores_kpi)]
                txt_kpi_modo = Paragraph(
                    f"<font size=7 color='#7E8299'><b>{modo.upper()}</b></font><br/><font size=12 color='{c_hex}'><b>${monto:,.2f}</b></font>",
                    ParagraphStyle(f'Kpi{idx}', parent=estilos['Normal'], alignment=1)
                )
                kpi_cells.append(txt_kpi_modo)

            # Ajustar anchos dinámicos para las tarjetas
            ancho_disponible = 540
            num_kpis = len(kpi_cells)
            ancho_col = ancho_disponible / num_kpis if num_kpis > 0 else ancho_disponible

            tabla_kpi = Table([kpi_cells], colWidths=[ancho_col] * num_kpis)
            tabla_kpi.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F5F8FA")),
                ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#E4E6EF")),
                ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E4E6EF")),
                ('PADDING', (0, 0), (-1, -1), 8),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            elementos.append(tabla_kpi)
            elementos.append(Spacer(1, 20))

            # --- 3. TABLA DETALLADA DE TRANSACCIONES ---
            elementos.append(Paragraph("Detalle de Ventas Registradas", estilo_seccion))

            headers_tabla = [
                Paragraph("<b>Fecha y Hora</b>", estilo_celda_header),
                Paragraph("<b>Cliente</b>", estilo_celda_header),
                Paragraph("<b>Medio de Pago</b>", estilo_celda_header),
                Paragraph("<b align='right'>Importe</b>", estilo_celda_header)
            ]
            
            datos_tabla = [headers_tabla]

            for v in self.ventas_actuales:
                fec = Paragraph(str(v.get("fecha", "")), estilo_celda)
                cli = Paragraph(str(v.get("cliente", "Consumidor Final")), estilo_celda)
                pago = Paragraph(str(v.get("modo_pago", "Efectivo")), estilo_celda)
                imp_val = float(v.get('importe', 0))
                imp = Paragraph(f"${imp_val:,.2f}", ParagraphStyle('RightImp', parent=estilo_celda, alignment=2))

                datos_tabla.append([fec, cli, pago, imp])

            # Ancho total: 540 ptos
            tabla_ventas = Table(datos_tabla, colWidths=[130, 210, 110, 90])
            
            estilos_tabla = [
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#151521")),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor("#E4E6EF")),
            ]

            # Filas alternadas para mayor legibilidad
            for i in range(1, len(datos_tabla)):
                if i % 2 == 0:
                    estilos_tabla.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor("#F9F9FA")))

            tabla_ventas.setStyle(TableStyle(estilos_tabla))
            elementos.append(tabla_ventas)

            # Construir PDF usando NumberedCanvas para paginación profesional
            doc.build(elementos, canvasmaker=NumberedCanvas)

            messagebox.showinfo("Éxito", f"Reporte PDF generado exitosamente:\n{filepath}")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el archivo PDF: {e}")