# views/vista_monitoreo_jornadas.py
import tkinter as tk
from tkinter import ttk, messagebox
from database.monitoreo_db import obtener_datos_monitoreo, finalizar_jornada_activa

# Constantes de Color y Estilo
COLOR_MAIN_BG = "#0f0f17"
COLOR_CARD_BG = "#181825"
COLOR_CARD_BORDER = "#313244"
TEXT_LIGHT = "#f8f9fa"
TEXT_MUTED = "#a6adc8"
COLOR_SUCCESS = "#2ea043"
COLOR_INACTIVE = "#313244"
COLOR_DANGER = "#da3633"

class VistaMonitoreoJornadas(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_MAIN_BG)

        # Variables de estado 
        self.jornada_actual = None
        self.bucle_monitoreo_id = None # Para controlar el refresco automático

        self._crear_encabezado()
        self._crear_contenedor_cards()
        
        # Iniciamos la carga dinámica de datos
        self.cargar_datos_dinamicos()

        # Limpieza al cerrar/destruir el widget para evitar fugas de timers
        self.bind("<Destroy>", self._al_destruir)

    def _crear_encabezado(self):
        """Encabezado superior compacto."""
        frame_header = tk.Frame(self, bg=COLOR_MAIN_BG)
        frame_header.pack(fill="x", padx=15, pady=(10, 10))

        f_info = tk.Frame(frame_header, bg=COLOR_MAIN_BG)
        f_info.pack(side="left")

        lbl_icon = tk.Label(f_info, text="📡", font=("Segoe UI", 13), fg=TEXT_LIGHT, bg=COLOR_MAIN_BG)
        lbl_icon.pack(side="left", padx=(0, 6))

        lbl_titulo = tk.Label(
            f_info, text="Monitoreo de Jornada Activa",
            font=("Segoe UI", 13, "bold"), fg=TEXT_LIGHT, bg=COLOR_MAIN_BG
        )
        lbl_titulo.pack(anchor="w")

        self.lbl_subtitulo = tk.Label(
            f_info, text="Buscando jornada activa...",
            font=("Segoe UI", 8), fg=COLOR_SUCCESS, bg=COLOR_MAIN_BG
        )
        self.lbl_subtitulo.pack(anchor="w")

        self.btn_finalizar = tk.Button(
            frame_header, text="⛔ Finalizar Jornada",
            font=("Segoe UI", 8, "bold"), bg=COLOR_DANGER, fg="white",
            bd=0, cursor="hand2", padx=10, pady=4,
            command=self.confirmar_finalizar_jornada
        )
        self.btn_finalizar.pack(side="right")

    def _crear_contenedor_cards(self):
        """Área scrolleable donde se dibujan las tarjetas de las cajas."""
        canvas = tk.Canvas(self, bg=COLOR_MAIN_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)

        self.f_cards_grid = tk.Frame(canvas, bg=COLOR_MAIN_BG)
        id_win = canvas.create_window((0, 0), window=self.f_cards_grid, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        def _on_canvas_configure(event):
            canvas.itemconfig(id_win, width=event.width)

        canvas.bind('<Configure>', _on_canvas_configure)
        canvas.pack(side="left", fill="both", expand=True, padx=15)
        scrollbar.pack(side="right", fill="y")

        self.f_cards_grid.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

    def cargar_datos_dinamicos(self):
        """Consulta la BD y dibuja las tarjetas. Se re-ejecuta cada 5 segundos."""
        # Cancelar cualquier timer pendiente antes de crear uno nuevo
        if self.bucle_monitoreo_id:
            self.after_cancel(self.bucle_monitoreo_id)
            self.bucle_monitoreo_id = None

        jornada, cajas = obtener_datos_monitoreo()

        # Limpiar tarjetas anteriores
        for widget in self.f_cards_grid.winfo_children():
            widget.destroy()

        if not jornada:
            self.lbl_subtitulo.config(text="No hay ninguna jornada activa en este momento", fg=COLOR_DANGER)
            self.btn_finalizar.config(state="disabled", bg=COLOR_INACTIVE)
            self.jornada_actual = None
        else:
            # Actualizar variables y labels con los datos reales
            self.jornada_actual = jornada
            self.lbl_subtitulo.config(text=f"Jornada en curso: {jornada['nombre']}", fg=COLOR_SUCCESS)
            self.btn_finalizar.config(state="normal", bg=COLOR_DANGER)

            # Dibujar las tarjetas traídas de la DB
            row = 0
            col = 0
            for caja in cajas:
                self._crear_card_caja(self.f_cards_grid, caja, row, col)
                col += 1
                if col > 5:  # 6 tarjetas por fila
                    col = 0
                    row += 1

        # Mantiene SIEMPRE el refresco activo cada 5 segundos (incluso si no hay jornada activa)
        self.bucle_monitoreo_id = self.after(5000, self.cargar_datos_dinamicos)

    def _crear_card_caja(self, parent, datos_caja, row, col):
        """Dibuja una tarjeta (Card) individual."""
        es_activa = datos_caja["activa"]
        color_borde = COLOR_SUCCESS if es_activa else COLOR_CARD_BORDER
        
        card = tk.Frame(parent, bg=COLOR_CARD_BG, highlightbackground=color_borde, highlightthickness=1, padx=8, pady=8)
        card.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")

        f_top = tk.Frame(card, bg=COLOR_CARD_BG)
        f_top.pack(fill="x")

        tk.Label(f_top, text="🖥️", font=("Segoe UI", 10), bg=COLOR_CARD_BG).pack(side="left", padx=(0, 2))
        tk.Label(f_top, text=datos_caja["nombre"], font=("Segoe UI", 8, "bold"), fg=TEXT_LIGHT, bg=COLOR_CARD_BG).pack(side="left")

        txt_estado = "ACTIVA" if es_activa else "INACTIVA"
        bg_badge = COLOR_SUCCESS if es_activa else COLOR_INACTIVE
        
        tk.Label(card, text=txt_estado, font=("Segoe UI", 6, "bold"), fg="white", bg=bg_badge, padx=3, pady=1).pack(anchor="w", pady=(2, 4))
        tk.Frame(card, bg=COLOR_CARD_BORDER, height=1).pack(fill="x", pady=(0, 4))

        if es_activa:
            # Formatear moneda a formato AR ($ 10.500,50)
            monto_fmt = f"{datos_caja['recaudacion']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            
            tk.Label(card, text=f"👤 {datos_caja['operador']}", font=("Segoe UI", 7), fg=TEXT_LIGHT, bg=COLOR_CARD_BG, anchor="w").pack(fill="x")
            tk.Label(card, text="Parcial:", font=("Segoe UI", 7), fg=TEXT_MUTED, bg=COLOR_CARD_BG, anchor="w").pack(fill="x", pady=(2, 0))
            tk.Label(card, text=f"${monto_fmt}", font=("Segoe UI", 9, "bold"), fg=COLOR_SUCCESS, bg=COLOR_CARD_BG, anchor="w").pack(fill="x")
        else:
            tk.Label(card, text="Sin asignar", font=("Segoe UI", 7, "italic"), fg=TEXT_MUTED, bg=COLOR_CARD_BG, anchor="w").pack(fill="x", pady=(6, 6))

    def confirmar_finalizar_jornada(self):
        """Confirmación antes de dar por cerrada la jornada."""
        if not self.jornada_actual:
            return

        respuesta = messagebox.askyesno(
            "Finalizar Jornada",
            f"¿Está seguro de que desea finalizar la jornada '{self.jornada_actual['nombre']}'?\n\nNo se podrán realizar más ventas en las cajas hasta abrir una nueva.",
            icon="warning"
        )
        
        if respuesta:
            exito = finalizar_jornada_activa(self.jornada_actual['idjornada'])
            if exito:
                messagebox.showinfo("Éxito", "La jornada ha sido finalizada correctamente.")
                # Recargamos la interfaz (que limpiará y programará el bucle)
                self.cargar_datos_dinamicos()
            else:
                messagebox.showerror("Error", "Ocurrió un problema al intentar finalizar la jornada.")

    def _al_destruir(self, event):
        """Limpia el timer de polling si la pantalla se cierra para evitar consumo en segundo plano."""
        if self.bucle_monitoreo_id:
            self.after_cancel(self.bucle_monitoreo_id)
            self.bucle_monitoreo_id = None