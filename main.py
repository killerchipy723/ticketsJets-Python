# main.py
import os
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk
import subprocess

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

# Referencias globales UI
ventana = None
lbl_reloj = None
lbl_total_num = None
lbl_recaudacion_val = None
frame_lista_carrito = None

# Cargar catálogo de productos
productos_bebidas = obtener_productos()


# ==========================================================
# FUNCIONES REFRESCO DE INTERFAZ
# ==========================================================

def actualizar_reloj():
    if ventana and ventana.winfo_exists():
        ahora = datetime.now().strftime("%d/%m/%Y  |  %H:%M:%S")
        lbl_reloj.config(text=ahora)
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
            command=lambda n=nombre: [modificar_cantidad(n, -1), actualizar_interfaz_carrito()],
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
            command=lambda n=nombre: [modificar_cantidad(n, 1), actualizar_interfaz_carrito()],
        )
        btn_mas.pack(side="right", padx=2)

    if lbl_total_num:
        lbl_total_num.config(text=f"${obtener_total_carrito():,.2f}")


def ejecutar_agregar_producto(prod):
    agregar_al_carrito(prod)
    actualizar_interfaz_carrito()


# ==========================================================
# VENTANA DE COBRO AVANZADA (SIMPLE, COMBINADO Y CORTESÍA)
# ==========================================================

