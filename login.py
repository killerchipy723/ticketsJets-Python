# login.py
import os
import tkinter as tk
from tkinter import messagebox
from database.usuarios import iniciar_sesion
from sesion import Sesion
from PIL import Image, ImageTk


def validar_login():
    usuario = entry_usuario.get().strip()
    password = entry_password.get().strip()

    if not usuario or not password:
        messagebox.showwarning("Atención", "Por favor complete todos los campos.")
        return

    # Obtener los datos de la sesión y el mensaje de error si ocurriera alguno
    datos, error = iniciar_sesion(usuario, password)

    if error:
        messagebox.showerror("Error de Autenticación", error)
        return

    if datos:
        # 1. Guardar la sesión activa
        Sesion.iniciar(datos)

        # 2. Obtener el rol estandarizado en minúsculas
        rol_usuario = (datos.get("rol") or "").strip().lower()

        # 3. Cerrar la ventana actual de Login
        ventana.destroy()

        # 4. Redireccionar según el rol del usuario
        if rol_usuario in ["administrador", "admin"]:
            import admin
            app = admin.AdminDashboard()
            app.mainloop()

        elif "bolet" in rol_usuario:
            # RUTA PARA BOLETERÍA
            from views.boleteria import VistaBoleteria
            
            app_boleteria = tk.Tk()
            app_boleteria.title("TicketsJets - Módulo Boletería")
            app_boleteria.state("zoomed")  # Iniciar maximizado

            session_data = {
                "idusuario": datos.get("id"),
                "nombre": datos.get("nombre"),
                "operador": datos.get("operador") or "Boletería",
                "idjornada": datos.get("idjornada"),
                "jornada_nombre": datos.get("nombre_jornada"),
                "idpunto": datos.get("idpunto"),
                "punto_nombre": datos.get("punto")
            }

            def cerrar_sesion():
                Sesion.cerrar()
                app_boleteria.destroy()
                os.system("python login.py")

            vista = VistaBoleteria(app_boleteria, session_data, logout_callback=cerrar_sesion)
            vista.pack(fill="both", expand=True)
            app_boleteria.mainloop()

        else:
            # Ventas estándar / Punto de Venta general
            import main
            main.iniciar_sistema()


# ==========================================================
# CONSTRUCCIÓN DE LA INTERFAZ GRÁFICA
# ==========================================================

ventana = tk.Tk()
ventana.title("TicketsJets - Login")
ventana.resizable(False, False)

DIRECTORIO_BASE = os.path.dirname(os.path.abspath(__file__))
RUTA_ICONO = os.path.join(DIRECTORIO_BASE, "icono.ico")

if os.path.exists(RUTA_ICONO):
    try:
        ventana.iconbitmap(RUTA_ICONO)
    except tk.TclError:
        pass

ancho_ventana = 400
alto_ventana = 550

ventana.update_idletasks()
ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()

x = (ancho_pantalla // 2) - (ancho_ventana // 2)
y = max(0, ((alto_pantalla // 2) - (alto_ventana // 2)) - 30)

ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

# --- Fondo Degradado Avanzado ---
canvas = tk.Canvas(ventana, width=ancho_ventana, height=alto_ventana, highlightthickness=0)
canvas.pack(fill="both", expand=True)

R_INICIO, G_INICIO, B_INICIO = 141, 19, 36   # Rojo Marfil
R_FIN, G_FIN, B_FIN = 17, 17, 17            # Negro Dark
TEXT_COLOR = "#f8f9fa"
INPUT_BG = "#212529"
BTN_PRIMARY = "#0d6efd"
BTN_ACTIVE = "#0b5ed7"

for i in range(alto_ventana):
    factor = i / alto_ventana
    r = int(R_INICIO + (R_FIN - R_INICIO) * factor)
    g = int(G_INICIO + (G_FIN - G_INICIO) * factor)
    b = int(B_INICIO + (B_FIN - B_INICIO) * factor)
    color_hex = f"#{r:02x}{g:02x}{b:02x}"
    canvas.create_line(0, i, ancho_ventana, i, fill=color_hex)

img_logo_tk = None
RUTA_LOGO_PNG = os.path.join(DIRECTORIO_BASE, "static", "img", "logoJetSmall.png")

if os.path.exists(RUTA_LOGO_PNG):
    try:
        img_raw = Image.open(RUTA_LOGO_PNG)
        img_resized = img_raw.resize((64, 64), Image.Resampling.LANCZOS)
        img_logo_tk = ImageTk.PhotoImage(img_resized)
        canvas.create_image(200, 75, image=img_logo_tk)
    except Exception:
        pass

# Título del Sistema
canvas.create_text(200, 130, text="TicketsJets", font=("Segoe UI", 24, "bold"), fill=TEXT_COLOR)
canvas.create_text(200, 160, text="Sistema de Gestión Integral", font=("Segoe UI", 10), fill="#adb5bd")

# --- Campos de Entrada ---
canvas.create_text(60, 210, text="Usuario o Email", font=("Segoe UI", 11, "bold"), fill=TEXT_COLOR, anchor="w")
canvas.create_oval(60, 238, 72, 250, outline="#adb5bd", width=2)
canvas.create_arc(54, 252, 78, 268, start=0, extent=180, outline="#adb5bd", width=2, style="arc")

entry_usuario = tk.Entry(
    ventana,
    font=("Segoe UI", 12),
    bg=INPUT_BG,
    fg=TEXT_COLOR,
    bd=0,
    relief="flat",
    insertbackground="white"
)
canvas.create_window(230, 250, window=entry_usuario, width=280, height=35)

canvas.create_text(60, 310, text="Contraseña", font=("Segoe UI", 11, "bold"), fill=TEXT_COLOR, anchor="w")
canvas.create_rectangle(58, 344, 74, 358, outline="#adb5bd", width=2)
canvas.create_arc(61, 336, 71, 348, start=0, extent=180, outline="#adb5bd", width=2, style="arc")

entry_password = tk.Entry(
    ventana,
    font=("Segoe UI", 12),
    show="*",
    bg=INPUT_BG,
    fg=TEXT_COLOR,
    bd=0,
    relief="flat",
    insertbackground="white"
)
canvas.create_window(230, 350, window=entry_password, width=280, height=35)

entry_usuario.bind("<Return>", lambda e: validar_login())
entry_password.bind("<Return>", lambda e: validar_login())

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

enlace = canvas.create_text(
    200,
    500,
    text="¿Olvidaste tu contraseña?",
    font=("Segoe UI", 10, "underline"),
    fill="#adb5bd"
)

def al_entrar_enlace(e):
    canvas.itemconfig(enlace, fill=BTN_PRIMARY)
    ventana.config(cursor="hand2")

def al_salir_enlace(e):
    canvas.itemconfig(enlace, fill="#adb5bd")
    ventana.config(cursor="")

canvas.tag_bind(enlace, "<Enter>", al_entrar_enlace)
canvas.tag_bind(enlace, "<Leave>", al_salir_enlace)

entry_usuario.focus_set()
ventana.mainloop()