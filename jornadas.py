import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry  # Importamos el selector de fecha con calendario
import os

# Paleta de colores
COLOR_CARD_BG = "#212529"
COLOR_MAIN_BG = "#0f0f17"
TEXT_LIGHT = "#f8f9fa"
TEXT_MUTED = "#adb5bd"
BTN_PRIMARY = "#0d6efd"
BTN_WARNING = "#ffc107"
BTN_DANGER = "#dc3545"

class VistaJornadas(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_MAIN_BG)

        # Encabezado
        lbl_titulo = tk.Label(
            self, text="📅 Gestión de Jornadas", 
            font=("Segoe UI", 16, "bold"), fg=TEXT_LIGHT, bg=COLOR_MAIN_BG
        )
        lbl_titulo.pack(anchor="w", pady=(0, 15))

         # Obtener la ruta dinámica del archivo .ico
        DIRECTORIO_BASE = os.path.dirname(os.path.abspath(__file__))
        RUTA_ICONO = os.path.join(DIRECTORIO_BASE, "icono.ico")
        
                # Aplicar el ícono de forma segura si existe
        if os.path.exists(RUTA_ICONO):
                    try:
                        self.iconbitmap(RUTA_ICONO)
                    except tk.TclError:
                        pass

        # Botón para Crear Nueva Jornada
        btn_nueva = tk.Button(
            self, text="➕ Crear Nueva Jornada",
            font=("Segoe UI", 10, "bold"), bg=BTN_PRIMARY, fg="white",
            bd=0, padx=15, pady=8, cursor="hand2", command=self.abrir_modal_crear
        )
        btn_nueva.pack(anchor="w", pady=(0, 15))

        # Tabla de Jornadas
        self._crear_tabla()
        
        # Botones de Acción
        frame_acciones = tk.Frame(self, bg=COLOR_MAIN_BG)
        frame_acciones.pack(fill="x", pady=10)

        tk.Button(
            frame_acciones, text="✏️ Editar Seleccionada",
            bg=BTN_WARNING, fg="black", bd=0, padx=12, pady=6,
            font=("Segoe UI", 9, "bold"), cursor="hand2", command=self.abrir_modal_editar
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            frame_acciones, text="🗑️ Eliminar Seleccionada",
            bg=BTN_DANGER, fg="white", bd=0, padx=12, pady=6,
            font=("Segoe UI", 9, "bold"), cursor="hand2", command=self.eliminar_jornada
        ).pack(side="left")

    def _crear_tabla(self):
        frame_tabla = tk.Frame(self, bg=COLOR_CARD_BG, highlightbackground="#313244", highlightthickness=1)
        frame_tabla.pack(fill="both", expand=True)

        columnas = ("id", "nombre", "clave", "finicio", "ffin", "estado")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", selectmode="browse")

        self.tabla.heading("id", text="ID")
        self.tabla.heading("nombre", text="Jornada")
        self.tabla.heading("clave", text="Clave")
        self.tabla.heading("finicio", text="Inicio")
        self.tabla.heading("ffin", text="Fin")
        self.tabla.heading("estado", text="Estado")

        self.tabla.column("id", width=50, anchor="center")
        self.tabla.column("nombre", width=200)
        self.tabla.column("clave", width=100, anchor="center")
        self.tabla.column("finicio", width=110, anchor="center")
        self.tabla.column("ffin", width=110, anchor="center")
        self.tabla.column("estado", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.cargar_datos_demo()

    def cargar_datos_demo(self):
        jornadas_demo = [
            (1, "NOCHE VIERNES 24", "J24V", "2026-07-24", "2026-07-25", "Activa"),
            (2, "SÁBADO PREMIUM", "J25S", "2026-07-25", "2026-07-26", "Pendiente")
        ]
        for item in jornadas_demo:
            self.tabla.insert("", "end", values=item)

    def abrir_modal_crear(self):
        FormularioJornadaModal(
            self, 
            titulo="Crear Nueva Jornada", 
            on_save=self.guardar_nueva_jornada
        )

    def abrir_modal_editar(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione una jornada de la tabla para editar.")
            return

        item_id = seleccion[0]
        datos_fila = self.tabla.item(item_id, "values")

        FormularioJornadaModal(
            self, 
            titulo=f"Editar: {datos_fila[1]}", 
            datos=datos_fila,
            on_save=lambda nuevos_datos: self.actualizar_jornada(item_id, nuevos_datos)
        )

    def guardar_nueva_jornada(self, datos):
        nuevo_id = len(self.tabla.get_children()) + 1
        fila = (nuevo_id, datos["nombre"], datos["clave"], datos["finicio"], datos["ffin"], "Activa")
        self.tabla.insert("", "end", values=fila)
        messagebox.showinfo("Éxito", f"Jornada '{datos['nombre']}' creada exitosamente.")

    def actualizar_jornada(self, item_id, datos):
        id_existente = self.tabla.item(item_id, "values")[0]
        fila_actualizada = (id_existente, datos["nombre"], datos["clave"], datos["finicio"], datos["ffin"], "Activa")
        self.tabla.item(item_id, values=fila_actualizada)
        messagebox.showinfo("Éxito", f"Jornada '{datos['nombre']}' actualizada correctamente.")

    def eliminar_jornada(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione una jornada para eliminar.")
            return

        datos_fila = self.tabla.item(seleccion[0], "values")
        if messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro que desea eliminar la jornada '{datos_fila[1]}'?"):
            self.tabla.delete(seleccion[0])
            messagebox.showinfo("Éxito", "La jornada ha sido eliminada.")


# --------------------------------------------------
# MODAL CENTRADO CON CALENDARIO
# --------------------------------------------------
class FormularioJornadaModal(tk.Toplevel):
    def __init__(self, parent, titulo="Jornada", datos=None, on_save=None):
        super().__init__(parent)
        self.title(titulo)
        self.configure(bg=COLOR_MAIN_BG)
        self.transient(parent)

        self.datos = datos
        self.on_save = on_save

        # 1. CENTRAR VENTANA MODAL EN LA PANTALLA
        ancho = 650
        alto = 650
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")
        self.grab_set()  # Modal activo

        # Título
        lbl_head = tk.Label(self, text=titulo, font=("Segoe UI", 14, "bold"), fg=TEXT_LIGHT, bg=COLOR_MAIN_BG)
        lbl_head.pack(anchor="w", padx=20, pady=(15, 10))

        # Contenedor
        container = tk.Frame(self, bg=COLOR_MAIN_BG)
        container.pack(fill="both", expand=True, padx=20, pady=5)

        # Inputs Formulario Principal
        frame_inputs = tk.Frame(container, bg=COLOR_CARD_BG, padx=15, pady=15)
        frame_inputs.pack(fill="x", pady=(0, 10))

        tk.Label(frame_inputs, text="Nombre del Evento:", fg=TEXT_LIGHT, bg=COLOR_CARD_BG).grid(row=0, column=0, sticky="w", pady=2)
        self.ent_nombre = tk.Entry(frame_inputs, font=("Segoe UI", 10))
        self.ent_nombre.grid(row=1, column=0, sticky="ew", padx=(0, 10), pady=(0, 10))

        tk.Label(frame_inputs, text="Clave:", fg=TEXT_LIGHT, bg=COLOR_CARD_BG).grid(row=0, column=1, sticky="w", pady=2)
        self.ent_clave = tk.Entry(frame_inputs, font=("Segoe UI", 10))
        self.ent_clave.grid(row=1, column=1, sticky="ew", pady=(0, 10))

        # 2. INPUTS TIPO CALENDARIO (DateEntry)
        tk.Label(frame_inputs, text="Fecha Inicio:", fg=TEXT_LIGHT, bg=COLOR_CARD_BG).grid(row=2, column=0, sticky="w", pady=2)
        self.ent_finicio = DateEntry(
            frame_inputs, font=("Segoe UI", 10), date_pattern="yyyy-mm-dd",
            background="#0d6efd", foreground="white", headersbackground="#212529"
        )
        self.ent_finicio.grid(row=3, column=0, sticky="ew", padx=(0, 10))

        tk.Label(frame_inputs, text="Fecha Fin:", fg=TEXT_LIGHT, bg=COLOR_CARD_BG).grid(row=2, column=1, sticky="w", pady=2)
        self.ent_ffin = DateEntry(
            frame_inputs, font=("Segoe UI", 10), date_pattern="yyyy-mm-dd",
            background="#0d6efd", foreground="white", headersbackground="#212529"
        )
        self.ent_ffin.grid(row=3, column=1, sticky="ew")

        frame_inputs.columnconfigure(0, weight=1)
        frame_inputs.columnconfigure(1, weight=1)

        # --- SECCIÓN EQUIPOS ---
        self.lista_equipos = ["Punto Boletería 1", "Punto Boletería 2", "Caja Barra VIP", "Punto Entrada Norte"]
        self.vars_equipos = []
        self._crear_seccion_checkboxes(
            parent_container=container,
            titulo="Equipos / Puntos de Venta",
            check_todos_label="Habilitar todos los equipos",
            items=self.lista_equipos,
            vars_list=self.vars_equipos
        )

        # --- SECCIÓN PRODUCTOS ---
        self.lista_productos = ["Entrada General ($1500)", "Entrada VIP ($3000)", "Bebida ($500)", "Estacionamiento ($1000)"]
        self.vars_productos = []
        self._crear_seccion_checkboxes(
            parent_container=container,
            titulo="Productos Habilitados",
            check_todos_label="Habilitar todos los productos",
            items=self.lista_productos,
            vars_list=self.vars_productos
        )

        # Botón Guardar
        btn_guardar = tk.Button(
            self, text="💾 Guardar Jornada",
            font=("Segoe UI", 11, "bold"), bg=BTN_PRIMARY, fg="white",
            bd=0, pady=10, cursor="hand2", command=self.guardar
        )
        btn_guardar.pack(fill="x", padx=20, pady=15)

        # Pre-cargar valores en caso de edición
        if self.datos:
            self.ent_nombre.insert(0, self.datos[1])
            self.ent_clave.insert(0, self.datos[2])
            # Seteamos las fechas en el selector con formato AAAA-MM-DD
            if self.datos[3]:
                self.ent_finicio.set_date(self.datos[3])
            if self.datos[4]:
                self.ent_ffin.set_date(self.datos[4])

    def _crear_seccion_checkboxes(self, parent_container, titulo, check_todos_label, items, vars_list):
        frame_box = tk.LabelFrame(parent_container, text=f" {titulo} ", fg=TEXT_LIGHT, bg=COLOR_CARD_BG, padx=10, pady=10)
        frame_box.pack(fill="x", pady=5)

        var_todos = tk.BooleanVar(value=False)

        def toggle_todos():
            estado = var_todos.get()
            for v in vars_list:
                v.set(estado)

        chk_todos = tk.Checkbutton(
            frame_box, text=check_todos_label, variable=var_todos,
            font=("Segoe UI", 9, "bold"), fg=TEXT_LIGHT, bg=COLOR_CARD_BG,
            selectcolor="#313244", activebackground=COLOR_CARD_BG, activeforeground=TEXT_LIGHT,
            command=toggle_todos
        )
        chk_todos.pack(anchor="w", pady=(0, 5))

        frame_grid = tk.Frame(frame_box, bg=COLOR_CARD_BG)
        frame_grid.pack(fill="x")

        for index, item_nombre in enumerate(items):
            var_item = tk.BooleanVar(value=False)
            vars_list.append(var_item)

            chk = tk.Checkbutton(
                frame_grid, text=item_nombre, variable=var_item,
                fg=TEXT_LIGHT, bg=COLOR_CARD_BG, selectcolor="#313244",
                activebackground=COLOR_CARD_BG, activeforeground=TEXT_LIGHT
            )
            chk.grid(row=index // 2, column=index % 2, sticky="w", padx=5, pady=2)

    def guardar(self):
        nombre = self.ent_nombre.get().strip().upper()
        clave = self.ent_clave.get().strip().upper()
        finicio = self.ent_finicio.get_date().strftime("%Y-%m-%d")
        ffin = self.ent_ffin.get_date().strftime("%Y-%m-%d")

        if not nombre or not clave:
            messagebox.showerror("Error", "Nombre y Clave son obligatorios.", parent=self)
            return

        equipos_sel = [self.lista_equipos[i] for i, v in enumerate(self.vars_equipos) if v.get()]
        productos_sel = [self.lista_productos[i] for i, v in enumerate(self.vars_productos) if v.get()]

        datos_formulario = {
            "nombre": nombre,
            "clave": clave,
            "finicio": finicio,
            "ffin": ffin,
            "equipos": equipos_sel,
            "productos": productos_sel
        }

        if self.on_save:
            self.on_save(datos_formulario)

        self.destroy()