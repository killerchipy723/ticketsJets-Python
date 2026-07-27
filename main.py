import os
import subprocess
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

# EN MAIN.PY - LÍNEA 7
from database.cerrarCaja import cerrar_caja_bd, obtener_datos_cierre_caja  #  CORRECTO
from database.ventas import (
    agregar_al_carrito,
    carrito,
    modificar_cantidad,
    obtener_datos_sesion_actual,
    obtener_modos_pago,
    obtener_productos,
    obtener_recaudacion_acumulada_jornada,
    obtener_total_carrito,
    registrar_venta,
)
from reports.impresion import imprimir_ticket_silencioso
from sesion import Sesion


from reports.impresion import imprimir_ticket_cierre_silencioso

# Referencias globales UI
ventana = None
lbl_reloj = None
lbl_total_num = None
lbl_recaudacion_val = None
frame_lista_carrito = None

# Variables de Tipo de Pago e Insumos UI
var_tipo_pago = None  # "SIMPLE" o "COMBINADO"
combo_modo_simple = None  # Combobox para seleccionar método en Pago Simple
modos_pago_cache = []  # Lista cacheada de modos de pago

# Cargar catálogo de productos
productos_bebidas = obtener_productos()


# ==========================================================
# FUNCIONES REFRESCO DE INTERFAZ
# ==========================================================


def actualizar_reloj():
    if ventana and ventana.winfo_exists():
        ahora = datetime.now().strftime("%d/%m/%Y  |  %H:%M:%S")
        lbl_reloj.config(text=f"🕒 {ahora}")
        ventana.after(1000, actualizar_reloj)


def actualizar_recaudacion_ui():
    """Consulta a la base de datos el acumulado real de la jornada."""
    if lbl_recaudacion_val:
        monto_acumulado = obtener_recaudacion_acumulada_jornada()
        lbl_recaudacion_val.config(text=f"${monto_acumulado:,.2f}")


def actualizar_interfaz_carrito():
    if not frame_lista_carrito:
        return

    for widget in frame_lista_carrito.winfo_children():
        widget.destroy()

    for nombre, datos in carrito.items():
        item_frame = tk.Frame(frame_lista_carrito, bg="#212529", pady=5)
        item_frame.pack(fill="x", padx=5, pady=2)

        lbl_prod = tk.Label(
            item_frame,
            text=f"{nombre} x{datos['cantidad']}",
            fg="#f8f9fa",
            bg="#212529",
            font=("Segoe UI", 10),
            anchor="w",
        )
        lbl_prod.pack(side="left", fill="x", expand=True)

        lbl_subtotal = tk.Label(
            item_frame,
            text=f"${datos['precio']*datos['cantidad']:,.2f}",
            fg="#adb5bd",
            bg="#212529",
            font=("Segoe UI", 10, "bold"),
        )
        lbl_subtotal.pack(side="left", padx=10)

        btn_menos = tk.Button(
            item_frame,
            text="-",
            font=("Segoe UI", 9, "bold"),
            bg="#dc3545",
            fg="white",
            bd=0,
            width=2,
            cursor="hand2",
            command=lambda n=nombre: [
                modificar_cantidad(n, -1),
                actualizar_interfaz_carrito(),
            ],
        )
        btn_menos.pack(side="right", padx=2)

        btn_mas = tk.Button(
            item_frame,
            text="+",
            font=("Segoe UI", 9, "bold"),
            bg="#198754",
            fg="white",
            bd=0,
            width=2,
            cursor="hand2",
            command=lambda n=nombre: [
                modificar_cantidad(n, 1),
                actualizar_interfaz_carrito(),
            ],
        )
        btn_mas.pack(side="right", padx=2)

    if lbl_total_num:
        lbl_total_num.config(text=f"${obtener_total_carrito():,.2f}")


def ejecutar_agregar_producto(prod):
    agregar_al_carrito(prod)
    actualizar_interfaz_carrito()


# ==========================================================
# ACCIONES DE SESIÓN Y CAJA
# ==========================================================


