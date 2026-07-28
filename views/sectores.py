# views/sectores.py
import tkinter as tk
from tkinter import ttk, messagebox
from database.sectores import (
    obtener_sectores_y_jornadas,
    guardar_sector_entrada_db,
    actualizar_sector_entrada_db,
    eliminar_sector_entrada_db
)


class VistaSectoresEntradas(tk.Frame):
    def __init__(self, parent, session_data=None):
        super().__init__(parent, bg="#1e1e1e")
        self.session_data = session_data

        self.jornadas_map = {}  # Mapeo 'Nombre Jornada' -> idjornada
        self.id_sector_seleccionado = None

        self.crear_interfaz()
        self.cargar_datos()

    def crear_interfaz(self):
        # Header
        lbl_titulo = tk.Label(
            self, text="⚙️ Gestión y Vinculación de Sectores de Entradas",
            font=("Segoe UI", 14, "bold"), fg="white", bg="#1e1e1e"
        )
        lbl_titulo.pack(anchor="w", padx=20, pady=15)

        # Contenedor Split (Izquierda: Formulario, Derecha: Tabla)
        frame_main = tk.Frame(self, bg="#1e1e1e")
        frame_main.pack(fill="both", expand=True, padx=20, pady=10)

        # --- Formulario (Izquierda) ---
        frame_form = tk.LabelFrame(
            frame_main, text=" Datos del Sector ",
            font=("Segoe UI", 10, "bold"), fg="white", bg="#252526", bd=1
        )
        frame_form.pack(side="left", fill="y", padx=(0, 15), ipadx=10, ipady=10)

        # Jornada
        tk.Label(frame_form, text="Jornada:", font=("Segoe UI", 9), fg="white", bg="#252526").pack(anchor="w", padx=10, pady=(10, 2))
        self.cb_jornada = ttk.Combobox(frame_form, state="readonly", width=28)
        self.cb_jornada.pack(padx=10, pady=2)

        # Nombre Sector
        tk.Label(frame_form, text="Nombre del Sector:", font=("Segoe UI", 9), fg="white", bg="#252526").pack(anchor="w", padx=10, pady=(10, 2))
        self.txt_nombre = tk.Entry(frame_form, font=("Segoe UI", 10), width=30)
        self.txt_nombre.pack(padx=10, pady=2)

        # Precio
        tk.Label(frame_form, text="Precio ($):", font=("Segoe UI", 9), fg="white", bg="#252526").pack(anchor="w", padx=10, pady=(10, 2))
        self.txt_precio = tk.Entry(frame_form, font=("Segoe UI", 10), width=30)
        self.txt_precio.pack(padx=10, pady=2)

        # Estado
        tk.Label(frame_form, text="Estado:", font=("Segoe UI", 9), fg="white", bg="#252526").pack(anchor="w", padx=10, pady=(10, 2))
        self.cb_estado = ttk.Combobox(frame_form, values=["activo", "inactivo"], state="readonly", width=28)
        self.cb_estado.current(0)
        self.cb_estado.pack(padx=10, pady=2)

        # Botones Acción
        btn_frame = tk.Frame(frame_form, bg="#252526")
        btn_frame.pack(fill="x", padx=10, pady=20)

        self.btn_guardar = tk.Button(
            btn_frame, text="Guardar", bg="#198754", fg="white",
            font=("Segoe UI", 9, "bold"), bd=0, pady=6, command=self.guardar_sector
        )
        self.btn_guardar.pack(fill="x", pady=3)

        self.btn_eliminar = tk.Button(
            btn_frame, text="Eliminar Selección", bg="#dc3545", fg="white",
            font=("Segoe UI", 9, "bold"), bd=0, pady=6, command=self.eliminar_sector, state="disabled"
        )
        self.btn_eliminar.pack(fill="x", pady=3)

        self.btn_limpiar = tk.Button(
            btn_frame, text="Limpiar / Nuevo", bg="#6c757d", fg="white",
            font=("Segoe UI", 9), bd=0, pady=4, command=self.limpiar_formulario
        )
        self.btn_limpiar.pack(fill="x", pady=3)

        # --- Tabla (Derecha) ---
        frame_tabla = tk.Frame(frame_main, bg="#1e1e1e")
        frame_tabla.pack(side="right", fill="both", expand=True)

        columnas = ("idsector", "jornada", "nombre", "precio", "estado")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", selectmode="browse")

        self.tabla.heading("idsector", text="ID")
        self.tabla.heading("jornada", text="Jornada Vinculada")
        self.tabla.heading("nombre", text="Sector")
        self.tabla.heading("precio", text="Precio")
        self.tabla.heading("estado", text="Estado")

        self.tabla.column("idsector", width=40, anchor="center")
        self.tabla.column("jornada", width=180, anchor="w")
        self.tabla.column("nombre", width=140, anchor="w")
        self.tabla.column("precio", width=80, anchor="e")
        self.tabla.column("estado", width=80, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tabla.bind("<<TreeviewSelect>>", self.al_seleccionar_registro)

    def cargar_datos(self):
        sectores, jornadas, err = obtener_sectores_y_jornadas()
        if err:
            messagebox.showerror("Error", err)
            return

        # Cargar Jornadas en el Selector
        self.jornadas_map = {j["nombre"]: j["idjornada"] for j in jornadas}
        nombres_jornadas = list(self.jornadas_map.keys())
        self.cb_jornada["values"] = nombres_jornadas
        if nombres_jornadas:
            self.cb_jornada.current(0)

        # Limpiar y rellenar tabla de sectores
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for s in sectores:
            self.tabla.insert("", "end", values=(
                s["idsector"],
                s["jornada"],
                s["nombre"],
                f"${s['precio']:.2f}",
                s["estado"]
            ), tags=(s["idjornada"],))

    def al_seleccionar_registro(self, event):
        item_sel = self.tabla.selection()
        if not item_sel:
            return

        valores = self.tabla.item(item_sel[0], "values")
        idjornada_tags = self.tabla.item(item_sel[0], "tags")

        self.id_sector_seleccionado = valores[0]
        self.cb_jornada.set(valores[1])
        self.txt_nombre.delete(0, tk.END)
        self.txt_nombre.insert(0, valores[2])

        # Limpiar signo $ para edición
        precio_clean = valores[3].replace("$", "").strip()
        self.txt_precio.delete(0, tk.END)
        self.txt_precio.insert(0, precio_clean)

        self.cb_estado.set(valores[4])

        self.btn_guardar.config(text="Actualizar Sector", bg="#ffc107", fg="black")
        self.btn_eliminar.config(state="normal")

    def guardar_sector(self):
        jornada_nombre = self.cb_jornada.get()
        nombre = self.txt_nombre.get().strip()
        precio_str = self.txt_precio.get().strip()
        estado = self.cb_estado.get()

        if not jornada_nombre or not nombre or not precio_str:
            messagebox.showwarning("Atención", "Complete todos los campos obligatorios.")
            return

        try:
            precio = float(precio_str)
        except ValueError:
            messagebox.showwarning("Atención", "Ingrese un precio numérico válido.")
            return

        idjornada = self.jornadas_map.get(jornada_nombre)

        if self.id_sector_seleccionado is None:
            # Insertar
            ok, msg = guardar_sector_entrada_db(idjornada, nombre, precio, estado)
        else:
            # Actualizar
            ok, msg = actualizar_sector_entrada_db(self.id_sector_seleccionado, idjornada, nombre, precio, estado)

        if ok:
            messagebox.showinfo("Éxito", msg)
            self.limpiar_formulario()
            self.cargar_datos()
        else:
            messagebox.showerror("Error", msg)

    def eliminar_sector(self):
        if not self.id_sector_seleccionado:
            return

        if messagebox.askyesno("Confirmar", "¿Desea eliminar el sector seleccionado?"):
            ok, msg = eliminar_sector_entrada_db(self.id_sector_seleccionado)
            if ok:
                messagebox.showinfo("Éxito", msg)
                self.limpiar_formulario()
                self.cargar_datos()
            else:
                messagebox.showerror("Error", msg)

    def limpiar_formulario(self):
        self.id_sector_seleccionado = None
        self.txt_nombre.delete(0, tk.END)
        self.txt_precio.delete(0, tk.END)
        self.cb_estado.current(0)
        self.btn_guardar.config(text="Guardar", bg="#198754", fg="white")
        self.btn_eliminar.config(state="disabled")