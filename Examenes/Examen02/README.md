# Examen 02 - Patrones de Diseño y Arquitectura C4

## 📁 Estructura del Proyecto

```text
Examen02/
├── Code/
│   ├── ejercicio1_tienda_online.py
│   └── ejercicio2_gestor_documentos.py
├── Diagrams/
│   ├── ejercicio01/
│   │   ├── c4_context.puml
│   │   ├── c4_container.puml
│   │   └── c4_component.puml
│   └── ejercicio02/
│       ├── c4_context.puml
│       ├── c4_container.puml
│       ├── c4_component.puml
│       └── README_C4_LAYERS.md
└── README.md                            
```

---

## 🎯 Ejercicio 1: Sistema de Notificaciones de Pedidos

**Archivo:** `Code/ejercicio1_tienda_online.py`  

### Descripción

Sistema de notificaciones multicanal para pedidos de una tienda online que soporta Email, SMS y Push Notifications.

### Principios SOLID Aplicados

- **S (Single Responsibility):** Cada clase tiene una única responsabilidad
  - `EmailNotifier`, `SMSNotifier`, `PushNotifier` - Solo envían notificaciones
  - `NotificationLogger` - Solo registra historial
  - `OrderBuilder` - Solo construye pedidos

- **O (Open/Closed):** Extensible sin modificar código existente
  - Nuevos notificadores se agregan implementando `INotifier`
  - Factory permite registrar nuevos tipos dinámicamente

- **D (Dependency Inversion):** Depende de abstracciones
  - `OrderNotificationSystem` depende de `INotifier` (interfaz)
  - Usa Dependency Injection para factories y loggers

### Patrones de Diseño Implementados

#### Patrones Creacionales (3)

1. **Factory Method** (`NotificationFactory`)
   - Crea notificadores según el tipo solicitado
   - Permite registrar nuevos notificadores dinámicamente

2. **Singleton** (`NotificationConfig`)
   - Una única instancia de configuración global
   - Garantiza consistencia en toda la aplicación

3. **Builder** (`OrderBuilder`)
   - Construcción fluida de pedidos complejos
   - Permite crear pedidos paso a paso con validación

#### Patrones Estructurales (2)

4. **Decorator** (`RetryDecorator`, `LoggingDecorator`)
   - Añade funcionalidad de reintentos
   - Añade logging sin modificar notificadores base

5. **Composite** (`CompositeNotifier`)
   - Agrupa múltiples notificadores
   - Envía notificaciones a todos los canales simultáneamente

#### Patrones de Comportamiento (2)

6. **Observer** (`AnalyticsObserver`, `AuditObserver`)
   - Observadores reaccionan a notificaciones enviadas
   - Analytics cuenta notificaciones, Audit registra auditoría

7. **Chain of Responsibility** (`OrderIdValidator`, `CustomerValidator`, `TotalValidator`)
   - Cadena de validadores para pedidos
   - Cada validador verifica un aspecto específico

---

## 📊 Ejercicio 2: Sistema de Generación de Reportes

**Archivo:** `Code/ejercicio2_gestor_documentos.py`  

### Descripción

Sistema completo de generación, formateo y entrega de reportes empresariales con soporte para múltiples tipos de reportes, formatos de salida y métodos de entrega.

### Principios SOLID Aplicados

- **S (Single Responsibility):** Separación clara de responsabilidades
  - `SalesReportGenerator`, `InventoryReportGenerator`, `FinancialReportGenerator` - Generan reportes
  - `PDFFormatter`, `ExcelFormatter`, `HTMLFormatter` - Formatean contenido
  - `EmailDelivery`, `DownloadDelivery`, `CloudDelivery` - Entregan reportes

- **O (Open/Closed):** Extensible sin modificaciones
  - Tres factories permiten agregar nuevos tipos sin modificar código existente
  - Fácil agregar nuevos formatos o métodos de entrega

