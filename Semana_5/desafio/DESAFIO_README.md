# 🎯 DESAFÍO SEMANA 5: Sistema de Gestión con JSON

## 📋 Objetivo

Crear un **sistema completo de gestión** con **3 entidades relacionadas** que guarde toda la información en archivos JSON.

---

## 🎓 ¿Qué voy a aprender?

Al completar este desafío aprenderás a:

✅ Definir entidades (clases) para representar datos del mundo real
✅ Usar archivos JSON para persistir información
✅ Implementar operaciones CRUD (Crear, Leer, Actualizar, Eliminar)
✅ Relacionar diferentes entidades entre sí
✅ Crear un sistema completo y funcional
✅ Estructurar código de forma profesional

---

## 📁 Estructura del Proyecto

```
Semana_5/
├── CONCEPTOS_CLAVE.md          👈 Lee esto primero si tienes dudas sobre @dataclass, herencia, etc.
├── framework/
│   └── database_framework.py   👈 Framework completo (NO MODIFICAR)
├── ejemplo/
│   └── ejemplo_tienda.py       👈 Ejemplo completo para estudiar
└── desafio/
    ├── DESAFIO_README.md       👈 Estás aquí
    └── DESAFIO.py              👈 Aquí trabajarás
```

---

## 🚀 Paso a Paso

### PASO 0: Preparación (5 minutos)

#### 1. Lee primero:
- 📖 [CONCEPTOS_CLAVE.md](../CONCEPTOS_CLAVE.md) - Especialmente la sección de @dataclass

#### 2. Estudia el ejemplo:
- 📂 Abre [ejemplo_tienda.py](../ejemplo/ejemplo_tienda.py)
- ▶️ Ejecútalo: `python3 Semana_5/ejemplo/ejemplo_tienda.py`
- 👀 Observa qué archivos JSON se crean en `datos/tienda_ejemplo/`
- 📊 Revisa los archivos JSON generados

#### 3. Elige tu sistema:

Decide qué sistema quieres crear. Aquí hay ideas:

| Sistema | Entidades | Relación |
|---------|-----------|----------|
| 🏥 **Hospital** | Doctores, Pacientes, Citas | Un doctor atiende pacientes en citas |
| 📚 **Biblioteca** | Libros, Usuarios, Préstamos | Los usuarios piden libros prestados |
| 🎓 **Escuela** | Estudiantes, Profesores, Cursos | Profesores enseñan cursos a estudiantes |
| 🍕 **Restaurante** | Platillos, Ingredientes, Pedidos | Los pedidos contienen platillos |
| 🏨 **Hotel** | Habitaciones, Huéspedes, Reservaciones | Huéspedes reservan habitaciones |
| 🚗 **Renta de Autos** | Vehículos, Clientes, Rentas | Clientes rentan vehículos |
| 💪 **Gimnasio** | Miembros, Entrenadores, Clases | Entrenadores dan clases a miembros |
| 🎬 **Cine** | Películas, Salas, Funciones | Las funciones proyectan películas en salas |

**O inventa tu propio sistema** - ¡Sé creativo!

---

### PASO 1: Definir tus Entidades (15-20 minutos)

Abre [DESAFIO.py](DESAFIO.py) y busca donde dice `PASO 1: DEFINIR TUS ENTIDADES`.

#### Ejemplo: Sistema de Biblioteca

