from movie_search import TMDBApiClient, BuscadorPeliculas, InterfazUsuario, ApiException

# Reemplaza con tu API key real
API_KEY = "APIKEY"

def ejemplo_basico():
    """Ejemplo básico de búsqueda de películas"""
    print("=== EJEMPLO BÁSICO ===")
    

    
    try:
        # Inicializar componentes
        api_client = TMDBApiClient(API_KEY)
        buscador = BuscadorPeliculas(api_client)
        
        # Buscar películas
        peliculas = buscador.buscar("Inception")
        
        print(f"Encontradas {len(peliculas)} películas:")
        for pelicula in peliculas[:3]:  # Mostrar solo las primeras 3
            print(f"- {pelicula}")
            
    except ApiException as e:
        print(f"Error de API: {e.mensaje}")
    except Exception as e:
        print(f"Error: {e}")

def ejemplo_interfaz_completa():
    """Ejemplo usando la interfaz completa"""
    print("\n=== EJEMPLO CON INTERFAZ ===")
    
    
    try:
        api_client = TMDBApiClient(API_KEY)
        buscador = BuscadorPeliculas(api_client)
        interfaz = InterfazUsuario(buscador)
        
        interfaz.ejecutar()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    ejemplo_basico()
    ejemplo_interfaz_completa()
