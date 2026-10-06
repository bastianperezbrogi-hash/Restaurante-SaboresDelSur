import sys
import conectar
from dao.mesa_dao import MesaDao
from dao.ingrediente_dao import IngredienteDao
from dao.itemmenu_dao import ItemMenuDao
from model.mesa import Mesa
from model.ingrediente import Ingrediente
from model.mesero import Mesero
from model.cocinero import Cocinero
from model.platocaliente import PlatoCaliente
from model.bebida import Bebida
from model.bebidaimportada import BebidaImportada
from model.postre import Postre
from model.pedido import Pedido
from model.boleta import Boleta
from model.itemmenu import ItemMenu
from model.excepciones import (
    MesaOcupadaException,
    StockInsuficienteException,
    RutInvalidoException,
    PedidoCerradoException
)
from servicios.miindicador import MiIndicador

# Constantes de literales de texto para evitar duplicación (SonarLint S1192)
MSG_VOLVER_MENU = "6. Volver al menú principal"
PROMPT_OPCION_1_6 = "Seleccione una opción (1-6): "
PROMPT_PRECIO_BASE = "Precio base en CLP: "
ERR_ID_NUMERICO = "Error: Ingrese un ID numérico."
ERR_MESA_NO_ENCONTRADA = "Mesa no encontrada."
ITEM_WHISKY_DEMO = "Whisky Escocés 12 Años"