```python
from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class Libro(Entidad):
    """Representa un libro en la biblioteca."""
    id: int
    titulo: str
    autor: str
    isbn: str
    disponible: bool  # True = disponible, False = prestado

    def obtener_id(self) -> int:
        return self.id

    @classmethod
    def desde_diccionario(cls, datos: Dict[str, Any]) -> 'Libro':
        return cls(**datos)

    def validar(self) -> bool:
        """Valida que los datos del libro sean correctos."""
        if not validar_no_vacio(self.titulo, "título"):
            return False
        if not validar_no_vacio(self.autor, "autor"):
            return False
        if not validar_no_vacio(self.isbn, "ISBN"):
            return False
        return True

@dataclass
class Usuario(Entidad):
    """Representa un usuario de la biblioteca."""
    id: int
    nombre: str
    email: str
    telefono: str

    def obtener_id(self) -> int:
        return self.id

    @classmethod
    def desde_diccionario(cls, datos: Dict[str, Any]) -> 'Usuario':
        return cls(**datos)

    def validar(self) -> bool:
        if not validar_no_vacio(self.nombre, "nombre"):
            return False
        if not validar_no_vacio(self.email, "email"):
            return False
        if "@" not in self.email:
            print("❌ Error: Email inválido")
            return False
        return True

@dataclass
class Prestamo(Entidad):
    """Representa un préstamo de libro."""
    id: int
    libro_id: int      # ⬅️ Relaciona con Libro
    usuario_id: int    # ⬅️ Relaciona con Usuario
    fecha_prestamo: str
    fecha_devolucion: str
    devuelto: bool

    def obtener_id(self) -> int:
        return self.id

    @classmethod
    def desde_diccionario(cls, datos: Dict[str, Any]) -> 'Prestamo':
        return cls(**datos)
```

#### 📝 Checklist para tus Entidades:

Para cada entidad verifica:
- [ ] Tiene el decorador `@dataclass`
- [ ] Hereda de `Entidad`
- [ ] Tiene un campo `id`
- [ ] Tiene al menos 4 campos en total
- [ ] Implementa `obtener_id()`
- [ ] Implementa `desde_diccionario()`
- [ ] Implementa `validar()` con al menos 2 validaciones

Para la **tercera entidad** (la relación):
- [ ] Tiene campos que referencian las otras dos (ej: `libro_id`, `usuario_id`)

---

### PASO 2: Crear tu Sistema de Gestión (10-15 minutos)

Busca donde dice `PASO 2: CREAR TU SISTEMA DE GESTIÓN`.

#### Ejemplo: Sistema de Biblioteca

```python
class SistemaBiblioteca(SistemaGestion):
    """Sistema completo de gestión de biblioteca."""

    def __init__(self):
        super().__init__("biblioteca")

        # Crear los tres repositorios
        self.libros = RepositorioJSON("libros", Libro, self.directorio_datos)
        self.usuarios = RepositorioJSON("usuarios", Usuario, self.directorio_datos)
        self.prestamos = RepositorioJSON("prestamos", Prestamo, self.directorio_datos)
```

#### 📝 Checklist:

- [ ] La clase hereda de `SistemaGestion`
- [ ] Llama a `super().__init__(nombre_sistema)`
- [ ] Crea 3 repositorios (uno por cada entidad)
- [ ] Los repositorios tienen nombres descriptivos

---

### PASO 3: Implementar Operaciones Básicas (15-20 minutos)

Busca donde dice `PASO 3: IMPLEMENTAR OPERACIONES BÁSICAS`.

#### Ejemplo: Métodos básicos

```python
# Agregar entidades
def agregar_libro(self, libro: Libro) -> bool:
    """Agrega un nuevo libro al catálogo."""
    if not libro.validar():
        return False
    return self.libros.insertar(libro)

def agregar_usuario(self, usuario: Usuario) -> bool:
    """Registra un nuevo usuario."""
    if not usuario.validar():
        return False
    return self.usuarios.insertar(usuario)

# Listar entidades
def listar_libros(self) -> List[Libro]:
    """Retorna todos los libros."""
    return self.libros.consultar_todos()

def listar_usuarios(self) -> List[Usuario]:
    """Retorna todos los usuarios."""
    return self.usuarios.consultar_todos()

# Buscar por ID
def buscar_libro(self, libro_id: int) -> Libro | None:
    """Busca un libro por su ID."""
    return self.libros.consultar_por_id(libro_id)

def buscar_usuario(self, usuario_id: int) -> Usuario | None:
    """Busca un usuario por su ID."""
    return self.usuarios.consultar_por_id(usuario_id)

# Buscar por campo
def libros_disponibles(self) -> List[Libro]:
    """Retorna solo los libros disponibles."""
    return self.libros.consultar_por_campo("disponible", True)
```

