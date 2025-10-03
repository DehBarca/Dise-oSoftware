"""
EJERCICIO 1: Open/Closed Principle (OCP)
Refactorización del método buscar_libro() usando patrón Strategy

Alumno: Barraza Cárdenas Diego Alejandro
"""

from abc import ABC, abstractmethod
from datetime import datetime


# ========================== CLASES BASE (Sin modificar) ==========================
class Libro:
    def __init__(self, id, titulo, autor, isbn, disponible=True):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.disponible = disponible


class Prestamo:
    def __init__(self, id, libro_id, usuario, fecha):
        self.id = libro_id
        self.libro_id = libro_id
        self.usuario = usuario
        self.fecha = fecha
        self.devuelto = False


# ========================== 1. CLASE ABSTRACTA ==========================
class EstrategiaBusqueda(ABC):
    """Clase abstracta para estrategias de búsqueda"""

    @abstractmethod
    def buscar(self, libros, valor):
        """Método abstracto que cada estrategia debe implementar"""
        pass


# ========================== 2. ESTRATEGIAS CONCRETAS ==========================


class BusquedaPorTitulo(EstrategiaBusqueda):
    """Busca libros por título"""

    def buscar(self, libros, valor):
        resultados = []
        for libro in libros:
            if valor.lower() in libro.titulo.lower():
                resultados.append(libro)
        return resultados


class BusquedaPorAutor(EstrategiaBusqueda):
    """Busca libros por autor"""

    def buscar(self, libros, valor):
        resultados = []
        for libro in libros:
            if valor.lower() in libro.autor.lower():
                resultados.append(libro)
        return resultados


class BusquedaPorISBN(EstrategiaBusqueda):
    """Busca libros por ISBN"""

    def buscar(self, libros, valor):
        resultados = []
        for libro in libros:
            if libro.isbn == valor:
                resultados.append(libro)
        return resultados


class BusquedaPorDisponibilidad(EstrategiaBusqueda):
    """Busca libros por disponibilidad (NUEVA - agregada SIN modificar código existente)"""

    def buscar(self, libros, valor):
        disponible = valor.lower() == "true" if isinstance(valor, str) else bool(valor)
        resultados = []
        for libro in libros:
            if libro.disponible == disponible:
                resultados.append(libro)
        return resultados


# ========================== 3. SISTEMA REFACTORIZADO ==========================


class SistemaBibliotecaOCP:
    """Sistema refactorizado usando OCP"""

    def __init__(self):
        self.libros = []
        self.prestamos = []
        self.contador_libro = 1
        self.contador_prestamo = 1
        self.archivo = "biblioteca.txt"

        # Diccionario de estrategias - permite extensión sin modificación
        self.estrategias = {
            "titulo": BusquedaPorTitulo(),
            "autor": BusquedaPorAutor(),
            "isbn": BusquedaPorISBN(),
            "disponible": BusquedaPorDisponibilidad(),
        }

    # MÉTODO REFACTORIZADO: Ahora usa estrategias en lugar de if/elif
    def buscar_libro(self, criterio, valor):
        """
        Busca libros usando estrategias.
        CUMPLE OCP: Abierto a extensión (nuevas estrategias), cerrado a modificación.
        """
        estrategia = self.estrategias.get(criterio)
        if estrategia:
            return estrategia.buscar(self.libros, valor)
        return []

    def agregar_libro(self, titulo, autor, isbn):
        if not titulo or len(titulo) < 2:
            return "Error: Título inválido"
        if not autor or len(autor) < 3:
            return "Error: Autor inválido"
        if not isbn or len(isbn) < 10:
            return "Error: ISBN inválido"

        libro = Libro(self.contador_libro, titulo, autor, isbn)
        self.libros.append(libro)
        self.contador_libro += 1
        self._guardar_en_archivo()

        return f"Libro '{titulo}' agregado exitosamente"

    def realizar_prestamo(self, libro_id, usuario):
        if not usuario or len(usuario) < 3:
            return "Error: Nombre de usuario inválido"

        libro = None
        for l in self.libros:
            if l.id == libro_id:
                libro = l
                break

        if not libro:
            return "Error: Libro no encontrado"
        if not libro.disponible:
            return "Error: Libro no disponible"

        prestamo = Prestamo(
            self.contador_prestamo,
            libro_id,
            usuario,
            datetime.now().strftime("%Y-%m-%d"),
        )

        self.prestamos.append(prestamo)
        self.contador_prestamo += 1
        libro.disponible = False
        self._guardar_en_archivo()
        self._enviar_notificacion(usuario, libro.titulo)

        return f"Préstamo realizado a {usuario}"

    def devolver_libro(self, prestamo_id):
        prestamo = None
        for p in self.prestamos:
            if p.id == prestamo_id:
                prestamo = p
                break

        if not prestamo:
            return "Error: Préstamo no encontrado"
        if prestamo.devuelto:
            return "Error: Libro ya devuelto"

        for libro in self.libros:
            if libro.id == prestamo.libro_id:
                libro.disponible = True
                break

        prestamo.devuelto = True
        self._guardar_en_archivo()

        return "Libro devuelto exitosamente"

    def obtener_todos_libros(self):
        return self.libros

    def obtener_libros_disponibles(self):
        return [libro for libro in self.libros if libro.disponible]

    def obtener_prestamos_activos(self):
        return [p for p in self.prestamos if not p.devuelto]

    def _guardar_en_archivo(self):
        with open(self.archivo, "w") as f:
            f.write(f"Libros: {len(self.libros)}\n")
            f.write(f"Prestamos: {len(self.prestamos)}\n")

    def _enviar_notificacion(self, usuario, libro):
        print(f"[NOTIFICACIÓN] {usuario}: Préstamo de '{libro}'")