def demostracion_evaluacion_sumativa_2():
    """
    Demostración oficial requerida para la Evaluación Sumativa N°2:
    1. Tres subtipos con su método distinto (polimorfismo con super()).
    2. Atributo privado con property y validación en setter (RUT chileno Módulo 11 en Boleta).
    3. Transacción con sus líneas de detalle (Composición Pedido -> DetallePedido).
    4. Dos reglas del negocio provocadas a propósito y capturadas con try/except.
    """
    print("\n" + "="*70)
    print("  EVALUACIÓN SUMATIVA N°2: DEMOSTRACIÓN DEL MODELO DE CLASES EN PYTHON")
    print("  Proyecto: Restaurante Sabores del Sur | POO Seguro (INACAP)")
    print("="*70)

    # -------------------------------------------------------------
    # 1. TRES SUBTIPOS CON SU MÉTODO POLIMÓRFICO DISTINTO
    # -------------------------------------------------------------
    print("\n[1] DEMOSTRACIÓN DE HERENCIA Y POLIMORFISMO (3 Subtipos de ItemMenu):")
    plato = PlatoCaliente(nombre="Cazuela de Vacuno", precio_base=8500, tiempo_preparacion=25)
    bebida_imp = BebidaImportada(nombre=ITEM_WHISKY_DEMO, precio_usd=15.0)
    bebida_imp.cotizar_segun_dolar(980.0)
    postre = Postre(nombre="Leche Asada Tradicional", precio_base=3500)

    subtipos = [plato, bebida_imp, postre]
    for idx, item in enumerate(subtipos, 1):
        print(f"  {idx}. Clase: {item.__class__.__name__:<16} | Ítem: {item.nombre:<26} | Estación: {item.estacion_cocina:<16} | Precio Calculado: ${item.calcular_precio():,} CLP")

    # -------------------------------------------------------------
    # 2. ENCAPSULAMIENTO Y DATO CON VALIDACIÓN EN SETTER
    # -------------------------------------------------------------
    print("\n[2] DEMOSTRACIÓN DE DATO CON VALIDACIÓN EN SETTER (Módulo 11 en Boleta):")
    try:
        boleta_valida = Boleta(numero_boleta=1001, rut_cliente="12.345.678-5", monto_total=12000)
        print(f"  -> Éxito: Boleta #{boleta_valida.numero_boleta} creada correctamente para cliente con RUT válido: {boleta_valida.rut_cliente}")
    except RutInvalidoException as e:
        print(f"  -> Error inesperado: {e}")

    try:
        print("  -> Provocando validación fallida con RUT inválido '12.345.678-9'...")
        Boleta(numero_boleta=1002, rut_cliente="12.345.678-9", monto_total=15000)
    except RutInvalidoException as e:
        print(f"  -> [TRY/EXCEPT CAPTURADO] Excepción propia capturada: {e}")

    # -------------------------------------------------------------
    # 3. TRANSACCIÓN CON LÍNEAS DE DETALLE (COMPOSICIÓN Y AGREGACIÓN)
    # -------------------------------------------------------------
    print("\n[3] DEMOSTRACIÓN DE TRANSACCIÓN Y COMPOSICIÓN (Pedido -> DetallePedido):")
    mesa_demo = Mesa(numero=5)
    mesero_demo = Mesero(rut="15.890.123-4", nombre="Juan Pérez")
    cocinero_demo = Cocinero(rut="17.432.876-1", nombre="Carlos Tapia", estacion_asignada="Cocina Caliente")

    ing_carne = Ingrediente(nombre="Carne Vacuno", stock_actual=10, es_clave=True)
    plato.agregar_ingrediente(ing_carne)

    pedido_demo = mesero_demo.tomar_pedido(mesa_demo, numero_pedido=201, cliente="Ana Morales")
    print(f"  -> Pedido #{pedido_demo.numero_pedido} a nombre de '{pedido_demo.cliente}' abierto por el mesero {mesero_demo.nombre} para Mesa #{mesa_demo.numero}.")

    pedido_demo.agregar_detalle(item=plato, cant=2, obs="Bien caliente y sin sal")
    pedido_demo.agregar_detalle(item=postre, cant=1, obs="Con salsa de caramelo")

    print("  -> Líneas de Detalle creadas dentro del Pedido:")
    for det in pedido_demo.detalles:
        print(f"     * {det.cantidad}x {det.item_menu.nombre} ({det.observacion}) -> Subtotal: ${det.calcular_subtotal():,} CLP")
    print(f"  -> MONTO TOTAL DE LA TRANSACCIÓN: ${pedido_demo.calcular_total():,} CLP")

    for det in pedido_demo.detalles:
        cocinero_demo.marcar_listo(det)
    print(f"  -> Comanda preparada por {cocinero_demo.nombre} ({cocinero_demo.estacion_asignada}).")

    boleta_final = pedido_demo.cerrar_pedido(rut_cliente="12.345.678-5")
    print(f"  -> Transacción cerrada: Boleta #{boleta_final.numero_boleta} a nombre de '{boleta_final.nombre_cliente}' emitida por ${boleta_final.monto_total:,} CLP. Mesa #{mesa_demo.numero} liberada.")


    # -------------------------------------------------------------
    # 4. DOS REGLAS DE NEGOCIO PROVOCADAS Y CAPTURADAS CON TRY/EXCEPT
    # -------------------------------------------------------------
    print("\n[4] DEMOSTRACIÓN DE LAS DOS REGLAS DE NEGOCIO (Excepciones Propias):")

    print("\n  [Regla 1] Intentando abrir una mesa que ya está ocupada:")
    mesa_ocupada = Mesa(numero=2)
    mesa_ocupada.abrir_mesa()
    try:
        print(f"  -> Mesa #{mesa_ocupada.numero} estado actual: '{mesa_ocupada.estado}'. Intentando abrirla nuevamente...")
        mesa_ocupada.abrir_mesa()
    except MesaOcupadaException as e:
        print(f"  -> [TRY/EXCEPT CAPTURADO] MesaOcupadaException: {e}")

    print("\n  [Regla 2] Intentando ordenar un ítem sin stock suficiente de ingredientes:")
    ing_escaso = Ingrediente(nombre="Mariscos Frescos", stock_actual=1, es_clave=True)
    plato_mariscos = PlatoCaliente(nombre="Paila Marina", precio_base=11000, tiempo_preparacion=20)
    plato_mariscos.agregar_ingrediente(ing_escaso)

    mesa_regla2 = Mesa(numero=3)
    pedido_regla2 = Pedido(numero_pedido=202, mesa=mesa_regla2)
    try:
        print(f"  -> Solicitando 5 unidades de '{plato_mariscos.nombre}' teniendo solo {ing_escaso.stock_actual} en stock...")
        pedido_regla2.agregar_detalle(item=plato_mariscos, cant=5, obs="Urgente")
    except StockInsuficienteException as e:
        print(f"  -> [TRY/EXCEPT CAPTURADO] StockInsuficienteException: {e}")

    print("\n" + "="*70)
    print("  ¡DEMOSTRACIÓN DE LA EVALUACIÓN SUMATIVA N°2 COMPLETADA CON ÉXITO!")
    print("  El programa continuó su ejecución sin caídas ni errores no controlados.")
    print("="*70 + "\n")


