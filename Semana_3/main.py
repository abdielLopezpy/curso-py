# Aplicación de Línea de Comandos: Sistema de Gestión de Entregas
# Gestiona tres entidades: Usuario (clientes), Pedido (órdenes) y Estado (estado de los pedidos).
# Contexto: Un negocio local, como un restaurante o servicio de delivery, que organiza clientes y pedidos.
# Objetivo: Implementar un sistema funcional basado en un documento de requerimientos, usando diccionarios para almacenar datos.
# Los comentarios explican cada sección para que se entienda cómo se relaciona con los requerimientos y el flujo del programa.

try:
    from colorama import init, Fore, Style
except ImportError:
    print("Módulo 'colorama' no encontrado. Instale con: pip install colorama")
    exit(1)
init()  # Inicializa colorama para colores en la consola, mejorando la interfaz

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
    print(f"\n{Fore.CYAN}=== Sistema de Gestión de Entregas ==={Style.RESET_ALL}")
    print(f"{Fore.GREEN}1. Agregar cliente{Style.RESET_ALL}")
    print(f"{Fore.GREEN}2. Ver clientes{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}3. Agregar pedido{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}4. Ver pedidos{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}5. Actualizar estado de pedido{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}6. Ver estados de pedidos{Style.RESET_ALL}")
    print(f"{Fore.RED}7. Salir{Style.RESET_ALL}")

# Función para agregar un usuario
# Implementa el requerimiento de registrar clientes (entidad Usuario)
def agregar_usuario():
    global usuario_id_counter
    # Solicita el nombre del cliente
    nombre = input(f"{Fore.CYAN}Ingrese el nombre del cliente: {Style.RESET_ALL}").strip()
    # Valida que el nombre no esté vacío
    if not nombre:
        print(f"{Fore.RED}Error: El nombre no puede estar vacío.{Style.RESET_ALL}")
        return
    # Verifica que el nombre no esté ya registrado
    if nombre in usuarios.values():
        print(f"{Fore.RED}Error: El cliente ya está registrado.{Style.RESET_ALL}")
        return
    # Asigna un ID único y guarda el usuario en el diccionario
    usuarios[usuario_id_counter] = nombre
    print(f"{Fore.GREEN}✅ Cliente '{nombre}' agregado con ID {usuario_id_counter}.{Style.RESET_ALL}")
    usuario_id_counter += 1

# Función para mostrar la lista de usuarios
# Cumple con el requerimiento de visualizar los datos de los clientes
def ver_usuarios():
    if not usuarios:
        print(f"{Fore.YELLOW}No hay clientes registrados.{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.CYAN}📋 Lista de clientes:{Style.RESET_ALL}")
        # Recorre el diccionario de usuarios mostrando ID y nombre
        for id_usuario, nombre in usuarios.items():
            print(f"{Fore.GREEN}ID {id_usuario}: {nombre}{Style.RESET_ALL}")

# Función para agregar un pedido
# Implementa el requerimiento de registrar pedidos (entidad Pedido) asociados a un usuario
def agregar_pedido():
    global pedido_id_counter
    # Verifica que haya usuarios registrados
    if not usuarios:
        print(f"{Fore.RED}Error: No hay clientes registrados. Agregue un cliente primero.{Style.RESET_ALL}")
        return
    # Muestra los usuarios disponibles
    ver_usuarios()
    try:
        # Solicita el ID del usuario
        usuario_id = int(input(f"{Fore.CYAN}Ingrese el ID del cliente: {Style.RESET_ALL}"))
        # Valida que el ID exista
        if usuario_id not in usuarios:
            print(f"{Fore.RED}Error: Cliente no válido.{Style.RESET_ALL}")
            return
        # Solicita la descripción del pedido
        descripcion = input(f"{Fore.CYAN}Ingrese la descripción del pedido (ej. 'Pizza y refresco'): {Style.RESET_ALL}").strip()
        # Valida que la descripción no esté vacía
        if not descripcion:
            print(f"{Fore.RED}Error: La descripción no puede estar vacía.{Style.RESET_ALL}")
            return
        # Guarda el pedido en el diccionario con un ID único
        pedidos[pedido_id_counter] = {"usuario_id": usuario_id, "descripcion": descripcion}
        print(f"{Fore.YELLOW}📦 Pedido #{pedido_id_counter} agregado correctamente.{Style.RESET_ALL}")
        pedido_id_counter += 1
    except ValueError:
        print(f"{Fore.RED}Error: Ingrese un número válido.{Style.RESET_ALL}")

