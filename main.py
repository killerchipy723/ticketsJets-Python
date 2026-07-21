import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

# --- Variables Globales de Simulación ---
usuario_activo = "Claudio Admin"
punto_venta = "Caja 1"
recaudacion_total = 0.0
carrito = {}

# Productos de ejemplo (Matriz de Bebidas para el panel de 5x5)
productos_bebidas = [
    {"nombre": "Coca-Cola 500ml", "precio": 1500},
    {"nombre": "Pepsi 500ml", "precio": 1400},
    {"nombre": "Agua Mineral 600ml", "precio": 1100},
    {"nombre": "Fanta Naranja", "precio": 1450},
    {"nombre": "Sprite Lima", "precio": 1450},
    {"nombre": "Cerveza Corona", "precio": 2500},
    {"nombre": "Heineken Lata", "precio": 2200},
    {"nombre": "Energizante RedBull", "precio": 3000},
    {"nombre": "Jugo de Naranja", "precio": 1300},
    {"nombre": "Agua Tónica", "precio": 1200},
    {"nombre": "Gatorade Frutos", "precio": 1800},
    {"nombre": "Té Frío Limón", "precio": 1500},
    {"nombre": "Fernet Branca", "precio": 5500},
    {"nombre": "Vodka Absolut", "precio": 7000},
    {"nombre": "Ron Blanco", "precio": 4800},
    {"nombre": "Agua con Gas", "precio": 1100},
    {"nombre": "Limonada Menta", "precio": 1600},
    {"nombre": "Pisco Especial", "precio": 6000},
    {"nombre": "Vino Tinto Tinto", "precio": 3500},
    {"nombre": "Champagne Brut", "precio": 9000},
    {"nombre": "Jugo Multifruta", "precio": 1300},
    {"nombre": "Cerveza IPALata", "precio": 2400},
    {"nombre": "Agua Saborizada", "precio": 1250},
    {"nombre": "Licor de Café", "precio": 4000},
    {"nombre": "Malta Tostada", "precio": 1700}
]

# --- Lógica de la Aplicación ---
def actualizar_reloj():
    ahora = datetime.now().strftime("%d/%m/%Y  |  %H:%M:%S")
    lbl_reloj.config(text=ahora)
    ventana.after(1000, actualizar_reloj)

def agregar_al_carrito(producto):
    nombre = producto["nombre"]
    precio = producto["precio"]
    if nombre in carrito:
        carrito[nombre]["cantidad"] += 1
    else:
        carrito[nombre] = {"precio": precio, "cantidad": 1}
    actualizar_interfaz_carrito()

def modificar_cantidad(nombre, cambio):
    if nombre in carrito:
        carrito[nombre]["cantidad"] += cambio
        if carrito[nombre]["cantidad"] <= 0:
            del carrito[nombre]
    actualizar_interfaz_carrito()

def obtener_total_carrito(): 
    return sum(item["precio"] * item["cantidad"] for item in carrito.values())

def actualizar_interfaz_carrito():
    # Limpiar lista visual
    for widget in frame_lista_carrito.winfo_children():
        widget.destroy()
        
    for nombre, datos in carrito.items():
        item_frame = tk.Frame(frame_lista_carrito, bg="#212529", pady=5)
        item_frame.pack(fill="x", padx=5, pady=2)
        
        lbl_prod = tk.Label(item_frame, text=f"{nombre} x{datos['cantidad']}", fg="#f8f9fa", bg="#212529", font=("Segoe UI", 10), anchor="w")
        lbl_prod.pack(side="left", fill="x", expand=True)
        
        lbl_subtotal = tk.Label(item_frame, text=f"${datos['precio']*datos['cantidad']}", fg="#adb5bd", bg="#212529", font=("Segoe UI", 10, "bold"))
        lbl_subtotal.pack(side="left", padx=10)
        
        btn_menos = tk.Button(item_frame, text="-", font=("Segoe UI", 9, "bold"), bg="#dc3545", fg="white", bd=0, width=2, command=lambda n=nombre: modificar_cantidad(n, -1))
        btn_menos.pack(side="right", padx=2)
        
        btn_mas = tk.Button(item_frame, text="+", font=("Segoe UI", 9, "bold"), bg="#198754", fg="white", bd=0, width=2, command=lambda n=nombre: modificar_cantidad(n, 1))
        btn_mas.pack(side="right", padx=2)

    lbl_total_num.config(text=f"${obtener_total_carrito():,.2f}")