def mostrar_menu_principal():
    print("\n" + "="*55)
    print("      RESTAURANTE SABORES DEL SUR - SISTEMA DE GESTIÓN")
    print("="*55)
    print("1. Ejecutar Demostración Oficial Evaluación N°2")
    print("2. Ver carta / menú y precios (Polimorfismo)")
    print("3. Mantenedor de Ítems del Menú (CRUD)")
    print("4. Mantenedor de Ingredientes / Inventario (CRUD)")
    print("5. Mantenedor de Mesas (CRUD)")
    print("6. Crear y procesar un Pedido interactivo")
    print("7. Consultar Valores Económicos (API mindicador.cl)")
    print("8. Cotizar Bebida/Licor Importado (Dólar en vivo)")
    print("9. Salir")
    print("="*55)


def obtener_tasa_dolar_actual(indicador: MiIndicador) -> float:
    try:
        return indicador.valor("dolar")
    except Exception:
        return 950.0


def inicializar_datos_prueba(mesa_dao: MesaDao, ingrediente_dao: IngredienteDao, item_dao: ItemMenuDao):
    if not mesa_dao.listar():
        for i in range(1, 6):
            mesa_dao.insertar(Mesa(numero=i))

    if not ingrediente_dao.listar():
        ingredientes_base = [
            Ingrediente(nombre="Carne de Vacuno", stock_actual=25, es_clave=True),
            Ingrediente(nombre="Choclo molido", stock_actual=30, es_clave=True),
            Ingrediente(nombre="Papas", stock_actual=50, es_clave=False),
            Ingrediente(nombre="Fruta fresca", stock_actual=40, es_clave=False),
            Ingrediente(nombre="Leche condensada", stock_actual=20, es_clave=False),
        ]
        for ing in ingredientes_base:
            ingrediente_dao.insertar(ing)

    if not item_dao.listar():
        items_base = [
            PlatoCaliente(nombre="Cazuela Vacuno", precio_base=8500, tiempo_preparacion=20),
            PlatoCaliente(nombre="Pastel de Choclo", precio_base=9000, tiempo_preparacion=25),
            Bebida(nombre="Jugo Natural", precio_base=2500),
            BebidaImportada(nombre=ITEM_WHISKY_DEMO, precio_usd=15),
            Postre(nombre="Leche Asada", precio_base=3500)
        ]
        for it in items_base:
            item_dao.insertar(it)


# -------------------------------------------------------------
# SUB-FUNCIONES PARA MANTENEDOR DE ÍTEMS DE MENÚ (REDUCCIÓN S3776)
# -------------------------------------------------------------

def _listar_items(item_dao: ItemMenuDao):
    items = item_dao.listar()
    print("\n--- Ítems en Base de Datos ---")
    if not items:
        print("No hay ítems registrados.")
        return
    for it in items:
        print(f"ID: {it.id} | Nombre: {it.nombre} | Precio Base: ${it.precio_base:,} | Prep: {it.tiempo_preparacion}m | Estación: {it.estacion_cocina}")


def _buscar_item(item_dao: ItemMenuDao):
    try:
        id_buscar = int(input("Ingrese ID del ítem: "))
        it = item_dao.buscar(id_buscar)
        if it:
            print(f"\n[Encontrado] ID: {it.id} | Nombre: {it.nombre} | Precio: ${it.precio_base:,} | Estación: {it.estacion_cocina}")
        else:
            print("No se encontró ningún ítem con ese ID.")
    except ValueError:
        print(ERR_ID_NUMERICO)


def _crear_instancia_item(t_sel: str, nombre: str, indicador: MiIndicador) -> ItemMenu:
    if t_sel == "1":
        precio = int(input(PROMPT_PRECIO_BASE))
        tiempo = int(input("Tiempo de preparación (min): "))
        return PlatoCaliente(nombre=nombre, precio_base=precio, tiempo_preparacion=tiempo)
    if t_sel == "2":
        precio = int(input(PROMPT_PRECIO_BASE))
        return Bebida(nombre=nombre, precio_base=precio)
    if t_sel == "3":
        precio_usd = float(input("Precio en USD ($): "))
        dolar = obtener_tasa_dolar_actual(indicador)
        nuevo_bi = BebidaImportada(nombre=nombre, precio_usd=precio_usd)
        precio_clp = nuevo_bi.cotizar_segun_dolar(dolar)
        return ItemMenu(nombre=nombre, precio_base=precio_clp, tiempo_preparacion=2, estacion_cocina="Barra")
    if t_sel == "4":
        precio = int(input(PROMPT_PRECIO_BASE))
        return Postre(nombre=nombre, precio_base=precio)
    return None