# ========================== DOCUMENTACIÓN Y PRUEBAS ==========================


def main():
    """
    DOCUMENTACIÓN: Cómo probar que funciona

    Demuestra:
    1. Las 4 estrategias funcionan correctamente
    2. Se puede agregar BusquedaPorDisponibilidad SIN modificar código
    3. El sistema mantiene la funcionalidad original
    """

    print("=" * 80)
    print("EJERCICIO 1: OCP - PATRÓN STRATEGY PARA BÚSQUEDAS")
    print("=" * 80)

    sistema = SistemaBibliotecaOCP()

    # Agregar libros
    print("\n📚 AGREGANDO LIBROS")
    print("-" * 80)
    print(
        sistema.agregar_libro(
            "Cien Años de Soledad", "Gabriel García Márquez", "9780060883287"
        )
    )
    print(
        sistema.agregar_libro(
            "El Principito", "Antoine de Saint-Exupéry", "9780156012195"
        )
    )
    print(sistema.agregar_libro("1984", "George Orwell", "9780451524935"))

    # PRUEBA 1: Búsqueda por Título
    print("\n🔍 PRUEBA 1: Búsqueda por Título")
    print("-" * 80)
    resultados = sistema.buscar_libro("titulo", "cien")
    print(f"Buscando 'cien': {len(resultados)} resultado(s)")
    for libro in resultados:
        print(f"  - {libro.titulo} por {libro.autor}")

    # PRUEBA 2: Búsqueda por Autor
    print("\n🔍 PRUEBA 2: Búsqueda por Autor")
    print("-" * 80)
    resultados = sistema.buscar_libro("autor", "garcia")
    print(f"Buscando autor 'garcia': {len(resultados)} resultado(s)")
    for libro in resultados:
        print(f"  - {libro.titulo} por {libro.autor}")

    # PRUEBA 3: Búsqueda por ISBN
    print("\n🔍 PRUEBA 3: Búsqueda por ISBN")
    print("-" * 80)
    resultados = sistema.buscar_libro("isbn", "9780156012195")
    print(f"Buscando ISBN '9780156012195': {len(resultados)} resultado(s)")
    for libro in resultados:
        print(f"  - {libro.titulo} (ISBN: {libro.isbn})")

    # Realizar préstamo
    print("\n📋 REALIZANDO PRÉSTAMO")
    print("-" * 80)
    print(sistema.realizar_prestamo(1, "Juan Pérez"))

    # PRUEBA 4: Búsqueda por Disponibilidad (NUEVA ESTRATEGIA)
    print("\n🔍 PRUEBA 4: Búsqueda por Disponibilidad (NUEVA - Sin modificar código)")
    print("-" * 80)
    print("Buscando libros disponibles:")
    resultados = sistema.buscar_libro("disponible", "true")
    print(f"Libros disponibles: {len(resultados)}")
    for libro in resultados:
        print(f"  - {libro.titulo}")

    print("\nBuscando libros prestados:")
    resultados = sistema.buscar_libro("disponible", "false")
    print(f"Libros prestados: {len(resultados)}")
    for libro in resultados:
        print(f"  - {libro.titulo}")

    print("\n")


if __name__ == "__main__":
    main()
