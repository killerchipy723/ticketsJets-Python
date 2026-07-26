# utils/network.py
import uuid

def obtener_mac_local() -> str:
    """
    Retorna la dirección MAC de la placa de red principal
    formateada en mayúsculas (ej: AA:BB:CC:DD:EE:FF).
    """
    try:
        mac_num = uuid.getnode()
        mac = ':'.join(['{:02x}'.format((mac_num >> elements) & 0xff) for elements in range(0, 8*6, 8)][::-1])
        return mac.upper()
    except Exception:
        return "DESCONOCIDO"