def _insertar_item(item_dao: ItemMenuDao, indicador: MiIndicador):
    print("\n--- Insertar Nuevo Ítem ---")
    print("Tipos: 1. Plato Caliente | 2. Bebida | 3. Bebida Importada (USD) | 4. Postre")
    t_sel = input("Seleccione tipo (1-4): ").strip()
    nombre = input("Nombre del ítem: ").strip()
    if not nombre:
        print("Error: El nombre no puede estar vacío.")
        return
    try:
        nuevo = _crear_instancia_item(t_sel, nombre, indicador)
        if nuevo is None:
            print("Tipo no válido.")
            return
        item_dao.insertar(nuevo)
        print(f"¡Ítem '{nuevo.nombre}' insertado exitosamente con ID {nuevo.id}!")
    except ValueError:
        print("Error: Ingrese valores numéricos válidos.")


def _actualizar_item(item_dao: ItemMenuDao):
    try:
        id_act = int(input("Ingrese ID del ítem a actualizar: "))
        it_actual = item_dao.buscar(id_act)
        if not it_actual:
            print("No se encontró el ítem.")
            return
        nuevo_nom = input(f"Nuevo nombre (enter para mantener '{it_actual.nombre}'): ").strip() or it_actual.nombre
        p_str = input(f"Nuevo precio base (enter para mantener {it_actual.precio_base}): ").strip()
        nuevo_precio = int(p_str) if p_str else it_actual.precio_base
        t_str = input(f"Nuevo tiempo preparación en min (enter para mantener {it_actual.tiempo_preparacion}): ").strip()
        nuevo_tiempo = int(t_str) if t_str else it_actual.tiempo_preparacion
        e_str = input(f"Nueva estación (enter para mantener '{it_actual.estacion_cocina}'): ").strip()
        nueva_estacion = e_str if e_str else it_actual.estacion_cocina
        item_modificado = ItemMenu(nuevo_nom, nuevo_precio, nuevo_tiempo, nueva_estacion, id_item=id_act)
        item_dao.actualizar(item_modificado)
        print("¡Ítem actualizado exitosamente!")
    except ValueError:
        print("Error: Entrada numérica no válida.")


def _eliminar_item(item_dao: ItemMenuDao):
    try:
        id_del = int(input("Ingrese ID del ítem a eliminar: "))
        it_del = item_dao.buscar(id_del)
        if it_del:
            conf = input(f"¿Confirma eliminar '{it_del.nombre}'? (s/n): ").strip().lower()
            if conf == 's':
                item_dao.eliminar(id_del)
                print("Ítem eliminado con éxito.")
        else:
            print("No existe el ítem.")
    except ValueError:
        print(ERR_ID_NUMERICO)


def menu_crud_items(item_dao: ItemMenuDao, indicador: MiIndicador):
    while True:
        print("\n" + "-"*40)
        print("   MANTENEDOR DE ÍTEMS DE MENÚ")
        print("-"*40)
        print("1. Listar todos los ítems")
        print("2. Buscar ítem por ID")
        print("3. Insertar nuevo ítem")
        print("4. Actualizar ítem")
        print("5. Eliminar ítem")
        print(MSG_VOLVER_MENU)
        print("-"*40)
        
        op = input(PROMPT_OPCION_1_6).strip()
        if op == "1":
            _listar_items(item_dao)
        elif op == "2":
            _buscar_item(item_dao)
        elif op == "3":
            _insertar_item(item_dao, indicador)
        elif op == "4":
            _actualizar_item(item_dao)
        elif op == "5":
            _eliminar_item(item_dao)
        elif op == "6":
            break


# -------------------------------------------------------------
# SUB-FUNCIONES PARA MANTENEDOR DE INGREDIENTES (REDUCCIÓN S3776)
# -------------------------------------------------------------

