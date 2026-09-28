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

def mostrar_menu_principal():
    print("\n" + "="*55)
    print("      RESTAURANTE SABORES DEL SUR - MENÚ DE OPCIONES      ")
    print("="*55)
    print("1. Ver carta / menú y precios (Polimorfismo)")
    print("2. Crear un nuevo plato / ítem de menú")
    print("3. Registrar nuevo ingrediente en inventario")
    print("4. Crear y procesar un nuevo Pedido interactivo")
    print("5. Ejecutar simulación automática completa")
    print("6. Salir")
    print("="*55)

def flujo_interactivo():
    conn = conectar.crear_conexion()
    mesa_dao = MesaDao(conn)
    ingrediente_dao = IngredienteDao(conn)
    item_dao = ItemMenuDao(conn)

    # Inicializar tablas
    mesa_dao.crear_tabla()
    ingrediente_dao.crear_tabla()
    item_dao.crear_tabla()

    # Datos base en memoria y BD
    mesa1 = Mesa(numero=1)
    mesa_dao.insertar(mesa1)

    menu_items = [
        PlatoCaliente(nombre="Cazuela Vacuno", precio_base=8500, tiempo_preparacion=20),
        PlatoCaliente(nombre="Pastel de Choclo", precio_base=9000, tiempo_preparacion=25),
        Bebida(nombre="Jugo Natural", precio_base=2500),
        BebidaImportada(nombre="Whisky Escocés 12 Años", precio_usd=15),
        Postre(nombre="Leche Asada", precio_base=3500)
    ]

    # Cotizar bebida importada por defecto
    for item in menu_items:
        if isinstance(item, BebidaImportada):
            item.cotizar_segun_dolar(960)

    mesero = Mesero(rut="15.890.123-4", nombre="Juan Pérez")
    cocinero = Cocinero(rut="17.432.876-1", nombre="Carlos Tapia", estacion_asignada="Cocina Caliente")

    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opción (1-6): ").strip()

        if opcion == "1":
            print("\n--- CARTA ACTUAL DEL RESTAURANTE ---")
            for idx, item in enumerate(menu_items, 1):
                tipo = item.__class__.__name__
                precio = item.calcular_precio()
                print(f"[{idx}] {item.nombre} ({tipo}) - Precio: ${precio:,} CLP | Estación: {item.estacion_cocina}")

        elif opcion == "2":
            print("\n--- CREAR NUEVO ÍTEM DE MENÚ ---")
            print("Tipos disponibles: 1. Plato Caliente | 2. Bebida | 3. Bebida Importada (USD) | 4. Postre")
            tipo_sel = input("Seleccione tipo (1-4): ").strip()
            nombre = input("Nombre del ítem: ").strip()

            if tipo_sel == "1":
                precio = int(input("Precio base en CLP: "))
                tiempo = int(input("Tiempo de preparación (min): "))
                nuevo_item = PlatoCaliente(nombre=nombre, precio_base=precio, tiempo_preparacion=tiempo)
            elif tipo_sel == "2":
                precio = int(input("Precio base en CLP: "))
                nuevo_item = Bebida(nombre=nombre, precio_base=precio)
            elif tipo_sel == "3":
                precio_usd = int(input("Precio en USD ($): "))
                dolar = int(input("Cotización dólar del día (ej. 960): "))
                nuevo_item = BebidaImportada(nombre=nombre, precio_usd=precio_usd)
                nuevo_item.cotizar_segun_dolar(dolar)
            elif tipo_sel == "4":
                precio = int(input("Precio base en CLP: "))
                nuevo_item = Postre(nombre=nombre, precio_base=precio)
            else:
                print("Tipo inválido.")
                continue

            menu_items.append(nuevo_item)
            item_dao.insertar(nuevo_item)
            print(f"¡'{nuevo_item.nombre}' agregado con éxito! Precio calculado: ${nuevo_item.calcular_precio():,} CLP")

        elif opcion == "3":
            print("\n--- REGISTRAR INGREDIENTE EN INVENTARIO ---")
            nombre_ing = input("Nombre del ingrediente: ").strip()
            stock = int(input("Stock inicial (unidades): "))
            es_clave = input("¿Es ingrediente clave/crítico? (s/n): ").strip().lower() == "s"
            ing = Ingrediente(nombre=nombre_ing, stock_actual=stock, es_clave=es_clave)
            ingrediente_dao.insertar(ing)
            print(f"Ingrediente '{ing.nombre}' registrado con ID: {ing.id} y stock: {ing.stock_actual}")

        elif opcion == "4":
            print("\n--- CREAR Y PROCESAR NUEVO PEDIDO ---")
            num_mesa = int(input("Número de mesa para el pedido (ej. 1): "))
            mesa = Mesa(numero=num_mesa)
            pedido = mesero.tomar_pedido(mesa, numero_pedido=201)
            print(f"Pedido #{pedido.numero_pedido} abierto por el mesero {mesero.nombre}. Mesa estado: {mesa.estado}")

            while True:
                print("\nSeleccione qué ítem agregar:")
                for idx, item in enumerate(menu_items, 1):
                    print(f"  {idx}. {item.nombre} (${item.calcular_precio():,} CLP)")
                print("  0. Terminar de agregar ítems al pedido")

                sel_item = input("Opción: ").strip()
                if sel_item == "0":
                    break
                try:
                    idx_elegido = int(sel_item) - 1
                    if 0 <= idx_elegido < len(menu_items):
                        item_elegido = menu_items[idx_elegido]
                        cant = int(input(f"Cantidad de '{item_elegido.nombre}': "))
                        obs = input("Observación especial (opcional): ").strip()
                        pedido.agregar_detalle(item=item_elegido, cant=cant, obs=obs)
                        print(f"-> Añadido: {cant}x {item_elegido.nombre}")
                    else:
                        print("Opción fuera de rango.")
                except ValueError:
                    print("Por favor ingrese un número válido.")

            if not pedido.detalles:
                print("El pedido no tiene ningún ítem. Cancelando...")
                mesa.cerrar_mesa()
                continue

            print("\n--- RESUMEN DEL PEDIDO ---")
            for det in pedido.detalles:
                print(f"- {det.cantidad}x {det.item_menu.nombre} | Subtotal: ${det.calcular_subtotal():,}")
            print(f"TOTAL A PAGAR: ${pedido.calcular_total():,} CLP")

            # Cocinero prepara
            print("\n--- COCINA ---")
            for det in pedido.detalles:
                cocinero.marcar_listo(det)
                print(f"-> Plato '{det.item_menu.nombre}' preparado por {cocinero.nombre}.")

            # Cierre y boleta
            print("\n--- CIERRE Y EMISIÓN DE BOLETA ---")
            rut_in = input("Ingrese RUT del cliente para la boleta (ej: 12.345.678-5): ").strip()
            boleta = pedido.cerrar_pedido(rut_cliente=rut_in)
            if boleta and boleta.emitir_documento():
                print(f"\n¡BOLETA #{boleta.numero_boleta} EMITIDA CON ÉXITO!")
                print(f"Cliente: {boleta.rut_cliente}")
                print(f"Monto Total: ${boleta.monto_total:,} CLP")
                print(f"Mesa #{mesa.numero} ahora queda: {mesa.estado}")
            else:
                print("\n[!] Error: El RUT ingresado no es válido según el algoritmo Módulo 11 o el total es 0.")

        elif opcion == "5":
            print("\n--- SIMULACIÓN AUTOMÁTICA ---")
            p = mesero.tomar_pedido(mesa1, numero_pedido=101)
            p.agregar_detalle(menu_items[0], 2, "Sin sal")
            p.agregar_detalle(menu_items[3], 1, "Con hielo")
            print(f"Pedido simulado creado con total: ${p.calcular_total():,} CLP")
            for d in p.detalles:
                cocinero.marcar_listo(d)
            b = p.cerrar_pedido("12.345.678-5")
            if b and b.emitir_documento():
                print(f"Boleta #{b.numero_boleta} emitida con éxito para {b.rut_cliente}. Total: ${b.monto_total:,} CLP")

        elif opcion == "6":
            print("\nGracias por usar el sistema de Restaurante Sabores del Sur. ¡Hasta pronto!")
            break
        else:
            print("Opción no válida. Ingrese un número del 1 al 6.")

if __name__ == "__main__":
    flujo_interactivo()
