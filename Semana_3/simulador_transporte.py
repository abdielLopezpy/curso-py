# Programa: Simulador de Transporte Público
# Autor: Alejandro, profesor
# Objetivo: Enseñar Programación Orientada a Objetos (POO) a estudiantes sin experiencia, usando un ejemplo cotidiano: un sistema de buses
# Fecha: 22 de mayo de 2025

# Importamos 'os' para limpiar la pantalla y mejorar la experiencia del usuario
import os

# CLASE 1: Bus
# Representa un bus de transporte público, como los que ves en una ciudad
class Bus:
    # Atributos de clase: Compartidos por todos los buses
    # '_total_buses': Cuenta cuántos buses se han creado
    _total_buses = 0
    # '_total_pasajeros_transportados': Registra todos los pasajeros que han usado los buses
    _total_pasajeros_transportados = 0
    # '_capacidad_estandar': Capacidad predeterminada para nuevos buses
    _capacidad_estandar = 50

    # Constructor: Crea un nuevo bus con sus características
    # Parámetros: ruta (str, ej: "Ruta 1"), capacidad (int, ej: 50), numero_bus (str, ej: "B-123")
    def __init__(self, ruta, capacidad, numero_bus):
        # Atributos de instancia: Únicos para cada bus
        # Usamos '__' para hacerlos privados (encapsulamiento, como guardar las piezas de un bus en un garaje privado)
        self.__ruta = ruta              # La ruta que cubre el bus, ej: "Ruta 1"
        self.__capacidad = capacidad    # Cuántos pasajeros puede llevar, ej: 50
        self.__numero_bus = numero_bus  # Identificador único, ej: "B-123"
        self.__pasajeros_actuales = 0   # Pasajeros actualmente en el bus
        # Incrementamos el contador de buses
        Bus._total_buses += 1
        # Analogía: Crear un bus es como añadir un nuevo vehículo a la flota de una empresa de transporte

    # Método de instancia: Sube pasajeros al bus
    # Ejemplo: Pasajeros subiendo en una parada
    def subir_pasajeros(self, cantidad):
        # 'self' se refiere a este bus específico, como un chofer manejando su propio vehículo
        if self.__pasajeros_actuales + cantidad <= self.__capacidad:
            self.__pasajeros_actuales += cantidad
            Bus._total_pasajeros_transportados += cantidad
            return f"Subieron {cantidad} pasajeros al bus {self.__numero_bus}. Ahora hay {self.__pasajeros_actuales} pasajeros."
        else:
            return f"Error: No hay espacio. Capacidad máxima: {self.__capacidad}, hay {self.__pasajeros_actuales} pasajeros."

    # Método de instancia: Baja pasajeros del bus
    # Ejemplo: Pasajeros llegando a su destino
    def bajar_pasajeros(self, cantidad):
        if cantidad <= self.__pasajeros_actuales:
            self.__pasajeros_actuales -= cantidad
            return f"Bajaron {cantidad} pasajeros del bus {self.__numero_bus}. Ahora hay {self.__pasajeros_actuales} pasajeros."
        else:
            return f"Error: Solo hay {self.__pasajeros_actuales} pasajeros en el bus {self.__numero_bus}."

    # Método de instancia: Cambia la ruta del bus
    # Ejemplo: El bus cambia de una ruta a otra por decisión del chofer
    def cambiar_ruta(self, nueva_ruta):
        self.__ruta = nueva_ruta
        return f"El bus {self.__numero_bus} ahora va por la ruta {self.__ruta}."

    # Método de instancia: Simula una revisión del bus (como mantenimiento)
    # Ejemplo: Chequear si el bus está listo para salir
    def revisar_bus(self):
        return f"El bus {self.__numero_bus} ha sido revisado y está listo para operar en la ruta {self.__ruta}."

    # Método de instancia: Muestra la información del bus
    def mostrar_info(self):
        return f"Bus: {self.__numero_bus}, Ruta: {self.__ruta}, Pasajeros: {self.__pasajeros_actuales}/{self.__capacidad}"

    # Método de clase: Cuenta cuántos buses existen
    # Usa '@classmethod' y 'cls' para acceder a datos de la clase
    @classmethod
    def contar_buses(cls):
        # Analogía: Es como revisar el registro de una empresa para ver cuántos buses tiene
        return f"Existen {cls._total_buses} buses en la flota."

    # Método de clase: Muestra el total de pasajeros transportados
    @classmethod
    def contar_pasajeros_transportados(cls):
        # Analogía: Es como un reporte de cuántas personas han usado los buses en un día
        return f"Se han transportado {cls._total_pasajeros_transportados} pasajeros en total."

    # Método de clase: Establece una capacidad estándar para todos los buses
    @classmethod
    def definir_capacidad_estandar(cls, nueva_capacidad):
        if nueva_capacidad > 0:
            cls._capacidad_estandar = nueva_capacidad
            return f"Capacidad estándar actualizada a {cls._capacidad_estandar} pasajeros."
        else:
            return "Error: La capacidad debe ser mayor a 0."

