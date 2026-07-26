# views/vista_productos.py
import tkinter as tk
from tkinter import ttk, messagebox
from database.productos import ModelProductos

# Estilos de color (Dark Mode Bootstrap)
COLOR_CARD_BG = "#212529"
COLOR_MAIN_BG = "#0f0f17"
COLOR_INPUT_BG = "#11111b"
TEXT_LIGHT = "#f8f9fa"
TEXT_MUTED = "#adb5bd"
BTN_PRIMARY = "#0d6efd"
BTN_WARNING = "#ffc107"
BTN_DANGER = "#dc3545"


class VistaProductos(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_MAIN_BG)

        # Título principal
        lbl_titulo = tk.Label(
            self,
            text="📦 Catálogo y Gestión de Productos",
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
        self.cargar_productos()

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
            text=" Registrar Nuevo Producto ",
            font=("Segoe UI", 12, "bold"),
            fg=TEXT_LIGHT,
            bg=COLOR_CARD_BG
        ).pack(anchor="w", pady=(0, 10))

        # --- FILA 1: Nombre, Importe, Stock y Estado ---
        f1 = tk.Frame(frame_card, bg=COLOR_CARD_BG)
        f1.pack(fill="x", pady=(0, 10))

        # Nombre
        tk.Label(f1, text="Nombre del Producto:", font=("Segoe UI", 9, "bold"), fg=TEXT_MUTED, bg=COLOR_CARD_BG).grid(row=0, column=0, sticky="w", padx=5)
        self.txt_nombre = tk.Entry(f1, font=("Segoe UI", 10), bg=COLOR_INPUT_BG, fg="white", insertbackground="white")
        self.txt_nombre.grid(row=1, column=0, sticky="ew", padx=5, pady=(2, 5))

        # Importe / Precio
        tk.Label(f1, text="Importe / Precio ($):", font=("Segoe UI", 9, "bold"), fg=TEXT_MUTED, bg=COLOR_CARD_BG).grid(row=0, column=1, sticky="w", padx=5)
        self.txt_importe = tk.Entry(f1, font=("Segoe UI", 10), bg=COLOR_INPUT_BG, fg="white", insertbackground="white")
        self.txt_importe.grid(row=1, column=1, sticky="ew", padx=5, pady=(2, 5))

        # Stock
        tk.Label(f1, text="Stock Inicial:", font=("Segoe UI", 9, "bold"), fg=TEXT_MUTED, bg=COLOR_CARD_BG).grid(row=0, column=2, sticky="w", padx=5)
        self.txt_stock = tk.Entry(f1, font=("Segoe UI", 10), bg=COLOR_INPUT_BG, fg="white", insertbackground="white")
        self.txt_stock.insert(0, "0")
        self.txt_stock.grid(row=1, column=2, sticky="ew", padx=5, pady=(2, 5))

        # Estado
        tk.Label(f1, text="Estado:", font=("Segoe UI", 9, "bold"), fg=TEXT_MUTED, bg=COLOR_CARD_BG).grid(row=0, column=3, sticky="w", padx=5)
        self.cmb_estado = ttk.Combobox(f1, values=["Activo", "Inactivo"], state="readonly", font=("Segoe UI", 10))
        self.cmb_estado.set("Activo")
        self.cmb_estado.grid(row=1, column=3, sticky="ew", padx=5, pady=(2, 5))

        f1.columnconfigure((0, 1, 2, 3), weight=1)

        # --- BOTÓN REGISTRAR ---
        btn_registrar = tk.Button(
            frame_card,
            text="Guardar Producto",
            font=("Segoe UI", 10, "bold"),
            bg=BTN_PRIMARY,
            fg="white",
            bd=0,
            cursor="hand2",
            command=self.guardar_producto
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

        cols = ("idproductos", "nombre", "importe", "stock", "estado")
        self.tree = ttk.Treeview(frame_tabla, columns=cols, show="headings", height=10)

        self.tree.heading("idproductos", text="ID")
        self.tree.heading("nombre", text="Nombre del Producto")
        self.tree.heading("importe", text="Importe ($)")
        self.tree.heading("stock", text="Stock Disponible")
        self.tree.heading("estado", text="Estado")

        self.tree.column("idproductos", width=50, anchor="center")
        self.tree.column("nombre", width=250)
        self.tree.column("importe", width=120, anchor="e")
        self.tree.column("stock", width=120, anchor="center")
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
    def cargar_productos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        productos = ModelProductos.obtener_productos()
        for prod in productos:
            # prod[0]=idproductos, prod[1]=nombre, prod[2]=importe, prod[3]=estado, prod[4]=stock
            importe_fmt = f"$ {float(prod[2] or 0):,.2f}"
            self.tree.insert("", "end", values=(prod[0], prod[1], importe_fmt, prod[4], prod[3]))

    def guardar_producto(self):
        nombre = self.txt_nombre.get().strip()
        str_importe = self.txt_importe.get().strip().replace(",", ".")
        str_stock = self.txt_stock.get().strip()
        estado = self.cmb_estado.get()

        if not nombre or not str_importe or not str_stock:
            messagebox.showwarning("Atención", "Por favor complete todos los campos obligatorios.")
            return

        try:
            importe = float(str_importe)
            stock = int(str_stock)
        except ValueError:
            messagebox.showerror("Error", "El importe debe ser un número decimal válido y el stock un número entero.")
            return

        exito, msj = ModelProductos.crear_producto(nombre, importe, estado, stock)
        if exito:
            messagebox.showinfo("Éxito", msj)
            self.txt_nombre.delete(0, tk.END)
            self.txt_importe.delete(0, tk.END)
            self.txt_stock.delete(0, tk.END)
            self.txt_stock.insert(0, "0")
            self.cmb_estado.set("Activo")
            self.cargar_productos()
        else:
            messagebox.showerror("Error", msj)

    # --- ACCIONES MODALES (EDITAR / ELIMINAR) ---
    def modal_editar(self):
        item = self.tree.focus()
        if not item:
            messagebox.showwarning("Atención", "Seleccione un producto de la tabla.")
            return

        vals = self.tree.item(item, "values")
        idproductos, nombre, importe_str, stock, estado = vals

        # Limpiar el formato de moneda ($ 1,000.00 -> 1000.00)
        importe_clean = importe_str.replace("$", "").replace(",", "").strip()

        top = tk.Toplevel(self)
        top.title(f"Editar: {nombre}")
        top.geometry("380x340")
        top.configure(bg=COLOR_CARD_BG)
        top.grab_set()

        # Nombre
        tk.Label(top, text="Nombre del Producto:", fg=TEXT_MUTED, bg=COLOR_CARD_BG, font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=15, pady=(15, 2))
        e_nombre = tk.Entry(top, font=("Segoe UI", 10), bg=COLOR_INPUT_BG, fg="white", insertbackground="white")
        e_nombre.insert(0, nombre)
        e_nombre.pack(fill="x", padx=15)

        # Importe
        tk.Label(top, text="Importe / Precio ($):", fg=TEXT_MUTED, bg=COLOR_CARD_BG, font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=15, pady=(10, 2))
        e_importe = tk.Entry(top, font=("Segoe UI", 10), bg=COLOR_INPUT_BG, fg="white", insertbackground="white")
        e_importe.insert(0, importe_clean)
        e_importe.pack(fill="x", padx=15)

        # Stock
        tk.Label(top, text="Stock:", fg=TEXT_MUTED, bg=COLOR_CARD_BG, font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=15, pady=(10, 2))
        e_stock = tk.Entry(top, font=("Segoe UI", 10), bg=COLOR_INPUT_BG, fg="white", insertbackground="white")
        e_stock.insert(0, stock)
        e_stock.pack(fill="x", padx=15)

        # Estado
        tk.Label(top, text="Estado:", fg=TEXT_MUTED, bg=COLOR_CARD_BG, font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=15, pady=(10, 2))
        c_estado = ttk.Combobox(top, values=["Activo", "Inactivo"], state="readonly", font=("Segoe UI", 10))
        c_estado.set(estado)
        c_estado.pack(fill="x", padx=15)

        def actualizar():
            nom = e_nombre.get().strip()
            str_imp = e_importe.get().strip().replace(",", ".")
            str_stk = e_stock.get().strip()
            est = c_estado.get()

            if not nom or not str_imp or not str_stk:
                messagebox.showwarning("Atención", "Todos los campos son obligatorios.")
                return

            try:
                imp = float(str_imp)
                stk = int(str_stk)
            except ValueError:
                messagebox.showerror("Error", "Valores numéricos inválidos para importe o stock.")
                return

            ok, msj = ModelProductos.actualizar_producto(idproductos, nom, imp, est, stk)
            if ok:
                messagebox.showinfo("Éxito", msj)
                top.destroy()
                self.cargar_productos()
            else:
                messagebox.showerror("Error", msj)

        tk.Button(top, text="Actualizar Producto", bg=BTN_PRIMARY, fg="white", font=("Segoe UI", 10, "bold"), command=actualizar, bd=0, cursor="hand2").pack(fill="x", padx=15, pady=20, ipady=4)

    def modal_eliminar(self):
        item = self.tree.focus()
        if not item:
            messagebox.showwarning("Atención", "Seleccione un producto de la tabla.")
            return

        vals = self.tree.item(item, "values")
        idproductos = vals[0]
        nombre = vals[1]

        if messagebox.askyesno("Confirmar", f"¿Está seguro que desea eliminar el producto '{nombre}'?"):
            ok, msj = ModelProductos.eliminar_producto(idproductos)
            if ok:
                messagebox.showinfo("Éxito", msj)
                self.cargar_productos()
            else:
                messagebox.showerror("Error", msj)