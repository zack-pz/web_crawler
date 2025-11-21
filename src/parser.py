from bs4 import BeautifulSoup
from typing import Set, Tuple

def extraer_enlaces(contenido_html: str) -> Set[str]:
    """Extrae todos los href de las etiquetas <a>."""
    sopa = BeautifulSoup(contenido_html, 'html.parser')
    enlaces = set()
    for etiqueta_a in sopa.find_all('a', href=True):
        enlaces.add(etiqueta_a['href'])
    return enlaces

def extraer_datos_pagina(contenido_html: str) -> Tuple[str, str]:
    """Extrae título y contenido de texto (opcional pero útil)."""
    sopa = BeautifulSoup(contenido_html, 'html.parser')
    titulo = sopa.title.string if sopa.title else "Sin Título"
    # Extracción básica de texto
    texto = sopa.get_text(separator=' ', strip=True)[:200] + "..." # Vista previa
    return titulo, texto

def analizar_robots_txt(contenido_robots: str, agente_usuario: str = "*") -> list[str]:
    """
    Analiza robots.txt para encontrar reglas Disallow para el agente de usuario dado.
    Este es un parser simplificado.
    """
    rutas_no_permitidas = []
    if not contenido_robots:
        return rutas_no_permitidas

    lineas = contenido_robots.splitlines()
    agente_actual = None
    
    for linea in lineas:
        linea = linea.strip()
        if not linea or linea.startswith('#'):
            continue
            
        if linea.lower().startswith('user-agent:'):
            agente_actual = linea.split(':', 1)[1].strip()
        elif linea.lower().startswith('disallow:') and agente_actual:
            # Verificar si esta regla aplica a nosotros
            if agente_actual == '*' or agente_actual in agente_usuario:
                ruta = linea.split(':', 1)[1].strip()
                if ruta:
                    rutas_no_permitidas.append(ruta)
    
    return rutas_no_permitidas