# CLASE 2: Persona
# Clase base para representar a cualquier persona (choferes o pasajeros)
class Persona:
    # Constructor: Inicializa el nombre de la persona
    def __init__(self, nombre):
        self.nombre = nombre  # Atributo público, ej: "José"
        # Analogía: Es como darle una identificación a cada persona en el sistema

    # Método de instancia: Presenta a la persona
    def presentarse(self):
        return f"¡Hola, soy {self.nombre}!"

# CLASE 3: Chofer (hereda de Persona)
# Representa un chofer que maneja un bus
class Chofer(Persona):
    # Constructor: Inicializa el nombre y el bus asignado
    def __init__(self, nombre, bus):
        super().__init__(nombre)  # Llama al constructor de Persona
        self.bus = bus  # El bus que maneja el chofer
        # Analogía: Es como asignarle un bus específico a un chofer en su turno

    # Método de instancia: El chofer hace que el bus suba pasajeros
    def manejar_y_subir_pasajeros(self, cantidad):
        # Usa el método de instancia del bus
        return f"{self.nombre} dice: {self.bus.subir_pasajeros(cantidad)}"

    # Método de instancia: El chofer cambia la ruta del bus
    def cambiar_ruta_bus(self, nueva_ruta):
        return f"{self.nombre} dice: {self.bus.cambiar_ruta(nueva_ruta)}"

# CLASE 4: Pasajero (hereda de Persona)
# Representa un pasajero que usa el bus
class Pasajero(Persona):
    # Constructor: Inicializa el nombre y la ruta preferida
    def __init__(self, nombre, ruta_preferida):
        super().__init__(nombre)
        self.ruta_preferida = ruta_preferida  # Ejemplo: "Ruta 1"
        # Analogía: Es como un pasajero que sabe a qué ruta quiere ir

    # Método de instancia: El pasajero sube a un bus
    def subir_a_bus(self, bus):
        if bus._Bus__ruta == self.ruta_preferida:  # Acceso directo para simplicidad
            return f"{self.nombre} dice: {bus.subir_pasajeros(1)}"
        else:
            return f"{self.nombre} dice: Este bus no va por mi ruta preferida ({self.ruta_preferida})."