def salir_quiosco(event=None):
    if messagebox.askyesno(
        "TicketsJets", "¿Desea cerrar la sesión actual?", parent=ventana
    ):
        if ventana:
            ventana.destroy()


from database.cerrarCaja import cerrar_caja_bd, obtener_datos_cierre_caja
from reports.impresion import imprimir_ticket_cierre_silencioso


# main.py


def solicitar_cierre_caja():
    info_sesion = obtener_datos_sesion_actual()
    idjornada = info_sesion.get("idjornada")
    idpunto = info_sesion.get("idpunto")
    operador = info_sesion.get("operador", "OPERADOR")

    if not idjornada or not idpunto:
        messagebox.showwarning("Cierre de Caja", "No hay una caja o jornada activa registrada.")
        return

    # Sin el parámetro 'parent', evitas que falle si la ventana se destruyó previamente
    if not messagebox.askyesno(
        "Confirmar Cierre de Caja",
        "¿Está seguro de que desea cerrar la caja actual?\n\nSe imprimirá el resumen y finalizará la sesión."
    ):
        return

    datos_cierre, error = obtener_datos_cierre_caja(idjornada, idpunto)
    if error or not datos_cierre:
        messagebox.showerror("Error", f"No se pudieron obtener los datos de la caja: {error}")
        return

    exito, msj = cerrar_caja_bd(idjornada, idpunto)

    if exito:
        imprimir_ticket_cierre_silencioso(datos_cierre, operador_nombre=operador)
        messagebox.showinfo("Caja Cerrada", "La caja se cerró y el ticket fue impreso con éxito.")

        # Ocultamos y destruimos de forma segura
        try:
            ventana.withdraw()
            ventana.destroy()
        except Exception:
            pass

        subprocess.Popen(["python", "login.py"])
    else:
        messagebox.showerror("Error", msj)
# ==========================================================
# VENTANA DE COBRO MODAL (PAGO COMBINADO O CORTESÍA)
# ==========================================================


