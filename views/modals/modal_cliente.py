# views/modals/modal_cliente.py
import tkinter as tk
from tkinter import ttk, messagebox
from database.clientes_db import buscar_clientes_db, guardar_cliente_db


class ModalBuscarCliente(tk.Toplevel):
    def __init__(self, parent, callback_seleccion):
        super().__init__(parent)
        self.title("🔍 Seleccionar / Agregar Cliente")
        self.geometry("680x520")
        self.configure(bg="#1e1e1e")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        self.callback_seleccion = callback_seleccion

        self.crear_interfaz()
        self.filtrar_clientes()

        # 👈 Centramos el modal en la pantalla
        self.centrar_en_pantalla()

    def centrar_en_pantalla(self):
        """Calcula el centro de la pantalla y posiciona la ventana."""
        self.update_idletasks()

        ancho_ventana = 680
        alto_ventana = 520

        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()

        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)

        self.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

    def crear_interfaz(self):
        # --- Búsqueda ---
        frame_busqueda = tk.Frame(self, bg="#1e1e1e")
        frame_busqueda.pack(fill="x", padx=15, pady=(15, 5))

        tk.Label(
            frame_busqueda, text="Buscar (DNI o Apellido/Nombre):", 
            font=("Segoe UI", 10, "bold"), fg="white", bg="#1e1e1e"
        ).pack(anchor="w")

        self.txt_buscar = tk.Entry(frame_busqueda, font=("Segoe UI", 11), bg="#252526", fg="white", insertbackground="white")
        self.txt_buscar.pack(fill="x", pady=5)
        self.txt_buscar.bind("<KeyRelease>", lambda e: self.filtrar_clientes())
        self.txt_buscar.focus_set()

        # --- Tabla de Resultados ---
        frame_tabla = tk.Frame(self, bg="#1e1e1e")
        frame_tabla.pack(fill="both", expand=True, padx=15, pady=5)

        columnas = ("id", "apenomb", "dni", "cuil", "correo")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=7, selectmode="browse")

        self.tabla.heading("id", text="ID")
        self.tabla.heading("apenomb", text="Apellido y Nombre")
        self.tabla.heading("dni", text="DNI")
        self.tabla.heading("cuil", text="CUIL")
        self.tabla.heading("correo", text="Correo")

        self.tabla.column("id", width=40, anchor="center")
        self.tabla.column("apenomb", width=200)
        self.tabla.column("dni", width=90)
        self.tabla.column("cuil", width=100)
        self.tabla.column("correo", width=160)

        scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscroll=scroll.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        self.tabla.bind("<Double-1>", lambda e: self.confirmar_seleccion())

        # --- Botones Acción ---
        frame_acciones = tk.Frame(self, bg="#1e1e1e")
        frame_acciones.pack(fill="x", padx=15, pady=10)

        btn_seleccionar = tk.Button(
            frame_acciones, text="✓ Seleccionar Existente", bg="#0d6efd", fg="white",
            font=("Segoe UI", 9, "bold"), bd=0, pady=6, command=self.confirmar_seleccion
        )
        btn_seleccionar.pack(side="left", fill="x", expand=True, padx=(0, 5))

        btn_nuevo = tk.Button(
            frame_acciones, text="+ Registrar Nuevo Cliente", bg="#198754", fg="white",
            font=("Segoe UI", 9, "bold"), bd=0, pady=6, command=self.desplegar_formulario_nuevo
        )
        btn_nuevo.pack(side="right", fill="x", expand=True, padx=(5, 0))

        # --- Formulario Rápido Alta ---
        self.frame_nuevo = tk.LabelFrame(
            self, text=" Alta Rápida de Cliente ", font=("Segoe UI", 9, "bold"), 
            fg="white", bg="#252526", bd=1
        )

        tk.Label(self.frame_nuevo, text="Ape. y Nom.:*", fg="white", bg="#252526").grid(row=0, column=0, padx=5, pady=4, sticky="e")
        self.txt_nuevo_apenomb = tk.Entry(self.frame_nuevo, width=22)
        self.txt_nuevo_apenomb.grid(row=0, column=1, padx=5, pady=4)

        tk.Label(self.frame_nuevo, text="DNI:*", fg="white", bg="#252526").grid(row=0, column=2, padx=5, pady=4, sticky="e")
        self.txt_nuevo_dni = tk.Entry(self.frame_nuevo, width=15)
        self.txt_nuevo_dni.grid(row=0, column=3, padx=5, pady=4)

        tk.Label(self.frame_nuevo, text="CUIL:", fg="white", bg="#252526").grid(row=1, column=0, padx=5, pady=4, sticky="e")
        self.txt_nuevo_cuil = tk.Entry(self.frame_nuevo, width=22)
        self.txt_nuevo_cuil.grid(row=1, column=1, padx=5, pady=4)

        tk.Label(self.frame_nuevo, text="Correo:", fg="white", bg="#252526").grid(row=1, column=2, padx=5, pady=4, sticky="e")
        self.txt_nuevo_correo = tk.Entry(self.frame_nuevo, width=15)
        self.txt_nuevo_correo.grid(row=1, column=3, padx=5, pady=4)

        btn_guardar_nuevo = tk.Button(
            self.frame_nuevo, text="Guardar y Seleccionar", bg="#ffc107", fg="black",
            font=("Segoe UI", 9, "bold"), bd=0, pady=5, command=self.guardar_y_seleccionar_nuevo
        )
        btn_guardar_nuevo.grid(row=2, column=0, columnspan=4, pady=8, sticky="ew", padx=10)

    def filtrar_clientes(self):
        criterio = self.txt_buscar.get().strip()
        clientes, err = buscar_clientes_db(criterio)
        if err:
            return

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for c in clientes:
            self.tabla.insert("", "end", values=(
                c["idclientes"], c["apenomb"], c["dni"], c.get("cuil", ""), c.get("correo", "")
            ))

    def desplegar_formulario_nuevo(self):
        self.frame_nuevo.pack(fill="x", padx=15, pady=(0, 15))
        texto = self.txt_buscar.get().strip()
        if texto.isdigit():
            self.txt_nuevo_dni.insert(0, texto)
            self.txt_nuevo_apenomb.focus_set()
        else:
            self.txt_nuevo_apenomb.insert(0, texto)
            self.txt_nuevo_dni.focus_set()

    def guardar_y_seleccionar_nuevo(self):
        apenomb = self.txt_nuevo_apenomb.get().strip()
        dni = self.txt_nuevo_dni.get().strip()
        cuil = self.txt_nuevo_cuil.get().strip()
        correo = self.txt_nuevo_correo.get().strip()

        if not apenomb or not dni:
            messagebox.showwarning("Atención", "Apellido/Nombre y DNI son obligatorios.", parent=self)
            return

        ok, id_nuevo, msg = guardar_cliente_db(apenomb, dni, cuil, correo)
        if ok:
            cliente = {
                "idclientes": id_nuevo,
                "apenomb": apenomb.upper(),
                "dni": dni,
                "cuil": cuil,
                "correo": correo
            }
            self.callback_seleccion(cliente)
            self.destroy()
        else:
            messagebox.showerror("Error", msg, parent=self)

    def confirmar_seleccion(self):
        item_sel = self.tabla.selection()
        if not item_sel:
            messagebox.showwarning("Atención", "Seleccione un cliente de la lista.", parent=self)
            return

        v = self.tabla.item(item_sel[0], "values")
        cliente = {
            "idclientes": v[0],
            "apenomb": v[1],
            "dni": v[2],
            "cuil": v[3],
            "correo": v[4]
        }
        self.callback_seleccion(cliente)
        self.destroy()