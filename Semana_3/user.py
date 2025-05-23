

class Persona(object):
    # Constructor de la clase
    # Define la clase Persona con atributos nombre y edad
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad
    # Métodos de la clase
    # Implementa el requerimiento de saludar y despedirse
    def saludar(self):
        print(f"Hola, mi nombre es {self.nombre} y tengo {self.edad} años.")

    # Método para despedirse
    # Implementa el requerimiento de despedirse
    def despedirse(self):
        print(f"Adiós, soy {self.nombre}.")
    
    # Método de clase para mostrar la edad
    @classmethod
    def mostrar_edad(cls, edad):
        print(f"La edad es: {edad}")
        
        
    # coloca mayúscula al nombre
    @staticmethod
    def nombre_mayuscula(nombre):
        print(f"Nombre en mayúsculas: {nombre.upper()}")
        

if __name__ == "__main__":
    Abel = Persona("Abel", 45)
    Abel.saludar()
    Leo = Persona("Leo", 50)
    Leo.saludar()
    Jaime = Persona("Jaime", 55)
    Jaime.saludar()
    Didi = Persona("Didi", 60)
    Didi.saludar()
    Ronaldo = Persona("Ronaldo", 65)
    Ronaldo.saludar()
    Lince = Persona("Lince", 70)
    Lince.saludar()
    Persona.mostrar_edad(30)
    Persona.mostrar_edad(25)
    Persona.nombre_mayuscula("Juan")
    