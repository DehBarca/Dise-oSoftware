"""
EJERCICIO 2: Single Responsibility Principle (SRP)
Sistema de Biblioteca - Refactorización separando responsabilidades
"""

from datetime import datetime


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


class ValidadorBiblioteca:
    """Responsabilidad: Validar datos de entrada"""

    @staticmethod
    def validar_titulo(titulo):
        if not titulo or len(titulo) < 2:
            return False, "Error: Título inválido"
        return True, ""

    @staticmethod
    def validar_autor(autor):
        if not autor or len(autor) < 3:
            return False, "Error: Autor inválido"
        return True, ""

    @staticmethod
    def validar_isbn(isbn):
        if not isbn or len(isbn) < 10:
            return False, "Error: ISBN inválido"
        return True, ""

    @staticmethod
    def validar_usuario(usuario):
        if not usuario or len(usuario) < 3:
            return False, "Error: Nombre de usuario inválido"
        return True, ""

    @staticmethod
    def validar_libro_completo(titulo, autor, isbn):
        valido, mensaje = ValidadorBiblioteca.validar_titulo(titulo)
        if not valido:
            return False, mensaje

        valido, mensaje = ValidadorBiblioteca.validar_autor(autor)
        if not valido:
            return False, mensaje

        valido, mensaje = ValidadorBiblioteca.validar_isbn(isbn)
        if not valido:
            return False, mensaje

        return True, "Validación exitosa"


class RepositorioBiblioteca:
    """Responsabilidad: Persistencia de datos"""

    def __init__(self, archivo="biblioteca_srp.txt"):
        self.archivo = archivo

    def guardar(self, libros, prestamos):
        try:
            with open(self.archivo, "w", encoding="utf-8") as f:
                f.write(f"Libros: {len(libros)}\n")
                f.write(f"Préstamos: {len(prestamos)}\n")
                f.write("\n=== LIBROS ===\n")
                for libro in libros:
                    f.write(
                        f"ID: {libro.id}, Título: {libro.titulo}, "
                        f"Autor: {libro.autor}, ISBN: {libro.isbn}, "
                        f"Disponible: {libro.disponible}\n"
                    )

                f.write("\n=== PRÉSTAMOS ===\n")
                for prestamo in prestamos:
                    f.write(
                        f"ID: {prestamo.id}, Libro ID: {prestamo.libro_id}, "
                        f"Usuario: {prestamo.usuario}, Fecha: {prestamo.fecha}, "
                        f"Devuelto: {prestamo.devuelto}\n"
                    )
            return True
        except Exception as e:
            print(f"Error al guardar: {e}")
            return False

    def cargar(self):
        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                data = f.read()
            return True, data
        except FileNotFoundError:
            return False, "Archivo no encontrado"
        except Exception as e:
            return False, f"Error al cargar: {e}"


class ServicioNotificaciones:
    """Responsabilidad: Enviar notificaciones"""

    @staticmethod
    def enviar_notificacion_prestamo(usuario, libro_titulo):
        print(f"[NOTIFICACIÓN] {usuario}: Préstamo de '{libro_titulo}'")

    @staticmethod
    def enviar_notificacion_devolucion(usuario, libro_titulo):
        print(f"[NOTIFICACIÓN] {usuario}: Devolución de '{libro_titulo}'")

    @staticmethod
    def enviar_notificacion_nuevo_libro(titulo):
        print(f"[NOTIFICACIÓN] Nuevo libro agregado: '{titulo}'")


class SistemaBiblioteca:
    """Responsabilidad: Lógica de negocio de la biblioteca"""

    def __init__(self, validador, repositorio, notificador):
        self.libros = []
        self.prestamos = []
        self.contador_libro = 1
        self.contador_prestamo = 1
        self.validador = validador
        self.repositorio = repositorio
        self.notificador = notificador

    def agregar_libro(self, titulo, autor, isbn):
        valido, mensaje = self.validador.validar_libro_completo(titulo, autor, isbn)
        if not valido:
            return mensaje

        libro = Libro(self.contador_libro, titulo, autor, isbn)
        self.libros.append(libro)
        self.contador_libro += 1

        self.repositorio.guardar(self.libros, self.prestamos)
        self.notificador.enviar_notificacion_nuevo_libro(titulo)

        return f"Libro '{titulo}' agregado exitosamente"

    def buscar_libro(self, criterio, valor):
        resultados = []

        if criterio == "titulo":
            for libro in self.libros:
                if valor.lower() in libro.titulo.lower():
                    resultados.append(libro)

        elif criterio == "autor":
            for libro in self.libros:
                if valor.lower() in libro.autor.lower():
                    resultados.append(libro)

        elif criterio == "isbn":
            for libro in self.libros:
                if libro.isbn == valor:
                    resultados.append(libro)

        elif criterio == "disponible":
            disponible = valor.lower() == "true"
            for libro in self.libros:
                if libro.disponible == disponible:
                    resultados.append(libro)

        return resultados

    def realizar_prestamo(self, libro_id, usuario):
        valido, mensaje = self.validador.validar_usuario(usuario)
        if not valido:
            return mensaje

        libro = None
        for lib in self.libros:
            if lib.id == libro_id:
                libro = lib
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

        self.repositorio.guardar(self.libros, self.prestamos)
        self.notificador.enviar_notificacion_prestamo(usuario, libro.titulo)

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
        self.repositorio.guardar(self.libros, self.prestamos)

        return "Libro devuelto exitosamente"

    def obtener_todos_libros(self):
        return self.libros

    def obtener_libros_disponibles(self):
        return [libro for libro in self.libros if libro.disponible]

    def obtener_prestamos_activos(self):
        return [p for p in self.prestamos if not p.devuelto]


def main():
    print("=" * 60)
    print("EJERCICIO 2: Single Responsibility Principle (SRP)")
    print("=" * 60)

    validador = ValidadorBiblioteca()
    repositorio = RepositorioBiblioteca("biblioteca_srp.txt")
    notificador = ServicioNotificaciones()
    sistema = SistemaBiblioteca(validador, repositorio, notificador)

    print("\n=== AGREGANDO LIBROS ===")
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

    print("\n=== BÚSQUEDA POR AUTOR ===")
    resultados = sistema.buscar_libro("autor", "Garcia")
    for libro in resultados:
        print(f"- {libro.titulo} por {libro.autor}")

    print("\n=== REALIZAR PRÉSTAMO ===")
    print(sistema.realizar_prestamo(1, "Juan Pérez"))

    print("\n=== LIBROS DISPONIBLES ===")
    disponibles = sistema.obtener_libros_disponibles()
    for libro in disponibles:
        print(f"- {libro.titulo}")

    print("\n=== DEVOLVER LIBRO ===")
    print(sistema.devolver_libro(1))

    print("\n=== PRÉSTAMOS ACTIVOS ===")
    activos = sistema.obtener_prestamos_activos()
    print(f"Total de préstamos activos: {len(activos)}")

    print("\n")


if __name__ == "__main__":
    main()
