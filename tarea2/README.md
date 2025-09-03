# Sistema de Búsqueda de Películas - TMDB

Sistema desarrollado en Python que permite buscar películas utilizando la API de The Movie Database (TMDB).

## Reflexión de Aprendizaje
Esta actividad me ayudo para prácticar mi forma de visualizar el código antes de empezar a programar haciendo diagramas así como poder empezar a visualizar el como va a ir las llamadas paso a paso para poder llegar al resultado esperado, también práctique el como hacer los diagramas con la herramienta PlantUML aunque tuve que investigar para poder hacerlo bien.

## Entregables

### 1. Código Principal
- **`movie_search.py`**: Módulo principal con todas las clases del sistema
- **`ejemplo_uso.py`**: Ejemplos de cómo usar el módulo

### 2. Diagramas UML
- **`diagrama.puml`**: Contiene diagrama de clases y diagrama de secuencia

### 3. Documentación
- **`reflexion_aprendizaje.md`**: Análisis del diseño y aprendizajes obtenidos

## Requisitos

### Dependencias
```bash
pip install requests
```

### API Key de TMDB
1. Regístrate en [The Movie Database](https://www.themoviedb.org/)
2. Obtén tu API key en [API Settings](https://www.themoviedb.org/settings/api)
3. Configura la variable de entorno:
   ```bash
   # Windows
   set TMDB_API_KEY=tu_api_key_aqui
   
   # Linux/Mac
   export TMDB_API_KEY=tu_api_key_aqui
   ```

## Ejecución

### Opción 1: Interfaz Interactiva
```bash
python movie_search.py
```

### Opción 2: Uso Programático
```python
from movie_search import TMDBApiClient, BuscadorPeliculas

api_client = TMDBApiClient("tu_api_key")
buscador = BuscadorPeliculas(api_client)
peliculas = buscador.buscar("Inception")
```

### Opción 3: Ejecutar Ejemplos
```bash
python ejemplo_uso.py
```

## Visualizar Diagramas UML

### Con VS Code (Recomendado)
1. Instala la extensión "PlantUML"
2. Abre `diagrama.puml`
3. Presiona `Alt+D` para ver el diagrama

### Con PlantUML Local
```bash
java -jar plantuml.jar diagrama.puml
```

## Arquitectura

El sistema sigue una arquitectura en capas:

```
Usuario → InterfazUsuario → BuscadorPeliculas → TMDBApiClient → TMDB API
```

### Componentes Principales

- **TMDBApiClient**: Cliente HTTP para la API de TMDB
- **BuscadorPeliculas**: Lógica de negocio y validaciones
- **InterfazUsuario**: Interfaz de línea de comandos
- **Pelicula**: Modelo de datos para películas

## Funcionalidades

- ✅ Búsqueda de películas por título
- ✅ Validación de entrada
- ✅ Manejo robusto de errores
- ✅ Interfaz amigable
- ✅ Soporte para caracteres especiales
- ✅ Limitación de resultados mostrados
- ✅ Información detallada de películas

## Ejemplo de Uso

```
🎬 BUSCADOR DE PELÍCULAS - TMDB
==================================================

📝 Título de la película: Inception

🔍 Buscando películas con 'Inception'...

✅ Encontradas 3 película(s):
--------------------------------------------------
 1. Inception (2010) - ⭐ 8.4/10
    📖 Dom Cobb es un ladrón hábil, el mejor en el peligroso arte de la extracción...

 2. The Inception of Lies (2014) - ⭐ 6.2/10
    📖 Una historia sobre secretos y mentiras...
```

## Estructura del Proyecto

```
tarea2/
├── movie_search.py           # Módulo principal
├── ejemplo_uso.py           # Ejemplos de uso
├── diagrama.puml           # Diagramas UML
├── reflexion_aprendizaje.md # Análisis del diseño
└── README.md               # Este archivo
```

## Links de Referencia

- [TMDB API Documentation](https://developer.themoviedb.org/docs)
- [Search Movie Endpoint](https://developer.themoviedb.org/reference/search-movie)
- [PlantUML Documentation](https://plantuml.com/)
