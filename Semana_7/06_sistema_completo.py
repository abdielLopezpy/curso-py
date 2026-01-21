# ============================================================================
# PASO 6: Sistema Completo con ORM
# ============================================================================
# Este archivo demuestra lo FÁCIL que es crear un sistema completo con ORM.
# Compara con el sistema de la Semana 6 (SQL manual) - ¡mucho menos código!
# ============================================================================

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import declarative_base, Session, relationship
from datetime import datetime
import os

Base = declarative_base()

# ============================================================================
# MODELOS - Definimos nuestras tablas como clases Python
# ============================================================================

class Categoria(Base):
    """Modelo de Categoría."""
    __tablename__ = 'categorias'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(String(500))
    activa = Column(Boolean, default=True)

    # Relación con productos
    productos = relationship("Producto", back_populates="categoria")

    def __repr__(self):
        return f"<Categoria({self.nombre})>"


class Producto(Base):
    """Modelo de Producto."""
    __tablename__ = 'productos'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    categoria_id = Column(Integer, ForeignKey('categorias.id'))
    creado_en = Column(DateTime, default=datetime.now)

    # Relación con categoría
    categoria = relationship("Categoria", back_populates="productos")

    def __repr__(self):
        return f"<Producto({self.nombre}, ${self.precio})>"


class Cliente(Base):
    """Modelo de Cliente."""
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    telefono = Column(String(20))
    registrado_en = Column(DateTime, default=datetime.now)

    # Relación con ventas
    ventas = relationship("Venta", back_populates="cliente")

    def __repr__(self):
        return f"<Cliente({self.nombre})>"


class Venta(Base):
    """Modelo de Venta."""
    __tablename__ = 'ventas'

    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    producto_id = Column(Integer, ForeignKey('productos.id'))
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    fecha = Column(DateTime, default=datetime.now)

    # Relaciones
    cliente = relationship("Cliente", back_populates="ventas")
    producto = relationship("Producto")

    def __repr__(self):
        return f"<Venta(#{self.id}, ${self.total})>"


# ============================================================================
# SISTEMA DE TIENDA - ¡Mira qué simple es con ORM!
# ============================================================================

