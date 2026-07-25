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
        super().__init__(parent, bg=COLOR_MAIN_BG)

        self.jornada_id_seleccionada = None
        self.check_equipos = []
        self.check_productos = []

        # Título principal
        lbl_titulo = tk.Label(
            self,
            text="📅 Control y Gestión de Jornadas",
            font=("Segoe UI", 16, "bold"),
            fg=TEXT_LIGHT,
            bg=COLOR_MAIN_BG,
            anchor="w"
        )
        lbl_titulo.pack(fill="x", pady=(0, 10))

        # Panel desplazable para organizar formulario + tabla en pantallas reducidas
        canvas_main = tk.Canvas(self, bg=COLOR_MAIN_BG, highlightthickness=0)
        scroll_v = ttk.Scrollbar(self, orient="vertical", command=canvas_main.yview)
        
        self.contenedor = tk.Frame(canvas_main, bg=COLOR_MAIN_BG)
        self.contenedor.bind(
            "<Configure>", 
            lambda e: canvas_main.configure(scrollregion=canvas_main.bbox("all"))
        )

        canvas_main.create_window((0, 0), window=self.contenedor, anchor="nw")
        canvas_main.configure(yscrollcommand=scroll_v.set)

        canvas_main.pack(side="left", fill="both", expand=True)
        scroll_v.pack(side="right", fill="y")

        # Construir UI
        self._crear_formulario(self.contenedor)
        self._crear_tabla(self.contenedor)

        # Cargar Datos Iniciales
        self.cargar_datos_formulario()
        self.cargar_jornadas()

    def _crear_formulario(self, parent):
        frame_card = tk.Frame(
            parent, 
            bg=COLOR_CARD_BG, 
            highlightbackground="#313244", 
            highlightthickness=1, 
            padx=15, 
            pady=15
        )
        frame_card.pack(fill="x", pady=(0, 15))

        tk.Label(
            frame_card, 
            text="Apertura / Registro de Jornada", 
            font=("Segoe UI", 12, "bold"), 
            fg=TEXT_LIGHT, 
            bg=COLOR_CARD_BG
        ).pack(anchor="w", pady=(0, 10))

        # --- FILA 1: Nombre, Clave, Fecha Inicio, Fecha Fin ---
        f1 = tk.Frame(frame_card, bg=COLOR_CARD_BG)
        f1.pack(fill="x", pady=(0, 10))

        # Nombre Evento
        tk.Label(f1, text="Nombre del Evento:", font=("Segoe UI", 9, "bold"), fg=TEXT_MUTED, bg=COLOR_CARD_BG).grid(row=0, column=0, sticky="w", padx=5)
        self.txt_nombre = tk.Entry(f1, font=("Segoe UI", 10), bg=COLOR_INPUT_BG, fg="white", insertbackground="white")
        self.txt_nombre.grid(row=1, column=0, sticky="ew", padx=5, pady=(2, 5))

        # Clave
        tk.Label(f1, text="Clave:", font=("Segoe UI", 9, "bold"), fg=TEXT_MUTED, bg=COLOR_CARD_BG).grid(row=0, column=1, sticky="w", padx=5)
        self.txt_clave = tk.Entry(f1, font=("Segoe UI", 10), bg=COLOR_INPUT_BG, fg="white", insertbackground="white")
        self.txt_clave.grid(row=1, column=1, sticky="ew", padx=5, pady=(2, 5))

        # Calendario Fecha Inicio
        tk.Label(f1, text="Fecha de Inicio:", font=("Segoe UI", 9, "bold"), fg=TEXT_MUTED, bg=COLOR_CARD_BG).grid(row=0, column=2, sticky="w", padx=5)
        self.dt_inicio = DateEntry(
            f1, 
            font=("Segoe UI", 10), 
            date_pattern="yyyy-mm-dd", 
            background="#1e1e2e", 
            foreground="white", 
            headersbackground="#313244"
        )
        self.dt_inicio.grid(row=1, column=2, sticky="ew", padx=5, pady=(2, 5))

        # Calendario Fecha Fin
        tk.Label(f1, text="Fecha de Finalización:", font=("Segoe UI", 9, "bold"), fg=TEXT_MUTED, bg=COLOR_CARD_BG).grid(row=0, column=3, sticky="w", padx=5)
        self.dt_fin = DateEntry(
            f1, 
            font=("Segoe UI", 10), 
            date_pattern="yyyy-mm-dd", 
            background="#1e1e2e", 
            foreground="white", 
            headersbackground="#313244"
        )
        self.dt_fin.grid(row=1, column=3, sticky="ew", padx=5, pady=(2, 5))

        f1.columnconfigure((0, 1, 2, 3), weight=1)

        # --- SECCIÓN EQUIPOS / PUNTOS DE VENTA ---
        self.frame_equipos = tk.LabelFrame(
            frame_card, 
            text=" Equipos / Puntos de Venta ", 
            font=("Segoe UI", 10, "bold"), 
            fg=TEXT_LIGHT, 
            bg=COLOR_CARD_BG, 
            padx=10, 
            pady=10
        )
        self.frame_equipos.pack(fill="x", pady=5)

        self.var_equipos_todos = tk.BooleanVar(value=False)
        chk_eq_todos = tk.Checkbutton(
            self.frame_equipos, 
            text="Habilitar todos los equipos", 
            variable=self.var_equipos_todos,
            font=("Segoe UI", 9, "bold"), 
            fg=BTN_PRIMARY, 
            bg=COLOR_CARD_BG, 
            activebackground=COLOR_CARD_BG,
            command=self._toggle_todos_equipos
        )
        chk_eq_todos.pack(anchor="w", pady=(0, 5))

        self.subframe_equipos = tk.Frame(self.frame_equipos, bg=COLOR_CARD_BG)
        self.subframe_equipos.pack(fill="x")

        # --- SECCIÓN PRODUCTOS HABILITADOS ---
        self.frame_productos = tk.LabelFrame(
            frame_card, 
            text=" Productos Habilitados ", 
            font=("Segoe UI", 10, "bold"), 
            fg=TEXT_LIGHT, 
            bg=COLOR_CARD_BG, 
            padx=10, 
            pady=10
        )
        self.frame_productos.pack(fill="x", pady=5)

        self.var_productos_todos = tk.BooleanVar(value=False)
        chk_pr_todos = tk.Checkbutton(
            self.frame_productos, 
            text="Habilitar todos los productos", 
            variable=self.var_productos_todos,
            font=("Segoe UI", 9, "bold"), 
            fg=BTN_PRIMARY, 
            bg=COLOR_CARD_BG, 
            activebackground=COLOR_CARD_BG,
            command=self._toggle_todos_productos
        )
        chk_pr_todos.pack(anchor="w", pady=(0, 5))

        self.subframe_productos = tk.Frame(self.frame_productos, bg=COLOR_CARD_BG)
        self.subframe_productos.pack(fill="x")

        # --- BOTÓN REGISTRAR ---
        btn_registrar = tk.Button(
            frame_card,
            text="Registrar Jornada",
            font=("Segoe UI", 10, "bold"),
            bg=BTN_PRIMARY,
            fg="white",
            bd=0,
            cursor="hand2",
            command=self.guardar_jornada
        )
        btn_registrar.pack(fill="x", pady=(10, 0), ipady=6)

    def _crear_tabla(self, parent):
        frame_tabla = tk.Frame(
            parent, 
            bg=COLOR_CARD_BG, 
            highlightbackground="#313244", 
            highlightthickness=1, 
            padx=10, 
            pady=10
        )
        frame_tabla.pack(fill="x", pady=(0, 15))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#181825", foreground=TEXT_LIGHT, fieldbackground="#181825", rowheight=28, font=("Segoe UI", 9))
        style.configure("Treeview.Heading", background=COLOR_CARD_BG, foreground=TEXT_LIGHT, font=("Segoe UI", 9, "bold"))
        style.map("Treeview", background=[("selected", BTN_PRIMARY)])

        cols = ("idjornada", "nombre", "clave", "finicio", "ffinal", "estado")
        self.tree = ttk.Treeview(frame_tabla, columns=cols, show="headings", height=6)

        self.tree.heading("idjornada", text="ID")
        self.tree.heading("nombre", text="Jornada")
        self.tree.heading("clave", text="Clave")
        self.tree.heading("finicio", text="Inicio")
        self.tree.heading("ffinal", text="Fin")
        self.tree.heading("estado", text="Estado")

        self.tree.column("idjornada", width=50, anchor="center")
        self.tree.column("nombre", width=180)
        self.tree.column("clave", width=100, anchor="center")
        self.tree.column("finicio", width=130, anchor="center")
        self.tree.column("ffinal", width=130, anchor="center")
        self.tree.column("estado", width=90, anchor="center")

        scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scroll.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # Acciones de la tabla (Modales / Edición)
        f_acciones = tk.Frame(frame_tabla, bg=COLOR_CARD_BG)
        f_acciones.pack(fill="x", pady=(8, 0))

        btn_editar = tk.Button(f_acciones, text="✏️ Editar Seleccionado", bg=BTN_WARNING, fg="black", font=("Segoe UI", 9, "bold"), bd=0, cursor="hand2", command=self.modal_editar)
        btn_editar.pack(side="left", padx=(0, 5), ipady=3, ipadx=10)

        btn_eliminar = tk.Button(f_acciones, text="🗑️ Eliminar Seleccionado", bg=BTN_DANGER, fg="white", font=("Segoe UI", 9, "bold"), bd=0, cursor="hand2", command=self.modal_eliminar)
        btn_eliminar.pack(side="left", ipady=3, ipadx=10)

    # --- LÓGICA Y DILIGENCIAMIENTO DE DATOS ---
    def cargar_datos_formulario(self):
        """Genera dinámicamente los checkboxes de Equipos y Productos."""
        # Limpiar
        for w in self.subframe_equipos.winfo_children(): w.destroy()
        for w in self.subframe_productos.winfo_children(): w.destroy()
        self.check_equipos.clear()
        self.check_productos.clear()

        # Puntos de Venta
        puntos = ModelJornadas.obtener_puntos_venta()
        for i, p in enumerate(puntos):
            var = tk.BooleanVar(value=False)
            chk = tk.Checkbutton(
                self.subframe_equipos, text=p[1], variable=var,
                bg=COLOR_CARD_BG, fg=TEXT_LIGHT, selectcolor=COLOR_INPUT_BG,
                activebackground=COLOR_CARD_BG, activeforeground=TEXT_LIGHT
            )
            chk.grid(row=i//4, column=i%4, sticky="w", padx=10, pady=2)
            self.check_equipos.append((p[0], var))

        # Productos
        prods = ModelJornadas.obtener_productos()
        for i, pr in enumerate(prods):
            var = tk.BooleanVar(value=False)
            chk = tk.Checkbutton(
                self.subframe_productos, text=f"{pr[1]} (${pr[2]})", variable=var,
                bg=COLOR_CARD_BG, fg=TEXT_LIGHT, selectcolor=COLOR_INPUT_BG,
                activebackground=COLOR_CARD_BG, activeforeground=TEXT_LIGHT
            )
            chk.grid(row=i//4, column=i%4, sticky="w", padx=10, pady=2)
            self.check_productos.append((pr[0], var))

    def _toggle_todos_equipos(self):
        estado = self.var_equipos_todos.get()
        for _, var in self.check_equipos:
            var.set(estado)

    def _toggle_todos_productos(self):
        estado = self.var_productos_todos.get()
        for _, var in self.check_productos:
            var.set(estado)

    def cargar_jornadas(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        jornadas = ModelJornadas.obtener_jornadas()
        for j in jornadas:
            self.tree.insert("", "end", values=j)

    def guardar_jornada(self):
        nombre = self.txt_nombre.get().upper().strip()
        clave = self.txt_clave.get().upper().strip()
        finicio = self.dt_inicio.get_date().strftime("%Y-%m-%d")
        ffin = self.dt_fin.get_date().strftime("%Y-%m-%d")

        eq_sel = [eq_id for eq_id, var in self.check_equipos if var.get()]
        pr_sel = [pr_id for pr_id, var in self.check_productos if var.get()]

        if not nombre or not clave:
            messagebox.showwarning("Atención", "Nombre del evento y Clave son obligatorios.")
            return

        exito, msj = ModelJornadas.crear_jornada(nombre, clave, finicio, ffin, eq_sel, pr_sel)
        if exito:
            messagebox.showinfo("Éxito", msj)
            self.txt_nombre.delete(0, tk.END)
            self.txt_clave.delete(0, tk.END)
            self.cargar_jornadas()
        else:
            messagebox.showerror("Error", msj)

    # --- ACCIONES MODALES (EDITAR / ELIMINAR) ---
    def modal_editar(self):
        item = self.tree.focus()
        if not item:
            messagebox.showwarning("Atención", "Seleccione una jornada de la tabla.")
            return

        vals = self.tree.item(item, "values")
        idjornada, nombre, clave, finicio, ffinal, _ = vals

        top = tk.Toplevel(self)
        top.title(f"Editar: {nombre}")
        top.geometry("380x300")
        top.configure(bg=COLOR_CARD_BG)
        top.grab_set()

        tk.Label(top, text="Nombre del Evento:", fg=TEXT_MUTED, bg=COLOR_CARD_BG, font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=15, pady=(15, 2))
        e_nombre = tk.Entry(top, font=("Segoe UI", 10), bg=COLOR_INPUT_BG, fg="white")
        e_nombre.insert(0, nombre)
        e_nombre.pack(fill="x", padx=15)

        tk.Label(top, text="Clave:", fg=TEXT_MUTED, bg=COLOR_CARD_BG, font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=15, pady=(10, 2))
        e_clave = tk.Entry(top, font=("Segoe UI", 10), bg=COLOR_INPUT_BG, fg="white")
        e_clave.insert(0, clave)
        e_clave.pack(fill="x", padx=15)

        tk.Label(top, text="Fecha Inicio:", fg=TEXT_MUTED, bg=COLOR_CARD_BG, font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=15, pady=(10, 2))
        e_finicio = DateEntry(top, font=("Segoe UI", 10), date_pattern="yyyy-mm-dd")
        e_finicio.set_date(finicio)
        e_finicio.pack(fill="x", padx=15)

        tk.Label(top, text="Fecha Finalización:", fg=TEXT_MUTED, bg=COLOR_CARD_BG, font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=15, pady=(10, 2))
        e_ffin = DateEntry(top, font=("Segoe UI", 10), date_pattern="yyyy-mm-dd")
        e_ffin.set_date(ffinal)
        e_ffin.pack(fill="x", padx=15)

        def actualizar():
            ok, msj = ModelJornadas.actualizar_jornada(
                idjornada, 
                e_nombre.get().upper().strip(), 
                e_clave.get().upper().strip(), 
                e_finicio.get_date().strftime("%Y-%m-%d"), 
                e_ffin.get_date().strftime("%Y-%m-%d")
            )
            if ok:
                messagebox.showinfo("Éxito", msj)
                top.destroy()
                self.cargar_jornadas()
            else:
                messagebox.showerror("Error", msj)

        tk.Button(top, text="Actualizar", bg=BTN_PRIMARY, fg="white", font=("Segoe UI", 10, "bold"), command=actualizar, bd=0).pack(fill="x", padx=15, pady=20)

    def modal_eliminar(self):
        item = self.tree.focus()
        if not item:
            messagebox.showwarning("Atención", "Seleccione una jornada de la tabla.")
            return

        vals = self.tree.item(item, "values")
        idjornada = vals[0]

        if messagebox.askyesno("Confirmar", "¿Está seguro que desea eliminar esta jornada?"):
            ok, msj = ModelJornadas.eliminar_jornada(idjornada)
            if ok:
                messagebox.showinfo("Éxito", msj)
                self.cargar_jornadas()
            else:
                messagebox.showerror("Error", msj)