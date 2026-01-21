# ============================================================================
# PASO 5: Consultas Avanzadas con ORM
# ============================================================================
# SQLAlchemy permite hacer consultas muy poderosas sin escribir SQL.
# ============================================================================

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, func, and_, or_, desc, asc
from sqlalchemy.orm import declarative_base, Session, relationship
from datetime import datetime, timedelta

Base = declarative_base()

# ============================================================================
# MODELOS
# ============================================================================

class Categoria(Base):
    __tablename__ = 'categorias'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    productos = relationship("Producto", back_populates="categoria")

    def __repr__(self):
        return f"<Categoria(nombre='{self.nombre}')>"


class Producto(Base):
    __tablename__ = 'productos'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    categoria_id = Column(Integer, ForeignKey('categorias.id'))
    creado_en = Column(DateTime, default=datetime.now)
    categoria = relationship("Categoria", back_populates="productos")

    def __repr__(self):
        return f"<Producto(nombre='{self.nombre}', precio={self.precio})>"


class Venta(Base):
    __tablename__ = 'ventas'
    id = Column(Integer, primary_key=True)
    producto_id = Column(Integer, ForeignKey('productos.id'))
    cantidad = Column(Integer, nullable=False)
    total = Column(Float, nullable=False)
    fecha = Column(DateTime, default=datetime.now)
    producto = relationship("Producto")

    def __repr__(self):
        return f"<Venta(producto_id={self.producto_id}, total={self.total})>"


# ============================================================================
# CONFIGURACIÓN
# ============================================================================

engine = create_engine('sqlite:///datos/consultas_avanzadas.db', echo=False)
Base.metadata.create_all(engine)

print("=" * 60)
print("CONSULTAS AVANZADAS CON ORM")
print("=" * 60)