def abrir_ventana_cobro():
    total_a_cobrar = obtener_total_carrito()
    if total_a_cobrar <= 0:
        messagebox.showwarning("TicketsJets", "El carrito está vacío.")
        return

    modos = obtener_modos_pago()

    win_cobro = tk.Toplevel(ventana)
    win_cobro.title("Procesar Pago - TicketsJets")
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
        frame_top, text="TOTAL A COBRAR", font=("Segoe UI", 11, "bold"), fg="#adb5bd", bg="#8d1324"
    ).pack()
    tk.Label(
        frame_top, text=f"${total_a_cobrar:,.2f}", font=("Segoe UI", 24, "bold"), fg="#a6e3a1", bg="#8d1324"
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

        lbl_m = tk.Label(
            f_row, text=m["nombre"], font=("Segoe UI", 11), fg="#f8f9fa", bg="#212529", width=22, anchor="w"
        )
        lbl_m.pack(side="left")

        ent_m = tk.Entry(
            f_row, font=("Segoe UI", 12, "bold"), bg="#11111b", fg="#a6e3a1", insertbackground="white", justify="right"
        )
        ent_m.pack(side="right", fill="x", expand=True)
        entries_pago[m["idmodopago"]] = (ent_m, m["nombre"])

    # Si hay un solo método o predeterminado "Efectivo", colocar el total por defecto
    if 1 in entries_pago:
        entries_pago[1][0].insert(0, f"{total_a_cobrar:.2f}")

    # Cálculo de Cambio / Vuelto
    lbl_vuelto = tk.Label(
        frame_body, text="Vuelto: $0.00", font=("Segoe UI", 12, "bold"), fg="#20c997", bg="#11111b"
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
            lbl_vuelto.config(text=f"Vuelto a entregar: ${vuelto:,.2f}", fg="#20c997")
        elif vuelto == 0:
            lbl_vuelto.config(text="Monto Exacto", fg="#adb5bd")
        else:
            lbl_vuelto.config(text=f"Falta ingresar: ${abs(vuelto):,.2f}", fg="#dc3545")

    for ent, _ in entries_pago.values():
        ent.bind("<KeyRelease>", recalcular_vuelto)
    recalcular_vuelto()

    # Opción de Cortesía
    frame_cortesia = tk.LabelFrame(
        frame_body, text=" Opción Cortesía ($0.00) ", font=("Segoe UI", 9, "bold"), fg="#adb5bd", bg="#11111b", pady=5, padx=10
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
        frame_cortesia, font=("Segoe UI", 10), bg="#212529", fg="white", insertbackground="white"
    )
    ent_autorizado.insert(0, "Nombre de quien Autoriza")
    ent_autorizado.pack(fill="x", pady=5)

    def confirmar_pago():
        es_cortesia = var_es_cortesia.get()
        autoriza_str = ent_autorizado.get().strip()

        if es_cortesia:
            if not autoriza_str or autoriza_str == "Nombre de quien Autoriza":
                messagebox.showwarning("Cortesía", "Por favor ingrese el nombre del autorizante.", parent=win_cobro)
                return
            desgloses = []
        else:
            desgloses = []
            for id_m, (ent, nom) in entries_pago.items():
                try:
                    val = float(ent.get().strip() or 0)
                    if val > 0:
                        desgloses.append({"idmodopago": id_m, "importe": val})
                except ValueError:
                    messagebox.showerror("Error", f"Monto inválido en {nom}.", parent=win_cobro)
                    return

        exito, msj = registrar_venta(
            desgloses_pago=desgloses,
            es_cortesia=es_cortesia,
            autoriza_cortesia=autoriza_str,
        )

        if exito:
            messagebox.showinfo("Éxito", msj, parent=ventana)
            win_cobro.destroy()
            actualizar_interfaz_carrito()
            actualizar_recaudacion_ui()
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
        command=confirmar_pago,
    )
    btn_confirmar.pack(fill="x", side="bottom")

    win_cobro.bind("<Return>", lambda e: confirmar_pago())


def salir_quiosco(event=None):
    if messagebox.askyesno("TicketsJets", "¿Desea cerrar el sistema de ventas?"):
        if ventana:
            ventana.destroy()

        subprocess.Popen(["python", "login.py"])


# ==========================================================
# CONSTRUCCIÓN DE LA VENTANA PRINCIPAL
# ==========================================================

def iniciar_sistema():
    global ventana, lbl_reloj, lbl_total_num, lbl_recaudacion_val, frame_lista_carrito

    info_sesion = obtener_datos_sesion_actual()

    ventana = tk.Tk()
    ventana.title("TicketsJets - Módulo de Ventas")
    ventana.attributes("-fullscreen", True)
    ventana.configure(bg="#11111b")

    ventana.bind("<Escape>", salir_quiosco)
    ventana.bind("<F2>", lambda e: abrir_ventana_cobro())

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
    # HEADER / CABECERA SUPERIOR
    # ======================================================
    header = tk.Frame(main_container, bg=COLOR_HEADER_BG, height=80)
    header.pack(fill="x")
    header.pack_propagate(False)

    DIRECTORIO_BASE = os.path.dirname(os.path.abspath(__file__))
    RUTA_PNG = os.path.join(DIRECTORIO_BASE, "icono.png")

    if os.path.exists(RUTA_PNG):
        ventana.img_marca = tk.PhotoImage(file=RUTA_PNG)
        lbl_marca = tk.Label(
            header,
            text=" TicketsJets",
            image=ventana.img_marca,
            compound="left",
            font=("Segoe UI", 22, "bold"),
            bg=COLOR_HEADER_BG,
            fg="white",
        )
    else:
        lbl_marca = tk.Label(
            header,
            text="TicketsJets",
            font=("Segoe UI", 22, "bold"),
            bg=COLOR_HEADER_BG,
            fg="white",
        )
    lbl_marca.pack(side="left", padx=20)

    texto_cabecera = f"Punto: {info_sesion['punto']}   |   Usuario: {info_sesion['usuario']} ({info_sesion['rol']})   |   Operador: {info_sesion['operador']}"
    lbl_pos = tk.Label(
        header,
        text=texto_cabecera,
        font=("Segoe UI", 11, "bold"),
        bg=COLOR_HEADER_BG,
        fg="white",
    )
    lbl_pos.pack(side="left", padx=15)

    # Recaudación Persistente
    frame_recaudacion = tk.Frame(header, bg="#5a101b", padx=15, pady=6)
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
        font=("Segoe UI", 15, "bold"),
        bg="#5a101b",
        fg="#8be28b",
    )
    lbl_recaudacion_val.pack(anchor="w")

    lbl_reloj = tk.Label(
        header,
        text="",
        font=("Segoe UI", 13, "bold"),
        bg=COLOR_HEADER_BG,
        fg="white",
    )
    lbl_reloj.pack(side="right", padx=15)

    btn_salir = tk.Button(
        header,
        text="❌ Cerrar Sistema",
        font=("Segoe UI", 10, "bold"),
        bg=BTN_DANGER,
        fg="white",
        bd=0,
        padx=15,
        cursor="hand2",
        command=salir_quiosco,
    )
    btn_salir.pack(side="right", padx=10)

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

    # --- PANEL DERECHO: CARRITO ---
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

    # Botón de Cobro Inferior
    frame_inferior_cart = tk.Frame(panel_derecho, bg=COLOR_CARD_BG, padx=10, pady=10)
    frame_inferior_cart.pack(fill="x", side="bottom")

    frame_total_texto = tk.Frame(frame_inferior_cart, bg=COLOR_CARD_BG)
    frame_total_texto.pack(fill="x", pady=(0, 15))

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
        command=abrir_ventana_cobro,
    )
    btn_cobrar.pack(fill="x", ipady=12)

    # ======================================================
    # BARRA DE ESTADO INFERIOR
    # ======================================================
    status_bar = tk.Frame(
        ventana,
        bg="#212529",
        height=45,
        highlightbackground="#343a40",
        highlightthickness=1,
    )
    status_bar.pack(side="bottom", fill="x")
    status_bar.pack_propagate(False)

    lbl_estado = tk.Label(
        status_bar,
        text=f"🟢 Caja: {info_sesion['estado_caja']}",
        bg="#212529",
        fg="#20c997",
        font=("Segoe UI", 10, "bold"),
    )
    lbl_estado.pack(side="left", padx=(15, 10))

    lbl_jornada = tk.Label(
        status_bar,
        text=f"📅 Jornada: {info_sesion['jornada']}",
        bg="#212529",
        fg="white",
        font=("Segoe UI", 10),
    )
    lbl_jornada.pack(side="left", padx=10)

    lbl_operador_bar = tk.Label(
        status_bar,
        text=f"👤 Operador: {info_sesion['operador']}",
        bg="#212529",
        fg="white",
        font=("Segoe UI", 10, "bold"),
    )
    lbl_operador_bar.pack(side="left", padx=10)

    lbl_punto_bar = tk.Label(
        status_bar,
        text=f"🏦 {info_sesion['punto']}",
        bg="#212529",
        fg="white",
        font=("Segoe UI", 10),
    )
    lbl_punto_bar.pack(side="left", padx=10)

    lbl_servidor = tk.Label(
        status_bar,
        text="🟢 Servidor Online",
        bg="#212529",
        fg="#20c997",
        font=("Segoe UI", 10, "bold"),
    )
    lbl_servidor.pack(side="left", padx=10)

    frame_atajos = tk.Frame(status_bar, bg="#212529")
    frame_atajos.pack(side="left", padx=30)

    for atajo in ["F2 Cobrar", "ESC Salir"]:
        tk.Label(
            frame_atajos,
            text=atajo,
            bg="#212529",
            fg="#adb5bd",
            font=("Segoe UI", 9),
        ).pack(side="left", padx=6)

    frame_botones_estado = tk.Frame(status_bar, bg="#212529")
    frame_botones_estado.pack(side="right", padx=15)

    btn_cerrar_caja = tk.Button(
        frame_botones_estado,
        text="🔒 Cerrar Caja",
        bg="#dc3545",
        fg="white",
        font=("Segoe UI", 9, "bold"),
        bd=0,
        cursor="hand2",
        padx=15,
        pady=3,
    )
    btn_cerrar_caja.pack(side="right")

    # Iniciar ciclos y sincronizar datos reales
    actualizar_reloj()
    actualizar_interfaz_carrito()
    actualizar_recaudacion_ui()
    ventana.mainloop()


if __name__ == "__main__":
    iniciar_sistema()