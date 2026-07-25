# vista_usuarios.py
import tkinter as tk
from tkinter import ttk, messagebox

# Intentamos importar la lógica de base de datos desde la carpeta database
try:
    from database.users import ModelUsuarios
except ImportError:
    ModelUsuarios = None


# --------------------------------------------------
# PALETA DE COLORES (Estilo TicketsJets / Admin Dashboard)
# --------------------------------------------------
COLOR_CARD_BG = "#212529"
COLOR_MAIN_BG = "#0f0f17"
TEXT_LIGHT = "#f8f9fa"
TEXT_MUTED = "#adb5bd"

BTN_PRIMARY = "#0d6efd"   # Azul (Guardar / Seleccionar)
BTN_SUCCESS = "#198754"   # Verde (Crear)
BTN_DANGER = "#dc3545"    # Rojo (Eliminar)
BTN_HOVER = "#313244"     # Hover


class VistaUsuarios(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_MAIN_BG)

        # Variables internas para gestión de estado
        self.usuario_id_seleccionado = None

        # --------------------------------------------------
        # TÍTULO DEL MÓDULO
        # --------------------------------------------------
        lbl_titulo = tk.Label(
            self,
            text="👤 Gestión y Registro de Usuarios",
            font=("Segoe UI", 16, "bold"),
            fg=TEXT_LIGHT,
            bg=COLOR_MAIN_BG,
            anchor="w"
        )
        lbl_titulo.pack(fill="x", pady=(0, 15))

        # --------------------------------------------------
        # CONTENEDOR PRINCIPAL
        # --------------------------------------------------
        contenedor = tk.Frame(self, bg=COLOR_MAIN_BG)
        contenedor.pack(fill="both", expand=True)

        self._crear_formulario(contenedor)
        self._crear_tabla(contenedor)

        # Cargar lista inicial
        self.cargar_usuarios()

    # ==========================================================
    # 1. PANEL FORMULARIO (ABM)
    # ==========================================================
    def _crear_formulario(self, parent):
        frame_form = tk.Frame(
            parent,
            bg=COLOR_CARD_BG,
            highlightbackground="#313244",
            highlightthickness=1,
            width=320,
            padx=15,
            pady=15
        )
        frame_form.pack(side="left", fill="y", padx=(0, 15))
        frame_form.pack_propagate(False)

        tk.Label(
            frame_form,
            text="Datos del Usuario",
            font=("Segoe UI", 12, "bold"),
            fg=TEXT_LIGHT,
            bg=COLOR_CARD_BG
        ).pack(anchor="w", pady=(0, 10))

        # --- Campos del Formulario ---
        self.txt_nombre = self._crear_campo(frame_form, "Usuario / Nombre:")
        self.txt_clave = self._crear_campo(frame_form, "Contraseña:", show="*")
        
        # Combo Rol
        tk.Label(frame_form, text="Rol:", font=("Segoe UI", 9, "bold"), fg=TEXT_MUTED, bg=COLOR_CARD_BG).pack(anchor="w", pady=(5, 2))
        self.cmb_rol = ttk.Combobox(
            frame_form,
            values=["Administrador", "Vendedor", "Supervisor", "Boletero"],
            state="readonly",
            font=("Segoe UI", 10)
        )
        self.cmb_rol.set("Vendedor")
        self.cmb_rol.pack(fill="x", pady=(0, 8))

        # Combo Estado
        tk.Label(frame_form, text="Estado:", font=("Segoe UI", 9, "bold"), fg=TEXT_MUTED, bg=COLOR_CARD_BG).pack(anchor="w", pady=(5, 2))
        self.cmb_estado = ttk.Combobox(
            frame_form,
            values=["ACTIVO", "INACTIVO"],
            state="readonly",
            font=("Segoe UI", 10)
        )
        self.cmb_estado.set("ACTIVO")
        self.cmb_estado.pack(fill="x", pady=(0, 8))

        self.txt_operador = self._crear_campo(frame_form, "Operador Asignado:")

        # --- Botones de Acción ---
        self.btn_guardar = tk.Button(
            frame_form,
            text="➕ Registrar Usuario",
            font=("Segoe UI", 10, "bold"),
            bg=BTN_SUCCESS,
            fg="white",
            bd=0,
            cursor="hand2",
            command=self.registrar_usuario
        )
        self.btn_guardar.pack(fill="x", pady=(10, 4), ipady=5)

        self.btn_actualizar = tk.Button(
            frame_form,
            text="✏️ Actualizar Usuario",
            font=("Segoe UI", 10, "bold"),
            bg=BTN_PRIMARY,
            fg="white",
            bd=0,
            cursor="hand2",
            state="disabled",
            command=self.actualizar_usuario
        )
        self.btn_actualizar.pack(fill="x", pady=4, ipady=5)

        self.btn_eliminar = tk.Button(
            frame_form,
            text="🗑️ Eliminar Usuario",
            font=("Segoe UI", 10, "bold"),
            bg=BTN_DANGER,
            fg="white",
            bd=0,
            cursor="hand2",
            state="disabled",
            command=self.eliminar_usuario
        )
        self.btn_eliminar.pack(fill="x", pady=4, ipady=5)

        btn_limpiar = tk.Button(
            frame_form,
            text="🧹 Limpiar Campos",
            font=("Segoe UI", 9),
            bg="#495057",
            fg="white",
            bd=0,
            cursor="hand2",
            command=self.limpiar_formulario
        )
        btn_limpiar.pack(fill="x", pady=(10, 0), ipady=4)

    def _crear_campo(self, parent, label_text, show=None):
        tk.Label(parent, text=label_text, font=("Segoe UI", 9, "bold"), fg=TEXT_MUTED, bg=COLOR_CARD_BG).pack(anchor="w", pady=(5, 2))
        entry = tk.Entry(
            parent,
            font=("Segoe UI", 10),
            bg="#11111b",
            fg="white",
            insertbackground="white",
            bd=1,
            relief="solid",
            show=show
        )
        entry.pack(fill="x", pady=(0, 5))
        return entry

    # ==========================================================
    # 2. PANEL TABLA (TREEVIEW)
    # ==========================================================
    def _crear_tabla(self, parent):
        frame_tabla = tk.Frame(
            parent,
            bg=COLOR_CARD_BG,
            highlightbackground="#313244",
            highlightthickness=1,
            padx=10,
            pady=10
        )
        frame_tabla.pack(side="right", fill="both", expand=True)

        # Personalización de Estilo Dark Mode
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="#181825",
            foreground=TEXT_LIGHT,
            fieldbackground="#181825",
            rowheight=30,
            font=("Segoe UI", 10)
        )
        style.configure(
            "Treeview.Heading",
            background=COLOR_CARD_BG,
            foreground=TEXT_LIGHT,
            font=("Segoe UI", 10, "bold")
        )
        style.map("Treeview", background=[("selected", BTN_PRIMARY)])

        cols = ("id", "nombre", "rol", "estado", "operador")
        self.tree = ttk.Treeview(frame_tabla, columns=cols, show="headings", selectmode="browse")

        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Usuario")
        self.tree.heading("rol", text="Rol")
        self.tree.heading("estado", text="Estado")
        self.tree.heading("operador", text="Operador")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("nombre", width=140)
        self.tree.column("rol", width=110, anchor="center")
        self.tree.column("estado", width=90, anchor="center")
        self.tree.column("operador", width=150)

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Evento de selección en la tabla
        self.tree.bind("<<TreeviewSelect>>", self.al_seleccionar_registro)

    # ==========================================================
    # 3. LÓGICA DE OPERACIONES Y CONEXIÓN
    # ==========================================================
    def cargar_usuarios(self):
        """Carga y actualiza los registros en la tabla."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not ModelUsuarios:
            return

        usuarios = ModelUsuarios.obtener_usuarios()
        for u in usuarios:
            # Espera formato: (idusuarios, nombre, rol, estado, operador)
            self.tree.insert("", "end", values=u)

    def registrar_usuario(self):
        nombre = self.txt_nombre.get().upper().strip()
        clave = self.txt_clave.get().strip()
        rol = self.cmb_rol.get()
        estado = self.cmb_estado.get()
        operador = self.txt_operador.get().upper().strip()

        if not nombre or not clave:
            messagebox.showwarning("Atención", "El nombre de usuario y la clave son obligatorios.")
            return

        if ModelUsuarios:
            exito, mensaje = ModelUsuarios.crear_usuario(nombre, clave, rol, estado, operador)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.limpiar_formulario()
                self.cargar_usuarios()
            else:
                messagebox.showerror("Error", mensaje)

    def actualizar_usuario(self):
        if not self.usuario_id_seleccionado:
            return

        nombre = self.txt_nombre.get().upper().strip()
        clave = self.txt_clave.get().strip()
        rol = self.cmb_rol.get()
        estado = self.cmb_estado.get()
        operador = self.txt_operador.get().upper().strip()

        if not nombre or not clave:
            messagebox.showwarning("Atención", "El nombre de usuario y la clave son obligatorios.")
            return

        if ModelUsuarios:
            exito, mensaje = ModelUsuarios.actualizar_usuario(self.usuario_id_seleccionado, nombre, clave, rol, estado, operador)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.limpiar_formulario()
                self.cargar_usuarios()
            else:
                messagebox.showerror("Error", mensaje)

    def eliminar_usuario(self):
        if not self.usuario_id_seleccionado:
            return

        confirmar = messagebox.askyesno(
            "Confirmar Eliminación",
            "¿Desea eliminar permanentemente este usuario?"
        )
        if not confirmar:
            return

        if ModelUsuarios:
            exito, mensaje = ModelUsuarios.eliminar_usuario(self.usuario_id_seleccionado)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.limpiar_formulario()
                self.cargar_usuarios()
            else:
                messagebox.showerror("Error", mensaje)

    # ==========================================================
    # 4. FUNCIONES AUXILIARES
    # ==========================================================
    def al_seleccionar_registro(self, event):
        item = self.tree.focus()
        if not item:
            return

        valores = self.tree.item(item, "values")
        if valores:
            self.usuario_id_seleccionado = valores[0]

            self.txt_nombre.delete(0, tk.END)
            self.txt_nombre.insert(0, valores[1])

            self.cmb_rol.set(valores[2])
            self.cmb_estado.set(valores[3])

            self.txt_operador.delete(0, tk.END)
            self.txt_operador.insert(0, valores[4])

            self.txt_clave.delete(0, tk.END)  # Se deja vacío para ingresar clave nueva si se desea

            # Habilitar botones de edición y deshabilitar nuevo
            self.btn_guardar.config(state="disabled")
            self.btn_actualizar.config(state="normal")
            self.btn_eliminar.config(state="normal")

    def limpiar_formulario(self):
        self.usuario_id_seleccionado = None
        self.txt_nombre.delete(0, tk.END)
        self.txt_clave.delete(0, tk.END)
        self.txt_operador.delete(0, tk.END)
        self.cmb_rol.set("Vendedor")
        self.cmb_estado.set("ACTIVO")

        self.btn_guardar.config(state="normal")
        self.btn_actualizar.config(state="disabled")
        self.btn_eliminar.config(state="disabled")