#### 📝 Checklist:

Para cada entidad necesitas:
- [ ] Método para agregar
- [ ] Método para listar todos
- [ ] Método para buscar por ID
- [ ] (Opcional) Métodos para buscar por otros campos

---

### PASO 4: Implementar Operación que Relacione Entidades (20-25 minutos)

Busca donde dice `PASO 4: IMPLEMENTAR OPERACIONES QUE RELACIONEN ENTIDADES`.

Esta es **la parte más importante** del desafío. Debes crear un método que use las 3 entidades juntas.

#### Ejemplo: Prestar un libro

```python
def prestar_libro(self, libro_id: int, usuario_id: int) -> bool:
    """
    Registra el préstamo de un libro a un usuario.

    Pasos:
    1. Verificar que el libro existe
    2. Verificar que está disponible
    3. Verificar que el usuario existe
    4. Crear el préstamo
    5. Marcar el libro como no disponible
    """
    from datetime import datetime, timedelta

    # 1. Verificar que el libro existe
    libro = self.buscar_libro(libro_id)
    if libro is None:
        print(f"❌ Libro {libro_id} no encontrado")
        return False

    # 2. Verificar que está disponible
    if not libro.disponible:
        print(f"❌ El libro '{libro.titulo}' no está disponible")
        return False

    # 3. Verificar que el usuario existe
    usuario = self.buscar_usuario(usuario_id)
    if usuario is None:
        print(f"❌ Usuario {usuario_id} no encontrado")
        return False

    # 4. Crear el préstamo
    nuevo_id = self.prestamos.contar() + 1
    fecha_hoy = datetime.now().isoformat()
    fecha_devolucion = (datetime.now() + timedelta(days=14)).isoformat()

    prestamo = Prestamo(
        id=nuevo_id,
        libro_id=libro_id,
        usuario_id=usuario_id,
        fecha_prestamo=fecha_hoy,
        fecha_devolucion=fecha_devolucion,
        devuelto=False
    )

    if not self.prestamos.insertar(prestamo):
        return False

    # 5. Marcar el libro como no disponible
    libro.disponible = False
    self.libros.actualizar(libro)

    print(f"📚 Préstamo registrado: '{libro.titulo}' → {usuario.nombre}")
    return True
```

#### Otro Ejemplo: Devolver un libro

```python
def devolver_libro(self, prestamo_id: int) -> bool:
    """Registra la devolución de un libro."""

    # Buscar el préstamo
    prestamo = self.prestamos.consultar_por_id(prestamo_id)
    if prestamo is None:
        print(f"❌ Préstamo {prestamo_id} no encontrado")
        return False

    if prestamo.devuelto:
        print(f"❌ Este préstamo ya fue devuelto")
        return False

    # Buscar el libro
    libro = self.buscar_libro(prestamo.libro_id)
    if libro is None:
        return False

    # Actualizar el préstamo
    prestamo.devuelto = True
    self.prestamos.actualizar(prestamo)

    # Marcar el libro como disponible
    libro.disponible = True
    self.libros.actualizar(libro)

    print(f"✅ Libro '{libro.titulo}' devuelto correctamente")
    return True
```

#### 📝 Checklist:

Tu método de relación debe:
- [ ] Verificar que las entidades relacionadas existan
- [ ] Realizar validaciones (stock, disponibilidad, etc.)
- [ ] Crear una instancia de la tercera entidad
- [ ] Actualizar el estado de las otras entidades si es necesario
- [ ] Guardar todo usando los repositorios
- [ ] Retornar True si fue exitoso, False si hubo error
- [ ] Imprimir mensajes informativos

---

### PASO 5: Implementar Reportes (10 minutos)

