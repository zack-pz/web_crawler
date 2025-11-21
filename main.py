import argparse
import os
from datetime import datetime
from urllib.parse import urlparse
from src.config import ConfiguracionRastreador
from src.crawler import RastreadorWeb

def main():
    parser = argparse.ArgumentParser(description="Rastreador Web Simple en Python")
    parser.add_argument("url", help="URL Inicial")
    parser.add_argument("--max-paginas", type=int, default=50, help="Máximo de páginas a rastrear")
    parser.add_argument("--max-profundidad", type=int, default=3, help="Profundidad máxima")
    parser.add_argument("--salida", default="resultados.json", help="Nombre base del archivo JSON de salida")
    
    argumentos = parser.parse_args()
    
    # Extraer dominio de la URL inicial para establecer el dominio permitido
    dominio = urlparse(argumentos.url).netloc
    dominios_permitidos = [dominio]

    # Configurar carpeta y nombre de archivo
    carpeta_salida = "salida"
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)
    
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    nombre_archivo = f"{fecha_actual}_{argumentos.salida}"
    ruta_completa = os.path.join(carpeta_salida, nombre_archivo)
    
    config = ConfiguracionRastreador(
        url_inicial=argumentos.url,
        dominios_permitidos=dominios_permitidos,
        max_paginas=argumentos.max_paginas,
        max_profundidad=argumentos.max_profundidad,
        archivo_salida=ruta_completa
    )
    
    rastreador = RastreadorWeb(config)
    rastreador.ejecutar()

if __name__ == "__main__":
    main()