def procesar_cobro():
    global recaudacion_total
    total = obtener_total_carrito()
    if total == 0:
        messagebox.showwarning("TicketsJets", "El carrito está vacío.")
        return
        
    # Verificar métodos de pago seleccionados
    metodos_seleccionados = []
    if var_efectivo.get(): metodos_seleccionados.append("Efectivo")
    if var_tarjeta.get(): metodos_seleccionados.append("Tarjeta")
    if var_transferencia.get(): metodos_seleccionados.append("Transferencia")
    
    if not metodos_seleccionados:
        messagebox.showwarning("TicketsJets", "Por favor, seleccione al menos un método de pago.")
        return
        
    # Procesar Venta Exitosa
    recaudacion_total += total
    lbl_recaudacion_val.config(text=f"${recaudacion_total:,.2f}")
    
    modos_str = " + ".join(metodos_seleccionados)
    messagebox.showinfo("TicketsJets", f"¡Venta Procesada con Éxito!\nTotal: ${total:,.2f}\nMétodo: {modos_str}")
    
    # Limpiar para la siguiente venta
    carrito.clear()
    actualizar_interfaz_carrito()

def salir_quiosco(event=None):
    if messagebox.askyesno("TicketsJets", "¿Desea cerrar el sistema de quiosco?"):
        ventana.destroy()

# --- Configuración de la Ventana en Pantalla Completa ---
ventana = tk.Tk()
ventana.title("TicketsJets - Módulo Quiosco de Ventas")
ventana.attributes("-fullscreen", True)
ventana.config(bg="#11111b")

# Combinación de teclas de escape de emergencia (Esc) para salir de pantalla completa
ventana.bind("<Escape>", salir_quiosco)

# Paleta Estilo Bootstrap y Login
COLOR_HEADER_BG = "#8d1324"  # Rojo Marfil original del Login
COLOR_MAIN_BG = "#11111b"    # Negro Bootstrap Dark fondo
COLOR_CARD_BG = "#212529"    # Gris oscuro componentes
TEXT_LIGHT = "#f8f9fa"
BTN_PRIMARY = "#0d6efd"

# ==================== ENCABEZADO (HEADER) ====================
header = tk.Frame(ventana, bg=COLOR_HEADER_BG, height=80, padx=20)
header.pack(fill="x", side="top")
header.pack_propagate(False)  

# Título de Marca Izquierda
lbl_marca = tk.Label(header, text="TicketsJets  🚀", font=("Segoe UI", 22, "bold"), fg=TEXT_LIGHT, bg=COLOR_HEADER_BG)
lbl_marca.pack(side="left", pady=10)

lbl_pos = tk.Label(header, text=f"Punto: {punto_venta}  |  Operador: {usuario_activo}", font=("Segoe UI", 12), fg="#f8f9fa", bg=COLOR_HEADER_BG)

lbl_pos.pack(side="left", padx=40, pady=22)

# Salida / Cerrar Quiosco Derecha
btn_salir = tk.Button(header, text="Cerrar Sistema [ESC]", font=("Segoe UI", 10, "bold"), bg="#dc3545", fg=TEXT_LIGHT, bd=0, padx=15, cursor="hand2", command=salir_quiosco)
btn_salir.pack(side="right", pady=20)

# Fecha y Hora Central/Derecha
lbl_reloj = tk.Label(header, text="", font=("Segoe UI", 14, "bold"), fg=TEXT_LIGHT, bg=COLOR_HEADER_BG)
lbl_reloj.pack(side="right", padx=30, pady=20)

