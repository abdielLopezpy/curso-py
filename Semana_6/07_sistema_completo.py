# ============================================================================
# PASO 7: Sistema Completo con SQLite
# ============================================================================
# En este archivo construiremos un sistema de gestión completo
# que integra todo lo aprendido:
# - Clases y POO
# - CRUD completo
# - Relaciones entre tablas
# - Menú interactivo
# ============================================================================

import sqlite3
from dataclasses import dataclass
from typing import List, Optional
import os

# ============================================================================
# MODELO DE DATOS (Dataclasses)
# ============================================================================

@dataclass
class Categoria:
    id: Optional[int] = None
    nombre: str = ""
    descripcion: str = ""
    activa: bool = True


@dataclass
class Producto:
    id: Optional[int] = None
    nombre: str = ""
    precio: float = 0.0
    stock: int = 0
    categoria_id: Optional[int] = None


@dataclass
class Cliente:
    id: Optional[int] = None
    nombre: str = ""
    email: str = ""
    telefono: str = ""


# ============================================================================
# CLASE DATABASE - Manejo de conexión
# ============================================================================

class Database:
    """Clase para manejar la conexión a la base de datos."""

    def __init__(self, db_path: str = "datos/sistema_tienda.db"):
        """Inicializa la conexión a la base de datos."""
        # Crear carpeta si no existe
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.conexion = None
        self.cursor = None

    def conectar(self):
        """Abre la conexión a la base de datos."""
        self.conexion = sqlite3.connect(self.db_path)
        self.conexion.row_factory = sqlite3.Row  # Para acceder por nombre
        self.cursor = self.conexion.cursor()
        # Habilitar claves foráneas
        self.cursor.execute("PRAGMA foreign_keys = ON")
        return self

    def desconectar(self):
        """Cierra la conexión a la base de datos."""
        if self.conexion:
            self.conexion.close()

    def __enter__(self):
        """Permite usar 'with' para la conexión."""
        return self.conectar()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cierra al salir del bloque 'with'."""
        self.desconectar()

    def crear_tablas(self):
        """Crea las tablas si no existen."""
        # Tabla categorías
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                descripcion TEXT,
                activa INTEGER DEFAULT 1
            )
        """)

        # Tabla productos
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                precio REAL NOT NULL CHECK(precio >= 0),
                stock INTEGER DEFAULT 0 CHECK(stock >= 0),
                categoria_id INTEGER,
                FOREIGN KEY (categoria_id) REFERENCES categorias(id)
            )
        """)

        # Tabla clientes
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                telefono TEXT
            )
        """)

        self.conexion.commit()
        print("✅ Tablas creadas/verificadas correctamente")


# ============================================================================
# REPOSITORIO DE CATEGORÍAS
# ============================================================================

class CategoriaRepo:
    """Repositorio para operaciones CRUD de Categorías."""

    def __init__(self, db: Database):
        self.db = db

    def crear(self, categoria: Categoria) -> int:
        """Crea una nueva categoría. Retorna el ID."""
        self.db.cursor.execute("""
            INSERT INTO categorias (nombre, descripcion, activa)
            VALUES (?, ?, ?)
        """, (categoria.nombre, categoria.descripcion, categoria.activa))
        self.db.conexion.commit()
        return self.db.cursor.lastrowid

    def obtener_por_id(self, id: int) -> Optional[Categoria]:
        """Obtiene una categoría por su ID."""
        self.db.cursor.execute(
            "SELECT * FROM categorias WHERE id = ?", (id,)
        )
        fila = self.db.cursor.fetchone()
        if fila:
            return Categoria(
                id=fila['id'],
                nombre=fila['nombre'],
                descripcion=fila['descripcion'],
                activa=bool(fila['activa'])
            )
        return None

    def obtener_todas(self) -> List[Categoria]:
        """Obtiene todas las categorías."""
        self.db.cursor.execute("SELECT * FROM categorias ORDER BY nombre")
        return [
            Categoria(
                id=f['id'],
                nombre=f['nombre'],
                descripcion=f['descripcion'],
                activa=bool(f['activa'])
            )
            for f in self.db.cursor.fetchall()
        ]

    def actualizar(self, categoria: Categoria) -> bool:
        """Actualiza una categoría existente."""
        self.db.cursor.execute("""
            UPDATE categorias
            SET nombre = ?, descripcion = ?, activa = ?
            WHERE id = ?
        """, (categoria.nombre, categoria.descripcion,
              categoria.activa, categoria.id))
        self.db.conexion.commit()
        return self.db.cursor.rowcount > 0

    def eliminar(self, id: int) -> bool:
        """Elimina una categoría por su ID."""
        self.db.cursor.execute("DELETE FROM categorias WHERE id = ?", (id,))
        self.db.conexion.commit()
        return self.db.cursor.rowcount > 0