with Session(engine) as session:

    # =========================================================================
    # CREAR DATOS DE EJEMPLO
    # =========================================================================
    print("\n" + "-" * 60)
    print("CREANDO DATOS DE EJEMPLO")
    print("-" * 60)

    # Categorías
    cat1 = Categoria(nombre="Electrónica")
    cat2 = Categoria(nombre="Ropa")
    cat3 = Categoria(nombre="Deportes")
    session.add_all([cat1, cat2, cat3])
    session.commit()

    # Productos
    productos = [
        Producto(nombre="Laptop", precio=1200, stock=10, categoria=cat1),
        Producto(nombre="Smartphone", precio=800, stock=25, categoria=cat1),
        Producto(nombre="Tablet", precio=450, stock=15, categoria=cat1),
        Producto(nombre="Auriculares", precio=80, stock=50, categoria=cat1),
        Producto(nombre="Cargador", precio=25, stock=100, categoria=cat1),
        Producto(nombre="Camiseta", precio=30, stock=200, categoria=cat2),
        Producto(nombre="Pantalón", precio=50, stock=150, categoria=cat2),
        Producto(nombre="Zapatos", precio=90, stock=80, categoria=cat2),
        Producto(nombre="Balón", precio=35, stock=60, categoria=cat3),
        Producto(nombre="Raqueta", precio=120, stock=30, categoria=cat3),
    ]
    session.add_all(productos)
    session.commit()

    # Ventas (algunas de días anteriores)
    ventas = [
        Venta(producto_id=1, cantidad=2, total=2400, fecha=datetime.now() - timedelta(days=5)),
        Venta(producto_id=2, cantidad=3, total=2400, fecha=datetime.now() - timedelta(days=3)),
        Venta(producto_id=3, cantidad=1, total=450, fecha=datetime.now() - timedelta(days=2)),
        Venta(producto_id=4, cantidad=5, total=400, fecha=datetime.now() - timedelta(days=1)),
        Venta(producto_id=1, cantidad=1, total=1200, fecha=datetime.now()),
        Venta(producto_id=6, cantidad=10, total=300, fecha=datetime.now()),
    ]
    session.add_all(ventas)
    session.commit()

    print(f"Creados: {len(productos)} productos y {len(ventas)} ventas")

    # =========================================================================
    # FILTROS BÁSICOS
    # =========================================================================
    print("\n" + "=" * 60)
    print("FILTROS BÁSICOS")
    print("=" * 60)

    # --- Igual a ---
    print("\n--- Filtro: precio == 800 ---")
    resultado = session.query(Producto).filter(Producto.precio == 800).all()
    for p in resultado:
        print(f"  - {p.nombre}: ${p.precio}")

    # --- Mayor/Menor que ---
    print("\n--- Filtro: precio > 100 ---")
    resultado = session.query(Producto).filter(Producto.precio > 100).all()
    for p in resultado:
        print(f"  - {p.nombre}: ${p.precio}")

    # --- Entre valores ---
    print("\n--- Filtro: precio entre 50 y 200 ---")
    resultado = session.query(Producto).filter(
        Producto.precio.between(50, 200)
    ).all()
    for p in resultado:
        print(f"  - {p.nombre}: ${p.precio}")

    # --- En una lista ---
    print("\n--- Filtro: precio IN (30, 50, 80) ---")
    resultado = session.query(Producto).filter(
        Producto.precio.in_([30, 50, 80])
    ).all()
    for p in resultado:
        print(f"  - {p.nombre}: ${p.precio}")

    # --- LIKE (búsqueda parcial) ---
    print("\n--- Filtro: nombre contiene 'a' ---")
    resultado = session.query(Producto).filter(
        Producto.nombre.like("%a%")
    ).all()
    for p in resultado:
        print(f"  - {p.nombre}")

    # --- ILIKE (insensible a mayúsculas) ---
    print("\n--- Filtro: nombre contiene 'LAPTOP' (case insensitive) ---")
    resultado = session.query(Producto).filter(
        Producto.nombre.ilike("%laptop%")
    ).all()
    for p in resultado:
        print(f"  - {p.nombre}")

    # =========================================================================
    # FILTROS COMBINADOS (AND, OR)
    # =========================================================================
    print("\n" + "=" * 60)
    print("FILTROS COMBINADOS (AND, OR)")
    print("=" * 60)

    # --- AND implícito ---
    print("\n--- AND: precio < 100 Y stock > 50 ---")
    resultado = session.query(Producto).filter(
        Producto.precio < 100,
        Producto.stock > 50
    ).all()
    for p in resultado:
        print(f"  - {p.nombre}: ${p.precio} (stock: {p.stock})")

    # --- AND explícito ---
    print("\n--- AND explícito ---")
    resultado = session.query(Producto).filter(
        and_(Producto.precio < 100, Producto.stock > 50)
    ).all()
    for p in resultado:
        print(f"  - {p.nombre}")

    # --- OR ---
    print("\n--- OR: precio < 50 O stock > 100 ---")
    resultado = session.query(Producto).filter(
        or_(Producto.precio < 50, Producto.stock > 100)
    ).all()
    for p in resultado:
        print(f"  - {p.nombre}: ${p.precio} (stock: {p.stock})")

    # =========================================================================
    # ORDENAMIENTO
    # =========================================================================
    print("\n" + "=" * 60)
    print("ORDENAMIENTO")
    print("=" * 60)

    # --- Ascendente ---
    print("\n--- Ordenar por precio (ascendente) ---")
    resultado = session.query(Producto).order_by(Producto.precio).limit(5).all()
    for p in resultado:
        print(f"  - {p.nombre}: ${p.precio}")

    # --- Descendente ---
    print("\n--- Ordenar por precio (descendente) ---")
    resultado = session.query(Producto).order_by(desc(Producto.precio)).limit(5).all()
    for p in resultado:
        print(f"  - {p.nombre}: ${p.precio}")

    # --- Múltiples columnas ---
    print("\n--- Ordenar por categoría, luego precio ---")
    resultado = session.query(Producto).order_by(
        Producto.categoria_id,
        desc(Producto.precio)
    ).all()
    for p in resultado:
        print(f"  - [{p.categoria.nombre}] {p.nombre}: ${p.precio}")

    # =========================================================================
    # FUNCIONES DE AGREGACIÓN
    # =========================================================================
    print("\n" + "=" * 60)
    print("FUNCIONES DE AGREGACIÓN")
    print("=" * 60)

    # --- COUNT ---
    print("\n--- COUNT: Total de productos ---")
    total = session.query(func.count(Producto.id)).scalar()
    print(f"  Total: {total} productos")

    # --- SUM ---
    print("\n--- SUM: Valor total del inventario ---")
    valor = session.query(func.sum(Producto.precio * Producto.stock)).scalar()
    print(f"  Valor del inventario: ${valor:,.2f}")

    # --- AVG ---
    print("\n--- AVG: Precio promedio ---")
    promedio = session.query(func.avg(Producto.precio)).scalar()
    print(f"  Precio promedio: ${promedio:.2f}")

    # --- MIN/MAX ---
    print("\n--- MIN/MAX: Precios ---")
    minimo = session.query(func.min(Producto.precio)).scalar()
    maximo = session.query(func.max(Producto.precio)).scalar()
    print(f"  Precio mínimo: ${minimo}")
    print(f"  Precio máximo: ${maximo}")

    # =========================================================================
    # GROUP BY
    # =========================================================================
    print("\n" + "=" * 60)
    print("GROUP BY - Agrupar resultados")
    print("=" * 60)

    print("\n--- Productos por categoría ---")
    resultado = session.query(
        Categoria.nombre,
        func.count(Producto.id).label('total'),
        func.avg(Producto.precio).label('precio_promedio')
    ).join(Producto).group_by(Categoria.id).all()

    for nombre, total, promedio in resultado:
        print(f"  {nombre}: {total} productos, promedio ${promedio:.2f}")

    print("\n--- Ventas por producto ---")
    resultado = session.query(
        Producto.nombre,
        func.sum(Venta.cantidad).label('unidades'),
        func.sum(Venta.total).label('total_ventas')
    ).join(Venta).group_by(Producto.id).order_by(desc('total_ventas')).all()

    for nombre, unidades, total in resultado:
        print(f"  {nombre}: {unidades} unidades, ${total:.2f}")

    # =========================================================================
    # HAVING (filtrar grupos)
    # =========================================================================
    print("\n" + "=" * 60)
    print("HAVING - Filtrar grupos")
    print("=" * 60)

    print("\n--- Categorías con más de 3 productos ---")
    resultado = session.query(
        Categoria.nombre,
        func.count(Producto.id).label('total')
    ).join(Producto).group_by(Categoria.id).having(
        func.count(Producto.id) > 3
    ).all()

    for nombre, total in resultado:
        print(f"  {nombre}: {total} productos")

    # =========================================================================
    # SUBQUERIES
    # =========================================================================
    print("\n" + "=" * 60)
    print("SUBQUERIES")
    print("=" * 60)

    print("\n--- Productos con precio mayor al promedio ---")
    # Subquery para obtener el precio promedio
    precio_promedio = session.query(func.avg(Producto.precio)).scalar_subquery()

    resultado = session.query(Producto).filter(
        Producto.precio > precio_promedio
    ).all()

    for p in resultado:
        print(f"  - {p.nombre}: ${p.precio}")

    # =========================================================================
    # JOINS EXPLÍCITOS
    # =========================================================================
    print("\n" + "=" * 60)
    print("JOINS")
    print("=" * 60)

    print("\n--- Productos con su categoría (INNER JOIN) ---")
    resultado = session.query(
        Producto.nombre,
        Categoria.nombre.label('categoria')
    ).join(Categoria).limit(5).all()

    for nombre, categoria in resultado:
        print(f"  - {nombre} -> {categoria}")

    print("\n--- Productos sin ventas (LEFT JOIN) ---")
    resultado = session.query(Producto).outerjoin(Venta).filter(
        Venta.id == None
    ).all()

    for p in resultado:
        print(f"  - {p.nombre}")

    # =========================================================================
    # PAGINACIÓN
    # =========================================================================
    print("\n" + "=" * 60)
    print("PAGINACIÓN")
    print("=" * 60)

    page_size = 3

    print(f"\n--- Página 1 (primeros {page_size}) ---")
    pagina1 = session.query(Producto).order_by(Producto.id).limit(page_size).all()
    for p in pagina1:
        print(f"  - [{p.id}] {p.nombre}")

    print(f"\n--- Página 2 (siguientes {page_size}) ---")
    pagina2 = session.query(Producto).order_by(Producto.id).offset(page_size).limit(page_size).all()
    for p in pagina2:
        print(f"  - [{p.id}] {p.nombre}")

