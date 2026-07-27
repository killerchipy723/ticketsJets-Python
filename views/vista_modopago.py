# views/vista_modopago.py
import tkinter as tk
from tkinter import ttk, messagebox
from database.modopago_db import ModelModoPago

# Paleta de colores Dark Mode
COLOR_CARD_BG = "#212529"
COLOR_MAIN_BG = "#0f0f17"
COLOR_INPUT_BG = "#11111b"
TEXT_LIGHT = "#f8f9fa"
TEXT_MUTED = "#adb5bd"
BTN_PRIMARY = "#0d6efd"
BTN_WARNING = "#ffc107"
BTN_DANGER = "#dc3545"


class VistaModoPago(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_MAIN_BG, padx=10, pady=10)

        # Título Principal
        lbl_titulo = tk.Label(
            self,
            text="💳 Gestión de Modos de Pago",
            font=("Segoe UI", 14, "bold"),
            fg=TEXT_LIGHT,
            bg=COLOR_MAIN_BG,
            anchor="w",
        )
        lbl_titulo.pack(fill="x", pady=(0, 8))

        # Contenedor de 2 columnas (Formulario e Historial)
        paneles = tk.Frame(self, bg=COLOR_MAIN_BG)
        paneles.pack(fill="both", expand=True)

        # Panel Izquierdo (Formulario)
        self.f_izq = tk.Frame(
            paneles,
            bg=COLOR_CARD_BG,
            highlightbackground="#313244",
            highlightthickness=1,
            padx=12,
            pady=12,
        )
        self.f_izq.pack(side="left", fill="y", expand=False, padx=(0, 10))

        # Panel Derecho (Tabla)
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

        # Cargar Tabla al Iniciar
        self.cargar_modos_pago()

    def _crear_formulario(self, parent):
        tk.Label(
            parent,
            text="Registrar Modo de Pago",
            font=("Segoe UI", 11, "bold"),
            fg=TEXT_LIGHT,
            bg=COLOR_CARD_BG,
        ).pack(anchor="w", pady=(0, 10))

        # Campo: Modo de Pago
        tk.Label(
            parent,
            text="Modo de Pago:",
            font=("Segoe UI", 8, "bold"),
            fg=TEXT_MUTED,
            bg=COLOR_CARD_BG,
        ).pack(anchor="w", pady=(5, 2))

        self.txt_modo = tk.Entry(
            parent,
            font=("Segoe UI", 9),
            bg=COLOR_INPUT_BG,
            fg="white",
            insertbackground="white",
            width=28,
        )
        self.txt_modo.pack(fill="x", pady=(0, 10))

        # Campo: Estado
        tk.Label(
            parent,
            text="Estado:",
            font=("Segoe UI", 8, "bold"),
            fg=TEXT_MUTED,
            bg=COLOR_CARD_BG,
        ).pack(anchor="w", pady=(5, 2))

        self.cmb_estado = ttk.Combobox(
            parent,
            values=["Activo", "Inactivo"],
            state="readonly",
            font=("Segoe UI", 9),
        )
        self.cmb_estado.set("Activo")
        self.cmb_estado.pack(fill="x", pady=(0, 15))

        # Botón Guardar
        btn_guardar = tk.Button(
            parent,
            text="💾 Guardar",
            font=("Segoe UI", 9, "bold"),
            bg=BTN_PRIMARY,
            fg="white",
            bd=0,
            cursor="hand2",
            command=self.guardar_modo_pago,
        )
        btn_guardar.pack(fill="x", ipady=5)

    def _crear_tabla(self, parent):
        tk.Label(
            parent,
            text="Modos de Pago Registrados",
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

        f_tabla_inner = tk.Frame(parent, bg=COLOR_CARD_BG)
        f_tabla_inner.pack(fill="both", expand=True)

        cols = ("idmodo", "modo", "estado")
        self.tree = ttk.Treeview(
            f_tabla_inner, columns=cols, show="headings", selectmode="browse"
        )

        self.tree.heading("idmodo", text="ID")
        self.tree.heading("modo", text="Modo de Pago")
        self.tree.heading("estado", text="Estado")

        self.tree.column("idmodo", width=50, anchor="center")
        self.tree.column("modo", width=200)
        self.tree.column("estado", width=90, anchor="center")

        scroll = ttk.Scrollbar(
            f_tabla_inner, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscroll=scroll.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # Botones de Acción
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

    def cargar_modos_pago(self):
        """Limpia y vuelve a cargar los datos en el Treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        modos = ModelModoPago.obtener_modos_pago()
        for m in modos:
            if isinstance(m, dict):
                row = (m.get("idmodo"), m.get("modo"), m.get("estado"))
            else:
                row = (m[0], m[1], m[2])
            self.tree.insert("", "end", values=row)

    def guardar_modo_pago(self):
        modo = self.txt_modo.get().upper().strip()
        estado = self.cmb_estado.get().strip()

        if not modo:
            messagebox.showwarning(
                "Atención", "El nombre del modo de pago es obligatorio."
            )
            return

        exito, msj = ModelModoPago.crear_modo_pago(modo, estado)
        if exito:
            messagebox.showinfo("Éxito", msj)
            self.txt_modo.delete(0, tk.END)
            self.cmb_estado.set("Activo")
            self.cargar_modos_pago()
        else:
            messagebox.showerror("Error", msj)

    def modal_editar(self):
        item = self.tree.focus()
        if not item:
            messagebox.showwarning(
                "Atención", "Seleccione un registro de la tabla."
            )
            return

        vals = self.tree.item(item, "values")
        idmodo, modo, estado = vals

        top = tk.Toplevel(self)
        top.title(f"Editar Modo: {modo}")
        top.geometry("320x220")
        top.configure(bg=COLOR_CARD_BG)
        top.grab_set()

        tk.Label(
            top,
            text="Modo de Pago:",
            fg=TEXT_MUTED,
            bg=COLOR_CARD_BG,
            font=("Segoe UI", 8, "bold"),
        ).pack(anchor="w", padx=15, pady=(12, 2))

        e_modo = tk.Entry(
            top, font=("Segoe UI", 9), bg=COLOR_INPUT_BG, fg="white"
        )
        e_modo.insert(0, modo)
        e_modo.pack(fill="x", padx=15)

        tk.Label(
            top,
            text="Estado:",
            fg=TEXT_MUTED,
            bg=COLOR_CARD_BG,
            font=("Segoe UI", 8, "bold"),
        ).pack(anchor="w", padx=15, pady=(8, 2))

        c_estado = ttk.Combobox(
            top, values=["Activo", "Inactivo"], state="readonly"
        )
        c_estado.set(estado)
        c_estado.pack(fill="x", padx=15)

        def actualizar():
            nuevo_modo = e_modo.get().upper().strip()
            nuevo_estado = c_estado.get().strip()

            if not nuevo_modo:
                messagebox.showwarning("Atención", "El nombre es requerido.")
                return

            ok, msj = ModelModoPago.actualizar_modo_pago(
                idmodo, nuevo_modo, nuevo_estado
            )
            if ok:
                messagebox.showinfo("Éxito", msj)
                top.destroy()
                self.cargar_modos_pago()
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
            cursor="hand2",
        ).pack(fill="x", padx=15, pady=15)

    def modal_eliminar(self):
        item = self.tree.focus()
        if not item:
            messagebox.showwarning(
                "Atención", "Seleccione un registro de la tabla."
            )
            return

        vals = self.tree.item(item, "values")
        idmodo = vals[0]

        if messagebox.askyesno(
            "Confirmar", "¿Desea eliminar este modo de pago?"
        ):
            ok, msj = ModelModoPago.eliminar_modo_pago(idmodo)
            if ok:
                messagebox.showinfo("Éxito", msj)
                self.cargar_modos_pago()
            else:
                messagebox.showerror("Error", msj)