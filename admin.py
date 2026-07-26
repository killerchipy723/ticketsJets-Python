# admin.py
import os
import datetime
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk

# Importamos las vistas existentes
from views.vista_usuarios import VistaUsuarios
from views.vista_jornadas import VistaJornadas
from views.vista_puntos_venta import VistaPuntosVenta
from views.vista_productos import VistaProductos
from views.vista_jornadas_admin import VistaJornadasAdmin
from views.vista_monitoreo_jornadas import VistaMonitoreoJornadas


# Paleta de colores estilo Dark / Bootstrap Modern
COLOR_BG_MAIN = "#0f0f17"        # Fondo principal oscuro
COLOR_NAVBAR = "#1e1e2d"         # Fondo de la barra superior
COLOR_NAVBAR_TOP = "#151521"     # Fondo de la barra de usuario
COLOR_TEXT = "#ffffff"           # Texto blanco
COLOR_TEXT_MUTED = "#a2a3b7"     # Texto secundario (Gris)
COLOR_PRIMARY = "#009ef7"        # Accent azul
COLOR_DANGER = "#f1416c"         # Botón salir (Rojo)
COLOR_HOVER = "#2b2b40"          # Color hover para items de menú


class AdminDashboard(tk.Tk):
    def __init__(self, usuario="Administrador", rol="Admin"):
        super().__init__()
        
        self.usuario = usuario
        self.rol = rol

        self.title("TiketJets | Sistema de Gestión")

        
        
        # --- Configuración Pantalla Completa Adaptable ---
        self.state("zoomed") 
        self.configure(bg=COLOR_BG_MAIN)
        
        # Icono de la ventana
        self._cargar_icono_ventana()

        # 1. Crear primero el Área de Trabajo (para evitar el AttributeError)
        self.area_trabajo = tk.Frame(self, bg=COLOR_BG_MAIN, padx=20, pady=20)

        # 2. Construir la barra superior y navbar
        self._crear_cabecera_usuario()
        self._crear_navbar_principal()

        # 3. Empaquetar el contenedor central después de las barras superiores
        self.area_trabajo.pack(fill="both", expand=True)

        # 4. Cargar Vista por defecto
        self.mostrar_vista("Inicio")

    

    def _cargar_icono_ventana(self):
        ruta_ico = os.path.join("static", "img", "logoJetSmall.ico")
        if os.path.exists(ruta_ico):
            try:
                self.iconbitmap(ruta_ico)
            except Exception:
                pass

    # ------------------------------------------------------------------
    # 1. BARRA SUPERIOR (Info de usuario, rol y reloj)
    # ------------------------------------------------------------------
    def _crear_cabecera_usuario(self):
        top_bar = tk.Frame(self, bg=COLOR_NAVBAR_TOP, height=35)
        top_bar.pack(fill="x", side="top")

        # Info de Usuario
        lbl_info = tk.Label(
            top_bar, 
            text=f"👤 {self.usuario}  ({self.rol})", 
            bg=COLOR_NAVBAR_TOP, 
            fg=COLOR_TEXT, 
            font=("Segoe UI", 9, "bold")
        )
        lbl_info.pack(side="left", padx=15, pady=5)

        # Reloj en vivo
        self.lbl_reloj = tk.Label(
            top_bar, 
            text="", 
            bg=COLOR_NAVBAR_TOP, 
            fg=COLOR_TEXT_MUTED, 
            font=("Segoe UI", 9)
        )
        self.lbl_reloj.pack(side="left", padx=15, pady=5)
        self._actualizar_reloj()

        # Botón Cerrar Sesión
        btn_logout = tk.Button(
            top_bar,
            text="Cerrar sesión",
            bg=COLOR_DANGER,
            fg="white",
            font=("Segoe UI", 8, "bold"),
            bd=0,
            padx=10,
            pady=2,
            cursor="hand2",
            command=self.destroy
        )
        btn_logout.pack(side="right", padx=15, pady=5)

    def _actualizar_reloj(self):
        ahora = datetime.datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
        self.lbl_reloj.config(text=ahora)
        self.after(1000, self._actualizar_reloj)

    # ------------------------------------------------------------------
    # 2. NAVBAR MODERNO Y ELEGANTE
    # ------------------------------------------------------------------
    def _crear_navbar_principal(self):
        navbar = tk.Frame(self, bg=COLOR_NAVBAR, height=50)
        navbar.pack(fill="x", side="top")

        # -- Logo y Título Brand --
        brand_frame = tk.Frame(navbar, bg=COLOR_NAVBAR)
        brand_frame.pack(side="left", padx=(15, 25), pady=8)

        # Cargar logo
        ruta_logo = os.path.join("static", "img", "logoJetSmall.png")
        if os.path.exists(ruta_logo):
            try:
                img_raw = Image.open(ruta_logo)
                img_resized = img_raw.resize((28, 28), Image.Resampling.LANCZOS)
                self.logo_img = ImageTk.PhotoImage(img_resized)
                lbl_logo = tk.Label(brand_frame, image=self.logo_img, bg=COLOR_NAVBAR)
                lbl_logo.pack(side="left", padx=(0, 8))
            except Exception:
                pass

        lbl_brand = tk.Label(
            brand_frame, 
            text="TiketJets | Sistema de Gestión", 
            bg=COLOR_NAVBAR, 
            fg=COLOR_TEXT, 
            font=("Segoe UI", 11, "bold")
        )
        lbl_brand.pack(side="left")

        # -- Menús --
        # 1. Inicio
        self._crear_boton_nav(navbar, "Inicio", lambda: self.mostrar_vista("Inicio"))

        # 2. Jornadas
        mb_jornadas, menu_jornadas = self._crear_menubutton_nav(navbar, "Jornadas ▾")
        menu_jornadas.add_command(label="Crear Nueva Jornada", command=lambda: self.mostrar_vista("Jornadas"))
        menu_jornadas.add_command(label="Administrar Jornadas", command=lambda: self.mostrar_vista("Jornadas_Admin"))
        menu_jornadas.add_command(label="📡 Monitoreo de Jornadas", command=lambda: self.mostrar_vista("Monitoreo"))

        # 3. Cajas
        self._crear_boton_nav(navbar, "Cajas", lambda: self.mostrar_vista("Cajas"))

        # 4. Informes
        mb_informes, menu_informes = self._crear_menubutton_nav(navbar, "Informes ▾")
        menu_informes.add_command(label="Reportes Dashboard", command=lambda: self.mostrar_vista("Reportes"))
        menu_informes.add_command(label="Informes Recaudaciones", command=lambda: self.mostrar_vista("ReporteRecaudaciones"))
        menu_informes.add_command(label="Recaudación Boleterías", command=lambda: self.mostrar_vista("ReporteBoleteria"))

        # 5. Administración
        mb_admin, menu_admin = self._crear_menubutton_nav(navbar, "Administración ▾")
        menu_admin.add_command(label="Clientes", command=lambda: self.mostrar_vista("Clientes"))
        menu_admin.add_command(label="Usuarios", command=lambda: self.mostrar_vista("Usuarios"))
        menu_admin.add_command(label="Puntos de Venta", command=lambda: self.mostrar_vista("PuntosVenta"))
        menu_admin.add_command(label="Asignación Usuarios a Puntos", command=lambda: self.mostrar_vista("UsuariosPuntos"))
        menu_admin.add_separator()
        menu_admin.add_command(label="Modo de Pago", command=lambda: self.mostrar_vista("ModoPago"))
        menu_admin.add_command(label="Sectores", command=lambda: self.mostrar_vista("Sectores"))
        menu_admin.add_command(label="Productos", command=lambda: self.mostrar_vista("Productos"))

        # 6. Boletería
        mb_boleteria, menu_boleteria = self._crear_menubutton_nav(navbar, "Boletería ▾")
        menu_boleteria.add_command(label="Reporte Boletería Compacto", command=lambda: self.mostrar_vista("ReporteBoleteriaCompacto"))
        menu_boleteria.add_command(label="Reporte Boletería Detallado", command=lambda: self.mostrar_vista("ReporteBoleteriaDetallado"))

    # --- Helpers UI para Menús ---
    def _crear_boton_nav(self, parent, text, command):
        btn = tk.Button(
            parent,
            text=text,
            bg=COLOR_NAVBAR,
            fg=COLOR_TEXT_MUTED,
            activebackground=COLOR_HOVER,
            activeforeground=COLOR_TEXT,
            font=("Segoe UI", 10),
            bd=0,
            padx=12,
            pady=8,
            cursor="hand2",
            command=command
        )
        btn.pack(side="left", padx=2)
        btn.bind("<Enter>", lambda e: btn.config(fg=COLOR_TEXT, bg=COLOR_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(fg=COLOR_TEXT_MUTED, bg=COLOR_NAVBAR))
        return btn

    def _crear_menubutton_nav(self, parent, text):
        mb = tk.Menubutton(
            parent,
            text=text,
            bg=COLOR_NAVBAR,
            fg=COLOR_TEXT_MUTED,
            activebackground=COLOR_HOVER,
            activeforeground=COLOR_TEXT,
            font=("Segoe UI", 10),
            bd=0,
            padx=12,
            pady=8,
            cursor="hand2",
            direction="below"
        )
        mb.pack(side="left", padx=2)

        menu_desplegable = tk.Menu(
            mb, 
            tearoff=0, 
            bg=COLOR_NAVBAR, 
            fg=COLOR_TEXT, 
            activebackground=COLOR_PRIMARY, 
            activeforeground="white",
            bd=1,
            font=("Segoe UI", 9)
        )
        mb.config(menu=menu_desplegable)

        mb.bind("<Enter>", lambda e: mb.config(fg=COLOR_TEXT, bg=COLOR_HOVER))
        mb.bind("<Leave>", lambda e: mb.config(fg=COLOR_TEXT_MUTED, bg=COLOR_NAVBAR))
        
        # Retorna la tupla (menubutton, menu_desplegable)
        return mb, menu_desplegable

    # ------------------------------------------------------------------
    # 3. GESTOR DE VISTAS CENTRALES
    # ------------------------------------------------------------------
    def mostrar_vista(self, nombre_vista):
        for widget in self.area_trabajo.winfo_children():
            widget.destroy()

        if nombre_vista == "Usuarios":
            vista = VistaUsuarios(self.area_trabajo)
            vista.pack(fill="both", expand=True)
            
        elif nombre_vista == "Jornadas":
            vista = VistaJornadas(self.area_trabajo)
            vista.pack(fill="both", expand=True)

        elif nombre_vista == "PuntosVenta":
            vista = VistaPuntosVenta(self.area_trabajo)
            vista.pack(fill="both", expand=True)

        # ... otros controles de vistas (jornadas, puntos de venta, etc.) ...
        
        elif nombre_vista == "Productos":
            self.vista_actual = VistaProductos(self.area_trabajo)
            self.vista_actual.pack(fill="both", expand=True)
            
        # ...

        elif nombre_vista.lower() in ["jornadas_admin", "admin_jornadas"]:
            vista = VistaJornadasAdmin(self.area_trabajo)
            vista.pack(fill="both", expand=True)

        elif nombre_vista.lower() in ["monitoreo_jornadas", "monitoreo"]:
            vista = VistaMonitoreoJornadas(self.area_trabajo)
            vista.pack(fill="both", expand=True)

        elif nombre_vista == "Inicio":
            self._vista_bienvenida()
        else:
            self._vista_en_construccion(nombre_vista)

    def _vista_bienvenida(self):
        container = tk.Frame(self.area_trabajo, bg=COLOR_BG_MAIN)
        container.place(relx=0.5, rely=0.4, anchor="center")

        tk.Label(
            container, 
            text="Bienvenido a TiketJets", 
            font=("Segoe UI", 22, "bold"), 
            bg=COLOR_BG_MAIN, 
            fg=COLOR_PRIMARY
        ).pack(pady=10)

        tk.Label(
            container, 
            text="Selecciona una opción del menú superior para comenzar a administrar el sistema.", 
            font=("Segoe UI", 11), 
            bg=COLOR_BG_MAIN, 
            fg=COLOR_TEXT_MUTED
        ).pack()

    def _vista_en_construccion(self, nombre_modulo):
        container = tk.Frame(self.area_trabajo, bg=COLOR_BG_MAIN)
        container.place(relx=0.5, rely=0.4, anchor="center")

        tk.Label(
            container, 
            text=f"📂 Módulo: {nombre_modulo}", 
            font=("Segoe UI", 18, "bold"), 
            bg=COLOR_BG_MAIN, 
            fg=COLOR_TEXT
        ).pack(pady=10)

        tk.Label(
            container, 
            text="Esta vista aún no ha sido conectada o está en desarrollo.", 
            font=("Segoe UI", 10), 
            bg=COLOR_BG_MAIN, 
            fg=COLOR_TEXT_MUTED
        ).pack()


if __name__ == "__main__":
    app = AdminDashboard()
    app.mainloop()