import tkinter as tk
from tkinter import messagebox
from database.usuarios import iniciar_sesion
from sesion import Sesion
import subprocess
import sys

def validar_login():

    usuario = entry_usuario.get().strip()
    password = entry_password.get().strip()

    datos = iniciar_sesion(usuario, password)

    if datos:
     

        # Guardar la sesión
     Sesion.iniciar(datos)

    # Cerrar login
     ventana.destroy()

    # Importar y abrir el sistema principal
     import main
     main.iniciar_sistema()

    else:

        messagebox.showerror(
            "Error",
            "Usuario o contraseña incorrectos"
        )
# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("TicketsJets - Login")
ventana.resizable(False, False) 

# Quitar el icono de Tkinter
ventana.iconbitmap("") 

# Centrar la ventana en la pantalla
ancho_ventana = 400
alto_ventana = 550
ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()
x = (ancho_pantalla // 2) - (ancho_ventana // 2)
y = (alto_pantalla // 2) - (alto_ventana // 2)
ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

# --- Fondo Degradado Avanzado (Rojo Marfil a Negro) ---
canvas = tk.Canvas(ventana, width=ancho_ventana, height=alto_ventana, highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Paleta de colores Bootstrap Dark y Rojo Marfil
R_INICIO, G_INICIO, B_INICIO = 141, 19, 36   # Rojo Marfil / Vino profundo
R_FIN, G_FIN, B_FIN = 17, 17, 17            # Negro Bootstrap Dark
TEXT_COLOR = "#f8f9fa"         
INPUT_BG = "#212529"           
BTN_PRIMARY = "#0d6efd"        
BTN_ACTIVE = "#0b5ed7"         

# Dibujar el degradado línea por línea
for i in range(alto_ventana):
    factor = i / alto_ventana
    r = int(R_INICIO + (R_FIN - R_INICIO) * factor)
    g = int(G_INICIO + (G_FIN - G_INICIO) * factor)
    b = int(B_INICIO + (B_FIN - B_INICIO) * factor)
    color_hex = f"#{r:02x}{g:02x}{b:02x}"
    canvas.create_line(0, i, ancho_ventana, i, fill=color_hex)

# --- Contenedor de Elementos sobre el Canvas ---
# Icono de Avión/Jet Estilizado (TicketsJets)
canvas.create_polygon(200, 50, 225, 90, 200, 80, 175, 90, fill="#f8f9fa", outline="")
canvas.create_line(170, 85, 230, 85, fill="#f8f9fa", width=2)

# Título del Sistema
canvas.create_text(200, 130, text="TicketsJets", font=("Segoe UI", 24, "bold"), fill=TEXT_COLOR)
canvas.create_text(200, 160, text="Gestión de Pasajes y Destinos", font=("Segoe UI", 10), fill="#adb5bd")

# --- Campos de Entrada de Texto ---
# Campo: Usuario
canvas.create_text(60, 210, text="Usuario o Email", font=("Segoe UI", 11, "bold"), fill=TEXT_COLOR, anchor="w")
canvas.create_oval(60, 238, 72, 250, outline="#adb5bd", width=2)
canvas.create_arc(54, 252, 78, 268, start=0, extent=180, outline="#adb5bd", width=2, style="arc")

entry_usuario = tk.Entry(ventana, font=("Segoe UI", 12), bg=INPUT_BG, fg=TEXT_COLOR, bd=0, relief="flat", insertbackground="white")
canvas.create_window(230, 250, window=entry_usuario, width=280, height=35)

# Campo: Contraseña
canvas.create_text(60, 310, text="Contraseña", font=("Segoe UI", 11, "bold"), fill=TEXT_COLOR, anchor="w")
canvas.create_rectangle(58, 344, 74, 358, outline="#adb5bd", width=2)
canvas.create_arc(61, 336, 71, 348, start=0, extent=180, outline="#adb5bd", width=2, style="arc")

entry_password = tk.Entry(ventana, font=("Segoe UI", 12), show="*", bg=INPUT_BG, fg=TEXT_COLOR, bd=0, relief="flat", insertbackground="white")
canvas.create_window(230, 350, window=entry_password, width=280, height=35)

# --- Botón de Entrada Estilo Bootstrap Primary ---
boton_login = tk.Button(
    ventana, 
    text="Iniciar Sesión", 
    font=("Segoe UI", 12, "bold"), 
    bg=BTN_PRIMARY, 
    fg=TEXT_COLOR, 
    bd=0, 
    cursor="hand2", 
    activebackground=BTN_ACTIVE,
    activeforeground=TEXT_COLOR,
    command=validar_login
)
canvas.create_window(200, 440, window=boton_login, width=320, height=45)

# --- Enlace Secundario (¡Arreglado sin la opción -cursor!) ---
enlace = canvas.create_text(200, 500, text="¿Olvidaste tu contraseña?", font=("Segoe UI", 10, "underline"), fill="#adb5bd")

# Eventos manuales para el cursor y color en texto del Canvas
def al_entrar_enlace(e):
    canvas.itemconfig(enlace, fill=BTN_PRIMARY)
    ventana.config(cursor="hand2")  # Cambia cursor de la ventana a mano

def al_salir_enlace(e):
    canvas.itemconfig(enlace, fill="#adb5bd")
    ventana.config(cursor="")  # Restaura cursor normal

canvas.tag_bind(enlace, "<Enter>", al_entrar_enlace)
canvas.tag_bind(enlace, "<Leave>", al_salir_enlace)

ventana.mainloop()
