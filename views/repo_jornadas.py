# views/repo_jornadas.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from database.repo_jornadas_db import ModelReportesJornadas
from utils.impresion_reportes import GeneradorReportes

try:
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    MATPLOTLIB_DISPONIBLE = True
except ImportError:
    MATPLOTLIB_DISPONIBLE = False

COLOR_CARD_BG = "#212529"
COLOR_MAIN_BG = "#0f0f17"
TEXT_LIGHT = "#f8f9fa"
TEXT_MUTED = "#adb5bd"
BTN_PRIMARY = "#0d6efd"
BTN_SUCCESS = "#198754"
BTN_INFO = "#0dcaf0"


class VistaRepoJornadas(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_MAIN_BG, padx=10, pady=10)

        # Título
        lbl_titulo = tk.Label(
            self,
            text="📊 Reportes y Recaudaciones de Jornadas",
            font=("Segoe UI", 14, "bold"),
            fg=TEXT_LIGHT,
            bg=COLOR_MAIN_BG,
            anchor="w"
        )
        lbl_titulo.pack(fill="x", pady=(0, 10))

        # Pestañas
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self.tab_resumen = tk.Frame(self.notebook, bg=COLOR_CARD_BG, padx=10, pady=10)
        self.notebook.add(self.tab_resumen, text="📋 Resumen por Cajas")

        self.tab_detalle = tk.Frame(self.notebook, bg=COLOR_CARD_BG, padx=10, pady=10)
        self.notebook.add(self.tab_detalle, text="🔍 Detalle Filtrado")

        self.tab_grafico = tk.Frame(self.notebook, bg=COLOR_CARD_BG, padx=10, pady=10)
        self.notebook.add(self.tab_grafico, text="📈 Gráfico Estadístico")

        self._build_tab_resumen()
        self._build_tab_detalle()
        self._build_tab_grafico()

        self.cargar_combos()

    def cargar_combos(self):
        jornadas = ModelReportesJornadas.obtener_jornadas()
        self.dict_jornadas = {
            f"{j[1] if isinstance(j, tuple) else j['nombre']} (ID: {j[0] if isinstance(j, tuple) else j['idjornada']})": (j[0] if isinstance(j, tuple) else j['idjornada'])
            for j in jornadas
        }

        self.cmb_resumen_jornada['values'] = list(self.dict_jornadas.keys())
        if self.dict_jornadas:
            self.cmb_resumen_jornada.current(0)
            self.filtrar_resumen()

        self.cmb_det_jornada['values'] = ["Todas"] + list(self.dict_jornadas.keys())
        self.cmb_det_jornada.current(0)

        cajas = ModelReportesJornadas.obtener_puntos_venta()
        self.dict_cajas = {
            c[1] if isinstance(c, tuple) else c['nombre']: c[0] if isinstance(c, tuple) else c['idpunto']
            for c in cajas
        }
        self.cmb_det_caja['values'] = ["Todas"] + list(self.dict_cajas.keys())
        self.cmb_det_caja.current(0)

        productos = ModelReportesJornadas.obtener_productos()
        self.dict_prods = {
            p[1] if isinstance(p, tuple) else p['nombre']: p[0] if isinstance(p, tuple) else p['idproductos']
            for p in productos
        }
        self.cmb_det_prod['values'] = ["Todos"] + list(self.dict_prods.keys())
        self.cmb_det_prod.current(0)

    # =========================================================================
    # PESTAÑA 1: RESUMEN COMPACTO & TICKET TÉRMICO
    # =========================================================================
    def _build_tab_resumen(self):
        f_top = tk.Frame(self.tab_resumen, bg=COLOR_CARD_BG)
        f_top.pack(fill="x", pady=(0, 10))

        tk.Label(f_top, text="Seleccionar Jornada:", fg=TEXT_MUTED, bg=COLOR_CARD_BG, font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 5))
        self.cmb_resumen_jornada = ttk.Combobox(f_top, state="readonly", width=35)
        self.cmb_resumen_jornada.pack(side="left", padx=(0, 10))

        btn_consultar = tk.Button(f_top, text="🔍 Consultar", bg=BTN_PRIMARY, fg="white", font=("Segoe UI", 8, "bold"), command=self.filtrar_resumen, bd=0, cursor="hand2")
        btn_consultar.pack(side="left", ipadx=10, ipady=3)

        f_export = tk.Frame(self.tab_resumen, bg=COLOR_CARD_BG)
        f_export.pack(fill="x", pady=(0, 10))

        btn_pdf = tk.Button(f_export, text="📄 PDF Resumen A4", bg=BTN_SUCCESS, fg="white", font=("Segoe UI", 8, "bold"), command=self.exportar_resumen_pdf, bd=0, cursor="hand2")
        btn_pdf.pack(side="left", padx=(0, 5), ipadx=8, ipady=3)

        btn_ticket = tk.Button(f_export, text="🖨️ Ticket Térmico 80mm", bg=BTN_INFO, fg="black", font=("Segoe UI", 8, "bold"), command=self.imprimir_resumen_ticket, bd=0, cursor="hand2")
        btn_ticket.pack(side="left", ipadx=8, ipady=3)

        cols = ("punto", "total")
        self.tree_resumen = ttk.Treeview(self.tab_resumen, columns=cols, show="headings", height=10)
        self.tree_resumen.heading("punto", text="Punto de Venta / Caja")
        self.tree_resumen.heading("total", text="Total Recaudado ($)")
        self.tree_resumen.column("punto", width=300)
        self.tree_resumen.column("total", width=150, anchor="e")
        self.tree_resumen.pack(fill="both", expand=True)

        self.lbl_resumen_total = tk.Label(self.tab_resumen, text="TOTAL GENERAL: $0.00", font=("Segoe UI", 12, "bold"), fg=TEXT_LIGHT, bg=COLOR_CARD_BG, anchor="e")
        self.lbl_resumen_total.pack(fill="x", pady=(10, 0))

    def filtrar_resumen(self):
        txt_jornada = self.cmb_resumen_jornada.get()
        idjornada = self.dict_jornadas.get(txt_jornada)

        self.resumen_datos, self.resumen_jornada_nombre, self.resumen_total = ModelReportesJornadas.obtener_resumen_cajas(idjornada)

        for item in self.tree_resumen.get_children():
            self.tree_resumen.delete(item)

        for row in self.resumen_datos:
            punto = row[0] if isinstance(row, tuple) else row['punto']
            tot = row[1] if isinstance(row, tuple) else row['total']
            self.tree_resumen.insert("", "end", values=(punto, f"${tot:,.2f}"))

        self.lbl_resumen_total.config(text=f"TOTAL GENERAL: ${self.resumen_total:,.2f}")
        self.actualizar_grafico()

    def exportar_resumen_pdf(self):
        ruta = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Archivos PDF", "*.pdf")])
        if not ruta:
            return

        tabla_clean = [
            (r[0] if isinstance(r, tuple) else r['punto'], f"${r[1] if isinstance(r, tuple) else r['total']:,.2f}")
            for r in self.resumen_datos
        ]

        ok, msj = GeneradorReportes.generar_pdf_a4(
            "Resumen Recaudación por Caja",
            self.resumen_jornada_nombre,
            tabla_clean,
            ["Punto de Venta / Caja", "Total Recaudado"],
            self.resumen_total,
            ruta
        )
        if ok:
            messagebox.showinfo("Éxito", msj)
        else:
            messagebox.showerror("Error", msj)

    def imprimir_resumen_ticket(self):
        txt_jornada = self.cmb_resumen_jornada.get()
        idjornada = self.dict_jornadas.get(txt_jornada)

        resumen_cajas, jornada_nombre, total_gen = ModelReportesJornadas.obtener_resumen_termico_cajas(idjornada)

        if not resumen_cajas:
            messagebox.showwarning("Atención", "No se encontraron datos de recaudación para esta jornada.")
            return

        txt_ticket = GeneradorReportes.generar_ticket_resumen_cajas(jornada_nombre, resumen_cajas, total_gen)
        ok, msj = GeneradorReportes.imprimir_con_dialogo(txt_ticket, es_pdf=False)
        if ok:
            messagebox.showinfo("Impresión Térmica", msj)
        else:
            messagebox.showerror("Error", msj)

    # =========================================================================
    # PESTAÑA 2: DETALLE FILTRADO Y EXPORTACIÓN A4
    # =========================================================================
    def _build_tab_detalle(self):
        f_filtros = tk.Frame(self.tab_detalle, bg=COLOR_CARD_BG)
        f_filtros.pack(fill="x", pady=(0, 10))

        tk.Label(f_filtros, text="Jornada:", fg=TEXT_MUTED, bg=COLOR_CARD_BG, font=("Segoe UI", 8, "bold")).grid(row=0, column=0, sticky="w", padx=2, pady=2)
        self.cmb_det_jornada = ttk.Combobox(f_filtros, state="readonly", width=25)
        self.cmb_det_jornada.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(f_filtros, text="Caja:", fg=TEXT_MUTED, bg=COLOR_CARD_BG, font=("Segoe UI", 8, "bold")).grid(row=0, column=2, sticky="w", padx=2, pady=2)
        self.cmb_det_caja = ttk.Combobox(f_filtros, state="readonly", width=20)
        self.cmb_det_caja.grid(row=0, column=3, padx=5, pady=2)

        tk.Label(f_filtros, text="Producto:", fg=TEXT_MUTED, bg=COLOR_CARD_BG, font=("Segoe UI", 8, "bold")).grid(row=1, column=0, sticky="w", padx=2, pady=2)
        self.cmb_det_prod = ttk.Combobox(f_filtros, state="readonly", width=25)
        self.cmb_det_prod.grid(row=1, column=1, padx=5, pady=2)

        btn_buscar = tk.Button(f_filtros, text="🔎 Filtrar Detalle", bg=BTN_PRIMARY, fg="white", font=("Segoe UI", 8, "bold"), command=self.filtrar_detalle, bd=0, cursor="hand2")
        btn_buscar.grid(row=1, column=3, sticky="ew", padx=5, pady=2)

        # Botón para exportar Detalle en PDF A4
        btn_pdf_det = tk.Button(f_filtros, text="📄 Exportar Detalle PDF A4", bg=BTN_SUCCESS, fg="white", font=("Segoe UI", 8, "bold"), command=self.exportar_detalle_pdf, bd=0, cursor="hand2")
        btn_pdf_det.grid(row=1, column=4, padx=5, pady=2)

        # Tabla Detalle
        cols = ("id", "fecha", "jornada", "caja", "modo", "producto", "cant", "subtotal", "pago")
        self.tree_det = ttk.Treeview(self.tab_detalle, columns=cols, show="headings", height=12)

        headings = [("id", "ID"), ("fecha", "Fecha/Hora"), ("jornada", "Jornada"), ("caja", "Caja"), ("modo", "Modo Pago"), ("producto", "Producto"), ("cant", "Cant"), ("subtotal", "Subtotal"), ("pago", "Importe Pago")]
        for c, h in headings:
            self.tree_det.heading(c, text=h)
            self.tree_det.column(c, width=90 if c not in ["fecha", "producto"] else 130)

        self.tree_det.pack(fill="both", expand=True)

        self.lbl_det_total = tk.Label(self.tab_detalle, text="TOTAL FILTRADO: $0.00", font=("Segoe UI", 11, "bold"), fg=TEXT_LIGHT, bg=COLOR_CARD_BG, anchor="e")
        self.lbl_det_total.pack(fill="x", pady=(8, 0))

    def filtrar_detalle(self):
        idjornada = self.dict_jornadas.get(self.cmb_det_jornada.get())
        idcaja = self.dict_cajas.get(self.cmb_det_caja.get())
        idprod = self.dict_prods.get(self.cmb_det_prod.get())

        self.ventas_detalle_raw, self.total_detalle, self.jornada_det_nombre = ModelReportesJornadas.obtener_reporte_detalle(idjornada, idcaja, idprod)

        for item in self.tree_det.get_children():
            self.tree_det.delete(item)

        for v in self.ventas_detalle_raw:
            if isinstance(v, dict):
                row = (v["idventa"], str(v["fecha_hora"]), v["jornada"], v["caja"], v["modo_pago"] or "N/A", v["producto"], v["cantidad"], f"${v['subtotal']:,.2f}", f"${v['importe_pago'] or 0:,.2f}")
            else:
                row = (v[0], str(v[1]), v[2], v[3], v[4] or "N/A", v[5], v[8], f"${v[9]:,.2f}", f"${v[10] or 0:,.2f}")
            self.tree_det.insert("", "end", values=row)

        self.lbl_det_total.config(text=f"TOTAL FILTRADO: ${self.total_detalle:,.2f}")

    def exportar_detalle_pdf(self):
        if not hasattr(self, 'ventas_detalle_raw') or not self.ventas_detalle_raw:
            messagebox.showwarning("Atención", "Realiza una búsqueda primero para obtener datos a exportar.")
            return

        ruta = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Archivos PDF", "*.pdf")])
        if not ruta:
            return

        cols_pdf = ["ID", "Fecha/Hora", "Caja", "Modo Pago", "Producto", "Cant", "Subtotal"]
        tabla_pdf = []

        for v in self.ventas_detalle_raw:
            if isinstance(v, dict):
                tabla_pdf.append([v["idventa"], str(v["fecha_hora"])[:16], v["caja"][:12], (v["modo_pago"] or "N/A")[:10], v["producto"][:20], v["cantidad"], f"${v['subtotal']:,.2f}"])
            else:
                tabla_pdf.append([v[0], str(v[1])[:16], str(v[3])[:12], str(v[4] or "N/A")[:10], str(v[5])[:20], v[8], f"${v[9]:,.2f}"])

        ok, msj = GeneradorReportes.generar_pdf_a4(
            "Reporte Detallado de Ventas",
            getattr(self, 'jornada_det_nombre', 'Todas'),
            tabla_pdf,
            cols_pdf,
            self.total_detalle,
            ruta
        )
        if ok:
            messagebox.showinfo("Éxito", msj)
        else:
            messagebox.showerror("Error", msj)

    # =========================================================================
    # PESTAÑA 3: GRÁFICO ESTADÍSTICO
    # =========================================================================
    def _build_tab_grafico(self):
        if not MATPLOTLIB_DISPONIBLE:
            tk.Label(self.tab_grafico, text="Instala matplotlib para ver gráficos:\npip install matplotlib", fg="white", bg=COLOR_CARD_BG, font=("Segoe UI", 11)).pack(expand=True)
            return

        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.fig.patch.set_facecolor(COLOR_CARD_BG)
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tab_grafico)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def actualizar_grafico(self):
        if not MATPLOTLIB_DISPONIBLE or not hasattr(self, 'ax'):
            return

        self.ax.clear()
        self.ax.set_facecolor("#181825")

        if hasattr(self, 'resumen_datos') and self.resumen_datos:
            cajas = [r[0] if isinstance(r, tuple) else r['punto'] for r in self.resumen_datos]
            totales = [r[1] if isinstance(r, tuple) else r['total'] for r in self.resumen_datos]

            bars = self.ax.bar(cajas, totales, color="#0d6efd")
            self.ax.set_title(f"Recaudación por Caja - {getattr(self, 'resumen_jornada_nombre', '')}", color="white", fontsize=10, fontweight="bold")
            self.ax.tick_params(colors="white", labelsize=8)
            self.ax.spines['bottom'].set_color('white')
            self.ax.spines['left'].set_color('white')
            self.ax.spines['top'].set_visible(False)
            self.ax.spines['right'].set_visible(False)

            for bar in bars:
                yval = bar.get_height()
                self.ax.text(bar.get_x() + bar.get_width()/2, yval, f"${yval:,.0f}", ha='center', va='bottom', color='white', fontsize=7)

        self.fig.tight_layout()
        self.canvas.draw()