def abrir_ventana_cobro_combinado():
    total_a_cobrar = obtener_total_carrito()
    if total_a_cobrar <= 0:
        messagebox.showwarning(
            "TicketsJets", "El carrito está vacío.", parent=ventana
        )
        return

    modos = obtener_modos_pago()

    win_cobro = tk.Toplevel(ventana)
    win_cobro.title("Procesar Pago Combinado - TicketsJets")
    win_cobro.geometry("520x620")
    win_cobro.configure(bg="#11111b")
    win_cobro.grab_set()
    win_cobro.resizable(False, False)

    # Centrar la ventana
    win_cobro.update_idletasks()
    x = (win_cobro.winfo_screenwidth() // 2) - (520 // 2)
    y = (win_cobro.winfo_screenheight() // 2) - (620 // 2)
    win_cobro.geometry(f"+{x}+{y}")

    # Header de Cobro
    frame_top = tk.Frame(win_cobro, bg="#8d1324", pady=10)
    frame_top.pack(fill="x")

    tk.Label(
        frame_top,
        text="TOTAL A COBRAR",
        font=("Segoe UI", 11, "bold"),
        fg="#adb5bd",
        bg="#8d1324",
    ).pack()
    tk.Label(
        frame_top,
        text=f"${total_a_cobrar:,.2f}",
        font=("Segoe UI", 24, "bold"),
        fg="#a6e3a1",
        bg="#8d1324",
    ).pack()

    # Contenedor de Formas de Pago
    frame_body = tk.Frame(win_cobro, bg="#11111b", padx=20, pady=15)
    frame_body.pack(fill="both", expand=True)

    entries_pago = {}

    tk.Label(
        frame_body,
        text="Ingrese los montos recibidos por cada método:",
        font=("Segoe UI", 10, "bold"),
        fg="#f8f9fa",
        bg="#11111b",
    ).pack(anchor="w", pady=(0, 10))

    for m in modos:
        f_row = tk.Frame(frame_body, bg="#212529", pady=6, padx=10)
        f_row.pack(fill="x", pady=4)

        nombre_modo = m.get("nombre") or m.get("modo") or "Método de Pago"
        id_modo = m.get("idmodopago", 1)

        lbl_m = tk.Label(
            f_row,
            text=nombre_modo,
            font=("Segoe UI", 11),
            fg="#f8f9fa",
            bg="#212529",
            width=22,
            anchor="w",
        )
        lbl_m.pack(side="left")

        ent_m = tk.Entry(
            f_row,
            font=("Segoe UI", 12, "bold"),
            bg="#11111b",
            fg="#a6e3a1",
            insertbackground="white",
            justify="right",
        )
        ent_m.pack(side="right", fill="x", expand=True)
        entries_pago[id_modo] = (ent_m, nombre_modo)

    if 1 in entries_pago:
        entries_pago[1][0].insert(0, f"{total_a_cobrar:.2f}")

    # Cálculo de Cambio / Vuelto
    lbl_vuelto = tk.Label(
        frame_body,
        text="Vuelto: $0.00",
        font=("Segoe UI", 12, "bold"),
        fg="#20c997",
        bg="#11111b",
    )
    lbl_vuelto.pack(pady=10)

    def recalcular_vuelto(*args):
        ingresado = 0.0
        for ent, _ in entries_pago.values():
            try:
                val = float(ent.get().strip() or 0)
                ingresado += val
            except ValueError:
                pass
        vuelto = ingresado - total_a_cobrar
        if vuelto > 0:
            lbl_vuelto.config(
                text=f"Vuelto a entregar: ${vuelto:,.2f}", fg="#20c997"
            )
        elif vuelto == 0:
            lbl_vuelto.config(text="Monto Exacto", fg="#adb5bd")
        else:
            lbl_vuelto.config(
                text=f"Falta ingresar: ${abs(vuelto):,.2f}", fg="#dc3545"
            )

    for ent, _ in entries_pago.values():
        ent.bind("<KeyRelease>", recalcular_vuelto)
    recalcular_vuelto()

    # Opción de Cortesía
    frame_cortesia = tk.LabelFrame(
        frame_body,
        text=" Opción Cortesía ($0.00) ",
        font=("Segoe UI", 9, "bold"),
        fg="#adb5bd",
        bg="#11111b",
        pady=5,
        padx=10,
    )
    frame_cortesia.pack(fill="x", pady=10)

    var_es_cortesia = tk.BooleanVar(value=False)
    chk_cortesia = tk.Checkbutton(
        frame_cortesia,
        text="Marcar Venta como Cortesía",
        variable=var_es_cortesia,
        font=("Segoe UI", 10),
        fg="white",
        bg="#11111b",
        selectcolor="#212529",
    )
    chk_cortesia.pack(anchor="w")

    ent_autorizado = tk.Entry(
        frame_cortesia,
        font=("Segoe UI", 10),
        bg="#212529",
        fg="white",
        insertbackground="white",
    )
    ent_autorizado.insert(0, "Nombre de quien Autoriza")
    ent_autorizado.pack(fill="x", pady=5)

    def confirmar_pago_combinado():
        es_cortesia = var_es_cortesia.get()
        autoriza_str = ent_autorizado.get().strip()

        if es_cortesia:
            if not autoriza_str or autoriza_str == "Nombre de quien Autoriza":
                messagebox.showwarning(
                    "Cortesía",
                    "Por favor ingrese el nombre del autorizante.",
                    parent=win_cobro,
                )
                return
            desgloses = []
            pagos_ticket = [{"modo": "Cortesía", "importe": 0.0}]
        else:
            desgloses = []
            pagos_ticket = []
            for id_m, (ent, nom) in entries_pago.items():
                try:
                    val = float(ent.get().strip() or 0)
                    if val > 0:
                        desgloses.append({"idmodopago": id_m, "importe": val})
                        pagos_ticket.append({"modo": nom, "importe": val})
                except ValueError:
                    messagebox.showerror(
                        "Error",
                        f"Monto inválido en {nom}.",
                        parent=win_cobro,
                    )
                    return

        items_ticket = [
            {
                "producto": nombre,
                "cantidad": item["cantidad"],
                "subtotal": (
                    0.0 if es_cortesia else item["precio"] * item["cantidad"]
                ),
            }
            for nombre, item in carrito.items()
        ]

        info_sesion = obtener_datos_sesion_actual()

        exito, msj, idventa = registrar_venta(
            desgloses_pago=desgloses,
            es_cortesia=es_cortesia,
            autoriza_cortesia=autoriza_str,
            idjornada=info_sesion.get("idjornada"),
            idpunto=info_sesion.get("idpunto"),
            idusuario=info_sesion.get("idusuario"),
        )

        if exito:
            messagebox.showinfo("Éxito", msj, parent=ventana)
            win_cobro.destroy()

            actualizar_interfaz_carrito()
            actualizar_recaudacion_ui()

            if idventa:
                datos_para_ticket = {
                    "idventa": idventa,
                    "fecha_hora": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "total": total_a_cobrar if not es_cortesia else 0.0,
                    "cliente": "Consumidor Final",
                    "jornada": info_sesion.get("jornada", "Jornada Activa"),
                    "operador": info_sesion.get("operador", "Operador"),
                    "es_cortesia": es_cortesia,
                    "autorizado_cortesia": autoriza_str if es_cortesia else "",
                    "detalle": items_ticket,
                    "pagos": pagos_ticket,
                }
                imprimir_ticket_silencioso(datos_para_ticket)
        else:
            messagebox.showwarning("Error de Pago", msj, parent=win_cobro)

    btn_confirmar = tk.Button(
        win_cobro,
        text="✓ CONFIRMAR Y REGISTRAR VENTA (Enter)",
        font=("Segoe UI", 12, "bold"),
        bg="#0d6efd",
        fg="white",
        bd=0,
        pady=12,
        cursor="hand2",
        command=confirmar_pago_combinado,
    )
    btn_confirmar.pack(fill="x", side="bottom")

    win_cobro.bind("<Return>", lambda e: confirmar_pago_combinado())


# ==========================================================
# PROCESAR VENTA (GESTIÓN CENTRALIZADA PAGO SIMPLE / COMBINADO)
# ==========================================================


def procesar_cobro():
    total_a_cobrar = obtener_total_carrito()
    if total_a_cobrar <= 0:
        messagebox.showwarning(
            "TicketsJets", "El carrito está vacío.", parent=ventana
        )
        return

    # Si la opción elegida es PAGO COMBINADO, abrimos la ventana modal
    if var_tipo_pago and var_tipo_pago.get() == "COMBINADO":
        abrir_ventana_cobro_combinado()
        return

    # --- PAGO SIMPLE ---
    modo_seleccionado_str = (
        combo_modo_simple.get() if combo_modo_simple else "Efectivo"
    )

    id_modo_pago = 1
    for m in modos_pago_cache:
        nombre_m = m.get("nombre") or m.get("modo") or ""
        if nombre_m.lower() == modo_seleccionado_str.lower():
            id_modo_pago = m.get("idmodopago", 1)
            break

    resumen_items = "\n".join(
        [
            f"• {nombre} x{datos['cantidad']} (${datos['precio']*datos['cantidad']:,.2f})"
            for nombre, datos in carrito.items()
        ]
    )

    msg_confirmacion = (
        f"RESUMEN DE VENTA\n"
        f"----------------------------------------\n"
        f"{resumen_items}\n"
        f"----------------------------------------\n"
        f"Método de Pago: {modo_seleccionado_str}\n"
        f"Total: ${total_a_cobrar:,.2f}\n\n"
        f"¿Desea confirmar el cobro e imprimir el ticket?"
    )

    respuesta = messagebox.askyesno(
        "Confirmar Venta - TicketsJets", msg_confirmacion, parent=ventana
    )

    if not respuesta:
        return

    desgloses = [{"idmodopago": id_modo_pago, "importe": total_a_cobrar}]
    pagos_ticket = [{"modo": modo_seleccionado_str, "importe": total_a_cobrar}]

    items_ticket = [
        {
            "producto": nombre,
            "cantidad": item["cantidad"],
            "subtotal": item["precio"] * item["cantidad"],
        }
        for nombre, item in carrito.items()
    ]

    info_sesion = obtener_datos_sesion_actual()

    exito, msj, idventa = registrar_venta(
        desgloses_pago=desgloses,
        es_cortesia=False,
        autoriza_cortesia="",
        idjornada=info_sesion.get("idjornada"),
        idpunto=info_sesion.get("idpunto"),
        idusuario=info_sesion.get("idusuario"),
    )

    if exito:
        messagebox.showinfo("Éxito", msj, parent=ventana)

        actualizar_interfaz_carrito()
        actualizar_recaudacion_ui()

        if idventa:
            datos_para_ticket = {
                "idventa": idventa,
                "fecha_hora": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "total": total_a_cobrar,
                "cliente": "Consumidor Final",
                "jornada": info_sesion.get("jornada", "Jornada Activa"),
                "operador": info_sesion.get("operador", "Operador"),
                "es_cortesia": False,
                "autorizado_cortesia": "",
                "detalle": items_ticket,
                "pagos": pagos_ticket,
            }
            imprimir_ticket_silencioso(datos_para_ticket)
    else:
        messagebox.showwarning("Error de Pago", msj, parent=ventana)


# ==========================================================
# CONSTRUCCIÓN DE LA VENTANA PRINCIPAL
# ==========================================================


def iniciar_sistema():
    global ventana, lbl_reloj, lbl_total_num, lbl_recaudacion_val, frame_lista_carrito
    global var_tipo_pago, combo_modo_simple, modos_pago_cache

    info_sesion = obtener_datos_sesion_actual()
    modos_pago_cache = obtener_modos_pago()

    ventana = tk.Tk()
    ventana.title("TicketsJets - Módulo de Ventas")
    ventana.attributes("-fullscreen", True)
    ventana.configure(bg="#11111b")

    # Atajos de Teclado
    ventana.bind("<Escape>", salir_quiosco)
    ventana.bind("<c>", lambda e: procesar_cobro())
    ventana.bind("<F2>", lambda e: procesar_cobro())

    ventana.focus_set()
    ventana.focus_force()

    # Constantes de Colores
    COLOR_HEADER_BG = "#8d1324"
    COLOR_MAIN_BG = "#11111b"
    COLOR_CARD_BG = "#212529"
    TEXT_LIGHT = "#f8f9fa"
    BTN_PRIMARY = "#0d6efd"
    BTN_DANGER = "#dc3545"

    main_container = tk.Frame(ventana, bg=COLOR_MAIN_BG)
    main_container.pack(fill="both", expand=True)

    # ======================================================
    # HEADER / CABECERA SUPERIOR (INFORMACIÓN DE SESIÓN)
    # ======================================================
    header = tk.Frame(main_container, bg=COLOR_HEADER_BG, height=80)
    header.pack(fill="x")
    header.pack_propagate(False)

    DIRECTORIO_BASE = os.path.dirname(os.path.abspath(__file__))
    RUTA_PNG = os.path.join(DIRECTORIO_BASE, "icono.png")

    # Logo / Isotipo
    if os.path.exists(RUTA_PNG):
        ventana.img_marca = tk.PhotoImage(file=RUTA_PNG)
        lbl_marca = tk.Label(
            header,
            text=" TicketsJets",
            image=ventana.img_marca,
            compound="left",
            font=("Segoe UI", 20, "bold"),
            bg=COLOR_HEADER_BG,
            fg="white",
        )
    else:
        lbl_marca = tk.Label(
            header,
            text="TicketsJets",
            font=("Segoe UI", 20, "bold"),
            bg=COLOR_HEADER_BG,
            fg="white",
        )
    lbl_marca.pack(side="left", padx=(15, 20))

    # Bloque de Información de Sesión
    frame_info_sesion = tk.Frame(header, bg=COLOR_HEADER_BG)
    frame_info_sesion.pack(side="left", fill="y", pady=10)

    lbl_punto_op = tk.Label(
        frame_info_sesion,
        text=f"🏦 {info_sesion['punto']}  |  👤 Op: {info_sesion['operador']} ({info_sesion['rol']})",
        font=("Segoe UI", 11, "bold"),
        bg=COLOR_HEADER_BG,
        fg="white",
        anchor="w",
    )
    lbl_punto_op.pack(anchor="w")

    lbl_jornada_caja = tk.Label(
        frame_info_sesion,
        text=f"📅 Jornada: {info_sesion['jornada']}  |  🟢 Caja: {info_sesion['estado_caja']}",
        font=("Segoe UI", 10),
        bg=COLOR_HEADER_BG,
        fg="#e0e0e0",
        anchor="w",
    )
    lbl_jornada_caja.pack(anchor="w", pady=(2, 0))

    # Botones de Acción de Sesión (Derecha)
    btn_cerrar_sesion = tk.Button(
        header,
        text="🚪 Cerrar Sesión",
        font=("Segoe UI", 10, "bold"),
        bg=BTN_DANGER,
        fg="white",
        bd=0,
        padx=12,
        pady=6,
        cursor="hand2",
        command=salir_quiosco,
    )
    btn_cerrar_sesion.pack(side="right", padx=(5, 15))

    btn_cerrar_caja = tk.Button(
        header,
        text="🔒 Cerrar Caja",
        bg="#fd7e14",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        bd=0,
        padx=12,
        pady=6,
        cursor="hand2",
        command=solicitar_cierre_caja,
    )
    btn_cerrar_caja.pack(side="right", padx=5)

    # Recaudación Persistente
    frame_recaudacion = tk.Frame(header, bg="#5a101b", padx=12, pady=4)
    frame_recaudacion.pack(side="right", padx=15)

    tk.Label(
        frame_recaudacion,
        text="RECAUDACIÓN JORNADA",
        font=("Segoe UI", 8, "bold"),
        bg="#5a101b",
        fg="#adb5bd",
    ).pack(anchor="w")

    lbl_recaudacion_val = tk.Label(
        frame_recaudacion,
        text="$0.00",
        font=("Segoe UI", 14, "bold"),
        bg="#5a101b",
        fg="#8be28b",
    )
    lbl_recaudacion_val.pack(anchor="w")

    # ======================================================
    # CUERPO PRINCIPAL
    # ======================================================
    cuerpo = tk.Frame(main_container, bg=COLOR_MAIN_BG, padx=15, pady=15)
    cuerpo.pack(fill="both", expand=True)

    panel_izquierdo = tk.Frame(cuerpo, bg=COLOR_MAIN_BG)
    panel_izquierdo.pack(side="left", fill="both", expand=True, padx=(0, 15))

    lbl_sec_bebidas = tk.Label(
        panel_izquierdo,
        text="Catálogo de Bebidas Disponibles",
        font=("Segoe UI", 16, "bold"),
        fg=TEXT_LIGHT,
        bg=COLOR_MAIN_BG,
        anchor="w",
    )
    lbl_sec_bebidas.pack(fill="x", pady=(0, 10))

    grid_productos = tk.Frame(panel_izquierdo, bg=COLOR_MAIN_BG)
    grid_productos.pack(side="top", fill="both", expand=True)

    for col in range(5):
        grid_productos.columnconfigure(col, weight=1, uniform="grupo_bebidas")
    for fila in range(5):
        grid_productos.rowconfigure(fila, weight=1, uniform="grupo_bebidas")

    for indice, prod in enumerate(productos_bebidas):
        if indice >= 25:
            break

        fila = indice // 5
        columna = indice % 5

        card = tk.Frame(
            grid_productos,
            bg=COLOR_CARD_BG,
            highlightbackground="#313244",
            highlightthickness=1,
            cursor="hand2",
        )
        card.grid(row=fila, column=columna, padx=4, pady=4, sticky="nsew")

        lbl_pname = tk.Label(
            card,
            text=prod["nombre"],
            font=("Segoe UI", 10, "bold"),
            fg=TEXT_LIGHT,
            bg=COLOR_CARD_BG,
            wraplength=100,
            justify="center",
            cursor="hand2",
        )
        lbl_pname.pack(expand=True, fill="both", padx=4, pady=(6, 2))

        lbl_pprice = tk.Label(
            card,
            text=f"${prod['importe']}",
            font=("Segoe UI", 11, "bold"),
            fg="#a6e3a1",
            bg=COLOR_CARD_BG,
            cursor="hand2",
        )
        lbl_pprice.pack(expand=True, fill="both", padx=4, pady=(0, 6))

        def on_click(e, p=prod):
            ejecutar_agregar_producto(p)

        card.bind("<Button-1>", on_click)
        lbl_pname.bind("<Button-1>", on_click)
        lbl_pprice.bind("<Button-1>", on_click)

    # --- PANEL DERECHO: CARRITO Y OPCIONES DE PAGO ---
    panel_derecho = tk.Frame(
        cuerpo,
        bg=COLOR_CARD_BG,
        width=420,
        highlightbackground="#313244",
        highlightthickness=1,
    )
    panel_derecho.pack(side="right", fill="both", expand=False)
    panel_derecho.pack_propagate(False)

    lbl_tit_cart = tk.Label(
        panel_derecho,
        text="Resumen del Pedido",
        font=("Segoe UI", 14, "bold"),
        fg=TEXT_LIGHT,
        bg=COLOR_CARD_BG,
        pady=10,
        borderwidth=1,
        relief="groove",
    )
    lbl_tit_cart.pack(fill="x")

    frame_lista_carrito = tk.Frame(panel_derecho, bg="#1e1e2e")
    frame_lista_carrito.pack(fill="both", expand=True, padx=10, pady=10)

    # --- SECCIÓN DE SELECTOR DE MÉTODOS DE PAGO ---
    frame_opciones_pago = tk.LabelFrame(
        panel_derecho,
        text=" Formas de Pago ",
        font=("Segoe UI", 10, "bold"),
        fg="#a6e3a1",
        bg=COLOR_CARD_BG,
        padx=10,
        pady=8,
    )
    frame_opciones_pago.pack(fill="x", padx=10, pady=(0, 5))

    var_tipo_pago = tk.StringVar(value="SIMPLE")

    rb_simple = tk.Radiobutton(
        frame_opciones_pago,
        text="Pago Simple",
        variable=var_tipo_pago,
        value="SIMPLE",
        font=("Segoe UI", 10, "bold"),
        fg="white",
        bg=COLOR_CARD_BG,
        selectcolor="#11111b",
        activebackground=COLOR_CARD_BG,
        activeforeground="white",
    )
    rb_simple.pack(anchor="w")

    f_simple_detail = tk.Frame(frame_opciones_pago, bg=COLOR_CARD_BG)
    f_simple_detail.pack(fill="x", padx=20, pady=(2, 6))

    tk.Label(
        f_simple_detail,
        text="Método:",
        font=("Segoe UI", 9),
        fg="#adb5bd",
        bg=COLOR_CARD_BG,
    ).pack(side="left", padx=(0, 5))

    nombres_modos = [
        m.get("nombre") or m.get("modo") or "Efectivo" for m in modos_pago_cache
    ]
    if not nombres_modos:
        nombres_modos = ["Efectivo"]

    combo_modo_simple = ttk.Combobox(
        f_simple_detail,
        values=nombres_modos,
        state="readonly",
        font=("Segoe UI", 9, "bold"),
        width=18,
    )
    def_idx = 0
    for idx, name in enumerate(nombres_modos):
        if "efectivo" in name.lower():
            def_idx = idx
            break
    combo_modo_simple.current(def_idx)
    combo_modo_simple.pack(side="left", fill="x", expand=True)

    rb_combinado = tk.Radiobutton(
        frame_opciones_pago,
        text="Pago Combinado / Cortesía",
        variable=var_tipo_pago,
        value="COMBINADO",
        font=("Segoe UI", 10, "bold"),
        fg="white",
        bg=COLOR_CARD_BG,
        selectcolor="#11111b",
        activebackground=COLOR_CARD_BG,
        activeforeground="white",
    )
    rb_combinado.pack(anchor="w", pady=(4, 0))

    def alternar_estado_pago(*args):
        if var_tipo_pago.get() == "SIMPLE":
            combo_modo_simple.config(state="readonly")
        else:
            combo_modo_simple.config(state="disabled")

    var_tipo_pago.trace_add("write", alternar_estado_pago)

    # Botón de Cobro Inferior
    frame_inferior_cart = tk.Frame(
        panel_derecho, bg=COLOR_CARD_BG, padx=10, pady=10
    )
    frame_inferior_cart.pack(fill="x", side="bottom")

    frame_total_texto = tk.Frame(frame_inferior_cart, bg=COLOR_CARD_BG)
    frame_total_texto.pack(fill="x", pady=(0, 10))

    tk.Label(
        frame_total_texto,
        text="TOTAL A COBRAR:",
        font=("Segoe UI", 14, "bold"),
        fg=TEXT_LIGHT,
        bg=COLOR_CARD_BG,
    ).pack(side="left")

    lbl_total_num = tk.Label(
        frame_total_texto,
        text="$0.00",
        font=("Segoe UI", 18, "bold"),
        fg="#a6e3a1",
        bg=COLOR_CARD_BG,
    )
    lbl_total_num.pack(side="right")

    btn_cobrar = tk.Button(
        frame_inferior_cart,
        text="✓ PROCESAR COBRO (F2)",
        font=("Segoe UI", 14, "bold"),
        bg=BTN_PRIMARY,
        fg=TEXT_LIGHT,
        bd=0,
        cursor="hand2",
        activebackground="#0b5ed7",
        activeforeground=TEXT_LIGHT,
        command=procesar_cobro,
    )
    btn_cobrar.pack(fill="x", ipady=12)

    # ======================================================
    # BARRA INFERIOR (INFORMACIÓN DEL SISTEMA Y ATAJOS)
    # ======================================================
    status_bar = tk.Frame(
        ventana,
        bg="#212529",
        height=40,
        highlightbackground="#343a40",
        highlightthickness=1,
    )
    status_bar.pack(side="bottom", fill="x")
    status_bar.pack_propagate(False)

    # Sección Izquierda: Atajos de teclado rápidos
    frame_atajos = tk.Frame(status_bar, bg="#212529")
    frame_atajos.pack(side="left", padx=15)

    tk.Label(
        frame_atajos,
        text="⌨️ ATAJOS:",
        bg="#212529",
        fg="#a6e3a1",
        font=("Segoe UI", 9, "bold"),
    ).pack(side="left", padx=(0, 5))

    for atajo in ["[F2] Procesar Cobro", "[ESC] Cerrar Sesión"]:
        tk.Label(
            frame_atajos,
            text=atajo,
            bg="#212529",
            fg="#f8f9fa",
            font=("Segoe UI", 9, "bold"),
        ).pack(side="left", padx=8)

    # Sección Centro / Derecha: Reloj en vivo y Servidor
    lbl_reloj = tk.Label(
        status_bar,
        text="",
        bg="#212529",
        fg="#f8f9fa",
        font=("Segoe UI", 10, "bold"),
    )
    lbl_reloj.pack(side="right", padx=15)

    lbl_servidor = tk.Label(
        status_bar,
        text="🟢 Servidor Online",
        bg="#212529",
        fg="#20c997",
        font=("Segoe UI", 9, "bold"),
    )
    lbl_servidor.pack(side="right", padx=15)

    # Iniciar ciclos y sincronizar datos reales
    actualizar_reloj()
    actualizar_interfaz_carrito()
    actualizar_recaudacion_ui()
    ventana.mainloop()


if __name__ == "__main__":
    iniciar_sistema()