def _listar_ingredientes(ingrediente_dao: IngredienteDao):
    ings = ingrediente_dao.listar()
    print("\n--- Inventario de Ingredientes ---")
    if not ings:
        print("No hay ingredientes registrados.")
        return
    for i in ings:
        clave_txt = "[CRÍTICO/CLAVE]" if i.es_clave else "[ESTÁNDAR]"
        print(f"ID: {i.id} | {i.nombre} | Stock: {i.stock_actual} uds | {clave_txt}")


def _buscar_ingrediente(ingrediente_dao: IngredienteDao):
    try:
        id_buscar = int(input("Ingrese ID del ingrediente: "))
        i = ingrediente_dao.buscar(id_buscar)
        if i:
            clave_txt = "Sí" if i.es_clave else "No"
            print(f"\n[Encontrado] ID: {i.id} | {i.nombre} | Stock: {i.stock_actual} | Es Clave: {clave_txt}")
        else:
            print("No se encontró el ingrediente.")
    except ValueError:
        print(ERR_ID_NUMERICO)


def _insertar_ingrediente(ingrediente_dao: IngredienteDao):
    nombre = input("Nombre del ingrediente: ").strip()
    if not nombre:
        return
    try:
        stock = int(input("Stock inicial (unidades): "))
        es_clave = input("¿Es ingrediente crítico/clave? (s/n): ").strip().lower() == "s"
        nuevo_ing = Ingrediente(nombre=nombre, stock_actual=stock, es_clave=es_clave)
        ingrediente_dao.insertar(nuevo_ing)
        print(f"Ingrediente '{nuevo_ing.nombre}' registrado con ID {nuevo_ing.id}.")
    except ValueError:
        print("Error: El stock debe ser un número entero.")


def _actualizar_ingrediente(ingrediente_dao: IngredienteDao):
    try:
        id_act = int(input("Ingrese ID del ingrediente a actualizar: "))
        ing_act = ingrediente_dao.buscar(id_act)
        if not ing_act:
            print("Ingrediente no encontrado.")
            return
        n_nom = input(f"Nuevo nombre (enter para mantener '{ing_act.nombre}'): ").strip() or ing_act.nombre
        s_str = input(f"Nuevo stock (enter para mantener {ing_act.stock_actual}): ").strip()
        n_stock = int(s_str) if s_str else ing_act.stock_actual
        c_str = input("¿Es crítico? (s/n, enter para mantener): ").strip().lower()
        n_clave = (c_str == "s") if c_str in ["s", "n"] else ing_act.es_clave
        ing_mod = Ingrediente(nombre=n_nom, stock_actual=n_stock, es_clave=n_clave, id_ingrediente=id_act)
        ingrediente_dao.actualizar(ing_mod)
        print("¡Ingrediente actualizado con éxito!")
    except ValueError:
        print("Error: Ingrese valores válidos.")


def _eliminar_ingrediente(ingrediente_dao: IngredienteDao):
    try:
        id_del = int(input("Ingrese ID del ingrediente a eliminar: "))
        if ingrediente_dao.buscar(id_del):
            ingrediente_dao.eliminar(id_del)
            print("Ingrediente eliminado del inventario.")
        else:
            print("No se encontró el ingrediente.")
    except ValueError:
        print(ERR_ID_NUMERICO)


def menu_crud_ingredientes(ingrediente_dao: IngredienteDao):
    while True:
        print("\n" + "-"*40)
        print("   MANTENEDOR DE INGREDIENTES / STOCK")
        print("-"*40)
        print("1. Listar todos los ingredientes")
        print("2. Buscar ingrediente por ID")
        print("3. Registrar nuevo ingrediente")
        print("4. Actualizar ingrediente o stock")
        print("5. Eliminar ingrediente")
        print(MSG_VOLVER_MENU)
        print("-"*40)
        
        op = input(PROMPT_OPCION_1_6).strip()
        if op == "1":
            _listar_ingredientes(ingrediente_dao)
        elif op == "2":
            _buscar_ingrediente(ingrediente_dao)
        elif op == "3":
            _insertar_ingrediente(ingrediente_dao)
        elif op == "4":
            _actualizar_ingrediente(ingrediente_dao)
        elif op == "5":
            _eliminar_ingrediente(ingrediente_dao)
        elif op == "6":
            break


# -------------------------------------------------------------
# SUB-FUNCIONES PARA MANTENEDOR DE MESAS (REDUCCIÓN S3776)
# -------------------------------------------------------------

