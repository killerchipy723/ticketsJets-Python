class Sesion:
    """
    Maneja la sesión del usuario durante toda la ejecución
    de la aplicación.
    """

    usuario = None

    @classmethod
    def iniciar(cls, datos_usuario):
        """
        Guarda todos los datos del usuario autenticado.
        """
        cls.usuario = datos_usuario

    @classmethod
    def cerrar(cls):
        """
        Cierra la sesión.
        """
        cls.usuario = None

    @classmethod
    def activa(cls):
        """
        Devuelve True si existe una sesión iniciada.
        """
        return cls.usuario is not None

    @classmethod
    def obtener(cls):
        """
        Devuelve el diccionario completo del usuario.
        """
        return cls.usuario

    @classmethod
    def id(cls):
        return cls.usuario.get("idusuarios") if cls.usuario else None

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
        """
        Devuelve cualquier columna de la tabla usuarios.
        """
        if cls.usuario:
            return cls.usuario.get(campo)

        return None