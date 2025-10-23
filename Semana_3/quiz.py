class Curso:
    __total_cursos = 0
    __total_estudiantes = 0
    __capacidad_estandar = 20
    
    def __init__(self, materia, capacidad, numero_curso):
        self.__materia = materia
        self.__capacidad = capacidad
        self.__numero_curso = numero_curso
        self.__estudiantes_actuales = 0
        Curso.__total_cursos += 1
    
    def asistencias(self, cantidad):
        if self.__estudiantes_actuales + cantidad <= self.__capacidad:
            self.__estudiantes_actuales += cantidad
            Curso.__total_estudiantes += cantidad
            return f"Asistencias de {cantidad} estudiantes en el curso {self.__numero_curso}."
        else:
            return f"Error: No hay espacio. Capacidad máxima: {self.__capacidad}, hay {self.__estudiantes_actuales} estudiantes."
    
    def mostrar_info(self):
        return f"Curso: {self.__numero_curso}, Materia: {self.__materia}, Estudiantes: {self.__estudiantes_actuales}/{self.__capacidad}"

    
    @classmethod
    def contar_cursos(cls):
        return f"Existen {cls.__total_cursos} cursos en la flota."

    @classmethod
    def contar_estudiantes(cls):
        return f"Se han matriculados {cls.__total_estudiantes} estudiantes en total."

    @classmethod
    def definir_capacidad_estandar(cls, nueva_capacidad):
        if nueva_capacidad > 0:
            cls.__capacidad_estandar = nueva_capacidad
            return f"Capacidad estándar actualizada a {cls.__capacidad_estandar} estudiantes."
        else:
            return "Error: La capacidad debe ser mayor a 0."
        


class Persona:
    def __init__(self, nombre):
        self.nombre = nombre

    def presentarse(self):
        return f"¡Hola, soy {self.nombre}!" 


class Profesor(Persona):
    def __init__(self, nombre, curso):
        super().__init__(nombre)
        self.curso = curso
    
    def dar_clase(self, cantidad):
        return f"{self.nombre} dice: {self.curso.asistencias(cantidad)}"


class Estudiante(Persona):
    def __init__(self, nombre, curso_preferido):
        super().__init__(nombre)
        self.curso_preferido = curso_preferido

    def asistir_a_clase(self, curso):
        if curso._Curso__materia == self.curso_preferido:
            return f"{self.nombre} dice: {curso.asistencias(1)}"
        else:
            return f"{self.nombre} dice: Este curso no es de mi materia preferida ({self.curso_preferida})."



    
if __name__ == "__main__":
    curso1 = Curso("Matemáticas", 20, "C-123")
    curso2 = Curso("Historia", 15, "C-456")
    print(curso1.mostrar_info())
    curso1.contar_estudiantes()
    print(curso2.mostrar_info())
    profesor1 = Profesor("pepe", curso1)
    profesor2 = Profesor("juan", curso2)
    print(profesor1.dar_clase(10))
    print(profesor2.dar_clase(5))
    
    estudiante1 = Estudiante("pedro", "Matemáticas")
    estudiante2 = Estudiante("juan", "Historia")
    print(estudiante1.asistir_a_clase(curso1))
    print(estudiante2.asistir_a_clase(curso2))
    


            
        

    
    