# ============================================================================
# REPOSITORIO DE PRODUCTOS
# ============================================================================

class ProductoRepo:
    """Repositorio para operaciones CRUD de Productos."""

    def __init__(self, db: Database):
        self.db = db

    def crear(self, producto: Producto) -> int:
        """Crea un nuevo producto. Retorna el ID."""
        self.db.cursor.execute("""
            INSERT INTO productos (nombre, precio, stock, categoria_id)
            VALUES (?, ?, ?, ?)
        """, (producto.nombre, producto.precio,
              producto.stock, producto.categoria_id))
        self.db.conexion.commit()
        return self.db.cursor.lastrowid

    def obtener_por_id(self, id: int) -> Optional[Producto]:
        """Obtiene un producto por su ID."""
        self.db.cursor.execute(
            "SELECT * FROM productos WHERE id = ?", (id,)
        )
        fila = self.db.cursor.fetchone()
        if fila:
            return Producto(
                id=fila['id'],
                nombre=fila['nombre'],
                precio=fila['precio'],
                stock=fila['stock'],
                categoria_id=fila['categoria_id']
            )
        return None

    def obtener_todos(self) -> List[Producto]:
        """Obtiene todos los productos."""
        self.db.cursor.execute("SELECT * FROM productos ORDER BY nombre")
        return [
            Producto(
                id=f['id'],
                nombre=f['nombre'],
                precio=f['precio'],
                stock=f['stock'],
                categoria_id=f['categoria_id']
            )
            for f in self.db.cursor.fetchall()
        ]

    def obtener_con_categoria(self) -> List[dict]:
        """Obtiene productos con nombre de categoría."""
        self.db.cursor.execute("""
            SELECT p.*, c.nombre as categoria_nombre
            FROM productos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            ORDER BY p.nombre
        """)
        return [dict(row) for row in self.db.cursor.fetchall()]

    def buscar_por_nombre(self, termino: str) -> List[Producto]:
        """Busca productos por nombre."""
        self.db.cursor.execute(
            "SELECT * FROM productos WHERE nombre LIKE ?",
            (f"%{termino}%",)
        )
        return [
            Producto(
                id=f['id'],
                nombre=f['nombre'],
                precio=f['precio'],
                stock=f['stock'],
                categoria_id=f['categoria_id']
            )
            for f in self.db.cursor.fetchall()
        ]

    def actualizar(self, producto: Producto) -> bool:
        """Actualiza un producto existente."""
        self.db.cursor.execute("""
            UPDATE productos
            SET nombre = ?, precio = ?, stock = ?, categoria_id = ?
            WHERE id = ?
        """, (producto.nombre, producto.precio, producto.stock,
              producto.categoria_id, producto.id))
        self.db.conexion.commit()
        return self.db.cursor.rowcount > 0

    def eliminar(self, id: int) -> bool:
        """Elimina un producto por su ID."""
        self.db.cursor.execute("DELETE FROM productos WHERE id = ?", (id,))
        self.db.conexion.commit()
        return self.db.cursor.rowcount > 0


# ============================================================================
# REPOSITORIO DE CLIENTES
# ============================================================================