# Indicador de Recaudación en el Encabezado
frame_recaudacion = tk.Frame(header, bg="#510a14", padx=15, pady=5)
frame_recaudacion.pack(side="right", padx=10, pady=15)
lbl_recaudacion_txt = tk.Label(frame_recaudacion, text="RECAUDACIÓN CAJA:", font=("Segoe UI", 9, "bold"), fg="#adb5bd", bg="#510a14")
lbl_recaudacion_txt.pack(side="top", anchor="w")
lbl_recaudacion_val = tk.Label(frame_recaudacion, text="$0.00", font=("Segoe UI", 14, "bold"), fg="#a6e3a1", bg="#510a14")
lbl_recaudacion_val.pack(side="top", anchor="w")


# ==================== CUERPO PRINCIPAL ====================
cuerpo = tk.Frame(ventana, bg=COLOR_MAIN_BG, padx=15, pady=15)
cuerpo.pack(fill="both", expand=True)

# --- PANEL IZQUIERDO: MATRIZ DE CARDS 5x5 (PRODUCTOS) ---
panel_izquierdo = tk.Frame(cuerpo, bg=COLOR_MAIN_BG)
panel_izquierdo.pack(side="left", fill="both", expand=True, padx=(0, 15))

lbl_sec_bebidas = tk.Label(panel_izquierdo, text="Catálogo de Bebidas Disponibles", font=("Segoe UI", 16, "bold"), fg=TEXT_LIGHT, bg=COLOR_MAIN_BG, anchor="w")
lbl_sec_bebidas.pack(fill="x", pady=(0, 10))

# Contenedor Grid adaptable para simular las 5 columnas por 5 filas
grid_productos = tk.Frame(panel_izquierdo, bg=COLOR_MAIN_BG)
grid_productos.pack(fill="both", expand=True)

# Forzar configuración exacta de 5 columnas equidistantes
for col in range(5):
    grid_productos.columnconfigure(col, weight=1, uniform="grupo_bebidas")
for fila in range(5):
    grid_productos.rowconfigure(fila, weight=1, uniform="grupo_bebidas")

# Inyección dinámica de las Cards estilo Bootstrap
for indice, prod in enumerate(productos_bebidas):
    if indice >= 25: break # Limitar estrictamente al espacio de 5x5
    
    fila = indice // 5
    columna = indice % 5
    
    # Crear contenedor individual de la Card
    card = tk.Frame(grid_productos, bg=COLOR_CARD_BG, highlightbackground="#313244", highlightthickness=1)
    card.grid(row=fila, column=columna, padx=6, pady=6, sticky="nsew")
    
    # Textos internos de la Card
    lbl_pname = tk.Label(card, text=prod["nombre"], font=("Segoe UI", 11, "bold"), fg=TEXT_LIGHT, bg=COLOR_CARD_BG, wraplength=120, justify="center")
    lbl_pname.pack(expand=True, fill="x", pady=(10, 2))
    
    lbl_pprice = tk.Label(card, text=f"${prod['precio']}", font=("Segoe UI", 12), fg="#a6e3a1", bg=COLOR_CARD_BG)
    lbl_pprice.pack(expand=True, fill="x", pady=(0, 5))
    
    btn_add = tk.Button(card, text="Agregar", font=("Segoe UI", 9, "bold"), bg="#313244", fg=TEXT_LIGHT, bd=0, activebackground=BTN_PRIMARY, cursor="hand2", command=lambda p=prod: agregar_al_carrito(p))
    btn_add.pack(fill="x", side="bottom", ipady=4)


# --- PANEL DERECHO: CARRITO Y CONFIGURACIÓN DE PAGO ---
panel_derecho = tk.Frame(cuerpo, bg=COLOR_CARD_BG, width=420, highlightbackground="#313244", highlightthickness=1)
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
    relief="groove"
)
lbl_tit_cart.pack(fill="x")

# Área de la Lista de Productos del Carrito (Scrollable por packing interno)
frame_lista_carrito = tk.Frame(panel_derecho, bg="#1e1e2e")
frame_lista_carrito.pack(fill="both", expand=True, padx=10, pady=10)

