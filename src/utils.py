import logging
from urllib.parse import urljoin, urlparse

def configurar_logger():
    """Configura un logger simple que imprime en consola."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    return logging.getLogger("rastreador")

def normalizar_url(url: str, url_base: str) -> str:
    """Resuelve enlaces relativos y elimina fragmentos."""
    # Resolver URL relativa
    url_absoluta = urljoin(url_base, url)
    
    # Analizar para eliminar fragmento
    analizado = urlparse(url_absoluta)
    return analizado.scheme + "://" + analizado.netloc + analizado.path + (("?" + analizado.query) if analizado.query else "")

def es_dominio_valido(url: str, dominios_permitidos: list[str]) -> bool:
    """Verifica si la URL pertenece a uno de los dominios permitidos."""
    dominio = urlparse(url).netloc
    # Eliminar 'www.' para comparación si está presente, o manejo flexible
    # Chequeo simple: ¿el dominio termina con alguno de los permitidos?
    return any(dominio == d or dominio.endswith("." + d) for d in dominios_permitidos)
