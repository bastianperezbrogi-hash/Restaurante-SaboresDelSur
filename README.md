# Restaurante Sabores del Sur

Repositorio para la asignatura de Programación Orientada a Objetos Seguro.

**Proyecto:** Sistema de Gestión de Pedidos y Comandas - Restaurante Sabores del Sur  
**Integrantes:** Bastian Perez y Saul Saez  
**Institución:** Inacap  

---

## 📋 Descripción del Sistema

Software orientado a objetos basado en el modelo de dominio del **Restaurante Sabores del Sur**. Implementa una arquitectura modular con separación de responsabilidades (**Modelo - DAO - Persistencia SQLite**) respetando rigurosamente las correcciones del diagrama UML:

- **Herencia y Polimorfismo Real:** Jerarquía `ItemMenu` con sobrescritura uniforme del método `calcular_precio()` en `PlatoCaliente`, `Bebida`, `BebidaImportada` (con cotización según dólar) y `Postre`.
- **Transacciones y Composición:** `Pedido` contiene múltiples `DetallePedido` (composición $1 \to 1..*$), asociando `Mesa`, `Mesero` y emitiendo `Boleta`.
- **Reglas de Negocio:** Validación formal del RUT chileno mediante algoritmo Módulo 11 en `Boleta`, control de inventario con `Ingrediente` y gestión de mesas.
- **Persistencia con Patrón DAO:** Conexión a base de datos SQLite (`restaurante.db`) con soporte de claves foráneas (`PRAGMA foreign_keys = ON`).

---

## 🏛️ Estructura del Proyecto

```text
Restaurante-SaboresDelSur/
│
├── conectar.py              # Gestión de conexión SQLite con claves foráneas activadas
├── main.py                  # Script principal de prueba y flujo integral del negocio
├── README.md                # Bitácora de desarrollo y documentación de cambios
│
├── dao/                     # Paquete de acceso a datos (Data Access Object)
│   ├── __init__.py
│   ├── dao.py               # Clase base Dao con conexión y cursor
│   ├── ingrediente_dao.py   # DAO para la entidad Ingrediente
│   ├── itemmenu_dao.py      # DAO para la entidad ItemMenu
│   └── mesa_dao.py          # DAO para la entidad Mesa
│
└── model/                   # Paquete de modelos de dominio
    ├── __init__.py
    ├── boleta.py            # Entidad Boleta con validación de RUT chileno (Módulo 11)
    ├── cocinero.py          # Subclase / Rol Cocinero (atención de cocina)
    ├── detallepedido.py     # Línea de detalle del pedido (Composición con Pedido)
    ├── ingrediente.py       # Control de inventario y stock suficiente
    ├── itemmenu.py          # Superclase abstracta base para los ítems del menú
    ├── platocaliente.py     # Subclase PlatoCaliente (sobrescribe calcular_precio)
    ├── bebida.py            # Subclase Bebida (sobrescribe calcular_precio)
    ├── bebidaimportada.py   # Subclase BebidaImportada (precio según cotización USD)
    ├── postre.py            # Subclase Postre (sobrescribe calcular_precio)
    ├── mesa.py              # Gestión de estado y apertura de mesa
    ├── mesero.py            # Subclase / Rol Mesero (apertura de pedido)
    ├── pedido.py            # Transacción principal del restaurante
    └── trabajador.py        # Superclase base de trabajadores
```

---

## 📝 Bitácora de Avances y Cambios

### Fase 1: Corrección Estructural del Modelo de Dominio (UML)
- **Reconexión de Relaciones Flotantes:**
  - Se formalizó la herencia de `PlatoCaliente` hacia `ItemMenu`.
  - Se vinculó `Pedido` con `DetallePedido` mediante **Composición** ($1 \to 1..*$).
  - Se asoció `DetallePedido` con `ItemMenu` ($0..* \to 1$).
- **Corrección de Relaciones:**
  - `Mesero - Pedido` y `Pedido - Boleta` se ajustaron a **Asociación / Agregación**, eliminando el acoplamiento exclusivo erróneo (un pedido no es parte física del mesero).
  - Se agregaron los atributos de referencia en código (`mesa`, `mesero`, `boleta`, `detalles`, `item_menu`, `ingredientes`).
- **Polimorfismo:**
  - Se unificó el método `calcular_precio()` en `ItemMenu` y se sobrescribió en `PlatoCaliente`, `Bebida`, `BebidaImportada` y `Postre`.

### Fase 2: Implementación de la Capa de Modelos (`model/`)
- Creación de encapsulamiento con properties en todas las clases.
- **Validación de RUT:** Implementación del algoritmo Módulo 11 en `Boleta.validar_rut()`.
- **Cotización USD:** Implementación de `cotizar_segun_dolar()` y cálculo polimórfico en `BebidaImportada`.
- **Composición de Pedidos:** Implementación de cálculo de total mediante agregación de subtotales de líneas de detalle en `Pedido.calcular_total()`.

### Fase 3: Implementación de la Capa de Persistencia (`dao/` y `conectar.py`)
- Creación de `conectar.py` habilitando llaves foráneas (`PRAGMA foreign_keys = ON`).
- Creación de la clase base `Dao` que provee conexión y cursor.
- Creación de `MesaDao`, `IngredienteDao` y `ItemMenuDao` con métodos `crear_tabla()` e `insertar()`.

### Fase 4: Script de Integración y Pruebas (`main.py`)
- Ejecución completa del ciclo de vida del restaurante:
  1. Conexión y creación de tablas SQLite.
  2. Inserción de mesas e ingredientes en inventario.
  3. Demostración de cálculo de precios polimórfico en el menú.
  4. Mesero toma pedido en mesa (cambio de estado de mesa a ocupada).
  5. Adición de ítems con observaciones y descuento de insumos.
  6. Cocinero procesa comanda y marca ítems como listos.
  7. Cierre del pedido, cálculo del total, emisión y validación de la Boleta electrónica.

---

## 🚀 Cómo Ejecutar el Proyecto

1. Asegúrate de tener instalado Python 3.8 o superior.
2. Abre una terminal en la carpeta raíz del proyecto:
   ```bash
   cd "C:\Users\BASTIAN PC\Restaurante-SaboresDelSur"
   ```
3. Ejecuta el script principal:
   ```bash
   python main.py
   ```