- **L (Liskov Substitution):** Todas las implementaciones son intercambiables
  - Cualquier `IReportGenerator` puede usarse indistintamente
  - Cualquier `IReportFormatter` funciona con cualquier generador

- **D (Dependency Inversion):** Inyección de dependencias
  - `ReportSystem` depende de abstracciones, no de implementaciones concretas
  - Usa factories inyectadas para crear componentes

### Patrones de Diseño Implementados

#### Patrones Creacionales (3)

1. **Factory Method** (3 factories: `ReportGeneratorFactory`, `ReportFormatterFactory`, `DeliveryMethodFactory`)
   - Separa la lógica de creación del uso
   - Cada factory gestiona un tipo de componente

2. **Builder** (`ReportBuilder`)
   - Construcción fluida de reportes personalizados
   - Permite agregar secciones, metadata y footers

3. **Prototype** (`Report.clone()`)
   - Clonación profunda de reportes
   - Útil para crear variaciones de reportes base

#### Patrones Estructurales (2)

4. **Adapter** (`DataSourceAdapter`)
   - Adapta datos de sistemas legacy al formato estándar
   - Convierte estructuras incompatibles

5. **Facade** (`ReportGenerationFacade`)
   - Simplifica la interfaz del sistema complejo
   - Métodos de generación rápida preconfigurада

#### Patrones de Comportamiento (2)

6. **Template Method** (`ReportTemplate`, `DailySalesReport`)
   - Define el esqueleto del algoritmo de generación
   - Subclases implementan pasos específicos

7. **Strategy** (`DetailedStrategy`, `SummaryStrategy`, `ReportContext`)
   - Cambia el algoritmo de procesamiento en tiempo de ejecución
   - Permite generar reportes detallados o resumidos

---

## 🏗️ Diagramas C4

### Niveles del Modelo C4

#### C1 - Context (Contexto del Sistema)

- **Ejercicio 1:** Cliente → Sistema de Notificaciones → Servicios Externos
- **Ejercicio 2:** Analista → Sistema de Reportes → Fuentes de Datos

#### C2 - Container (Contenedores)

- **Ejercicio 1:** Procesador de Pedidos, Gestor de Notificaciones, Base de Datos
- **Ejercicio 2:** Web App, Generador de Reportes, Motor de Formateo, Gestor de Entrega

#### C3 - Component (Componentes)

- **Ejercicio 1:** Factory, Notificadores, Decorators, Validators
- **Ejercicio 2:** Factories, Generators, Formatters, Delivery Methods

#### C4 - Code (Código)

- Estructura de clases e interfaces

### Visualización de Diagramas

Los diagramas están en formato PlantUML (`.puml`). Para visualizarlos:

1. **VS Code:** Instalar extensión "PlantUML"
2. **Online:** [PlantUML Web Server](http://www.plantuml.com/plantuml/)
3. **Local:** Instalar PlantUML CLI

---

## 🚀 Ejecución

### Ejercicio 1

```bash
python Code/ejercicio1_tienda_online.py
```

**Salida esperada:**

- Demostración de Singleton (misma instancia)
- Construcción de pedido con Builder
- Notificaciones con Decorator (reintentos y logging)
- Notificación a grupo Composite (Email + SMS + Push)
- Validación con Chain of Responsibility
- Estadísticas de Analytics Observer
- Log de auditoría completo

### Ejercicio 2

```bash
python Code/ejercicio2_gestor_documentos.py
```

**Salida esperada:**

- Reportes de Ventas, Inventario y Financiero
- Formateo en PDF, Excel y HTML
- Entrega por Email, Download y Cloud
- Construcción de reporte personalizado con Builder
- Clonación de reportes con Prototype
- Adaptación de datos legacy con Adapter
- Generación rápida con Facade
- Reporte con Template Method
- Cambio de estrategia de procesamiento
- Historial completo en JSON

---

## 📝 Autor

Barraza Cárdenas Diego Alejandro
Proyecto de examen - Diseño de Software  
Fecha: 2024