def _listar_mesas(mesa_dao: MesaDao):
    mesas = mesa_dao.listar()
    print("\n--- Mesas del Restaurante ---")
    if not mesas:
        print("No hay mesas registradas.")
        return
    for m in mesas:
        ped_txt = "Con pedido activo" if m.tiene_pedido_abierto else "Sin pedido"
        print(f"Mesa #{m.numero} | Estado: {m.estado} | {ped_txt}")


def _buscar_mesa(mesa_dao: MesaDao):
    try:
        num = int(input("Ingrese número de mesa: "))
        m = mesa_dao.buscar(num)
        if m:
            ped_txt = "Sí" if m.tiene_pedido_abierto else "No"
            print(f"\n[Encontrada] Mesa #{m.numero} | Estado: {m.estado} | Pedido Activo: {ped_txt}")
        else:
            print(ERR_MESA_NO_ENCONTRADA)
    except ValueError:
        print("Error: Ingrese un número válido.")


def _insertar_mesa(mesa_dao: MesaDao):
    try:
        num = int(input("Ingrese el número de la nueva mesa: "))
        if mesa_dao.buscar(num):
            print(f"Error: La mesa #{num} ya existe.")
            return
        nueva_m = Mesa(numero=num)
        mesa_dao.insertar(nueva_m)
        print(f"Mesa #{num} registrada exitosamente.")
    except ValueError:
        print("Error: Ingrese un número entero.")


def _cambiar_estado_mesa(mesa_dao: MesaDao):
    try:
        num = int(input("Ingrese el número de mesa a modificar: "))
        m = mesa_dao.buscar(num)
        if not m:
            print(ERR_MESA_NO_ENCONTRADA)
            return
        print("Estados: 1. Disponible | 2. Ocupada | 3. Reservada")
        est_op = input("Seleccione opción: ").strip()
        estados_map = {"1": "Disponible", "2": "Ocupada", "3": "Reservada"}
        nuevo_estado = estados_map.get(est_op, "Disponible")
        m.estado = nuevo_estado
        if nuevo_estado == "Disponible":
            m.cerrar_mesa()
        elif nuevo_estado == "Ocupada":
            m.tiene_pedido_abierto = True
        mesa_dao.actualizar(m)
        print(f"Mesa #{num} actualizada a estado: '{m.estado}'.")
    except ValueError:
        print("Error: Ingrese un número de mesa válido.")


def _eliminar_mesa(mesa_dao: MesaDao):
    try:
        num = int(input("Ingrese número de mesa a eliminar: "))
        if mesa_dao.buscar(num):
            mesa_dao.eliminar(num)
            print("Mesa eliminada con éxito.")
        else:
            print(ERR_MESA_NO_ENCONTRADA)
    except ValueError:
        print("Error: Ingrese un número válido.")


def menu_crud_mesas(mesa_dao: MesaDao):
    while True:
        print("\n" + "-"*40)
        print("   MANTENEDOR DE MESAS")
        print("-"*40)
        print("1. Listar todas las mesas")
        print("2. Buscar mesa por número")
        print("3. Registrar nueva mesa")
        print("4. Cambiar estado de mesa")
        print("5. Eliminar mesa")
        print(MSG_VOLVER_MENU)
        print("-"*40)
        
        op = input(PROMPT_OPCION_1_6).strip()
        if op == "1":
            _listar_mesas(mesa_dao)
        elif op == "2":
            _buscar_mesa(mesa_dao)
        elif op == "3":
            _insertar_mesa(mesa_dao)
        elif op == "4":
            _cambiar_estado_mesa(mesa_dao)
        elif op == "5":
            _eliminar_mesa(mesa_dao)
        elif op == "6":
            break


# -------------------------------------------------------------
# SUB-FUNCIONES PARA EL FLUJO DE PEDIDOS Y CIERRE (REDUCCIÓN S3776)
# -------------------------------------------------------------