class ClienteRepo:
    """Repositorio para operaciones CRUD de Clientes."""

    def __init__(self, db: Database):
        self.db = db

    def crear(self, cliente: Cliente) -> int:
        """Crea un nuevo cliente. Retorna el ID."""
        self.db.cursor.execute("""
            INSERT INTO clientes (nombre, email, telefono)
            VALUES (?, ?, ?)
        """, (cliente.nombre, cliente.email, cliente.telefono))
        self.db.conexion.commit()
        return self.db.cursor.lastrowid

    def obtener_todos(self) -> List[Cliente]:
        """Obtiene todos los clientes."""
        self.db.cursor.execute("SELECT * FROM clientes ORDER BY nombre")
        return [
            Cliente(
                id=f['id'],
                nombre=f['nombre'],
                email=f['email'],
                telefono=f['telefono']
            )
            for f in self.db.cursor.fetchall()
        ]


# ============================================================================
# SISTEMA DE TIENDA (Menú Interactivo)
# ============================================================================

class SistemaTienda:
    """Sistema de gestión de tienda con menú interactivo."""

    def __init__(self):
        self.db = Database()
        self.categoria_repo = None
        self.producto_repo = None
        self.cliente_repo = None

    def inicializar(self):
        """Inicializa la base de datos y repositorios."""
        self.db.conectar()
        self.db.crear_tablas()
        self.categoria_repo = CategoriaRepo(self.db)
        self.producto_repo = ProductoRepo(self.db)
        self.cliente_repo = ClienteRepo(self.db)
        self._insertar_datos_ejemplo()

    def _insertar_datos_ejemplo(self):
        """Inserta datos de ejemplo si la BD está vacía."""
        # Verificar si hay datos
        self.db.cursor.execute("SELECT COUNT(*) FROM categorias")
        if self.db.cursor.fetchone()[0] > 0:
            return

        print("\n📦 Insertando datos de ejemplo...")

        # Categorías
        categorias = [
            Categoria(nombre="Electrónica", descripcion="Gadgets y dispositivos"),
            Categoria(nombre="Ropa", descripcion="Vestimenta"),
            Categoria(nombre="Hogar", descripcion="Artículos del hogar")
        ]
        for cat in categorias:
            self.categoria_repo.crear(cat)

        # Productos
        productos = [
            Producto(nombre="Laptop Gaming", precio=1299.99, stock=10, categoria_id=1),
            Producto(nombre="Smartphone", precio=799.99, stock=25, categoria_id=1),
            Producto(nombre="Audífonos BT", precio=89.99, stock=50, categoria_id=1),
            Producto(nombre="Camiseta", precio=29.99, stock=100, categoria_id=2),
            Producto(nombre="Pantalón", precio=49.99, stock=60, categoria_id=2),
            Producto(nombre="Lámpara LED", precio=34.99, stock=40, categoria_id=3)
        ]
        for prod in productos:
            self.producto_repo.crear(prod)

        # Clientes
        clientes = [
            Cliente(nombre="Ana García", email="ana@email.com", telefono="555-1234"),
            Cliente(nombre="Luis Pérez", email="luis@email.com", telefono="555-5678")
        ]
        for cli in clientes:
            self.cliente_repo.crear(cli)

        print("✅ Datos de ejemplo insertados")

    def limpiar_pantalla(self):
        """Limpia la pantalla de la terminal."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def mostrar_menu_principal(self):
        """Muestra el menú principal."""
        print("\n" + "=" * 50)
        print("🏪 SISTEMA DE GESTIÓN DE TIENDA")
        print("=" * 50)
        print("1. 📦 Gestionar Productos")
        print("2. 📁 Gestionar Categorías")
        print("3. 👥 Ver Clientes")
        print("4. 📊 Ver Reportes")
        print("0. 🚪 Salir")
        print("-" * 50)

    def menu_productos(self):
        """Submenú de productos."""
        while True:
            print("\n" + "-" * 40)
            print("📦 MENÚ PRODUCTOS")
            print("-" * 40)
            print("1. Ver todos los productos")
            print("2. Agregar producto")
            print("3. Buscar producto")
            print("4. Actualizar producto")
            print("5. Eliminar producto")
            print("0. Volver")

            opcion = input("\nOpción: ").strip()

            if opcion == "1":
                self.ver_productos()
            elif opcion == "2":
                self.agregar_producto()
            elif opcion == "3":
                self.buscar_producto()
            elif opcion == "4":
                self.actualizar_producto()
            elif opcion == "5":
                self.eliminar_producto()
            elif opcion == "0":
                break

    def ver_productos(self):
        """Muestra todos los productos."""
        productos = self.producto_repo.obtener_con_categoria()
        print("\n📦 LISTA DE PRODUCTOS")
        print("-" * 70)
        print(f"{'ID':<5} {'Nombre':<25} {'Precio':>10} {'Stock':>8} {'Categoría':<15}")
        print("-" * 70)
        for p in productos:
            cat = p['categoria_nombre'] or "Sin categoría"
            print(f"{p['id']:<5} {p['nombre']:<25} ${p['precio']:>9.2f} {p['stock']:>8} {cat:<15}")
        print("-" * 70)
        print(f"Total: {len(productos)} productos")

    def agregar_producto(self):
        """Agrega un nuevo producto."""
        print("\n➕ AGREGAR PRODUCTO")
        print("-" * 40)

        nombre = input("Nombre: ").strip()
        if not nombre:
            print("❌ El nombre es requerido")
            return

        try:
            precio = float(input("Precio: "))
            stock = int(input("Stock: "))
        except ValueError:
            print("❌ Precio y stock deben ser números")
            return

        # Mostrar categorías
        categorias = self.categoria_repo.obtener_todas()
        print("\nCategorías disponibles:")
        for c in categorias:
            print(f"  {c.id}. {c.nombre}")

        try:
            categoria_id = int(input("ID de categoría: "))
        except ValueError:
            categoria_id = None

        producto = Producto(
            nombre=nombre,
            precio=precio,
            stock=stock,
            categoria_id=categoria_id
        )

        id_nuevo = self.producto_repo.crear(producto)
        print(f"\n✅ Producto creado con ID: {id_nuevo}")

    def buscar_producto(self):
        """Busca productos por nombre."""
        termino = input("\nBuscar: ").strip()
        productos = self.producto_repo.buscar_por_nombre(termino)

        if productos:
            print(f"\n🔍 {len(productos)} resultados para '{termino}':")
            for p in productos:
                print(f"  [{p.id}] {p.nombre} - ${p.precio:.2f}")
        else:
            print("❌ No se encontraron productos")

    def actualizar_producto(self):
        """Actualiza un producto existente."""
        try:
            id_prod = int(input("\nID del producto a actualizar: "))
        except ValueError:
            print("❌ ID inválido")
            return

        producto = self.producto_repo.obtener_por_id(id_prod)
        if not producto:
            print("❌ Producto no encontrado")
            return

        print(f"\nProducto actual: {producto.nombre}")
        print(f"Precio: ${producto.precio:.2f}, Stock: {producto.stock}")
        print("\n(Deja vacío para mantener el valor actual)")

        nombre = input(f"Nuevo nombre [{producto.nombre}]: ").strip()
        precio_str = input(f"Nuevo precio [{producto.precio}]: ").strip()
        stock_str = input(f"Nuevo stock [{producto.stock}]: ").strip()

        if nombre:
            producto.nombre = nombre
        if precio_str:
            producto.precio = float(precio_str)
        if stock_str:
            producto.stock = int(stock_str)

        if self.producto_repo.actualizar(producto):
            print("✅ Producto actualizado")
        else:
            print("❌ No se pudo actualizar")

    def eliminar_producto(self):
        """Elimina un producto."""
        try:
            id_prod = int(input("\nID del producto a eliminar: "))
        except ValueError:
            print("❌ ID inválido")
            return

        producto = self.producto_repo.obtener_por_id(id_prod)
        if not producto:
            print("❌ Producto no encontrado")
            return

        confirmar = input(f"¿Eliminar '{producto.nombre}'? (s/n): ")
        if confirmar.lower() == 's':
            if self.producto_repo.eliminar(id_prod):
                print("✅ Producto eliminado")
            else:
                print("❌ No se pudo eliminar")

    def menu_categorias(self):
        """Submenú de categorías."""
        while True:
            print("\n" + "-" * 40)
            print("📁 MENÚ CATEGORÍAS")
            print("-" * 40)
            print("1. Ver categorías")
            print("2. Agregar categoría")
            print("0. Volver")

            opcion = input("\nOpción: ").strip()

            if opcion == "1":
                categorias = self.categoria_repo.obtener_todas()
                print("\n📁 CATEGORÍAS")
                print("-" * 40)
                for c in categorias:
                    estado = "✅" if c.activa else "❌"
                    print(f"  {c.id}. {c.nombre} {estado}")
                    if c.descripcion:
                        print(f"     {c.descripcion}")
            elif opcion == "2":
                nombre = input("Nombre: ").strip()
                desc = input("Descripción: ").strip()
                if nombre:
                    cat = Categoria(nombre=nombre, descripcion=desc)
                    id_nuevo = self.categoria_repo.crear(cat)
                    print(f"✅ Categoría creada con ID: {id_nuevo}")
            elif opcion == "0":
                break

    def ver_clientes(self):
        """Muestra todos los clientes."""
        clientes = self.cliente_repo.obtener_todos()
        print("\n👥 CLIENTES")
        print("-" * 50)
        for c in clientes:
            print(f"  {c.id}. {c.nombre}")
            print(f"     📧 {c.email} | 📞 {c.telefono}")
        print("-" * 50)
        print(f"Total: {len(clientes)} clientes")

    def ver_reportes(self):
        """Muestra reportes del sistema."""
        print("\n📊 REPORTES")
        print("-" * 50)

        # Total de productos
        self.db.cursor.execute("SELECT COUNT(*), SUM(precio * stock) FROM productos")
        total_prod, valor_inventario = self.db.cursor.fetchone()
        print(f"📦 Total productos: {total_prod}")
        print(f"💰 Valor del inventario: ${valor_inventario or 0:.2f}")

        # Productos por categoría
        self.db.cursor.execute("""
            SELECT c.nombre, COUNT(p.id) as total
            FROM categorias c
            LEFT JOIN productos p ON c.id = p.categoria_id
            GROUP BY c.id
        """)
        print("\n📁 Productos por categoría:")
        for nombre, total in self.db.cursor.fetchall():
            print(f"   {nombre}: {total}")

        # Productos con stock bajo
        self.db.cursor.execute(
            "SELECT nombre, stock FROM productos WHERE stock < 20"
        )
        bajo_stock = self.db.cursor.fetchall()
        if bajo_stock:
            print("\n⚠️ Productos con stock bajo (<20):")
            for nombre, stock in bajo_stock:
                print(f"   {nombre}: {stock} unidades")

    def ejecutar(self):
        """Ejecuta el sistema."""
        try:
            self.inicializar()

            while True:
                self.mostrar_menu_principal()
                opcion = input("Opción: ").strip()

                if opcion == "1":
                    self.menu_productos()
                elif opcion == "2":
                    self.menu_categorias()
                elif opcion == "3":
                    self.ver_clientes()
                elif opcion == "4":
                    self.ver_reportes()
                elif opcion == "0":
                    print("\n👋 ¡Hasta luego!")
                    break
                else:
                    print("❌ Opción no válida")

        finally:
            self.db.desconectar()


# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("🎓 PASO 7: Sistema Completo con SQLite")
    print("=" * 60)
    print("""
Este es un sistema de gestión de tienda completo que integra:
- Base de datos SQLite
- Programación Orientada a Objetos
- Patrón Repository
- CRUD completo
- Relaciones entre tablas
- Menú interactivo
""")

    iniciar = input("¿Deseas iniciar el sistema? (s/n): ").strip().lower()
    if iniciar == 's':
        sistema = SistemaTienda()
        sistema.ejecutar()
    else:
        print("\n📚 Puedes revisar el código para entender la estructura.")
        print("   Ejecuta nuevamente cuando estés listo.")

    print("\n" + "=" * 60)
    print("✅ ¡Felicidades! Has completado la Semana 6")
    print("=" * 60)
