"""
Módulo para búsqueda de películas usando The Movie Database (TMDB) API
Autor: Arquitecto de Software
Fecha: Septiembre 2025
"""

import requests
from typing import List, Dict, Optional
from dataclasses import dataclass
import os
from urllib.parse import urlencode


@dataclass
class Pelicula:
    """Representa una película obtenida de TMDB"""
    id: int
    titulo: str
    año: Optional[int]
    sinopsis: str
    poster_url: Optional[str]
    calificacion: float
    
    def __str__(self) -> str:
        return f"{self.titulo} ({self.año}) - ⭐ {self.calificacion}/10"


class ApiException(Exception):
    """Excepción personalizada para errores de la API"""
    def __init__(self, mensaje: str, codigo_error: int = None):
        self.mensaje = mensaje
        self.codigo_error = codigo_error
        super().__init__(self.mensaje)


class TMDBApiClient:
    """Cliente para interactuar con The Movie Database API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.themoviedb.org/3"
        self.image_base_url = "https://image.tmdb.org/t/p/w500"
        
    def search_movie(self, query: str) -> Dict:
        """
        Busca películas por título en TMDB
        
        Args:
            query: Título de la película a buscar
            
        Returns:
            Dict con los resultados de la búsqueda
            
        Raises:
            ApiException: Si hay errores en la petición
        """
        endpoint = "/search/movie"
        params = {
            "api_key": self.api_key,
            "query": query,
            "language": "es-ES",
            "include_adult": False
        }
        
        return self._hacer_peticion(endpoint, params)
    
    def _hacer_peticion(self, endpoint: str, params: Dict) -> Dict:
        """Realiza la petición HTTP a la API"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.Timeout:
            raise ApiException("Timeout al conectar con TMDB API", 408)
        except requests.exceptions.ConnectionError:
            raise ApiException("Error de conexión con TMDB API", 503)
        except requests.exceptions.HTTPError as e:
            raise ApiException(f"Error HTTP: {e.response.status_code}", e.response.status_code)
        except requests.exceptions.RequestException as e:
            raise ApiException(f"Error en la petición: {str(e)}")


class BuscadorPeliculas:
    """Servicio principal para búsqueda de películas"""
    
    def __init__(self, api_client: TMDBApiClient):
        self.api_client = api_client
    
    def buscar(self, titulo: str) -> List[Pelicula]:
        """
        Busca películas por título
        
        Args:
            titulo: Título de la película a buscar
            
        Returns:
            Lista de objetos Pelicula encontrados
            
        Raises:
            ValueError: Si el título no es válido
            ApiException: Si hay errores en la API
        """
        if not self._validar_titulo(titulo):
            raise ValueError("El título debe tener al menos 2 caracteres")
        
        try:
            response = self.api_client.search_movie(titulo)
            return self._convertir_a_peliculas(response.get("results", []))
            
        except ApiException:
            raise  # Re-lanza la excepción de la API
        except Exception as e:
            raise ApiException(f"Error inesperado: {str(e)}")
    
    def _validar_titulo(self, titulo: str) -> bool:
        """Valida que el título sea correcto"""
        return isinstance(titulo, str) and len(titulo.strip()) >= 2
    
    def _convertir_a_peliculas(self, resultados: List[Dict]) -> List[Pelicula]:
        """Convierte los resultados de la API en objetos Pelicula"""
        peliculas = []
        
        for item in resultados:
            # Extraer año de la fecha de lanzamiento
            año = None
            if item.get("release_date"):
                try:
                    año = int(item["release_date"][:4])
                except (ValueError, IndexError):
                    año = None
            
            # Construir URL del poster
            poster_url = None
            if item.get("poster_path"):
                poster_url = f"{self.api_client.image_base_url}{item['poster_path']}"
            
            pelicula = Pelicula(
                id=item.get("id", 0),
                titulo=item.get("title", "Sin título"),
                año=año,
                sinopsis=item.get("overview", "Sin sinopsis disponible"),
                poster_url=poster_url,
                calificacion=round(item.get("vote_average", 0.0), 1)
            )
            peliculas.append(pelicula)
        
        return peliculas


class InterfazUsuario:
    """Interfaz de usuario para el sistema de búsqueda"""
    
    def __init__(self, buscador: BuscadorPeliculas):
        self.buscador = buscador
    
    def ejecutar(self):
        """Método principal que ejecuta la interfaz"""
        self.mostrar_menu()
        
        while True:
            try:
                titulo = self.capturar_titulo()
                if titulo.lower() in ['salir', 'exit', 'quit']:
                    print("¡Hasta luego! 👋")
                    break
                
                print(f"\n🔍 Buscando películas con '{titulo}'...")
                peliculas = self.buscador.buscar(titulo)
                self.mostrar_resultados(peliculas)
                
            except ValueError as e:
                self.mostrar_error(f"Error de validación: {e}")
            except ApiException as e:
                self.mostrar_error(f"Error de API: {e.mensaje}")
            except KeyboardInterrupt:
                print("\n\n¡Hasta luego! 👋")
                break
            except Exception as e:
                self.mostrar_error(f"Error inesperado: {e}")
    
    def mostrar_menu(self):
        """Muestra el menú principal"""
        print("=" * 50)
        print("🎬 BUSCADOR DE PELÍCULAS - TMDB")
        print("=" * 50)
        print("Escribe el título de una película para buscarla")
        print("Escribe 'salir' para terminar")
        print("-" * 50)
    
    def capturar_titulo(self) -> str:
        """Captura el título ingresado por el usuario"""
        return input("\n📝 Título de la película: ").strip()
    
    def mostrar_resultados(self, peliculas: List[Pelicula]):
        """Muestra los resultados de la búsqueda"""
        if not peliculas:
            print("❌ No se encontraron películas con ese título")
            return
        
        print(f"\n✅ Encontradas {len(peliculas)} película(s):")
        print("-" * 50)
        
        for i, pelicula in enumerate(peliculas[:10], 1):  # Limitar a 10 resultados
            print(f"{i:2d}. {pelicula}")
            if pelicula.sinopsis and len(pelicula.sinopsis) > 100:
                print(f"    📖 {pelicula.sinopsis[:100]}...")
            elif pelicula.sinopsis:
                print(f"    📖 {pelicula.sinopsis}")
            print()
    
    def mostrar_error(self, mensaje: str):
        """Muestra mensajes de error"""
        print(f"\n❌ {mensaje}")


def main():
    """Función principal del programa"""
    # Obtener API key de variable de entorno o solicitar al usuario
    api_key = os.getenv("TMDB_API_KEY")
    
    if not api_key:
        print("⚠️  No se encontró TMDB_API_KEY en las variables de entorno")
        api_key = input("Por favor, ingresa tu API key de TMDB: ").strip()
        
        if not api_key:
            print("❌ API key requerida para usar el servicio")
            return
    
    try:
        # Inicializar componentes
        api_client = TMDBApiClient(api_key)
        buscador = BuscadorPeliculas(api_client)
        interfaz = InterfazUsuario(buscador)
        
        # Ejecutar aplicación
        interfaz.ejecutar()
        
    except Exception as e:
        print(f"❌ Error al inicializar la aplicación: {e}")


if __name__ == "__main__":
    main()