class TiendaORM:
    """
    Sistema de gestión de tienda usando ORM.

    Compara con la Semana 6:
    - NO escribimos SQL
    - NO mapeamos filas a objetos manualmente
    - NO manejamos conexiones complicadas
    """

    def __init__(self, db_path: str = "datos/tienda_orm.db"):
        """Inicializa el sistema."""
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.engine = create_engine(f'sqlite:///{db_path}', echo=False)
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)

    def cerrar(self):
        """Cierra la sesión."""
        self.session.close()

    # =========================================================================
    # CATEGORÍAS - CRUD en pocas líneas
    # =========================================================================

    def crear_categoria(self, nombre: str, descripcion: str = "") -> Categoria:
        """Crea una nueva categoría."""
        categoria = Categoria(nombre=nombre, descripcion=descripcion)
        self.session.add(categoria)
        self.session.commit()
        return categoria

    def obtener_categorias(self):
        """Obtiene todas las categorías activas."""
        return self.session.query(Categoria).filter(Categoria.activa == True).all()

    def obtener_categoria(self, id: int):
        """Obtiene una categoría por ID."""
        return self.session.get(Categoria, id)

    # =========================================================================
    # PRODUCTOS - Operaciones simples
    # =========================================================================

    def crear_producto(self, nombre: str, precio: float, stock: int, categoria_id: int) -> Producto:
        """Crea un nuevo producto."""
        producto = Producto(
            nombre=nombre,
            precio=precio,
            stock=stock,
            categoria_id=categoria_id
        )
        self.session.add(producto)
        self.session.commit()
        return producto

    def obtener_productos(self):
        """Obtiene todos los productos."""
        return self.session.query(Producto).all()

    def obtener_producto(self, id: int):
        """Obtiene un producto por ID."""
        return self.session.get(Producto, id)

    def buscar_productos(self, termino: str):
        """Busca productos por nombre."""
        return self.session.query(Producto).filter(
            Producto.nombre.ilike(f"%{termino}%")
        ).all()

    def actualizar_stock(self, producto_id: int, cantidad: int):
        """Actualiza el stock de un producto."""
        producto = self.session.get(Producto, producto_id)
        if producto:
            producto.stock += cantidad
            self.session.commit()
        return producto

    def productos_por_categoria(self, categoria_id: int):
        """Obtiene productos de una categoría."""
        return self.session.query(Producto).filter(
            Producto.categoria_id == categoria_id
        ).all()

    def productos_bajo_stock(self, minimo: int = 10):
        """Obtiene productos con stock bajo."""
        return self.session.query(Producto).filter(
            Producto.stock < minimo
        ).order_by(Producto.stock).all()

    # =========================================================================
    # CLIENTES
    # =========================================================================

    def crear_cliente(self, nombre: str, email: str, telefono: str = "") -> Cliente:
        """Crea un nuevo cliente."""
        cliente = Cliente(nombre=nombre, email=email, telefono=telefono)
        self.session.add(cliente)
        self.session.commit()
        return cliente

    def obtener_clientes(self):
        """Obtiene todos los clientes."""
        return self.session.query(Cliente).all()

    def obtener_cliente(self, id: int):
        """Obtiene un cliente por ID."""
        return self.session.get(Cliente, id)

    def buscar_cliente_por_email(self, email: str):
        """Busca un cliente por email."""
        return self.session.query(Cliente).filter(Cliente.email == email).first()

    # =========================================================================
    # VENTAS - La lógica de negocio es clara
    # =========================================================================

    def registrar_venta(self, cliente_id: int, producto_id: int, cantidad: int) -> Venta:
        """
        Registra una venta.

        Compara con SQL manual:
        - NO escribimos INSERT INTO ventas...
        - NO actualizamos stock con UPDATE productos...
        - NO hacemos múltiples commits manuales
        """
        # Obtener producto y cliente
        producto = self.session.get(Producto, producto_id)
        cliente = self.session.get(Cliente, cliente_id)

        if not producto:
            raise ValueError("Producto no encontrado")
        if not cliente:
            raise ValueError("Cliente no encontrado")
        if producto.stock < cantidad:
            raise ValueError(f"Stock insuficiente. Disponible: {producto.stock}")

        # Crear la venta
        venta = Venta(
            cliente_id=cliente_id,
            producto_id=producto_id,
            cantidad=cantidad,
            precio_unitario=producto.precio,
            total=producto.precio * cantidad
        )

        # Actualizar stock
        producto.stock -= cantidad

        # Guardar todo
        self.session.add(venta)
        self.session.commit()

        return venta

    def ventas_de_cliente(self, cliente_id: int):
        """Obtiene las ventas de un cliente."""
        return self.session.query(Venta).filter(
            Venta.cliente_id == cliente_id
        ).order_by(Venta.fecha.desc()).all()

    def historial_ventas(self, limite: int = 10):
        """Obtiene las últimas ventas."""
        return self.session.query(Venta).order_by(
            Venta.fecha.desc()
        ).limit(limite).all()

    # =========================================================================
    # REPORTES - Consultas agregadas fáciles
    # =========================================================================

    def reporte_inventario(self):
        """Genera reporte del inventario."""
        total_productos = self.session.query(func.count(Producto.id)).scalar()
        valor_total = self.session.query(
            func.sum(Producto.precio * Producto.stock)
        ).scalar() or 0

        # Productos por categoría
        por_categoria = self.session.query(
            Categoria.nombre,
            func.count(Producto.id).label('cantidad'),
            func.sum(Producto.stock).label('stock_total')
        ).join(Producto).group_by(Categoria.id).all()

        return {
            'total_productos': total_productos,
            'valor_inventario': valor_total,
            'por_categoria': por_categoria
        }

    def reporte_ventas(self):
        """Genera reporte de ventas."""
        total_ventas = self.session.query(func.count(Venta.id)).scalar()
        ingresos = self.session.query(func.sum(Venta.total)).scalar() or 0

        # Productos más vendidos
        mas_vendidos = self.session.query(
            Producto.nombre,
            func.sum(Venta.cantidad).label('unidades')
        ).join(Venta).group_by(Producto.id).order_by(
            func.sum(Venta.cantidad).desc()
        ).limit(5).all()

        return {
            'total_ventas': total_ventas,
            'ingresos_totales': ingresos,
            'mas_vendidos': mas_vendidos
        }