# Función para mostrar la lista de pedidos
# Cumple con el requerimiento de visualizar los pedidos registrados
def ver_pedidos():
    if not pedidos:
        print(f"{Fore.YELLOW}No hay pedidos registrados.{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.CYAN}📦 Lista de pedidos:{Style.RESET_ALL}")
        # Recorre el diccionario de pedidos mostrando detalles
        for id_pedido, pedido in pedidos.items():
            usuario_nombre = usuarios.get(pedido["usuario_id"], "Desconocido")
            print(f"{Fore.YELLOW}Pedido #{id_pedido}: {usuario_nombre} pidió {pedido['descripcion']}{Style.RESET_ALL}")

# Función para agregar o actualizar el estado de un pedido
# Implementa el requerimiento de gestionar la entidad Estado
def agregar_estado():
    # Verifica que haya pedidos registrados
    if not pedidos:
        print(f"{Fore.RED}Error: No hay pedidos registrados. Agregue un pedido primero.{Style.RESET_ALL}")
        return
    # Muestra los pedidos disponibles
    ver_pedidos()
    try:
        # Solicita el ID del pedido
        id_pedido = int(input(f"{Fore.CYAN}Ingrese el número del pedido para actualizar su estado: {Style.RESET_ALL}"))
        # Valida que el pedido exista
        if id_pedido not in pedidos:
            print(f"{Fore.RED}Error: Pedido no encontrado.{Style.RESET_ALL}")
            return
        # Muestra las opciones de estado
        print(f"{Fore.CYAN}Opciones de estado:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1. Pendiente{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}2. En Camino{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}3. Entregado{Style.RESET_ALL}")
        # Solicita la opción de estado
        opcion_estado = input(f"{Fore.CYAN}Seleccione el estado (1-3): {Style.RESET_ALL}")
        # Asigna el estado y su color
        if opcion_estado == "1":
            estado = "Pendiente"
            color_estado = Fore.GREEN
        elif opcion_estado == "2":
            estado = "En Camino"
            color_estado = Fore.YELLOW
        elif opcion_estado == "3":
            estado = "Entregado"
            color_estado = Fore.MAGENTA
        else:
            print(f"{Fore.RED}Error: Opción de estado no válida.{Style.RESET_ALL}")
            return
        # Guarda o actualiza el estado en el diccionario
        estados[id_pedido] = estado
        print(f"{color_estado}✅ Estado del pedido #{id_pedido} actualizado a '{estado}'.{Style.RESET_ALL}")
    except ValueError:
        print(f"{Fore.RED}Error: Ingrese un número válido.{Style.RESET_ALL}")

# Función para mostrar los estados de los pedidos
# Cumple con el requerimiento de visualizar los estados
def ver_estados():
    if not estados:
        print(f"{Fore.YELLOW}No hay estados registrados.{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.CYAN}📊 Estados de pedidos:{Style.RESET_ALL}")
        # Recorre el diccionario de estados mostrando detalles
        for id_pedido, estado in estados.items():
            color_estado = Fore.GREEN if estado == "Pendiente" else Fore.YELLOW if estado == "En Camino" else Fore.MAGENTA
            print(f"{color_estado}Pedido #{id_pedido}: {estado}{Style.RESET_ALL}")

# Función principal que controla el flujo del programa
# Integra todas las funciones para cumplir con el flujo definido en el documento de requerimientos
def main():
    print(f"{Fore.CYAN}🚚 Bienvenido al Sistema de Gestión de Entregas{Style.RESET_ALL}")
    # Bucle que mantiene el programa activo hasta que el usuario elija salir
    while True:
        mostrar_menu()
        opcion = input(f"{Fore.CYAN}Seleccione una opción (1-7): {Style.RESET_ALL}").strip()
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
            print(f"{Fore.RED}👋 ¡Gracias por usar el Sistema de Gestión de Entregas!{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Error: Opción no válida. Intente de nuevo.{Style.RESET_ALL}")

# Punto de entrada del programa
# Garantiza que el código solo se ejecute si se corre directamente
if __name__ == "__main__":
    main()