Busca donde dice `PASO 5: IMPLEMENTAR REPORTES`.

```python
def mostrar_resumen(self) -> None:
    """Muestra un resumen del sistema."""
    super().mostrar_resumen()

    total_libros = self.libros.contar()
    total_usuarios = self.usuarios.contar()
    total_prestamos = self.prestamos.contar()
    libros_disponibles = len(self.libros_disponibles())

    print(f"   📚 Libros en catálogo: {total_libros}")
    print(f"   ✅ Libros disponibles: {libros_disponibles}")
    print(f"   👥 Usuarios registrados: {total_usuarios}")
    print(f"   📖 Préstamos activos: {total_prestamos}")
    print(f"{'='*60}\n")
```

#### 📝 Checklist:

- [ ] Implementa `mostrar_resumen()`
- [ ] Muestra contadores de cada entidad
- [ ] (Opcional) Muestra estadísticas adicionales

---

### PASO 6: Función Principal (15-20 minutos)

Busca donde dice `PASO 6: FUNCIÓN PRINCIPAL`.

```python
def main():
    """Función principal que demuestra el sistema."""

    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           📚 SISTEMA DE GESTIÓN DE BIBLIOTECA               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)

    # Crear el sistema
    biblioteca = SistemaBiblioteca()

    # ========== AGREGAR DATOS DE EJEMPLO ==========
    print("\n📥 Agregando datos de ejemplo...")

    # Agregar libros
    libro1 = Libro(1, "Cien Años de Soledad", "Gabriel García Márquez", "978-0-307", True)
    libro2 = Libro(2, "Don Quijote", "Miguel de Cervantes", "978-0-060", True)
    libro3 = Libro(3, "El Principito", "Antoine de Saint-Exupéry", "978-0-156", True)

    biblioteca.agregar_libro(libro1)
    biblioteca.agregar_libro(libro2)
    biblioteca.agregar_libro(libro3)

    # Agregar usuarios
    usuario1 = Usuario(1, "Ana García", "ana@email.com", "555-0101")
    usuario2 = Usuario(2, "Carlos López", "carlos@email.com", "555-0102")

    biblioteca.agregar_usuario(usuario1)
    biblioteca.agregar_usuario(usuario2)

    # ========== REALIZAR OPERACIONES ==========
    print("\n🔄 Realizando operaciones...")

    # Ana pide prestado "Cien Años de Soledad"
    biblioteca.prestar_libro(libro_id=1, usuario_id=1)

    # Carlos pide prestado "El Principito"
    biblioteca.prestar_libro(libro_id=3, usuario_id=2)

    # ========== MOSTRAR REPORTES ==========

    biblioteca.mostrar_resumen()

    mostrar_tabla(biblioteca.listar_libros(), "Catálogo de Libros")
    mostrar_tabla(biblioteca.listar_usuarios(), "Usuarios Registrados")
    mostrar_tabla(biblioteca.prestamos.consultar_todos(), "Préstamos Activos")

    print("\n📊 Libros disponibles para préstamo:")
    for libro in biblioteca.libros_disponibles():
        print(f"   • {libro.titulo} - {libro.autor}")

    # Mostrar bitácoras
    print("\n📜 Últimas operaciones sobre libros:")
    biblioteca.libros.mostrar_bitacora(ultimas=5)

    # Estadísticas
    biblioteca.libros.mostrar_estadisticas()

    print("\n✅ ¡Sistema completado!")
    print(f"📁 Revisa la carpeta 'datos/biblioteca' para ver los archivos JSON")


if __name__ == "__main__":
    main()
```

#### 📝 Checklist:

- [ ] Crea el sistema
- [ ] Agrega al menos 3 instancias de cada entidad
- [ ] Realiza operaciones que relacionen las entidades
- [ ] Muestra el resumen
- [ ] Lista todas las entidades con `mostrar_tabla()`
- [ ] Realiza consultas filtradas
- [ ] Muestra bitácoras
- [ ] Muestra estadísticas