# Sección de Modos de Pago Combinables
frame_pagos = tk.LabelFrame(panel_derecho, text=" Selector de Métodos de Pago (Combinable) ", font=("Segoe UI", 10, "bold"), fg="#adb5bd", bg=COLOR_CARD_BG, padx=10, pady=10, bd=1)

frame_pagos.pack(fill="x", padx=10, pady=5)

# Variables de métodos de pago
var_efectivo = tk.BooleanVar(value=True)  # Por defecto efectivo marcado
var_tarjeta = tk.BooleanVar()
var_transferencia = tk.BooleanVar()

# Checkbuttons
chk_efectivo = tk.Checkbutton(
    frame_pagos,
    text="Efectivo",
    variable=var_efectivo,
    font=("Segoe UI", 11),
    fg=TEXT_LIGHT,
    bg=COLOR_CARD_BG,
    selectcolor="#11111b",
    activebackground=COLOR_CARD_BG,
    activeforeground=TEXT_LIGHT
)
chk_efectivo.pack(anchor="w", pady=2)

chk_tarjeta = tk.Checkbutton(
    frame_pagos,
    text="Tarjeta de Crédito / Débito",
    variable=var_tarjeta,
    font=("Segoe UI", 11),
    fg=TEXT_LIGHT,
    bg=COLOR_CARD_BG,
    selectcolor="#11111b",
    activebackground=COLOR_CARD_BG,
    activeforeground=TEXT_LIGHT
)
chk_tarjeta.pack(anchor="w", pady=2)

chk_transferencia = tk.Checkbutton(
    frame_pagos,
    text="Transferencia / Billetera Digital",
    variable=var_transferencia,
    font=("Segoe UI", 11),
    fg=TEXT_LIGHT,
    bg=COLOR_CARD_BG,
    selectcolor="#11111b",
    activebackground=COLOR_CARD_BG,
    activeforeground=TEXT_LIGHT
)
chk_transferencia.pack(anchor="w", pady=2)

# ==========================
# Sección inferior de Totales y Acción Cobrar
# ==========================

frame_inferior_cart = tk.Frame(
    panel_derecho,
    bg=COLOR_CARD_BG,
    padx=10,
    pady=10
)
frame_inferior_cart.pack(fill="x", side="bottom")

div_linea = tk.Frame(
    frame_inferior_cart,
    bg="#313244",
    height=2
)
div_linea.pack(fill="x", pady=10)

frame_total_texto = tk.Frame(
    frame_inferior_cart,
    bg=COLOR_CARD_BG
)
frame_total_texto.pack(fill="x", pady=(0, 15))

lbl_total_txt = tk.Label(
    frame_total_texto,
    text="TOTAL A COBRAR:",
    font=("Segoe UI", 14, "bold"),
    fg=TEXT_LIGHT,
    bg=COLOR_CARD_BG
)
lbl_total_txt.pack(side="left")

lbl_total_num = tk.Label(
    frame_total_texto,
    text="$0.00",
    font=("Segoe UI", 18, "bold"),
    fg="#a6e3a1",
    bg=COLOR_CARD_BG
)
lbl_total_num.pack(side="right")

# Botón Cobrar (Estilo Bootstrap Primary)
btn_cobrar = tk.Button(
    frame_inferior_cart,
    text="✓ PROCESAR COBRO",
    font=("Segoe UI", 14, "bold"),
    bg=BTN_PRIMARY,
    fg=TEXT_LIGHT,
    bd=0,
    cursor="hand2",
    activebackground="#0b5ed7",
    activeforeground=TEXT_LIGHT,
    command=procesar_cobro
)
btn_cobrar.pack(fill="x", ipady=12)

# ==========================
# Inicialización
# ==========================



def iniciar_sistema():
    actualizar_reloj()
    actualizar_interfaz_carrito()
    ventana.mainloop()


if __name__ == "__main__":
    iniciar_sistema()
