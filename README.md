# Restaurante Sabores del Sur

Repositorio para la asignatura de Programación Orientada a Objetos Seguro.

**Proyecto:** Sistema de Gestión de Pedidos, Comandas e Inventario - Restaurante Sabores del Sur  
**Integrantes:** Bastian Perez y Saul Saez  
**Institución:** Inacap  

---

## 📋 Descripción del Sistema

Software orientado a objetos basado en el modelo de dominio del **Restaurante Sabores del Sur**. Implementa una arquitectura modular con separación de responsabilidades (**Modelo - DAO - Servicios Externos - Persistencia SQLite**):

- **Herencia y Polimorfismo Real:** Jerarquía `ItemMenu` con sobrescritura uniforme del método `calcular_precio()` en `PlatoCaliente`, `Bebida`, `BebidaImportada` (con cotización según dólar en tiempo real) y `Postre`.
- **Integración con Servicios Web (API Externa):** Consumo de la API REST `mindicador.cl` mediante el módulo `servicios/miindicador.py` para consultar en tiempo real indicadores económicos chilenos (Dólar, UF, Euro, UTM, IPC) y cotizar bebidas o licores importados.
- **Transacciones y Composición:** `Pedido` contiene múltiples `DetallePedido` (composición $1 \to 1..*$), asociando `Mesa`, `Mesero` y emitiendo `Boleta`.
- **Reglas de Negocio:** Validación formal del RUT chileno mediante algoritmo Módulo 11 en `Boleta`, control de inventario con `Ingrediente` y gestión de mesas.
- **Persistencia con Patrón DAO Completo (CRUD):** DAOs (`MesaDao`, `IngredienteDao`, `ItemMenuDao`) con operaciones completas de creación de tablas, inserción, búsqueda, listado, actualización y eliminación sobre SQLite (`restaurante.db`) con soporte de claves foráneas (`PRAGMA foreign_keys = ON`).

---

## 🏛️ Estructura del Proyecto

```text
Restaurante-SaboresDelSur/
│
├── conectar.py              # Gestión de conexión SQLite con claves foráneas activadas
├── main.py                  # Menú interactivo con mantenedores CRUD y flujo del negocio
├── README.md                # Bitácora de desarrollo y documentación de cambios
├── requirements.txt         # Dependencias externas (requests, etc.)
│
├── dao/                     # Paquete de acceso a datos (Data Access Object - CRUD)
│   ├── __init__.py
│   ├── dao.py               # Clase base Dao con conexión y cursor
│   ├── ingrediente_dao.py   # DAO para la entidad Ingrediente (CRUD completo)
│   ├── itemmenu_dao.py      # DAO para la entidad ItemMenu (CRUD completo)
│   └── mesa_dao.py          # DAO para la entidad Mesa (CRUD completo)
│
├── model/                   # Paquete de modelos de dominio
│   ├── __init__.py
│   ├── boleta.py            # Entidad Boleta con validación de RUT chileno (Módulo 11)
│   ├── cocinero.py          # Subclase / Rol Cocinero (atención de cocina)
│   ├── detallepedido.py     # Línea de detalle del pedido (Composición con Pedido)
│   ├── ingrediente.py       # Control de inventario y stock suficiente
│   ├── itemmenu.py          # Superclase abstracta base para los ítems del menú
│   ├── platocaliente.py     # Subclase PlatoCaliente (sobrescribe calcular_precio)
│   ├── bebida.py            # Subclase Bebida (sobrescribe calcular_precio)
│   ├── bebidaimportada.py   # Subclase BebidaImportada (precio según cotización USD)
│   ├── postre.py            # Subclase Postre (sobrescribe calcular_precio)
│   ├── mesa.py              # Gestión de estado y apertura de mesa
│   ├── mesero.py            # Subclase / Rol Mesero (apertura de pedido)
│   ├── pedido.py            # Transacción principal del restaurante
│   └── trabajador.py        # Superclase base de trabajadores
│
└── servicios/               # Paquete de integración con APIs externas
    ├── __init__.py
    └── miindicador.py       # Cliente HTTP para API de mindicador.cl (Dólar, UF, Euro, etc.)
```

---

## 📝 Bitácora de Avances y Mejoras

### Fase 1: Corrección Estructural del Modelo de Dominio (UML)
- Jerarquía de clases con herencia y polimorfismo (`ItemMenu` -> `PlatoCaliente`, `Bebida`, `BebidaImportada`, `Postre`).
- Composición de `Pedido` con `DetallePedido`.
- Validación de RUT chileno con algoritmo Módulo 11.

### Fase 2: Servicios Externos y Consumo de API REST (`servicios/`)
- Creación de la capa `servicios/miindicador.py` utilizando la librería `requests`.
- Consulta en vivo de indicadores económicos chilenos (Dólar, UF, Euro, UTM, IPC).
- Cotización en tiempo real de bebidas y licores importados con el tipo de cambio del dólar del día.

### Fase 3: Capa de Persistencia y Patrón DAO con CRUD Completo (`dao/`)
- Implementación de métodos CRUD (`crear_tabla`, `insertar`, `buscar`, `listar`, `actualizar`, `eliminar`) en:
  - `MesaDao`
  - `IngredienteDao`
  - `ItemMenuDao`
- Mantenimiento de integridad referencial SQLite (`PRAGMA foreign_keys = ON`).

### Fase 4: Sistema de Menú Interactivo (`main.py`)
- Menú interactivo estructurado con opciones para:
  1. Ver la carta con precios polimórficos.
  2. Mantenedor CRUD de Ítems del Menú.
  3. Mantenedor CRUD de Ingredientes / Inventario.
  4. Mantenedor CRUD de Mesas.
  5. Flujo integral de Toma de Pedidos, Cocina y Emisión de Boletas.
  6. Consulta de Indicadores Económicos en tiempo real.
  7. Cotizador de Bebidas / Licores Importados (conversión USD a CLP).
  8. Simulación automática completa del sistema.
  9. Salida y cierre ordenado de conexiones.

---

## 🚀 Cómo Ejecutar el Proyecto

1. Asegúrate de tener instalado Python 3.8 o superior.
2. Instalar los requerimientos (si no están instalados):
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecutar el script principal:
   ```bash
   python main.py
   ```