# Función principal: Menú interactivo para los estudiantes
def main():
    # Limpiamos la pantalla para una experiencia más limpia
    os.system('cls' if os.name == 'nt' else 'clear')

    print("=============================================================")
    print("Simulador de Transporte Público -  Alejandro")
    print("Programa educativo para aprender Programación Orientada a Objetos")
    print("=============================================================\n")

    # Creamos algunos buses y personas iniciales
    bus1 = Bus("Ruta 1", 50, "B-123")
    bus2 = Bus("Ruta 2", 40, "B-456")
    chofer1 = Chofer("José", bus1)
    chofer2 = Chofer("Sofía", bus2)
    pasajero1 = Pasajero("Carlos", "Ruta 1")

    # Lista para almacenar buses creados dinámicamente
    buses = [bus1, bus2]

    while True:
        print("\n--- Menú del Sistema de Transporte ---")
        print("1. Mostrar total de buses (método de clase)")
        print("2. Mostrar pasajeros transportados (método de clase)")
        print("3. Cambiar capacidad estándar (método de clase)")
        print("4. Mostrar información de buses (método de instancia)")
        print("5. Subir pasajeros a un bus (método de instancia)")
        print("6. Bajar pasajeros de un bus (método de instancia)")
        print("7. Cambiar ruta de un bus (método de instancia)")
        print("8. Revisar un bus (método de instancia)")
        print("9. Crear un nuevo bus")
        print("10. Pasajero sube a un bus (método de instancia)")
        print("11. Salir")

        opcion = input("\nElige una opción (1-11): ")

        if opcion == "1":
            # Método de clase: Muestra el total de buses
            print("\n" + Bus.contar_buses())

        elif opcion == "2":
            # Método de clase: Muestra pasajeros transportados
            print("\n" + Bus.contar_pasajeros_transportados())

        elif opcion == "3":
            # Método de clase: Cambia la capacidad estándar
            try:
                nueva_capacidad = int(input("Ingresa la nueva capacidad estándar: "))
                print("\n" + Bus.definir_capacidad_estandar(nueva_capacidad))
            except ValueError:
                print("\nError: Ingresa un número válido")

        elif opcion == "4":
            # Método de instancia: Muestra información de todos los buses
            print("\n--- Información de buses ---")
            for bus in buses:
                print(bus.mostrar_info())

        elif opcion == "5":
            # Método de instancia: Subir pasajeros
            num_bus = input("Ingresa el número del bus (ej: B-123): ")
            for bus in buses:
                if bus._Bus__numero_bus == num_bus:
                    try:
                        cantidad = int(input("¿Cuántos pasajeros suben? "))
                        print("\n" + bus.subir_pasajeros(cantidad))
                        break
                    except ValueError:
                        print("\nError: Ingresa un número válido")
                        break
            else:
                print("\nError: No se encontró el bus")

        elif opcion == "6":
            # Método de instancia: Bajar pasajeros
            num_bus = input("Ingresa el número del bus (ej: B-123): ")
            for bus in buses:
                if bus._Bus__numero_bus == num_bus:
                    try:
                        cantidad = int(input("¿Cuántos pasajeros bajan? "))
                        print("\n" + bus.bajar_pasajeros(cantidad))
                        break
                    except ValueError:
                        print("\nError: Ingresa un número válido")
                        break
            else:
                print("\nError: No se encontró el bus")

        elif opcion == "7":
            # Método de instancia: Cambiar ruta
            num_bus = input("Ingresa el número del bus (ej: B-123): ")
            for bus in buses:
                if bus._Bus__numero_bus == num_bus:
                    nueva_ruta = input("Ingresa la nueva ruta: ")
                    print("\n" + bus.cambiar_ruta(nueva_ruta))
                    break
            else:
                print("\nError: No se encontró el bus")

        elif opcion == "8":
            # Método de instancia: Revisar bus
            num_bus = input("Ingresa el número del bus (ej: B-123): ")
            for bus in buses:
                if bus._Bus__numero_bus == num_bus:
                    print("\n" + bus.revisar_bus())
                    break
            else:
                print("\nError: No se encontró el bus")

        elif opcion == "9":
            # Crear un nuevo bus dinámicamente
            ruta = input("Ingresa la ruta del nuevo bus: ")
            try:
                capacidad = int(input("Ingresa la capacidad del nuevo bus: "))
                numero_bus = input("Ingresa el número del bus (ej: B-789): ")
                nuevo_bus = Bus(ruta, capacidad, numero_bus)
                buses.append(nuevo_bus)
                print(f"\nNuevo bus {numero_bus} creado con éxito.")
            except ValueError:
                print("\nError: Ingresa un número válido para la capacidad")

        elif opcion == "10":
            # Método de instancia: Pasajero sube a un bus
            num_bus = input("Ingresa el número del bus (ej: B-123): ")
            for bus in buses:
                if bus._Bus__numero_bus == num_bus:
                    print("\n" + pasajero1.subir_a_bus(bus))
                    break
            else:
                print("\nError: No se encontró el bus")

        elif opcion == "11":
            print("\n¡Gracias por usar el Simulador de Transporte Público!")
            break

        else:
            print("\nOpción inválida, intenta de nuevo")

# Ejecutamos el programa
if __name__ == "__main__":
    main()
