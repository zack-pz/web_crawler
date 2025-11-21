import requests
from requests.exceptions import RequestException

def descargar_pagina(url: str, agente_usuario: str, tiempo_espera: int = 10) -> str | None:
    """Descarga una página y devuelve su contenido como texto. Devuelve None si falla."""
    cabeceras = {'User-Agent': agente_usuario}
    try:
        respuesta = requests.get(url, headers=cabeceras, timeout=tiempo_espera)
        respuesta.raise_for_status()
        # Asegurar codificación correcta
        if respuesta.encoding is None:
            respuesta.encoding = 'utf-8'
        return respuesta.text
    except RequestException:
        # Dejamos que el llamador maneje el log si es necesario, o solo devolvemos None
        return None

def obtener_robots_txt(url_base: str, agente_usuario: str) -> str | None:
    """Obtiene el archivo robots.txt para una URL base dada."""
    url_robots = url_base.rstrip('/') + '/robots.txt'
    return descargar_pagina(url_robots, agente_usuario)