---

## ▶️ Ejecutar tu Desafío

```bash
# Desde la raíz del curso
python3 Semana_5/desafio/DESAFIO.py
```

---

## ✅ Checklist Final

Antes de entregar, verifica que:

### Código
- [ ] Definiste 3 entidades diferentes y coherentes
- [ ] Cada entidad tiene al menos 4 campos (incluyendo `id`)
- [ ] Implementaste `validar()` en cada entidad con al menos 2 validaciones
- [ ] Creaste tu sistema de gestión con 3 repositorios
- [ ] Implementaste métodos para agregar cada tipo de entidad
- [ ] Implementaste métodos para listar/buscar entidades
- [ ] Creaste **al menos UN método** que relacione las entidades
- [ ] La función `main()` tiene datos de ejemplo (mínimo 3 de cada tipo)

### Funcionalidad
- [ ] El programa se ejecuta sin errores
- [ ] Se crean archivos JSON en `datos/tu_sistema/`
- [ ] Los archivos JSON tienen datos válidos y legibles
- [ ] La bitácora registra las operaciones
- [ ] El resumen muestra estadísticas correctas

### Documentación
- [ ] Cambiaste todos los nombres genéricos por nombres específicos
- [ ] Agregaste docstrings a tus clases y métodos
- [ ] Los comentarios explican la lógica compleja
- [ ] El sistema tiene sentido y las entidades están bien relacionadas

---

## 📊 Criterios de Evaluación

| Criterio | Puntos | Descripción |
|----------|--------|-------------|
| **Entidades** | 30% | 3 entidades bien definidas con validaciones |
| **Repositorios** | 15% | Correcta creación y uso de repositorios |
| **Operaciones CRUD** | 20% | Implementación correcta de métodos básicos |
| **Relaciones** | 25% | Método(s) que relacionan las entidades |
| **Persistencia JSON** | 10% | Datos se guardan correctamente en JSON |

---

## 🆘 ¿Problemas?

### Error: "ModuleNotFoundError: No module named 'database_framework'"

**Solución**: Asegúrate de ejecutar desde la raíz del curso:
```bash
python3 Semana_5/desafio/DESAFIO.py
```

### Error: "TypeError: 'type' object is not subscriptable"

**Solución**: Usa Python 3.10 o superior, o cambia:
```python
def buscar(self) -> Libro | None:  # ❌ Python < 3.10
```
Por:
```python
from typing import Optional
def buscar(self) -> Optional[Libro]:  # ✅ Python >= 3.7
```

### Los archivos JSON no se crean

**Solución**: Verifica que:
1. Estés llamando a los métodos `insertar()` de los repositorios
2. Los datos pasen las validaciones
3. Tengas permisos de escritura en la carpeta

---

## 💡 Ideas para Extender el Desafío (Opcional)

Si terminas rápido, intenta agregar:

1. **Método para eliminar**: Implementa eliminación de entidades
2. **Búsquedas avanzadas**: Filtra por múltiples criterios
3. **Actualización de datos**: Permite modificar entidades existentes
4. **Reportes avanzados**: Estadísticas más detalladas
5. **Validaciones complejas**: Reglas de negocio más sofisticadas
6. **Manejo de errores**: Usa try/except para capturar errores
7. **Interfaz de usuario**: Crea un menú interactivo con input()

---

## 📚 Recursos

- [CONCEPTOS_CLAVE.md](../CONCEPTOS_CLAVE.md) - Explicación de @dataclass, herencia, etc.
- [ejemplo_tienda.py](../ejemplo/ejemplo_tienda.py) - Ejemplo completo de referencia
- [Documentación de dataclasses](https://docs.python.org/3/library/dataclasses.html)
- [Documentación de JSON](https://docs.python.org/3/library/json.html)

---

**¡Mucha suerte con tu desafío! 🚀**

Si tienes dudas, revisa el ejemplo completo o consulta la documentación de conceptos clave.
