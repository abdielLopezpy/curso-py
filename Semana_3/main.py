# Aplicación de Línea de Comandos: Sistema de Gestión de Entregas
# Gestiona tres entidades: Usuario (clientes), Pedido (órdenes) y Estado (estado de los pedidos).
# Contexto: Un negocio local, como un restaurante o servicio de delivery, que organiza clientes y pedidos.
# Objetivo: Implementar un sistema funcional basado en un documento de requerimientos, usando diccionarios para almacenar datos.
# Los comentarios explican cada sección para que se entienda cómo se relaciona con los requerimientos y el flujo del programa.


# Diccionarios para almacenar las entidades (en lugar de listas, para un acceso más estructurado)
# usuarios: clave es el ID del usuario, valor es el nombre
usuarios = {}  # Ejemplo: {1: "Juan", 2: "María"}
# pedidos: clave es el ID del pedido, valor es un diccionario con usuario y descripción
pedidos = {}  # Ejemplo: {1: {"usuario_id": 1, "descripcion": "Pizza"}, 2: {"usuario_id": 2, "descripcion": "Sancocho"}}
# estados: clave es el ID del pedido, valor es el estado
estados = {}  # Ejemplo: {1: "Pendiente", 2: "Entregado"}

# Contadores para generar IDs únicos
usuario_id_counter = 1
pedido_id_counter = 1

# Función para mostrar el menú principal
# Cumple con el requerimiento de ofrecer una interfaz clara y amigable
def mostrar_menu():
    print("\n=== Sistema de Gestión de Entregas ===")
    print("1. Agregar cliente")
    print("2. Ver clientes")
    print("3. Agregar pedido")
    print("4. Ver pedidos")
    print("5. Actualizar estado de pedido")
    print("6. Ver estados de pedidos")
    print("7. Salir")

# Función para agregar un usuario
# Implementa el requerimiento de registrar clientes (entidad Usuario)
def agregar_usuario():
    global usuario_id_counter
    # Solicita el nombre del cliente
    nombre = input("Ingrese el nombre del cliente: ").strip()
    # Valida que el nombre no esté vacío
    if not nombre:
        print("Error: El nombre no puede estar vacío.")
        return
    # Verifica que el nombre no esté ya registrado
    if nombre in usuarios.values():
        print("Error: El cliente ya está registrado.")
        return
    # Asigna un ID único y guarda el usuario en el diccionario
    usuarios[usuario_id_counter] = nombre
    print(f"✅ Cliente '{nombre}' agregado con ID {usuario_id_counter}.")
    usuario_id_counter += 1

# Función para mostrar la lista de usuarios
# Cumple con el requerimiento de visualizar los datos de los clientes
def ver_usuarios():
    if not usuarios:
        print("No hay clientes registrados.")
    else:
        print("\n📋 Lista de clientes:")
        # Recorre el diccionario de usuarios mostrando ID y nombre
        for id_usuario, nombre in usuarios.items():
            print(f"ID {id_usuario}: {nombre}")

# Función para agregar un pedido
# Implementa el requerimiento de registrar pedidos (entidad Pedido) asociados a un usuario
def agregar_pedido():
    global pedido_id_counter
    # Verifica que haya usuarios registrados
    if not usuarios:
        print("Error: No hay clientes registrados. Agregue un cliente primero.")
        return
    # Muestra los usuarios disponibles
    ver_usuarios()
    try:
        # Solicita el ID del usuario
        usuario_id = int(input("Ingrese el ID del cliente: "))
        # Valida que el ID exista
        if usuario_id not in usuarios:
            print("Error: Cliente no válido.")
            return
        # Solicita la descripción del pedido
        descripcion = input("Ingrese la descripción del pedido (ej. 'Pizza y refresco'): ").strip()
        # Valida que la descripción no esté vacía
        if not descripcion:
            print("Error: La descripción no puede estar vacía.")
            return
        # Guarda el pedido en el diccionario con un ID único
        pedidos[pedido_id_counter] = {"usuario_id": usuario_id, "descripcion": descripcion}
        print(f"📦 Pedido #{pedido_id_counter} agregado correctamente.")
        pedido_id_counter += 1
    except ValueError:
        print("Error: Ingrese un número válido.")

# Función para mostrar la lista de pedidos
# Cumple con el requerimiento de visualizar los pedidos registrados
def ver_pedidos():
    if not pedidos:
        print("No hay pedidos registrados.")
    else:
        print("\n📦 Lista de pedidos:")
        # Recorre el diccionario de pedidos mostrando detalles
        for id_pedido, pedido in pedidos.items():
            usuario_nombre = usuarios.get(pedido["usuario_id"], "Desconocido")
            print(f"Pedido #{id_pedido}: {usuario_nombre} pidió {pedido['descripcion']}")

# Función para agregar o actualizar el estado de un pedido
# Implementa el requerimiento de gestionar la entidad Estado
def agregar_estado():
    # Verifica que haya pedidos registrados
    if not pedidos:
        print("Error: No hay pedidos registrados. Agregue un pedido primero.")
        return
    # Muestra los pedidos disponibles
    ver_pedidos()
    try:
        # Solicita el ID del pedido
        id_pedido = int(input("Ingrese el número del pedido para actualizar su estado: "))
        # Valida que el pedido exista
        if id_pedido not in pedidos:
            print("Error: Pedido no encontrado.")
            return
        # Muestra las opciones de estado
        print("Opciones de estado:")
        print("1. Pendiente")
        print("2. En Camino")
        print("3. Entregado")
        # Solicita la opción de estado
        opcion_estado = input("Seleccione el estado (1-3): ")
        # Asigna el estado
        if opcion_estado == "1":
            estado = "Pendiente"
        elif opcion_estado == "2":
            estado = "En Camino"
        elif opcion_estado == "3":
            estado = "Entregado"
        else:
            print("Error: Opción de estado no válida.")
            return
        # Guarda o actualiza el estado en el diccionario
        estados[id_pedido] = estado
        print(f"✅ Estado del pedido #{id_pedido} actualizado a '{estado}'.")
    except ValueError:
        print("Error: Ingrese un número válido.")

# Función para mostrar los estados de los pedidos
# Cumple con el requerimiento de visualizar los estados
def ver_estados():
    if not estados:
        print("No hay estados registrados.")
    else:
        print("\n📊 Estados de pedidos:")
        # Recorre el diccionario de estados mostrando detalles
        for id_pedido, estado in estados.items():
            print(f"Pedido #{id_pedido}: {estado}")

# Función principal que controla el flujo del programa
# Integra todas las funciones para cumplir con el flujo definido en el documento de requerimientos
def main():
    print("🚚 Bienvenido al Sistema de Gestión de Entregas")
    # Bucle que mantiene el programa activo hasta que el usuario elija salir
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-7): ").strip()
        if opcion == "1":
            agregar_usuario()
        elif opcion == "2":
            ver_usuarios()
        elif opcion == "3":
            agregar_pedido()
        elif opcion == "4":
            ver_pedidos()
        elif opcion == "5":
            agregar_estado()
        elif opcion == "6":
            ver_estados()
        elif opcion == "7":
            print("👋 ¡Gracias por usar el Sistema de Gestión de Entregas!")
            break
        else:
            print("Error: Opción no válida. Intente de nuevo.")

# Punto de entrada del programa
# Garantiza que el código solo se ejecute si se corre directamente
if __name__ == "__main__":
    main()