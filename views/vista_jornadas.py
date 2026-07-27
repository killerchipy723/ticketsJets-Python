# views/vista_jornadas.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from database.jornadas import ModelJornadas

# Estilos de color (Dark Mode Bootstrap)
COLOR_CARD_BG = "#212529"
COLOR_MAIN_BG = "#0f0f17"
COLOR_INPUT_BG = "#11111b"
TEXT_LIGHT = "#f8f9fa"
TEXT_MUTED = "#adb5bd"
BTN_PRIMARY = "#0d6efd"
BTN_WARNING = "#ffc107"
BTN_DANGER = "#dc3545"


class VistaJornadas(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_MAIN_BG, padx=10, pady=10)

        self.jornada_id_seleccionada = None
        self.check_equipos = []
        self.check_productos = []

        # Título principal
        lbl_titulo = tk.Label(
            self,
            text="📅 Control y Gestión de Jornadas",
            font=("Segoe UI", 14, "bold"),
            fg=TEXT_LIGHT,
            bg=COLOR_MAIN_BG,
            anchor="w",
        )
        lbl_titulo.pack(fill="x", pady=(0, 8))

        # Contenedor principal en 2 columnas (Izquierda: Formulario, Derecha: Tabla)
        paneles = tk.Frame(self, bg=COLOR_MAIN_BG)
        paneles.pack(fill="both", expand=True)

        # Panel Izquierdo (Formulario de Apertura)
        self.f_izq = tk.Frame(
            paneles,
            bg=COLOR_CARD_BG,
            highlightbackground="#313244",
            highlightthickness=1,
            padx=10,
            pady=10,
        )
        self.f_izq.pack(side="left", fill="both", expand=False, padx=(0, 10))

        # Panel Derecho (Tabla e Historial)
        self.f_der = tk.Frame(
            paneles,
            bg=COLOR_CARD_BG,
            highlightbackground="#313244",
            highlightthickness=1,
            padx=10,
            pady=10,
        )
        self.f_der.pack(side="right", fill="both", expand=True)

        # Construir UI
        self._crear_formulario(self.f_izq)
        self._crear_tabla(self.f_der)

        # Cargar Datos Iniciales
        self.cargar_datos_formulario()
        self.cargar_jornadas()

    def _crear_formulario(self, parent):
        tk.Label(
            parent,
            text="Apertura / Registro de Jornada",
            font=("Segoe UI", 11, "bold"),
            fg=TEXT_LIGHT,
            bg=COLOR_CARD_BG,
        ).pack(anchor="w", pady=(0, 8))

        # --- FILA 1: Nombre y Clave ---
        f_campos1 = tk.Frame(parent, bg=COLOR_CARD_BG)
        f_campos1.pack(fill="x", pady=(0, 5))

        tk.Label(
            f_campos1,
            text="Evento:",
            font=("Segoe UI", 8, "bold"),
            fg=TEXT_MUTED,
            bg=COLOR_CARD_BG,
        ).grid(row=0, column=0, sticky="w")
        self.txt_nombre = tk.Entry(
            f_campos1,
            font=("Segoe UI", 9),
            bg=COLOR_INPUT_BG,
            fg="white",
            insertbackground="white",
            width=20,
        )
        self.txt_nombre.grid(row=1, column=0, sticky="ew", padx=(0, 5), pady=2)

        tk.Label(
            f_campos1,
            text="Clave:",
            font=("Segoe UI", 8, "bold"),
            fg=TEXT_MUTED,
            bg=COLOR_CARD_BG,
        ).grid(row=0, column=1, sticky="w")
        self.txt_clave = tk.Entry(
            f_campos1,
            font=("Segoe UI", 9),
            bg=COLOR_INPUT_BG,
            fg="white",
            insertbackground="white",
            width=15,
        )
        self.txt_clave.grid(row=1, column=1, sticky="ew", pady=2)

        f_campos1.columnconfigure(0, weight=2)
        f_campos1.columnconfigure(1, weight=1)

        # --- FILA 2: Fechas Inicio y Fin ---
        f_campos2 = tk.Frame(parent, bg=COLOR_CARD_BG)
        f_campos2.pack(fill="x", pady=(0, 5))

        tk.Label(
            f_campos2,
            text="Fecha Inicio:",
            font=("Segoe UI", 8, "bold"),
            fg=TEXT_MUTED,
            bg=COLOR_CARD_BG,
        ).grid(row=0, column=0, sticky="w")
        self.dt_inicio = DateEntry(
            f_campos2,
            font=("Segoe UI", 8),
            date_pattern="yyyy-mm-dd",
            background="#1e1e2e",
            foreground="white",
            headersbackground="#313244",
            width=12,
        )
        self.dt_inicio.grid(row=1, column=0, sticky="ew", padx=(0, 5), pady=2)

        tk.Label(
            f_campos2,
            text="Fecha Fin:",
            font=("Segoe UI", 8, "bold"),
            fg=TEXT_MUTED,
            bg=COLOR_CARD_BG,
        ).grid(row=0, column=1, sticky="w")
        self.dt_fin = DateEntry(
            f_campos2,
            font=("Segoe UI", 8),
            date_pattern="yyyy-mm-dd",
            background="#1e1e2e",
            foreground="white",
            headersbackground="#313244",
            width=12,
        )
        self.dt_fin.grid(row=1, column=1, sticky="ew", pady=2)

        f_campos2.columnconfigure((0, 1), weight=1)

        # --- SECCIÓN EQUIPOS ---
        f_eq_head = tk.Frame(parent, bg=COLOR_CARD_BG)
        f_eq_head.pack(fill="x", pady=(5, 2))

        tk.Label(
            f_eq_head,
            text="Equipos / Puntos",
            font=("Segoe UI", 9, "bold"),
            fg=TEXT_LIGHT,
            bg=COLOR_CARD_BG,
        ).pack(side="left")
        self.var_equipos_todos = tk.BooleanVar(value=False)
        chk_eq_todos = tk.Checkbutton(
            f_eq_head,
            text="Todos",
            variable=self.var_equipos_todos,
            font=("Segoe UI", 8),
            fg=BTN_PRIMARY,
            bg=COLOR_CARD_BG,
            activebackground=COLOR_CARD_BG,
            command=self._toggle_todos_equipos,
        )
        chk_eq_todos.pack(side="right")

        # Contenedor scrolleable interno para Equipos
        c_eq = tk.Canvas(
            parent, bg=COLOR_CARD_BG, height=80, highlightthickness=0
        )
        s_eq = ttk.Scrollbar(parent, orient="vertical", command=c_eq.yview)
        self.subframe_equipos = tk.Frame(c_eq, bg=COLOR_CARD_BG)

        self.subframe_equipos.bind(
            "<Configure>",
            lambda e: c_eq.configure(scrollregion=c_eq.bbox("all")),
        )
        c_eq.create_window((0, 0), window=self.subframe_equipos, anchor="nw")
        c_eq.configure(yscrollcommand=s_eq.set)

        c_eq.pack(side="top", fill="x", expand=False)
        s_eq.place(in_=c_eq, relx=1.0, rely=0, relheight=1.0, anchor="ne")

        # --- SECCIÓN PRODUCTOS ---
        f_pr_head = tk.Frame(parent, bg=COLOR_CARD_BG)
        f_pr_head.pack(fill="x", pady=(10, 2))

        tk.Label(
            f_pr_head,
            text="Productos Habilitados",
            font=("Segoe UI", 9, "bold"),
            fg=TEXT_LIGHT,
            bg=COLOR_CARD_BG,
        ).pack(side="left")
        self.var_productos_todos = tk.BooleanVar(value=False)
        chk_pr_todos = tk.Checkbutton(
            f_pr_head,
            text="Todos",
            variable=self.var_productos_todos,
            font=("Segoe UI", 8),
            fg=BTN_PRIMARY,
            bg=COLOR_CARD_BG,
            activebackground=COLOR_CARD_BG,
            command=self._toggle_todos_productos,
        )
        chk_pr_todos.pack(side="right")

        # Contenedor scrolleable interno para Productos
        c_pr = tk.Canvas(
            parent, bg=COLOR_CARD_BG, height=130, highlightthickness=0
        )
        s_pr = ttk.Scrollbar(parent, orient="vertical", command=c_pr.yview)
        self.subframe_productos = tk.Frame(c_pr, bg=COLOR_CARD_BG)

        self.subframe_productos.bind(
            "<Configure>",
            lambda e: c_pr.configure(scrollregion=c_pr.bbox("all")),
        )
        c_pr.create_window((0, 0), window=self.subframe_productos, anchor="nw")
        c_pr.configure(yscrollcommand=s_pr.set)

        c_pr.pack(side="top", fill="x", expand=False)
        s_pr.place(in_=c_pr, relx=1.0, rely=0, relheight=1.0, anchor="ne")

        # --- BOTÓN REGISTRAR ---
        btn_registrar = tk.Button(
            parent,
            text="💾 Registrar Jornada",
            font=("Segoe UI", 9, "bold"),
            bg=BTN_PRIMARY,
            fg="white",
            bd=0,
            cursor="hand2",
            command=self.guardar_jornada,
        )
        btn_registrar.pack(fill="x", pady=(12, 0), ipady=5)

    def _crear_tabla(self, parent):
        tk.Label(
            parent,
            text="Jornadas Registradas",
            font=("Segoe UI", 11, "bold"),
            fg=TEXT_LIGHT,
            bg=COLOR_CARD_BG,
        ).pack(anchor="w", pady=(0, 8))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="#181825",
            foreground=TEXT_LIGHT,
            fieldbackground="#181825",
            rowheight=24,
            font=("Segoe UI", 8),
        )
        style.configure(
            "Treeview.Heading",
            background=COLOR_CARD_BG,
            foreground=TEXT_LIGHT,
            font=("Segoe UI", 8, "bold"),
        )
        style.map("Treeview", background=[("selected", BTN_PRIMARY)])

        # Frame exclusivo para la tabla y su Scrollbar
        f_tabla_inner = tk.Frame(parent, bg=COLOR_CARD_BG)
        f_tabla_inner.pack(fill="both", expand=True)

        cols = ("idjornada", "nombre", "clave", "finicio", "ffinal", "estado")
        self.tree = ttk.Treeview(
            f_tabla_inner, columns=cols, show="headings", selectmode="browse"
        )

        self.tree.heading("idjornada", text="ID")
        self.tree.heading("nombre", text="Jornada")
        self.tree.heading("clave", text="Clave")
        self.tree.heading("finicio", text="Inicio")
        self.tree.heading("ffinal", text="Fin")
        self.tree.heading("estado", text="Estado")

        self.tree.column("idjornada", width=40, anchor="center")
        self.tree.column("nombre", width=140)
        self.tree.column("clave", width=80, anchor="center")
        self.tree.column("finicio", width=90, anchor="center")
        self.tree.column("ffinal", width=90, anchor="center")
        self.tree.column("estado", width=70, anchor="center")

        scroll = ttk.Scrollbar(
            f_tabla_inner, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscroll=scroll.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # Acciones de la tabla
        f_acciones = tk.Frame(parent, bg=COLOR_CARD_BG)
        f_acciones.pack(fill="x", pady=(8, 0))

        btn_editar = tk.Button(
            f_acciones,
            text="✏️ Editar",
            bg=BTN_WARNING,
            fg="black",
            font=("Segoe UI", 8, "bold"),
            bd=0,
            cursor="hand2",
            command=self.modal_editar,
        )
        btn_editar.pack(side="left", padx=(0, 5), ipady=3, ipadx=8)

        btn_eliminar = tk.Button(
            f_acciones,
            text="🗑️ Eliminar",
            bg=BTN_DANGER,
            fg="white",
            font=("Segoe UI", 8, "bold"),
            bd=0,
            cursor="hand2",
            command=self.modal_eliminar,
        )
        btn_eliminar.pack(side="left", ipady=3, ipadx=8)

    # --- LÓGICA Y DILIGENCIAMIENTO DE DATOS ---
    def cargar_datos_formulario(self):
        """Genera dinámicamente los checkboxes de Equipos y Productos."""
        for w in self.subframe_equipos.winfo_children():
            w.destroy()
        for w in self.subframe_productos.winfo_children():
            w.destroy()
        self.check_equipos.clear()
        self.check_productos.clear()

        # Puntos de Venta
        puntos = ModelJornadas.obtener_puntos_venta()
        for i, p in enumerate(puntos):
            p_id = p[0] if isinstance(p, (tuple, list)) else p["idpunto"]
            p_nom = p[1] if isinstance(p, (tuple, list)) else p["nombre"]

            var = tk.BooleanVar(value=False)
            chk = tk.Checkbutton(
                self.subframe_equipos,
                text=p_nom,
                variable=var,
                font=("Segoe UI", 8),
                bg=COLOR_CARD_BG,
                fg=TEXT_LIGHT,
                selectcolor=COLOR_INPUT_BG,
                activebackground=COLOR_CARD_BG,
                activeforeground=TEXT_LIGHT,
            )
            chk.grid(row=i // 2, column=i % 2, sticky="w", padx=2, pady=1)
            self.check_equipos.append((p_id, var))

        # Productos
        prods = ModelJornadas.obtener_productos()
        for i, pr in enumerate(prods):
            pr_id = pr[0] if isinstance(pr, (tuple, list)) else pr["idproductos"]
            pr_nom = pr[1] if isinstance(pr, (tuple, list)) else pr["nombre"]
            pr_imp = pr[2] if isinstance(pr, (tuple, list)) else pr["importe"]

            var = tk.BooleanVar(value=False)
            chk = tk.Checkbutton(
                self.subframe_productos,
                text=f"{pr_nom} (${pr_imp})",
                variable=var,
                font=("Segoe UI", 8),
                bg=COLOR_CARD_BG,
                fg=TEXT_LIGHT,
                selectcolor=COLOR_INPUT_BG,
                activebackground=COLOR_CARD_BG,
                activeforeground=TEXT_LIGHT,
            )
            chk.grid(row=i // 2, column=i % 2, sticky="w", padx=2, pady=1)
            self.check_productos.append((pr_id, var))

    def _toggle_todos_equipos(self):
        estado = self.var_equipos_todos.get()
        for _, var in self.check_equipos:
            var.set(estado)

    def _toggle_todos_productos(self):
        estado = self.var_productos_todos.get()
        for _, var in self.check_productos:
            var.set(estado)

    def cargar_jornadas(self):
        """Limpia y carga los registros de la base de datos en la tabla."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        jornadas = ModelJornadas.obtener_jornadas()
        for j in jornadas:
            # Compatibilidad tanto para tuplas como para diccionarios (DictCursor)
            if isinstance(j, dict):
                row = (
                    j.get("idjornada"),
                    j.get("nombre"),
                    j.get("clave"),
                    str(j.get("finicio")),
                    str(j.get("ffinal")),
                    j.get("estado"),
                )
            else:
                row = (
                    j[0],
                    j[1],
                    j[2],
                    str(j[3]),
                    str(j[4]),
                    j[5],
                )
            self.tree.insert("", "end", values=row)

    def guardar_jornada(self):
        nombre = self.txt_nombre.get().upper().strip()
        clave = self.txt_clave.get().upper().strip()
        finicio = self.dt_inicio.get_date().strftime("%Y-%m-%d")
        ffin = self.dt_fin.get_date().strftime("%Y-%m-%d")

        eq_sel = [eq_id for eq_id, var in self.check_equipos if var.get()]
        pr_sel = [pr_id for pr_id, var in self.check_productos if var.get()]

        if not nombre or not clave:
            messagebox.showwarning(
                "Atención", "Nombre del evento y Clave son obligatorios."
            )
            return

        # Intento inicial de registro
        exito, msj, requiere_confirmacion = ModelJornadas.crear_jornada(
            nombre, clave, finicio, ffin, eq_sel, pr_sel, forzar_cierre=False
        )

        # Si hay una jornada activa, preguntamos al usuario si desea cerrarla
        if requiere_confirmacion:
            if messagebox.askyesno("Jornada Activa Detectada", msj):
                # Reintentamos forzando el cierre de la jornada activa previa
                exito, msj, _ = ModelJornadas.crear_jornada(
                    nombre,
                    clave,
                    finicio,
                    ffin,
                    eq_sel,
                    pr_sel,
                    forzar_cierre=True,
                )

        if exito:
            messagebox.showinfo("Éxito", msj)
            self.txt_nombre.delete(0, tk.END)
            self.txt_clave.delete(0, tk.END)
            self.cargar_jornadas()
            self.var_equipos_todos.set(False)
            self.var_productos_todos.set(False)
            for _, var in self.check_equipos:
                var.set(False)
            for _, var in self.check_productos:
                var.set(False)
                
            self.cargar_jornadas()
        elif not requiere_confirmacion:
            messagebox.showerror("Error", msj)

    # --- ACCIONES MODALES (EDITAR / ELIMINAR) ---
    def modal_editar(self):
        item = self.tree.focus()
        if not item:
            messagebox.showwarning(
                "Atención", "Seleccione una jornada de la tabla."
            )
            return

        vals = self.tree.item(item, "values")
        idjornada, nombre, clave, finicio, ffinal, _ = vals

        top = tk.Toplevel(self)
        top.title(f"Editar: {nombre}")
        top.geometry("360x280")
        top.configure(bg=COLOR_CARD_BG)
        top.grab_set()

        tk.Label(
            top,
            text="Nombre del Evento:",
            fg=TEXT_MUTED,
            bg=COLOR_CARD_BG,
            font=("Segoe UI", 8, "bold"),
        ).pack(anchor="w", padx=15, pady=(12, 2))
        e_nombre = tk.Entry(
            top, font=("Segoe UI", 9), bg=COLOR_INPUT_BG, fg="white"
        )
        e_nombre.insert(0, nombre)
        e_nombre.pack(fill="x", padx=15)

        tk.Label(
            top,
            text="Clave:",
            fg=TEXT_MUTED,
            bg=COLOR_CARD_BG,
            font=("Segoe UI", 8, "bold"),
        ).pack(anchor="w", padx=15, pady=(8, 2))
        e_clave = tk.Entry(
            top, font=("Segoe UI", 9), bg=COLOR_INPUT_BG, fg="white"
        )
        e_clave.insert(0, clave)
        e_clave.pack(fill="x", padx=15)

        tk.Label(
            top,
            text="Fecha Inicio:",
            fg=TEXT_MUTED,
            bg=COLOR_CARD_BG,
            font=("Segoe UI", 8, "bold"),
        ).pack(anchor="w", padx=15, pady=(8, 2))
        e_finicio = DateEntry(
            top, font=("Segoe UI", 9), date_pattern="yyyy-mm-dd"
        )
        e_finicio.set_date(finicio)
        e_finicio.pack(fill="x", padx=15)

        tk.Label(
            top,
            text="Fecha Finalización:",
            fg=TEXT_MUTED,
            bg=COLOR_CARD_BG,
            font=("Segoe UI", 8, "bold"),
        ).pack(anchor="w", padx=15, pady=(8, 2))
        e_ffin = DateEntry(
            top, font=("Segoe UI", 9), date_pattern="yyyy-mm-dd"
        )
        e_ffin.set_date(ffinal)
        e_ffin.pack(fill="x", padx=15)

        def actualizar():
            ok, msj = ModelJornadas.actualizar_jornada(
                idjornada,
                e_nombre.get().upper().strip(),
                e_clave.get().upper().strip(),
                e_finicio.get_date().strftime("%Y-%m-%d"),
                e_ffin.get_date().strftime("%Y-%m-%d"),
            )
            if ok:
                messagebox.showinfo("Éxito", msj)
                top.destroy()
                self.cargar_jornadas()
            else:
                messagebox.showerror("Error", msj)

        tk.Button(
            top,
            text="Actualizar",
            bg=BTN_PRIMARY,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            command=actualizar,
            bd=0,
        ).pack(fill="x", padx=15, pady=15)

    def modal_eliminar(self):
        item = self.tree.focus()
        if not item:
            messagebox.showwarning(
                "Atención", "Seleccione una jornada de la tabla."
            )
            return

        vals = self.tree.item(item, "values")
        idjornada = vals[0]

        if messagebox.askyesno(
            "Confirmar", "¿Está seguro que desea eliminar esta jornada?"
        ):
            ok, msj = ModelJornadas.eliminar_jornada(idjornada)
            if ok:
                messagebox.showinfo("Éxito", msj)
                self.cargar_jornadas()
            else:
                messagebox.showerror("Error", msj)