# ============================================================================
# MENÚ INTERACTIVO
# ============================================================================

def mostrar_menu():
    """Muestra el menú principal."""
    print("\n" + "=" * 50)
    print("SISTEMA DE TIENDA CON ORM")
    print("=" * 50)
    print("1. Ver Productos")
    print("2. Agregar Producto")
    print("3. Buscar Producto")
    print("4. Ver Clientes")
    print("5. Registrar Venta")
    print("6. Historial de Ventas")
    print("7. Reportes")
    print("8. Agregar Datos de Ejemplo")
    print("0. Salir")
    print("-" * 50)


def main():
    """Función principal del sistema."""
    print("=" * 60)
    print("SISTEMA COMPLETO CON ORM")
    print("=" * 60)
    print("""
    Este sistema demuestra lo fácil que es trabajar con ORM:

    - Los modelos son clases Python simples
    - No escribimos SQL
    - Las relaciones funcionan automáticamente
    - El código es limpio y mantenible

    Compara con el sistema de la Semana 6 (SQL manual):
    - ¡Mucho menos código!
    - ¡Más fácil de entender!
    - ¡Menos errores!
    """)

    tienda = TiendaORM()

    try:
        while True:
            mostrar_menu()
            opcion = input("Opción: ").strip()

            if opcion == "1":
                # Ver productos
                print("\n" + "-" * 40)
                print("PRODUCTOS")
                print("-" * 40)
                productos = tienda.obtener_productos()
                if productos:
                    print(f"{'ID':<5} {'Nombre':<25} {'Precio':>10} {'Stock':>8} {'Categoría':<15}")
                    print("-" * 70)
                    for p in productos:
                        cat = p.categoria.nombre if p.categoria else "Sin categoría"
                        print(f"{p.id:<5} {p.nombre:<25} ${p.precio:>9.2f} {p.stock:>8} {cat:<15}")
                else:
                    print("No hay productos. Usa opción 8 para agregar datos de ejemplo.")

            elif opcion == "2":
                # Agregar producto
                print("\n--- Agregar Producto ---")
                nombre = input("Nombre: ").strip()
                precio = float(input("Precio: "))
                stock = int(input("Stock: "))

                categorias = tienda.obtener_categorias()
                if categorias:
                    print("\nCategorías:")
                    for c in categorias:
                        print(f"  {c.id}. {c.nombre}")
                    cat_id = int(input("ID Categoría: "))
                else:
                    print("No hay categorías. Creando 'General'...")
                    cat = tienda.crear_categoria("General", "Categoría general")
                    cat_id = cat.id

                producto = tienda.crear_producto(nombre, precio, stock, cat_id)
                print(f"Producto creado: {producto}")

            elif opcion == "3":
                # Buscar producto
                termino = input("\nBuscar: ").strip()
                productos = tienda.buscar_productos(termino)
                print(f"\nResultados para '{termino}':")
                for p in productos:
                    print(f"  - [{p.id}] {p.nombre}: ${p.precio:.2f}")

            elif opcion == "4":
                # Ver clientes
                print("\n" + "-" * 40)
                print("CLIENTES")
                print("-" * 40)
                clientes = tienda.obtener_clientes()
                if clientes:
                    for c in clientes:
                        print(f"  {c.id}. {c.nombre}")
                        print(f"     Email: {c.email}")
                        print(f"     Compras: {len(c.ventas)}")
                else:
                    print("No hay clientes. Usa opción 8 para agregar datos de ejemplo.")

            elif opcion == "5":
                # Registrar venta
                print("\n--- Registrar Venta ---")
                cliente_id = int(input("ID Cliente: "))
                producto_id = int(input("ID Producto: "))
                cantidad = int(input("Cantidad: "))

                try:
                    venta = tienda.registrar_venta(cliente_id, producto_id, cantidad)
                    print(f"Venta registrada: {venta}")
                    print(f"Total: ${venta.total:.2f}")
                except ValueError as e:
                    print(f"Error: {e}")

            elif opcion == "6":
                # Historial de ventas
                print("\n" + "-" * 40)
                print("HISTORIAL DE VENTAS")
                print("-" * 40)
                ventas = tienda.historial_ventas()
                if ventas:
                    for v in ventas:
                        print(f"  #{v.id} | {v.fecha.strftime('%Y-%m-%d %H:%M')}")
                        print(f"       Cliente: {v.cliente.nombre}")
                        print(f"       Producto: {v.producto.nombre} x{v.cantidad}")
                        print(f"       Total: ${v.total:.2f}")
                else:
                    print("No hay ventas registradas.")

            elif opcion == "7":
                # Reportes
                print("\n" + "-" * 40)
                print("REPORTES")
                print("-" * 40)

                inv = tienda.reporte_inventario()
                print(f"\nINVENTARIO:")
                print(f"  Total productos: {inv['total_productos']}")
                print(f"  Valor total: ${inv['valor_inventario']:.2f}")
                print(f"\n  Por categoría:")
                for nombre, cant, stock in inv['por_categoria']:
                    print(f"    - {nombre}: {cant} productos, {stock} unidades")

                vent = tienda.reporte_ventas()
                print(f"\nVENTAS:")
                print(f"  Total ventas: {vent['total_ventas']}")
                print(f"  Ingresos: ${vent['ingresos_totales']:.2f}")
                if vent['mas_vendidos']:
                    print(f"\n  Más vendidos:")
                    for nombre, unidades in vent['mas_vendidos']:
                        print(f"    - {nombre}: {unidades} unidades")

                bajo_stock = tienda.productos_bajo_stock()
                if bajo_stock:
                    print(f"\n  ALERTA - Stock bajo:")
                    for p in bajo_stock:
                        print(f"    - {p.nombre}: {p.stock} unidades")

            elif opcion == "8":
                # Datos de ejemplo
                print("\nAgregando datos de ejemplo...")

                # Categorías
                cat1 = tienda.crear_categoria("Electrónica", "Dispositivos electrónicos")
                cat2 = tienda.crear_categoria("Ropa", "Vestimenta")
                cat3 = tienda.crear_categoria("Hogar", "Artículos del hogar")
                print("  Categorías creadas")

                # Productos
                tienda.crear_producto("Laptop Gaming", 1299.99, 10, cat1.id)
                tienda.crear_producto("Smartphone", 799.99, 25, cat1.id)
                tienda.crear_producto("Auriculares BT", 89.99, 50, cat1.id)
                tienda.crear_producto("Camiseta", 29.99, 100, cat2.id)
                tienda.crear_producto("Pantalón", 49.99, 60, cat2.id)
                tienda.crear_producto("Lámpara LED", 34.99, 8, cat3.id)
                print("  Productos creados")

                # Clientes
                tienda.crear_cliente("Ana García", "ana@email.com", "555-1234")
                tienda.crear_cliente("Luis Pérez", "luis@email.com", "555-5678")
                print("  Clientes creados")

                print("Datos de ejemplo agregados.")

            elif opcion == "0":
                print("\n¡Hasta luego!")
                break

            else:
                print("Opción no válida")

    finally:
        tienda.cerrar()


# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

if __name__ == "__main__":
    iniciar = input("¿Iniciar el sistema? (s/n): ").strip().lower()
    if iniciar == 's':
        main()
    else:
        print("""
Puedes revisar el código para ver cómo funciona el ORM.

COMPARACIÓN CON SEMANA 6 (SQL Manual):

Semana 6 - SQL Manual:
    cursor.execute("INSERT INTO productos (nombre, precio) VALUES (?, ?)", ...)
    cursor.execute("SELECT * FROM productos WHERE id = ?", (id,))
    fila = cursor.fetchone()
    producto = Producto(id=fila['id'], nombre=fila['nombre'], ...)

Semana 7 - Con ORM:
    session.add(producto)
    session.commit()
    producto = session.get(Producto, id)

¡El ORM hace todo el trabajo pesado por ti!
        """)

    print("\n" + "=" * 60)
    print("FIN DE LA SEMANA 7: ORM")
    print("=" * 60)
