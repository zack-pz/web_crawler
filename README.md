# Rastreador Web en Python

Un rastreador web (web crawler) "completo pero rápido de construir" escrito en Python. Diseñado para ser funcional, robusto y fácil de entender, con todo el código y comentarios en español.

## Características

*   **Control de URLs**: Evita ciclos y valida dominios para no salir del sitio objetivo.
*   **Respeto a Robots.txt**: Lee y respeta las reglas `Disallow` del sitio.
*   **Rate Limiting**: Incluye demoras aleatorias entre peticiones para no saturar el servidor.
*   **Límites Configurables**: Permite definir máximo de páginas y profundidad de navegación.
*   **Salida Organizada**: Guarda los resultados en archivos JSON dentro de la carpeta `salida/`, con la fecha actual en el nombre.
*   **Sin Frameworks Pesados**: Construido con `requests` y `beautifulsoup4`.

## Instalación

Sigue estos pasos para configurar el proyecto en tu entorno local.

### 1. Clonar el repositorio
(Si ya tienes el código descargado, salta este paso)

**Con HTTPS:**
```bash
git clone https://github.com/zack-pz/web_crawler.git
```

**Con SSH:**
```bash
git clone git@github.com:zack-pz/web_crawler.git
```

### 2. Crear un Entorno Virtual (.venv)
Es recomendable usar un entorno virtual para aislar las dependencias del proyecto.

**En Windows:**
```bash
python -m venv .venv
```

**En macOS/Linux:**
```bash
python3 -m venv .venv
```

### 3. Activar el Entorno Virtual

**En Windows:**
```bash
.venv\Scripts\activate
```

**En macOS/Linux:**
```bash
source .venv/bin/activate
```

### 4. Instalar Dependencias
Una vez activado el entorno, instala las librerías necesarias:

```bash
pip install -r requirements.txt
```

## Uso

El script principal es `main.py`. Puedes ejecutarlo desde la terminal pasando la URL inicial.

### Ejecución Básica
```bash
python main.py https://books.toscrape.com
```

### Opciones Avanzadas
Puedes configurar el límite de páginas, la profundidad y el nombre base del archivo de salida.

```bash
python main.py https://books.toscrape.com --max-paginas 10 --max-profundidad 2 --salida mis_libros.json
```

**Argumentos Disponibles:**
*   `url`: (Obligatorio) La URL desde donde comenzar el rastreo.
*   `--max-paginas`: (Opcional) Número máximo de páginas a visitar (por defecto: 50).
*   `--max-profundidad`: (Opcional) Profundidad máxima de navegación desde la URL inicial (por defecto: 3).
*   `--salida`: (Opcional) Nombre base del archivo JSON (por defecto: `resultados.json`).

## Salida

Los resultados se guardarán automáticamente en la carpeta `salida/`.
El nombre del archivo tendrá el formato: `YYYY-MM-DD_[nombre_base]`.

**Ejemplo:** `salida/2025-11-21_resultados.json`

## Estructura del Proyecto

```
webcrawler/
├── main.py             # Punto de entrada del programa
├── requirements.txt    # Dependencias del proyecto
├── salida/             # Carpeta donde se guardan los resultados
├── src/
│   ├── config.py       # Clases de configuración
│   ├── crawler.py      # Lógica principal del rastreador
│   ├── network.py      # Manejo de red y robots.txt
│   ├── parser.py       # Extracción de datos con BeautifulSoup
│   └── utils.py        # Utilidades (logging, normalización de URLs)
└── .gitignore
```
