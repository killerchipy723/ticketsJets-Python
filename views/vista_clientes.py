# views/vista_clientes.py
import tkinter as tk
from tkinter import ttk, messagebox
from database.clientes_db import (
    obtener_todos_clientes_db,
    guardar_cliente_db,
    actualizar_cliente_db,
    eliminar_cliente_db,
    buscar_clientes_db
)

class VistaClientes(tk.Frame):
    def __init__(self, parent, session_data=None):
        super().__init__(parent, bg="#1e1e1e")
        self.session_data = session_data or {}
        self.id_cliente_seleccionado = None

        self.crear_interfaz()
        self.cargar_datos()

    def crear_interfaz(self):
        # Header
        lbl_titulo = tk.Label(
            self, text="👥 Gestión de Clientes",
            font=("Segoe UI", 14, "bold"), fg="white", bg="#1e1e1e"
        )
        lbl_titulo.pack(anchor="w", padx=20, pady=15)

        # Contenedor Principal
        frame_main = tk.Frame(self, bg="#1e1e1e")
        frame_main.pack(fill="both", expand=True, padx=20, pady=10)

        # --- Formulario (Izquierda) ---
        frame_form = tk.LabelFrame(
            frame_main, text=" Datos del Cliente ",
            font=("Segoe UI", 10, "bold"), fg="white", bg="#252526", bd=1
        )
        frame_form.pack(side="left", fill="y", padx=(0, 15), ipadx=10, ipady=10)

        # Apellido y Nombre
        tk.Label(frame_form, text="Apellido y Nombre:*", font=("Segoe UI", 9), fg="white", bg="#252526").pack(anchor="w", padx=10, pady=(10, 2))
        self.txt_apenomb = tk.Entry(frame_form, font=("Segoe UI", 10), width=30)
        self.txt_apenomb.pack(padx=10, pady=2)

        # DNI
        tk.Label(frame_form, text="DNI:*", font=("Segoe UI", 9), fg="white", bg="#252526").pack(anchor="w", padx=10, pady=(10, 2))
        self.txt_dni = tk.Entry(frame_form, font=("Segoe UI", 10), width=30)
        self.txt_dni.pack(padx=10, pady=2)

        # CUIL
        tk.Label(frame_form, text="CUIL:", font=("Segoe UI", 9), fg="white", bg="#252526").pack(anchor="w", padx=10, pady=(10, 2))
        self.txt_cuil = tk.Entry(frame_form, font=("Segoe UI", 10), width=30)
        self.txt_cuil.pack(padx=10, pady=2)

        # Correo
        tk.Label(frame_form, text="Correo Electrónico:", font=("Segoe UI", 9), fg="white", bg="#252526").pack(anchor="w", padx=10, pady=(10, 2))
        self.txt_correo = tk.Entry(frame_form, font=("Segoe UI", 10), width=30)
        self.txt_correo.pack(padx=10, pady=2)

        # Fecha Nacimiento (AAAA-MM-DD)
        tk.Label(frame_form, text="Fecha Nac. (AAAA-MM-DD):", font=("Segoe UI", 9), fg="white", bg="#252526").pack(anchor="w", padx=10, pady=(10, 2))
        self.txt_fecha_nac = tk.Entry(frame_form, font=("Segoe UI", 10), width=30)
        self.txt_fecha_nac.pack(padx=10, pady=2)

        # Botones
        btn_frame = tk.Frame(frame_form, bg="#252526")
        btn_frame.pack(fill="x", padx=10, pady=20)

        self.btn_guardar = tk.Button(
            btn_frame, text="Guardar Cliente", bg="#198754", fg="white",
            font=("Segoe UI", 9, "bold"), bd=0, pady=6, command=self.guardar_cliente
        )
        self.btn_guardar.pack(fill="x", pady=3)

        self.btn_eliminar = tk.Button(
            btn_frame, text="Eliminar Selección", bg="#dc3545", fg="white",
            font=("Segoe UI", 9, "bold"), bd=0, pady=6, command=self.eliminar_cliente, state="disabled"
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

        # Barra de búsqueda superior
        frame_buscar = tk.Frame(frame_tabla, bg="#1e1e1e")
        frame_buscar.pack(fill="x", pady=(0, 10))

        tk.Label(frame_buscar, text="🔍 Buscar:", fg="white", bg="#1e1e1e", font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 5))
        self.txt_buscar_tabla = tk.Entry(frame_buscar, font=("Segoe UI", 10))
        self.txt_buscar_tabla.pack(side="left", fill="x", expand=True)
        self.txt_buscar_tabla.bind("<KeyRelease>", lambda e: self.buscar_en_tabla())

        columnas = ("idclientes", "apenomb", "dni", "cuil", "correo", "fecha_nacimiento")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", selectmode="browse")

        self.tabla.heading("idclientes", text="ID")
        self.tabla.heading("apenomb", text="Apellido y Nombre")
        self.tabla.heading("dni", text="DNI")
        self.tabla.heading("cuil", text="CUIL")
        self.tabla.heading("correo", text="Correo")
        self.tabla.heading("fecha_nacimiento", text="F. Nacimiento")

        self.tabla.column("idclientes", width=40, anchor="center")
        self.tabla.column("apenomb", width=180)
        self.tabla.column("dni", width=90)
        self.tabla.column("cuil", width=100)
        self.tabla.column("correo", width=150)
        self.tabla.column("fecha_nacimiento", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tabla.bind("<<TreeviewSelect>>", self.al_seleccionar_registro)

    def cargar_datos(self):
        clientes, err = obtener_todos_clientes_db()
        if err:
            messagebox.showerror("Error", err)
            return

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for c in clientes:
            fnac = str(c["fecha_nacimiento"]) if c["fecha_nacimiento"] else ""
            self.tabla.insert("", "end", values=(
                c["idclientes"], c["apenomb"], c["dni"], c["cuil"] or "", c["correo"] or "", fnac
            ))

    def buscar_en_tabla(self):
        q = self.txt_buscar_tabla.get().strip()
        clientes, err = buscar_clientes_db(q)
        if err:
            return

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for c in clientes:
            fnac = str(c["fecha_nacimiento"]) if c.get("fecha_nacimiento") else ""
            self.tabla.insert("", "end", values=(
                c["idclientes"], c["apenomb"], c["dni"], c.get("cuil", ""), c.get("correo", ""), fnac
            ))

    def al_seleccionar_registro(self, event):
        item_sel = self.tabla.selection()
        if not item_sel:
            return

        v = self.tabla.item(item_sel[0], "values")
        self.id_cliente_seleccionado = v[0]

        self.txt_apenomb.delete(0, tk.END)
        self.txt_apenomb.insert(0, v[1])

        self.txt_dni.delete(0, tk.END)
        self.txt_dni.insert(0, v[2])

        self.txt_cuil.delete(0, tk.END)
        self.txt_cuil.insert(0, v[3])

        self.txt_correo.delete(0, tk.END)
        self.txt_correo.insert(0, v[4])

        self.txt_fecha_nac.delete(0, tk.END)
        self.txt_fecha_nac.insert(0, v[5])

        self.btn_guardar.config(text="Actualizar Cliente", bg="#ffc107", fg="black")
        self.btn_eliminar.config(state="normal")

    def guardar_cliente(self):
        apenomb = self.txt_apenomb.get().strip()
        dni = self.txt_dni.get().strip()
        cuil = self.txt_cuil.get().strip()
        correo = self.txt_correo.get().strip()
        fecha_nac = self.txt_fecha_nac.get().strip()

        if not apenomb or not dni:
            messagebox.showwarning("Atención", "Apellido/Nombre y DNI son obligatorios.")
            return

        if self.id_cliente_seleccionado is None:
            ok, _, msg = guardar_cliente_db(apenomb, dni, cuil, correo, fecha_nac)
        else:
            ok, msg = actualizar_cliente_db(self.id_cliente_seleccionado, apenomb, dni, cuil, correo, fecha_nac)

        if ok:
            messagebox.showinfo("Éxito", msg)
            self.limpiar_formulario()
            self.cargar_datos()
        else:
            messagebox.showerror("Error", msg)

    def eliminar_cliente(self):
        if not self.id_cliente_seleccionado:
            return

        if messagebox.askyesno("Confirmar", "¿Desea eliminar el cliente seleccionado?"):
            ok, msg = eliminar_cliente_db(self.id_cliente_seleccionado)
            if ok:
                messagebox.showinfo("Éxito", msg)
                self.limpiar_formulario()
                self.cargar_datos()
            else:
                messagebox.showerror("Error", msg)

    def limpiar_formulario(self):
        self.id_cliente_seleccionado = None
        self.txt_apenomb.delete(0, tk.END)
        self.txt_dni.delete(0, tk.END)
        self.txt_cuil.delete(0, tk.END)
        self.txt_correo.delete(0, tk.END)
        self.txt_fecha_nac.delete(0, tk.END)

        self.btn_guardar.config(text="Guardar Cliente", bg="#198754", fg="white")
        self.btn_eliminar.config(state="disabled")