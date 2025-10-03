# Documentación de Ejercicios SOLID

## Ejercicio 1: Open/Closed Principle (OCP)

### Archivo: `templates/ejercicio1_ocp.py`

### ✅ Componentes Creados

1. **EstrategiaBusqueda (Clase Abstracta)** - Patrón Strategy
   - Define el contrato para todas las estrategias de búsqueda
   - Método abstracto: `buscar(libros, valor)`

2. **Estrategias Concretas de Búsqueda**
   - `BusquedaPorTitulo`: Busca libros por título
   - `BusquedaPorAutor`: Busca libros por autor
   - `BusquedaPorISBN`: Busca libros por ISBN
   - `BusquedaPorDisponibilidad`: Busca por disponibilidad (NUEVA - agregada sin modificar código)

3. **SistemaBibliotecaOCP** - Sistema refactorizado
   - Usa diccionario de estrategias en lugar de if/elif
   - Método `buscar_libro()` refactorizado con OCP

### 🧪 Cómo Probar

```bash
python templates/ejercicio1_ocp.py
```

### 📊 Salida Esperada

- **Prueba 1**: Búsqueda por título ("cien")
- **Prueba 2**: Búsqueda por autor ("garcia")
- **Prueba 3**: Búsqueda por ISBN específico
- **Prueba 4**: Búsqueda por disponibilidad (nueva estrategia agregada sin modificar código)

### ✅ Verificación

- ✅ Las 4 estrategias funcionan correctamente
- ✅ `BusquedaPorDisponibilidad` fue agregada SIN modificar el código existente
- ✅ El método `buscar_libro()` no tiene if/elif (usa estrategias)
- ✅ Cumple OCP: Abierto a extensión, cerrado a modificación

### 💡 Beneficio del OCP

**Antes (con if/elif):**
- Para agregar un nuevo criterio de búsqueda, había que modificar el método `buscar_libro()`
- Violaba OCP (cerrado a modificación)

**Después (con Strategy):**
- Para agregar un nuevo criterio, solo se crea una nueva clase estrategia
- No se modifica código existente
- Cumple OCP perfectamente

---

## Ejercicio 2: Single Responsibility Principle (SRP)

### Archivo: `ejercicio2_srp.py`

### ✅ Clases Creadas

1. **ValidadorBiblioteca** - Responsabilidad: Validación de datos
   - `validar_titulo()`: Valida títulos de libros
   - `validar_autor()`: Valida nombres de autores
   - `validar_isbn()`: Valida códigos ISBN
   - `validar_usuario()`: Valida nombres de usuarios
   - `validar_libro_completo()`: Valida todos los campos de un libro

2. **RepositorioBiblioteca** - Responsabilidad: Persistencia de datos
   - `guardar()`: Guarda libros y préstamos en archivo
   - `cargar()`: Carga datos desde archivo

3. **ServicioNotificaciones** - Responsabilidad: Notificaciones
   - `enviar_notificacion_prestamo()`: Notifica préstamos
   - `enviar_notificacion_devolucion()`: Notifica devoluciones
   - `enviar_notificacion_nuevo_libro()`: Notifica nuevos libros

4. **SistemaBiblioteca** - Responsabilidad: Lógica de negocio
   - Usa las 3 clases anteriores mediante inyección de dependencias

### 🧪 Cómo Probar

```bash
python ejercicio2_srp.py
```

### 📊 Salida Esperada

- Mensajes de libros agregados con notificaciones
- Búsqueda de libros por autor
- Realización de préstamo con notificación
- Lista de libros disponibles
- Devolución de libro
- Resumen de SRP aplicado

### ✅ Verificación

El archivo `biblioteca_srp.txt` debe crearse con la información de libros y préstamos.

---

## Ejercicio 3: Dependency Inversion Principle (DIP)

### Archivo: `ejercicio3_dip.py`

### ✅ Componentes Creados

1. **IRepositorio (Interfaz Abstracta)** - Abstracción
   - Define el contrato para repositorios
   - Métodos abstractos: `guardar()`, `cargar()`

2. **RepositorioArchivo** - Implementación concreta
   - Guarda datos en archivo de texto
   - Implementa la interfaz `IRepositorio`

3. **RepositorioMemoria (BONUS)** - Implementación concreta
   - Guarda datos en memoria (diccionario)
   - Implementa la interfaz `IRepositorio`

4. **SistemaBiblioteca** - Depende de abstracción
   - Recibe `IRepositorio` en el constructor
   - No depende de implementación concreta

### 🧪 Cómo Probar

```bash
python ejercicio3_dip.py
```

### 📊 Salida Esperada

**Parte 1: Con RepositorioArchivo**
- Mensajes indicando guardado en archivo
- Operaciones normales de biblioteca

**Parte 2: Con RepositorioMemoria (BONUS)**
- Cambio de implementación sin modificar código
- Mensajes indicando guardado en memoria
- Demostración de flexibilidad del DIP

### ✅ Verificación

- El archivo `biblioteca_dip.txt` debe crearse
- El programa debe cambiar entre implementaciones fácilmente
- No hay referencias a implementaciones concretas en `SistemaBiblioteca`

---

## 🎯 Beneficios Demostrados

### OCP (Ejercicio 1)
- ✅ Sistema abierto a extensión (nuevas estrategias)
- ✅ Sistema cerrado a modificación (no cambiar código existente)
- ✅ Patrón Strategy permite agregar criterios de búsqueda fácilmente
- ✅ Código más mantenible y escalable

### SRP (Ejercicio 2)
- ✅ Cada clase tiene una única responsabilidad
- ✅ Fácil mantenimiento: cambiar validación no afecta persistencia
- ✅ Código más legible y organizado
- ✅ Reutilización de componentes

### DIP (Ejercicio 3)
- ✅ Sistema depende de abstracciones
- ✅ Fácil cambio de implementaciones
- ✅ Facilita testing (se pueden crear mocks)
- ✅ Bajo acoplamiento entre componentes

---

## 📝 Notas Importantes

1. El código original (`biblioteca_examen.py`) NO fue modificado
2. La funcionalidad original se mantiene intacta
3. Se eliminaron comentarios excesivos para mayor claridad
4. Los 3 ejercicios ejecutan correctamente

---

## 📋 Resumen de Archivos Entregados

### Ejercicio 1 (OCP)
- 📄 `templates/ejercicio1_ocp.py` - Sistema con patrón Strategy
- ✅ 1 clase abstracta + 4 estrategias concretas
- ✅ Método refactorizado sin if/elif

### Ejercicio 2 (SRP)
- 📄 `ejercicio2_srp.py` - Sistema con responsabilidades separadas
- ✅ 4 clases independientes (Validador, Repositorio, Notificaciones, Sistema)
- ✅ Archivo de persistencia: `biblioteca_srp.txt`

### Ejercicio 3 (DIP)
- 📄 `ejercicio3_dip.py` - Sistema con inyección de dependencias
- ✅ 1 interfaz abstracta + 2 implementaciones concretas (Archivo y Memoria)
- ✅ Archivo de persistencia: `biblioteca_dip.txt`

---

## 🚀 Comandos de Prueba Rápida

```bash
# Ejercicio 1 - OCP
cd templates
python ejercicio1_ocp.py

# Ejercicio 2 - SRP
python ejercicio2_srp.py

# Ejercicio 3 - DIP
python ejercicio3_dip.py
```

---

## 👤 Alumno

**Nombre:** Barraza Cárdenas Diego Alejandro