def _agregar_items_a_pedido(pedido: Pedido, menu_items: list):
    while True:
        print("\nSeleccione qué ítem agregar:")
        for idx, it in enumerate(menu_items, 1):
            print(f"  {idx}. {it.nombre} (${it.calcular_precio():,} CLP)")
        print("  0. Terminar de agregar ítems al pedido")

        sel_item = input("Opción: ").strip()
        if sel_item == "0":
            break
        try:
            idx_elegido = int(sel_item) - 1
            if 0 <= idx_elegido < len(menu_items):
                item_elegido = menu_items[idx_elegido]
                cant = int(input(f"Cantidad de '{item_elegido.nombre}': "))
                if cant <= 0:
                    print("La cantidad debe ser mayor a 0.")
                    continue
                obs = input("Observación especial (opcional): ").strip()
                try:
                    pedido.agregar_detalle(item=item_elegido, cant=cant, obs=obs)
                    print(f"-> Añadido: {cant}x {item_elegido.nombre}")
                except StockInsuficienteException as e:
                    print(f"[Error Stock] {e}")
            else:
                print("Opción fuera de rango.")
        except ValueError:
            print("Por favor ingrese un número válido.")


def _cerrar_y_emitir_boleta(pedido: Pedido, mesa_bd: Mesa, mesa_dao: MesaDao):
    print("\n--- CIERRE Y EMISIÓN DE BOLETA ---")
    while True:
        rut_in = input(f"Ingrese RUT de {pedido.cliente} para la boleta (ej: 12.345.678-5): ").strip()
        try:
            boleta = pedido.cerrar_pedido(rut_cliente=rut_in)
            mesa_dao.actualizar(mesa_bd)
            print(f"\n¡BOLETA #{boleta.numero_boleta} EMITIDA CON ÉXITO!")
            print(f"Cliente: {boleta.nombre_cliente} (RUT: {boleta.rut_cliente})")
            print(f"Monto Total: ${boleta.monto_total:,} CLP")
            print(f"Mesa #{mesa_bd.numero} ahora queda: {mesa_bd.estado}")
            break
        except RutInvalidoException as e:
            print(f"\n[!] Error en emisión de boleta: {e}")
            reint = input("¿Desea reintentar con otro RUT? (s/n): ").strip().lower()
            if reint != 's':
                print("El pedido permanece abierto.")
                break
        except PedidoCerradoException as e:
            print(f"\n[!] Error en emisión de boleta: {e}")
            break


def _procesar_pedido_interactivo(mesa_dao: MesaDao, mesero: Mesero, cocinero: Cocinero, menu_items: list):
    print("\n--- CREAR Y PROCESAR NUEVO PEDIDO ---")
    try:
        num_mesa = int(input("Número de mesa para el pedido (ej. 1): "))
        mesa_bd = mesa_dao.buscar(num_mesa)
        if not mesa_bd:
            mesa_bd = Mesa(numero=num_mesa)
            mesa_dao.insertar(mesa_bd)

        if mesa_bd.tiene_pedido_abierto or mesa_bd.estado == "Ocupada":
            print(f"\n[Aviso] La Mesa #{mesa_bd.numero} ya figura como '{mesa_bd.estado}'.")
            conf_abrir = input("¿Desea reabrirla para un nuevo pedido? (s/n): ").strip().lower()
            if conf_abrir != 's':
                return
            mesa_bd.cerrar_mesa()

        nom_cliente = input("Nombre del cliente a cargo del pedido: ").strip() or "Cliente"
        pedido = mesero.tomar_pedido(mesa_bd, numero_pedido=301, cliente=nom_cliente)
        mesa_dao.actualizar(mesa_bd)
        print(f"Pedido #{pedido.numero_pedido} a nombre de '{pedido.cliente}' abierto por {mesero.nombre}. Mesa #{mesa_bd.numero} estado: {mesa_bd.estado}")


        _agregar_items_a_pedido(pedido, menu_items)

        if not pedido.detalles:
            print("El pedido no tiene ningún ítem. Cancelando...")
            mesa_bd.cerrar_mesa()
            mesa_dao.actualizar(mesa_bd)
            return

        print("\n--- RESUMEN DEL PEDIDO ---")
        for det in pedido.detalles:
            print(f"- {det.cantidad}x {det.item_menu.nombre} | Subtotal: ${det.calcular_subtotal():,}")
        print(f"TOTAL A PAGAR: ${pedido.calcular_total():,} CLP")

        for det in pedido.detalles:
            cocinero.marcar_listo(det)
            print(f"-> Plato '{det.item_menu.nombre}' preparado por {cocinero.nombre}.")

        _cerrar_y_emitir_boleta(pedido, mesa_bd, mesa_dao)

    except ValueError:
        print("Error: Entrada numérica no válida.")


