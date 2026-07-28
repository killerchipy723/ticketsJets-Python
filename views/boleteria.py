# views/boleteria.py
import tkinter as tk
from tkinter import ttk, messagebox
from sesion import Sesion

from database.boleteria_db import (
    obtener_datos_boleteria_home,
    registrar_venta_entrada_db,
    obtener_datos_ticket_cierre,
    obtener_datos_ticket_venta_db,
    cerrar_caja_boleteria_db
)
from views.modals.modal_cliente import ModalBuscarCliente
from reports.impresion_boleteria import (
    imprimir_ticket_boleteria_silencioso,
    imprimir_ticket_cierre_silencioso
)


class VistaBoleteria(tk.Frame):
    def __init__(self, parent, session_data, logout_callback=None):
        super().__init__(parent, bg="#1e1e1e")
        self.session_data = session_data or {}
        self.logout_callback = logout_callback

        # Obtener valores directos o desde la clase Sesion de respaldo
        self.idjornada = self._obtener_idjornada_sesion()
        self.idusuario = self.session_data.get("idusuario")
        self.operador = self.session_data.get("operador")

        self.caja_cerrada = False  # Estado de la caja local

        self.cliente_actual = {
            "idclientes": 1,
            "apenomb": "CONSUMIDOR FINAL",
            "dni": "00000000"
        }

        self.sectores = []
        self.modos_pago = []

        self.crear_interfaz()
        self.cargar_datos_iniciales()

    def _obtener_idjornada_sesion(self):
        """Intenta extraer idjornada desde dicts o atributos globales de Sesion."""
        if isinstance(self.session_data, dict) and self.session_data.get("idjornada"):
            return self.session_data.get("idjornada")

        datos = {}
        if hasattr(Sesion, "datos") and isinstance(Sesion.datos, dict):
            datos = Sesion.datos
        elif hasattr(Sesion, "_datos") and isinstance(Sesion._datos, dict):
            datos = Sesion._datos

        return datos.get("idjornada") or getattr(Sesion, "idjornada", None)

    def obtener_nombre_punto_venta(self):
        return (
            self.session_data.get("punto_venta_nombre") or
            self.session_data.get("puntonombre") or
            self.session_data.get("punto_nombre") or
            "Punto no asignado"
        )

    def crear_interfaz(self):
        # --- Encabezado ---
        frame_top = tk.Frame(self, bg="#2d2d2d", height=60)
        frame_top.pack(fill="x", side="top")

        lbl_titulo = tk.Label(
            frame_top,
            text=f"🎟️ Módulo Boletería - {self.session_data.get('jornada_nombre', 'Sin Jornada')}",
            font=("Segoe UI", 14, "bold"),
            fg="white",
            bg="#2d2d2d"
        )
        lbl_titulo.pack(side="left", padx=20, pady=10)

        punto_venta = self.obtener_nombre_punto_venta()

        self.lbl_estado_caja = tk.Label(
            frame_top,
            text="🟢 CAJA ABIERTA",
            font=("Segoe UI", 10, "bold"),
            fg="#28a745",
            bg="#2d2d2d"
        )
        self.lbl_estado_caja.pack(side="right", padx=(5, 20))

        lbl_usuario = tk.Label(
            frame_top,
            text=f"👤 Operador: {self.operador}  |  💻 Caja: {punto_venta}  |",
            font=("Segoe UI", 10, "bold"),
            fg="#0dcaf0",
            bg="#2d2d2d"
        )
        lbl_usuario.pack(side="right", padx=5)

        # --- Panel Principal ---
        frame_contenido = tk.Frame(self, bg="#1e1e1e")
        frame_contenido.pack(fill="both", expand=True, padx=20, pady=20)

        # Columna Izquierda: Emisión de Entradas
        self.frame_emision = tk.LabelFrame(
            frame_contenido, text=" Emisión de Entradas ",
            font=("Segoe UI", 11, "bold"), fg="white", bg="#252526", bd=1
        )
        self.frame_emision.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Cliente
        tk.Label(self.frame_emision, text="Cliente:", font=("Segoe UI", 10), fg="white", bg="#252526").pack(anchor="w", padx=15, pady=(15, 2))

        frame_cliente_control = tk.Frame(self.frame_emision, bg="#252526")
        frame_cliente_control.pack(fill="x", padx=15, pady=5)

        self.txt_cliente = tk.Entry(
            frame_cliente_control, font=("Segoe UI", 10, "bold"),
            bg="#1e1e1e", fg="#0dcaf0", bd=1, relief="solid"
        )
        self.txt_cliente.pack(side="left", fill="x", expand=True, ipady=3)
        self.actualizar_input_cliente()

        self.btn_buscar_cli = tk.Button(
            frame_cliente_control, text="🔍 Buscar / Agregar",
            bg="#0d6efd", fg="white", font=("Segoe UI", 9, "bold"),
            bd=0, cursor="hand2", padx=10, command=self.abrir_modal_cliente
        )
        self.btn_buscar_cli.pack(side="right", padx=(5, 0))

        # Sector
        tk.Label(self.frame_emision, text="Sector:", font=("Segoe UI", 10), fg="white", bg="#252526").pack(anchor="w", padx=15, pady=(10, 2))
        self.cb_sector = ttk.Combobox(self.frame_emision, state="readonly", font=("Segoe UI", 11))
        self.cb_sector.pack(fill="x", padx=15, pady=5)
        self.cb_sector.bind("<<ComboboxSelected>>", self.calcular_total)

        # Cantidad
        tk.Label(self.frame_emision, text="Cantidad:", font=("Segoe UI", 10), fg="white", bg="#252526").pack(anchor="w", padx=15, pady=(10, 2))
        self.spin_cantidad = tk.Spinbox(self.frame_emision, from_=1, to=100, font=("Segoe UI", 11), command=self.calcular_total)
        self.spin_cantidad.pack(fill="x", padx=15, pady=5)
        self.spin_cantidad.bind("<KeyRelease>", lambda e: self.calcular_total())

        # Modo de Pago
        tk.Label(self.frame_emision, text="Modo de Pago:", font=("Segoe UI", 10), fg="white", bg="#252526").pack(anchor="w", padx=15, pady=(10, 2))
        self.cb_modopago = ttk.Combobox(self.frame_emision, state="readonly", font=("Segoe UI", 11))
        self.cb_modopago.pack(fill="x", padx=15, pady=5)

        # Total a Pagar
        self.lbl_total_venta = tk.Label(self.frame_emision, text="Total: $0.00", font=("Segoe UI", 16, "bold"), fg="#28a745", bg="#252526")
        self.lbl_total_venta.pack(anchor="w", padx=15, pady=20)

        self.btn_emitir = tk.Button(
            self.frame_emision, text="Emitir Entrada", font=("Segoe UI", 12, "bold"),
            bg="#0d6efd", fg="white", bd=0, cursor="hand2", command=self.procesar_venta
        )
        self.btn_emitir.pack(fill="x", padx=15, pady=10)

        # Columna Derecha: Indicadores y Acciones
        frame_stats = tk.Frame(frame_contenido, bg="#1e1e1e")
        frame_stats.pack(side="right", fill="both", expand=True, padx=(10, 0))

        # Recaudación
        box_rec = tk.Frame(frame_stats, bg="#2d2d2d", bd=1)
        box_rec.pack(fill="x", pady=(0, 15))

        tk.Label(box_rec, text="Recaudación Total (Jornada)", font=("Segoe UI", 10), fg="#adb5bd", bg="#2d2d2d").pack(anchor="w", padx=15, pady=(10, 0))
        self.lbl_recaudacion = tk.Label(box_rec, text="$0.00", font=("Segoe UI", 20, "bold"), fg="#198754", bg="#2d2d2d")
        self.lbl_recaudacion.pack(anchor="w", padx=15, pady=(0, 10))

        # Entradas Vendidas
        box_ent = tk.Frame(frame_stats, bg="#2d2d2d", bd=1)
        box_ent.pack(fill="x", pady=(0, 15))

        tk.Label(box_ent, text="Entradas Vendidas", font=("Segoe UI", 10), fg="#adb5bd", bg="#2d2d2d").pack(anchor="w", padx=15, pady=(10, 0))
        self.lbl_entradas_cant = tk.Label(box_ent, text="0", font=("Segoe UI", 20, "bold"), fg="#0dcaf0", bg="#2d2d2d")
        self.lbl_entradas_cant.pack(anchor="w", padx=15, pady=(0, 10))

        # Botón Cierre de Caja
        self.btn_cierre = tk.Button(
            frame_stats, text="🔒 Cerrar Caja e Imprimir Resumen", font=("Segoe UI", 11, "bold"),
            bg="#ffc107", fg="black", bd=0, cursor="hand2", command=self.ejecutar_cierre_caja
        )
        self.btn_cierre.pack(fill="x", pady=10)

        if self.logout_callback:
            btn_logout = tk.Button(
                frame_stats, text="Cerrar Sesión", font=("Segoe UI", 10, "bold"),
                bg="#dc3545", fg="white", bd=0, cursor="hand2", command=self.logout_callback
            )
            btn_logout.pack(fill="x", pady=10)

    def actualizar_input_cliente(self):
        self.txt_cliente.config(state="normal")
        self.txt_cliente.delete(0, tk.END)
        texto = f"{self.cliente_actual['apenomb']} (DNI: {self.cliente_actual['dni']})"
        self.txt_cliente.insert(0, texto)
        self.txt_cliente.config(state="readonly")

    def abrir_modal_cliente(self):
        if self.validar_estado_para_operar():
            ModalBuscarCliente(self, callback_seleccion=self.al_seleccionar_cliente)

    def al_seleccionar_cliente(self, cliente):
        self.cliente_actual = cliente
        self.actualizar_input_cliente()

    def resetear_cliente_defecto(self):
        self.cliente_actual = {
            "idclientes": 1,
            "apenomb": "CONSUMIDOR FINAL",
            "dni": "00000000"
        }
        self.actualizar_input_cliente()

    def cargar_datos_iniciales(self):
        self.idjornada = self._obtener_idjornada_sesion()
        if not self.idjornada:
            self.bloquear_modulo("No hay una jornada activa seleccionada.")
            return

        idpunto = self.session_data.get("idpunto") or self.session_data.get("idpunto_venta")
        datos, err = obtener_datos_boleteria_home(self.idjornada, idpunto=idpunto)
        if err:
            messagebox.showerror("Error", err)
            return

        if datos.get("cerrado_boleteria"):
            self.bloquear_modulo("La caja de boletería para esta jornada ya fue cerrada.")
            return

        self.sectores = datos["sectores"]
        self.modos_pago = datos["modopago"]

        nombres_sectores = [f"{s['nombre']} (${s['precio']:.2f})" for s in self.sectores]
        self.cb_sector["values"] = nombres_sectores
        if nombres_sectores:
            self.cb_sector.current(0)

        nombres_modos = [m["modo"] for m in self.modos_pago]
        self.cb_modopago["values"] = nombres_modos
        if nombres_modos:
            self.cb_modopago.current(0)

        self.lbl_recaudacion.config(text=f"${datos['recaudacion']:,.2f}")
        self.lbl_entradas_cant.config(text=str(datos["entradas_vendidas"]))

        self.calcular_total()

    def bloquear_modulo(self, mensaje_motivo):
        self.caja_cerrada = True
        self.btn_emitir.config(state="disabled", bg="#6c757d", cursor="arrow")
        self.btn_cierre.config(state="disabled", bg="#6c757d", cursor="arrow")
        self.btn_buscar_cli.config(state="disabled", bg="#6c757d", cursor="arrow")
        self.cb_sector.config(state="disabled")
        self.cb_modopago.config(state="disabled")
        self.spin_cantidad.config(state="disabled")

        self.lbl_estado_caja.config(text="🔴 CAJA CERRADA / INACTIVA", fg="#dc3545")
        messagebox.showwarning("Módulo Bloqueado", mensaje_motivo)

    def validar_estado_para_operar(self):
        self.idjornada = self._obtener_idjornada_sesion()
        if not self.idjornada:
            messagebox.showerror("Acción No Permitida", "No hay ninguna jornada activa.")
            return False
        if self.caja_cerrada:
            messagebox.showerror("Acción No Permitida", "La caja de boletería está cerrada.")
            return False
        return True

    def calcular_total(self, event=None):
        idx = self.cb_sector.current()
        if idx == -1 or not self.sectores:
            return

        try:
            cant = int(self.spin_cantidad.get())
        except ValueError:
            cant = 1

        precio = float(self.sectores[idx]["precio"])
        total = precio * cant
        self.lbl_total_venta.config(text=f"Total: ${total:,.2f}")

    def procesar_venta(self):
        if not self.validar_estado_para_operar():
            return

        idx_sec = self.cb_sector.current()
        idx_pago = self.cb_modopago.current()

        if idx_sec == -1 or idx_pago == -1:
            messagebox.showwarning("Atención", "Seleccione sector y forma de pago.")
            return

        try:
            cant = int(self.spin_cantidad.get())
            if cant <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showwarning("Atención", "Ingrese una cantidad válida.")
            return

        sector_sel = self.sectores[idx_sec]
        pago_sel = self.modos_pago[idx_pago]

        total = round(float(sector_sel["precio"]) * cant, 2)
        pagos = [{"idmodopago": int(pago_sel["idmodopago"]), "importe": total}]

        idcliente = self.cliente_actual["idclientes"]

        try:
            ok, res = registrar_venta_entrada_db(
                idusuario=self.idusuario,
                idjornada=self.idjornada,
                idcliente=idcliente,
                idsector=sector_sel["idsector"],
                cantidad=cant,
                total=total,
                pagos=pagos
            )

            if ok:
                idventa = res["idventa"]
                self.resetear_cliente_defecto()
                self.cargar_datos_iniciales()

                datos_ticket, err = obtener_datos_ticket_venta_db(idventa)
                if not err:
                    try:
                        imprimir_ticket_boleteria_silencioso(datos_ticket)
                    except Exception as e_imp:
                        print(f"⚠️ Error al imprimir ticket de venta: {e_imp}")
                else:
                    messagebox.showerror("Error al obtener datos ticket", err)
            else:
                messagebox.showerror("Error al procesar", res)

        except Exception as e:
            messagebox.showerror("Error inesperado", f"Ocurrió un problema en la venta: {e}")

    def ejecutar_cierre_caja(self):
        """Cierra la caja e imprime el ticket sin riesgo de crash por excepciones de impresión."""
        if not self.validar_estado_para_operar():
            return

        confirmar = messagebox.askyesno(
            "Confirmar Cierre de Caja",
            "¿Está seguro de que desea cerrar la caja de boletería?\n\n"
            "Una vez cerrada, no se podrán realizar más ventas de entradas para esta jornada.",
            icon="warning"
        )

        if not confirmar:
            return

        try:
            # Extraer idpunto de forma segura desde la sesión
            idpunto = self.session_data.get("idpunto") or self.session_data.get("idpunto_venta")

            # 1. Cierre en DB pasando idpunto
            ok, msg = cerrar_caja_boleteria_db(self.idjornada, self.idusuario, idpunto=idpunto)
            if not ok:
                messagebox.showerror("Error de Cierre", msg)
                return

            # 2. Obtener datos de resumen
            datos_cierre, err = obtener_datos_ticket_cierre(self.idjornada)

            if err:
                messagebox.showwarning("Cierre Registrado", f"La caja se cerró pero ocurrió un problema al obtener el resumen: {err}")
            else:
                # Intento de impresión protegido contra caídas
                try:
                    imprimir_ticket_cierre_silencioso(self.idjornada, session_data=self.session_data)
                    messagebox.showinfo("Cierre Exitoso", "La caja ha sido cerrada correctamente y el resumen ha sido impreso.")
                except Exception as e_print:
                    print(f"❌ Error al imprimir ticket de cierre: {e_print}")
                    messagebox.showwarning("Cierre Exitoso", f"La caja se cerró correctamente en la BD, pero falló la impresión: {e_print}")

            # 3. Bloquear el módulo
            self.bloquear_modulo("La caja de boletería ha sido cerrada.")

        except Exception as e:
            messagebox.showerror("Error Inesperado", f"Ocurrió un error crítico durante el cierre: {e}")