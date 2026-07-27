class Sesion:
    """
    Maneja la sesión del usuario, la jornada activa y el punto de venta
    durante toda la ejecución de la aplicación.
    """

    usuario = None
    idjornada = None
    idpunto = None
    nombre_jornada = None

    @classmethod
    def iniciar(cls, datos_usuario, idjornada=None, idpunto=None, nombre_jornada=""):
        """
        Guarda todos los datos del usuario autenticado y su contexto de caja.
        """
        cls.usuario = datos_usuario
        cls.idjornada = idjornada
        cls.idpunto = idpunto
        cls.nombre_jornada = nombre_jornada

    @classmethod
    def establecer_jornada(cls, idjornada, idpunto, nombre_jornada=""):
        """
        Permite asignar o actualizar la jornada y punto si se abren después del login.
        """
        cls.idjornada = idjornada
        cls.idpunto = idpunto
        cls.nombre_jornada = nombre_jornada

    @classmethod
    def cerrar(cls):
        """
        Cierra la sesión y limpia el contexto.
        """
        cls.usuario = None
        cls.idjornada = None
        cls.idpunto = None
        cls.nombre_jornada = None

    @classmethod
    def activa(cls):
        return cls.usuario is not None

    @classmethod
    def obtener(cls):
        return cls.usuario

    @classmethod
    def id(cls):
        # Mapea 'idusuario' o 'idusuarios'
        if not cls.usuario:
            return None
        return cls.usuario.get("idusuarios") or cls.usuario.get("idusuario") or cls.usuario.get("id")

    @classmethod
    def nombre(cls):
        return cls.usuario.get("nombre") if cls.usuario else ""

    @classmethod
    def apellido(cls):
        return cls.usuario.get("apellido") if cls.usuario else ""

    @classmethod
    def rol(cls):
        return cls.usuario.get("rol") if cls.usuario else ""

    @classmethod
    def estado(cls):
        return cls.usuario.get("estado") if cls.usuario else ""

    @classmethod
    def obtener_campo(cls, campo):
        if cls.usuario:
            return cls.usuario.get(campo)
        return None