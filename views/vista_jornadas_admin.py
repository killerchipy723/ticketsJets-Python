# views/vista_jornadas_admin.py
import tkinter as tk
from tkinter import ttk, messagebox
from database.jornadas_admin import ModelJornadasAdmin

COLOR_CARD_BG = "#212529"
COLOR_MAIN_BG = "#0f0f17"
COLOR_INPUT_BG = "#11111b"
TEXT_LIGHT = "#f8f9fa"
TEXT_MUTED = "#adb5bd"
BTN_PRIMARY = "#0d6efd"
BTN_SUCCESS = "#198754"
BTN_DANGER = "#dc3545"


class VistaJornadasAdmin(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_MAIN_BG)

        # Título
        lbl_titulo = tk.Label(
            self,
            text="⚡ Administración de Asignaciones por Jornada",
            font=("Segoe UI", 16, "bold"),
            fg=TEXT_LIGHT,
            bg=COLOR_MAIN_BG,
            anchor="w"
        )
        lbl_titulo.pack(fill="x", pady=(0, 15))

        self._crear_tabla_jornadas()
        self.cargar_jornadas()

    def _crear_tabla_jornadas(self):
        frame_tabla = tk.Frame(self, bg=COLOR_CARD_BG, highlightbackground="#313244", highlightthickness=1, padx=10, pady=10)
        frame_tabla.pack(fill="both", expand=True)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#181825", foreground=TEXT_LIGHT, fieldbackground="#181825", rowheight=30, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background=COLOR_CARD_BG, foreground=TEXT_LIGHT, font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", BTN_PRIMARY)])

        cols = ("idjornada", "nombre", "estado")
        self.tree = ttk.Treeview(frame_tabla, columns=cols, show="headings", height=8)

        self.tree.heading("idjornada", text="ID")
        self.tree.heading("nombre", text="Nombre de la Jornada")
        self.tree.heading("estado", text="Estado")

        self.tree.column("idjornada", width=60, anchor="center")
        self.tree.column("nombre", width=300)
        self.tree.column("estado", width=120, anchor="center")

        scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scroll.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # 🔹 MEJORA 1: Evento Doble Clic en la fila
        self.tree.bind("<Double-1>", lambda event: self.modal_administrar())

        btn_admin = tk.Button(
            self,
            text="⚙️ Administrar Equipos y Productos de la Jornada",
            font=("Segoe UI", 11, "bold"),
            bg=BTN_PRIMARY,
            fg="white",
            bd=0,
            cursor="hand2",
            command=self.modal_administrar
        )
        btn_admin.pack(fill="x", pady=(10, 0), ipady=8)

    def cargar_jornadas(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        jornadas = ModelJornadasAdmin.obtener_jornadas_activas()
        for j in jornadas:
            self.tree.insert("", "end", values=(j[0], j[1], j[2]))

    def modal_administrar(self):
        item = self.tree.focus()
        if not item:
            messagebox.showwarning("Atención", "Seleccione una jornada de la lista para administrar.")
            return

        vals = self.tree.item(item, "values")
        idjornada, nombre, estado = vals

        # Ventana Modal
        top = tk.Toplevel(self)
        top.title(f"Administrando: {nombre}")
        
        # 🔹 MEJORA 2: Centrado exacto en pantalla según la resolución del monitor
        ancho_modal = 850
        alto_modal = 580
        
        ancho_pantalla = top.winfo_screenwidth()
        alto_pantalla = top.winfo_screenheight()
        
        pos_x = (ancho_pantalla // 2) - (ancho_modal // 2)
        pos_y = (alto_pantalla // 2) - (alto_modal // 2)
        
        top.geometry(f"{ancho_modal}x{alto_modal}+{pos_x}+{pos_y}")
        top.configure(bg=COLOR_MAIN_BG)
        top.grab_set()

        lbl_top = tk.Label(top, text=f"Configurando Jornada: {nombre}", font=("Segoe UI", 12, "bold"), fg=TEXT_LIGHT, bg=COLOR_MAIN_BG)
        lbl_top.pack(pady=10)

        # Contenedor de 2 columnas (Puntos de Venta | Productos)
        f_columnas = tk.Frame(top, bg=COLOR_MAIN_BG)
        f_columnas.pack(fill="both", expand=True, padx=10, pady=5)
        f_columnas.columnconfigure((0, 1), weight=1)

        # --- COLUMNA IZQUIERDA: PUNTOS DE VENTA ---
        col_puntos = tk.LabelFrame(f_columnas, text=" Puntos de Venta / Cajas ", font=("Segoe UI", 10, "bold"), fg=TEXT_LIGHT, bg=COLOR_CARD_BG, padx=5, pady=5)
        col_puntos.grid(row=0, column=0, sticky="nsew", padx=5)

        canvas_p = tk.Canvas(col_puntos, bg=COLOR_CARD_BG, highlightthickness=0)
        scroll_p = ttk.Scrollbar(col_puntos, orient="vertical", command=canvas_p.yview)
        f_lista_p = tk.Frame(canvas_p, bg=COLOR_CARD_BG)
        
        id_win_p = canvas_p.create_window((0, 0), window=f_lista_p, anchor="nw")
        canvas_p.configure(yscrollcommand=scroll_p.set)

        def _on_canvas_configure_p(event):
            canvas_p.itemconfig(id_win_p, width=event.width)
        canvas_p.bind('<Configure>', _on_canvas_configure_p)

        canvas_p.pack(side="left", fill="both", expand=True)
        scroll_p.pack(side="right", fill="y")

        # --- COLUMNA DERECHA: PRODUCTOS ---
        col_prods = tk.LabelFrame(f_columnas, text=" Productos ", font=("Segoe UI", 10, "bold"), fg=TEXT_LIGHT, bg=COLOR_CARD_BG, padx=5, pady=5)
        col_prods.grid(row=0, column=1, sticky="nsew", padx=5)

        canvas_pr = tk.Canvas(col_prods, bg=COLOR_CARD_BG, highlightthickness=0)
        scroll_pr = ttk.Scrollbar(col_prods, orient="vertical", command=canvas_pr.yview)
        f_lista_pr = tk.Frame(canvas_pr, bg=COLOR_CARD_BG)
        
        id_win_pr = canvas_pr.create_window((0, 0), window=f_lista_pr, anchor="nw")
        canvas_pr.configure(yscrollcommand=scroll_pr.set)

        def _on_canvas_configure_pr(event):
            canvas_pr.itemconfig(id_win_pr, width=event.width)
        canvas_pr.bind('<Configure>', _on_canvas_configure_pr)

        canvas_pr.pack(side="left", fill="both", expand=True)
        scroll_pr.pack(side="right", fill="y")

        # Scroll con la rueda del ratón
        def _on_mousewheel(event, canvas):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas_p.bind_all("<MouseWheel>", lambda e: _on_mousewheel(e, canvas_p))
        canvas_pr.bind_all("<MouseWheel>", lambda e: _on_mousewheel(e, canvas_pr))

        # Funciones de Renderizado
        def renderizar_puntos():
            for w in f_lista_p.winfo_children():
                w.destroy()

            puntos = ModelJornadasAdmin.obtener_puntos_con_estado(idjornada)
            for p in puntos:
                f_item = tk.Frame(f_lista_p, bg=COLOR_INPUT_BG, pady=4, padx=8)
                f_item.pack(fill="x", pady=2, padx=2)

                tk.Label(f_item, text=p['nombre'], fg=TEXT_LIGHT, bg=COLOR_INPUT_BG, font=("Segoe UI", 9, "bold")).pack(side="left")

                if p['asignado']:
                    btn = tk.Button(f_item, text="✓ Asignado", bg=BTN_SUCCESS, fg="white", font=("Segoe UI", 8, "bold"), bd=0, cursor="hand2", padx=6,
                                    command=lambda id_p=p['idpunto']: toggle_p(id_p, True))
                else:
                    btn = tk.Button(f_item, text="+ Agregar", bg="#313244", fg=TEXT_LIGHT, font=("Segoe UI", 8), bd=0, cursor="hand2", padx=6,
                                    command=lambda id_p=p['idpunto']: toggle_p(id_p, False))
                btn.pack(side="right")

            f_lista_p.update_idletasks()
            canvas_p.configure(scrollregion=canvas_p.bbox("all"))

        def renderizar_productos():
            for w in f_lista_pr.winfo_children():
                w.destroy()

            prods = ModelJornadasAdmin.obtener_productos_con_estado(idjornada)
            for pr in prods:
                f_item = tk.Frame(f_lista_pr, bg=COLOR_INPUT_BG, pady=4, padx=8)
                f_item.pack(fill="x", pady=2, padx=2)

                txt = f"{pr['nombre']} (${pr['importe']:.2f})"
                tk.Label(f_item, text=txt, fg=TEXT_LIGHT, bg=COLOR_INPUT_BG, font=("Segoe UI", 9)).pack(side="left")

                if pr['asignado']:
                    btn = tk.Button(f_item, text="✓ Asignado", bg=BTN_SUCCESS, fg="white", font=("Segoe UI", 8, "bold"), bd=0, cursor="hand2", padx=6,
                                    command=lambda id_pr=pr['idproductos']: toggle_pr(id_pr, True))
                else:
                    btn = tk.Button(f_item, text="+ Agregar", bg="#313244", fg=TEXT_LIGHT, font=("Segoe UI", 8), bd=0, cursor="hand2", padx=6,
                                    command=lambda id_pr=pr['idproductos']: toggle_pr(id_pr, False))
                btn.pack(side="right")

            f_lista_pr.update_idletasks()
            canvas_pr.configure(scrollregion=canvas_pr.bbox("all"))

        def toggle_p(id_punto, estado_actual):
            ModelJornadasAdmin.toggle_punto_jornada(idjornada, id_punto, estado_actual)
            renderizar_puntos()

        def toggle_pr(id_producto, estado_actual):
            ModelJornadasAdmin.toggle_producto_jornada(idjornada, id_producto, estado_actual)
            renderizar_productos()

        # Cargar datos iniciales
        renderizar_puntos()
        renderizar_productos()

        # 🔹 MEJORA 3: Botonera inferior con botón "Aceptar"
        f_bottom = tk.Frame(top, bg=COLOR_MAIN_BG, pady=10)
        f_bottom.pack(fill="x", side="bottom")

        btn_aceptar = tk.Button(
            f_bottom,
            text="✓ Aceptar",
            font=("Segoe UI", 10, "bold"),
            bg=BTN_SUCCESS,
            fg="white",
            bd=0,
            cursor="hand2",
            padx=25,
            pady=6,
            command=top.destroy
        )
        btn_aceptar.pack(side="right", padx=15)