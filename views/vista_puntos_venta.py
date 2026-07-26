# views/vista_puntos_venta.py
import uuid
import tkinter as tk
from tkinter import ttk, messagebox
from database.puntos_venta import ModelPuntosVenta

# Estilos de color (Dark Mode Bootstrap)
COLOR_CARD_BG = "#212529"
COLOR_MAIN_BG = "#0f0f17"
COLOR_INPUT_BG = "#11111b"
TEXT_LIGHT = "#f8f9fa"
TEXT_MUTED = "#adb5bd"
BTN_PRIMARY = "#0d6efd"
BTN_WARNING = "#ffc107"
BTN_DANGER = "#dc3545"


class VistaPuntosVenta(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_MAIN_BG)

        self.mac_local = self._obtener_mac_local()

        # Título principal
        lbl_titulo = tk.Label(
            self,
            text="💻 Gestión de Puntos de Venta (POS)",
            font=("Segoe UI", 16, "bold"),
            fg=TEXT_LIGHT,
            bg=COLOR_MAIN_BG,
            anchor="w"
        )
        lbl_titulo.pack(fill="x", pady=(0, 10))

        # Panel desplazable
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
        self.cargar_puntos_venta()

    def _obtener_mac_local(self):
        """Obtiene la dirección MAC del equipo local."""
        try:
            mac_num = uuid.getnode()
            mac = ':'.join(['{:02x}'.format((mac_num >> elements) & 0xff) for elements in range(0, 8*6, 8)][::-1])
            return mac.upper()
        except Exception:
            return "DESCONOCIDO"

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
            text=" Configuración / Registro de Punto de Venta ",
            font=("Segoe UI", 12, "bold"),
            fg=TEXT_LIGHT,
            bg=COLOR_CARD_BG
        ).pack(anchor="w", pady=(0, 10))

        # --- FILA 1: Nombre, MAC y Estado ---
        f1 = tk.Frame(frame_card, bg=COLOR_CARD_BG)
        f1.pack(fill="x", pady=(0, 10))

        # Nombre
        tk.Label(f1, text="Nombre del Punto:", font=("Segoe UI", 9, "bold"), fg=TEXT_MUTED, bg=COLOR_CARD_BG).grid(row=0, column=0, sticky="w", padx=5)
        self.txt_nombre = tk.Entry(f1, font=("Segoe UI", 10), bg=COLOR_INPUT_BG, fg="white", insertbackground="white")
        self.txt_nombre.grid(row=1, column=0, sticky="ew", padx=5, pady=(2, 5))

        # MAC / idEquipo
        f_mac_lbl = tk.Frame(f1, bg=COLOR_CARD_BG)
        f_mac_lbl.grid(row=0, column=1, sticky="w", padx=5)

        tk.Label(f_mac_lbl, text="MAC (idEquipo):", font=("Segoe UI", 9, "bold"), fg=TEXT_MUTED, bg=COLOR_CARD_BG).pack(side="left")
        
        btn_automac = tk.Button(
            f_mac_lbl,
            text="🎯 Usar MAC Local",
            bg="#313244",
            fg=TEXT_LIGHT,
            font=("Segoe UI", 7, "bold"),
            bd=0,
            cursor="hand2",
            command=self._autocompletar_mac
        )
        btn_automac.pack(side="left", padx=(8, 0))

        self.txt_mac = tk.Entry(f1, font=("Segoe UI", 10), bg=COLOR_INPUT_BG, fg="white", insertbackground="white")
        self.txt_mac.grid(row=1, column=1, sticky="ew", padx=5, pady=(2, 5))
        self._autocompletar_mac()

        # Estado
        tk.Label(f1, text="Estado:", font=("Segoe UI", 9, "bold"), fg=TEXT_MUTED, bg=COLOR_CARD_BG).grid(row=0, column=2, sticky="w", padx=5)
        self.cmb_estado = ttk.Combobox(f1, values=["Activo", "Inactivo"], state="readonly", font=("Segoe UI", 10))
        self.cmb_estado.set("Activo")
        self.cmb_estado.grid(row=1, column=2, sticky="ew", padx=5, pady=(2, 5))

        f1.columnconfigure((0, 1, 2), weight=1)

        # --- BOTÓN REGISTRAR ---
        btn_registrar = tk.Button(
            frame_card,
            text="Registrar Punto de Venta",
            font=("Segoe UI", 10, "bold"),
            bg=BTN_PRIMARY,
            fg="white",
            bd=0,
            cursor="hand2",
            command=self.guardar_punto_venta
        )
        btn_registrar.pack(fill="x", pady=(10, 0), ipady=6)

    def _autocompletar_mac(self):
        self.txt_mac.delete(0, tk.END)
        self.txt_mac.insert(0, self.mac_local)

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

        cols = ("idpunto", "nombre", "idequipo", "estado")
        self.tree = ttk.Treeview(frame_tabla, columns=cols, show="headings", height=8)

        self.tree.heading("idpunto", text="ID")
        self.tree.heading("nombre", text="Nombre Punto de Venta")
        self.tree.heading("idequipo", text="Dirección MAC (idEquipo)")
        self.tree.heading("estado", text="Estado")

        self.tree.column("idpunto", width=50, anchor="center")
        self.tree.column("nombre", width=220)
        self.tree.column("idequipo", width=220, anchor="center")
        self.tree.column("estado", width=100, anchor="center")

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
    def cargar_puntos_venta(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        puntos = ModelPuntosVenta.obtener_puntos_venta()
        for p in puntos:
            # p[0]=idpunto, p[1]=nombre, p[2]=idequipo, p[3]=estado
            self.tree.insert("", "end", values=(p[0], p[1], p[2], p[3]))

    def guardar_punto_venta(self):
        nombre = self.txt_nombre.get().strip()
        mac = self.txt_mac.get().strip().upper()
        estado = self.cmb_estado.get()

        if not nombre or not mac:
            messagebox.showwarning("Atención", "El nombre y la dirección MAC son obligatorios.")
            return

        exito, msj = ModelPuntosVenta.crear_punto_venta(nombre, mac, estado)
        if exito:
            messagebox.showinfo("Éxito", msj)
            self.txt_nombre.delete(0, tk.END)
            self._autocompletar_mac()
            self.cmb_estado.set("Activo")
            self.cargar_puntos_venta()
        else:
            messagebox.showerror("Error", msj)

    # --- ACCIONES MODALES (EDITAR / ELIMINAR) ---
    def modal_editar(self):
        item = self.tree.focus()
        if not item:
            messagebox.showwarning("Atención", "Seleccione un equipo de la tabla.")
            return

        vals = self.tree.item(item, "values")
        idpunto, nombre, idequipo, estado = vals

        top = tk.Toplevel(self)
        top.title(f"Editar: {nombre}")
        top.geometry("380x280")
        top.configure(bg=COLOR_CARD_BG)
        top.grab_set()

        tk.Label(top, text="Nombre del Punto:", fg=TEXT_MUTED, bg=COLOR_CARD_BG, font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=15, pady=(15, 2))
        e_nombre = tk.Entry(top, font=("Segoe UI", 10), bg=COLOR_INPUT_BG, fg="white", insertbackground="white")
        e_nombre.insert(0, nombre)
        e_nombre.pack(fill="x", padx=15)

        tk.Label(top, text="MAC (idEquipo):", fg=TEXT_MUTED, bg=COLOR_CARD_BG, font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=15, pady=(10, 2))
        e_mac = tk.Entry(top, font=("Segoe UI", 10), bg=COLOR_INPUT_BG, fg="white", insertbackground="white")
        e_mac.insert(0, idequipo)
        e_mac.pack(fill="x", padx=15)

        tk.Label(top, text="Estado:", fg=TEXT_MUTED, bg=COLOR_CARD_BG, font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=15, pady=(10, 2))
        c_estado = ttk.Combobox(top, values=["Activo", "Inactivo"], state="readonly", font=("Segoe UI", 10))
        c_estado.set(estado)
        c_estado.pack(fill="x", padx=15)

        def actualizar():
            nom = e_nombre.get().strip()
            mc = e_mac.get().strip().upper()
            est = c_estado.get()

            if not nom or not mc:
                messagebox.showwarning("Atención", "Todos los campos son obligatorios.")
                return

            ok, msj = ModelPuntosVenta.actualizar_punto_venta(idpunto, nom, mc, est)
            if ok:
                messagebox.showinfo("Éxito", msj)
                top.destroy()
                self.cargar_puntos_venta()
            else:
                messagebox.showerror("Error", msj)

        tk.Button(top, text="Actualizar", bg=BTN_PRIMARY, fg="white", font=("Segoe UI", 10, "bold"), command=actualizar, bd=0, cursor="hand2").pack(fill="x", padx=15, pady=20, ipady=4)

    def modal_eliminar(self):
        item = self.tree.focus()
        if not item:
            messagebox.showwarning("Atención", "Seleccione un equipo de la tabla.")
            return

        vals = self.tree.item(item, "values")
        idpunto = vals[0]

        if messagebox.askyesno("Confirmar", "¿Está seguro que desea eliminar este punto de venta?"):
            ok, msj = ModelPuntosVenta.eliminar_punto_venta(idpunto)
            if ok:
                messagebox.showinfo("Éxito", msj)
                self.cargar_puntos_venta()
            else:
                messagebox.showerror("Error", msj)