def _consultar_indicador_en_vivo(indicador: MiIndicador):
    print("\n--- VALORES ECONÓMICOS EN TIEMPO REAL (MINDICADOR.CL) ---")
    print("Indicadores disponibles: dolar, uf, euro, utm, ipc")
    codigo = input("Ingrese el código del indicador: ").strip().lower()
    if codigo:
        try:
            val = indicador.valor(codigo)
            print(f"\n> El valor actual de '{codigo.upper()}' es: ${val:,.2f}")
        except Exception as e:
            print(f"\nError al consultar la API: {e}")
    else:
        print("Error: El código no puede estar vacío.")


def _cotizar_bebida_interactivo(indicador: MiIndicador):
    print("\n--- COTIZAR BEBIDA / LICOR IMPORTADO ---")
    try:
        nombre_beb = input("Nombre de la bebida importada: ").strip()
        precio_usd = float(input("Precio en USD ($): "))
        dolar_actual = indicador.valor("dolar")
        print(f"Valor del Dólar obtenido de la API: ${dolar_actual:,.2f} CLP")
        bebida_imp = BebidaImportada(nombre=nombre_beb, precio_usd=precio_usd)
        precio_final_clp = bebida_imp.cotizar_segun_dolar(dolar_actual)
        print(f"\n> El precio final de '{bebida_imp.nombre}' (${precio_usd} USD) es: ${precio_final_clp:,} CLP")
    except Exception as e:
        print(f"Error al cotizar: {e}")


def _mostrar_carta(menu_items: list):
    print("\n--- CARTA ACTUAL DEL RESTAURANTE (POLIMORFISMO) ---")
    for idx, item in enumerate(menu_items, 1):
        tipo = item.__class__.__name__
        precio = item.calcular_precio()
        print(f"[{idx}] {item.nombre} ({tipo}) - Precio: ${precio:,} CLP | Estación: {item.estacion_cocina}")


def main():
    conn = conectar.crear_conexion()
    mesa_dao = MesaDao(conn)

    ingrediente_dao = IngredienteDao(conn)
    item_dao = ItemMenuDao(conn)
    indicador = MiIndicador()

    mesa_dao.crear_tabla()
    ingrediente_dao.crear_tabla()
    item_dao.crear_tabla()

    inicializar_datos_prueba(mesa_dao, ingrediente_dao, item_dao)

    menu_items = [
        PlatoCaliente(nombre="Cazuela Vacuno", precio_base=8500, tiempo_preparacion=20),
        PlatoCaliente(nombre="Pastel de Choclo", precio_base=9000, tiempo_preparacion=25),
        Bebida(nombre="Jugo Natural", precio_base=2500),
        BebidaImportada(nombre=ITEM_WHISKY_DEMO, precio_usd=15.0),
        Postre(nombre="Leche Asada", precio_base=3500)
    ]

    tasa_dolar = obtener_tasa_dolar_actual(indicador)
    for item in menu_items:
        if isinstance(item, BebidaImportada):
            item.cotizar_segun_dolar(tasa_dolar)

    mesero = Mesero(rut="15.890.123-4", nombre="Juan Pérez")
    cocinero = Cocinero(rut="17.432.876-1", nombre="Carlos Tapia", estacion_asignada="Cocina Caliente")

    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opción (1-9): ").strip()

        if opcion == "1":
            demostracion_evaluacion_sumativa_2()
        elif opcion == "2":
            _mostrar_carta(menu_items)
        elif opcion == "3":
            menu_crud_items(item_dao, indicador)
        elif opcion == "4":
            menu_crud_ingredientes(ingrediente_dao)
        elif opcion == "5":
            menu_crud_mesas(mesa_dao)
        elif opcion == "6":
            _procesar_pedido_interactivo(mesa_dao, mesero, cocinero, menu_items)
        elif opcion == "7":
            _consultar_indicador_en_vivo(indicador)
        elif opcion == "8":
            _cotizar_bebida_interactivo(indicador)
        elif opcion == "9":
            print("\nCerrando el sistema del restaurante. ¡Hasta pronto!")
            conn.close()
            sys.exit(0)
        else:
            print("\nOpción no válida. Por favor, seleccione un número del 1 al 9.")


if __name__ == "__main__":
    main()
