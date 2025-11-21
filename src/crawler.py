import time
import random
import json
from collections import deque
from urllib.parse import urlparse

from .config import ConfiguracionRastreador
from .utils import configurar_logger, normalizar_url, es_dominio_valido
from .network import descargar_pagina, obtener_robots_txt
from .parser import extraer_enlaces, extraer_datos_pagina, analizar_robots_txt

class RastreadorWeb:
    def __init__(self, config: ConfiguracionRastreador):
        self.config = config
        self.logger = configurar_logger()
        self.visitados = set()
        self.cola = deque([(config.url_inicial, 0)]) # (url, profundidad)
        self.resultados = []
        self.rutas_no_permitidas = []

    def _inicializar_robots(self):
        """Obtiene y analiza robots.txt."""
        url_base = f"{urlparse(self.config.url_inicial).scheme}://{urlparse(self.config.url_inicial).netloc}"
        self.logger.info(f"Obteniendo robots.txt de {url_base}...")
        contenido = obtener_robots_txt(url_base, self.config.agente_usuario)
        if contenido:
            self.rutas_no_permitidas = analizar_robots_txt(contenido, self.config.agente_usuario)
            self.logger.info(f"Se encontraron {len(self.rutas_no_permitidas)} rutas no permitidas.")
        else:
            self.logger.warning("No se pudo obtener robots.txt o estaba vacío.")

    def _es_permitido(self, url: str) -> bool:
        """Verifica si una URL está permitida por robots.txt."""
        ruta = urlparse(url).path
        for no_permitida in self.rutas_no_permitidas:
            if ruta.startswith(no_permitida):
                return False
        return True

    def ejecutar(self):
        self._inicializar_robots()
        
        paginas_rastreadas = 0
        
        while self.cola and paginas_rastreadas < self.config.max_paginas:
            url_actual, profundidad = self.cola.popleft()
            
            if url_actual in self.visitados:
                continue
            
            if profundidad > self.config.max_profundidad:
                continue
            
            if not self._es_permitido(url_actual):
                self.logger.info(f"Saltando {url_actual} (robots.txt)")
                continue

            self.logger.info(f"Rastreando: {url_actual} (Profundidad: {profundidad})")
            
            # Rate limiting
            demora = random.uniform(*self.config.rango_demora)
            time.sleep(demora)
            
            contenido_html = descargar_pagina(url_actual, self.config.agente_usuario)
            
            if not contenido_html:
                self.logger.error(f"Fallo al descargar {url_actual}")
                self.visitados.add(url_actual) # Marcar como visitado para evitar reintentos
                continue

            # Parsear
            titulo, vista_previa = extraer_datos_pagina(contenido_html)
            enlaces_crudos = extraer_enlaces(contenido_html)
            
            # Procesar enlaces
            enlaces_encontrados = []
            for enlace in enlaces_crudos:
                url_completa = normalizar_url(enlace, url_actual)
                if es_dominio_valido(url_completa, self.config.dominios_permitidos):
                    enlaces_encontrados.append(url_completa)
                    if url_completa not in self.visitados:
                        self.cola.append((url_completa, profundidad + 1))
            
            # Guardar resultado
            self.resultados.append({
                "url": url_actual,
                "titulo": titulo,
                "conteo_enlaces": len(enlaces_encontrados),
                "vista_previa": vista_previa
            })
            
            self.visitados.add(url_actual)
            paginas_rastreadas += 1
            self.logger.info(f"Se encontraron {len(enlaces_encontrados)} enlaces válidos.")

        self._guardar_resultados()
        self.logger.info(f"Rastreo finalizado. Visitadas {len(self.visitados)} páginas.")

    def _guardar_resultados(self):
        try:
            with open(self.config.archivo_salida, 'w', encoding='utf-8') as f:
                json.dump(self.resultados, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Resultados guardados en {self.config.archivo_salida}")
        except Exception as e:
            self.logger.error(f"Fallo al guardar resultados: {e}")
