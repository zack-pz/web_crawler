from dataclasses import dataclass

@dataclass
class ConfiguracionRastreador:
    url_inicial: str
    dominios_permitidos: list[str]
    max_paginas: int = 50
    max_profundidad: int = 3
    rango_demora: tuple[float, float] = (0.5, 1.5)
    agente_usuario: str = "PythonWebCrawler/1.0"
    archivo_salida: str = "resultados.json"