print("\n" + "=" * 60)
print("RESUMEN: MÉTODOS DE CONSULTA")
print("=" * 60)
print("""
MÉTODOS DE FILTRADO:
  .filter(condicion)        - Filtrar resultados
  .filter_by(campo=valor)   - Filtrar por campo
  .first()                  - Primer resultado o None
  .one()                    - Exactamente un resultado
  .all()                    - Todos los resultados
  .count()                  - Contar resultados

OPERADORES DE FILTRO:
  ==, !=, <, >, <=, >=     - Comparación
  .like("%texto%")          - Búsqueda parcial
  .ilike("%texto%")         - Búsqueda case-insensitive
  .in_([lista])             - En una lista
  .between(a, b)            - Entre valores
  .is_(None)                - Es NULL
  .isnot(None)              - No es NULL

COMBINADORES:
  and_(c1, c2)              - Y lógico
  or_(c1, c2)               - O lógico
  not_(c)                   - Negación

ORDENAMIENTO:
  .order_by(campo)          - Ascendente
  .order_by(desc(campo))    - Descendente

AGREGACIÓN:
  func.count(campo)         - Contar
  func.sum(campo)           - Sumar
  func.avg(campo)           - Promedio
  func.min(campo)           - Mínimo
  func.max(campo)           - Máximo

AGRUPACIÓN:
  .group_by(campo)          - Agrupar
  .having(condicion)        - Filtrar grupos

PAGINACIÓN:
  .limit(n)                 - Limitar resultados
  .offset(n)                - Saltar n resultados
""")
