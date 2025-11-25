#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EJEMPLO COMPLETO: Sistema de Gestión de Tienda
===============================================

Este es un ejemplo COMPLETO y FUNCIONAL de cómo usar el framework
de base de datos JSON para crear un sistema de gestión de tienda.

El sistema maneja tres entidades:
1. Productos
2. Clientes
3. Ventas

Estudia este código para entender cómo crear tu propio sistema.
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import sys
from pathlib import Path
# Agregar la carpeta framework al path
sys.path.insert(0, str(Path(__file__).parent.parent / "framework"))

from database_framework import (
    Entidad,
    RepositorioJSON,
    SistemaGestion,
    validar_no_vacio,
    validar_positivo,
    mostrar_tabla
)


# ==================== DEFINICIÓN DE ENTIDADES ====================

@dataclass
class Producto(Entidad):
    """
    Entidad que representa un producto en la tienda.

    Atributos:
        id: Identificador único del producto
        nombre: Nombre del producto
        categoria: Categoría (ej: "Electrónica", "Ropa", etc.)
        precio: Precio unitario del producto
        stock: Cantidad disponible en inventario
    """
    id: int
    nombre: str
    categoria: str
    precio: float
    stock: int

    def obtener_id(self) -> int:
        return self.id

    @classmethod
    def desde_diccionario(cls, datos: Dict[str, Any]) -> Producto:
        return cls(**datos)

    def validar(self) -> bool:
        """Valida que el producto tenga datos correctos."""
        if not validar_no_vacio(self.nombre, "nombre"):
            return False
        if not validar_no_vacio(self.categoria, "categoría"):
            return False
        if not validar_positivo(self.precio, "precio"):
            return False
        if self.stock < 0:
            print("❌ Error: El stock no puede ser negativo")
            return False
        return True

    def tiene_stock(self) -> bool:
        """Verifica si hay stock disponible."""
        return self.stock > 0

    def descontar_stock(self, cantidad: int) -> bool:
        """Descuenta stock si hay suficiente disponible."""
        if self.stock >= cantidad:
            self.stock -= cantidad
            return True
        return False


@dataclass
class Cliente(Entidad):
    """
    Entidad que representa un cliente de la tienda.

    Atributos:
        id: Identificador único del cliente
        nombre: Nombre completo del cliente
        email: Correo electrónico
        telefono: Número de teléfono
        ciudad: Ciudad de residencia
    """
    id: int
    nombre: str
    email: str
    telefono: str
    ciudad: str

    def obtener_id(self) -> int:
        return self.id

    @classmethod
    def desde_diccionario(cls, datos: Dict[str, Any]) -> Cliente:
        return cls(**datos)

    def validar(self) -> bool:
        """Valida que el cliente tenga datos correctos."""
        if not validar_no_vacio(self.nombre, "nombre"):
            return False
        if not validar_no_vacio(self.email, "email"):
            return False
        if "@" not in self.email:
            print("❌ Error: El email debe tener formato válido")
            return False
        return True


@dataclass
class Venta(Entidad):
    """
    Entidad que representa una venta realizada.

    Atributos:
        id: Identificador único de la venta
        producto_id: ID del producto vendido
        cliente_id: ID del cliente que compró
        cantidad: Cantidad de productos vendidos
        total: Monto total de la venta
        fecha: Fecha y hora de la venta (ISO format)
    """
    id: int
    producto_id: int
    cliente_id: int
    cantidad: int
    total: float
    fecha: str

    def obtener_id(self) -> int:
        return self.id

    @classmethod
    def desde_diccionario(cls, datos: Dict[str, Any]) -> Venta:
        return cls(**datos)


# ==================== SISTEMA DE GESTIÓN ====================

class SistemaTienda(SistemaGestion):
    """
    Sistema completo de gestión de tienda.

    Maneja tres repositorios:
    - productos: Para gestionar el inventario
    - clientes: Para gestionar la base de clientes
    - ventas: Para registrar las ventas realizadas
    """

    def __init__(self):
        # Inicializa el sistema con nombre "tienda_ejemplo"
        super().__init__("tienda_ejemplo")

        # Crea los tres repositorios
        self.productos = RepositorioJSON("productos", Producto, self.directorio_datos)
        self.clientes = RepositorioJSON("clientes", Cliente, self.directorio_datos)
        self.ventas = RepositorioJSON("ventas", Venta, self.directorio_datos)

    # ==================== OPERACIONES DE PRODUCTOS ====================

    def agregar_producto(self, producto: Producto) -> bool:
        """Agrega un nuevo producto al inventario."""
        if not producto.validar():
            return False
        return self.productos.insertar(producto)

    def listar_productos(self) -> List[Producto]:
        """Retorna todos los productos."""
        return self.productos.consultar_todos()

    def buscar_producto(self, producto_id: int) -> Producto | None:
        """Busca un producto por su ID."""
        return self.productos.consultar_por_id(producto_id)

    def productos_por_categoria(self, categoria: str) -> List[Producto]:
        """Retorna productos de una categoría específica."""
        return self.productos.consultar_por_campo("categoria", categoria)

    def actualizar_precio(self, producto_id: int, nuevo_precio: float) -> bool:
        """Actualiza el precio de un producto."""
        producto = self.buscar_producto(producto_id)
        if producto is None:
            print(f"❌ Producto {producto_id} no encontrado")
            return False

        producto.precio = nuevo_precio
        return self.productos.actualizar(producto)

    # ==================== OPERACIONES DE CLIENTES ====================

    def agregar_cliente(self, cliente: Cliente) -> bool:
        """Agrega un nuevo cliente."""
        if not cliente.validar():
            return False
        return self.clientes.insertar(cliente)

    def listar_clientes(self) -> List[Cliente]:
        """Retorna todos los clientes."""
        return self.clientes.consultar_todos()

    def buscar_cliente(self, cliente_id: int) -> Cliente | None:
        """Busca un cliente por su ID."""
        return self.clientes.consultar_por_id(cliente_id)

    def clientes_por_ciudad(self, ciudad: str) -> List[Cliente]:
        """Retorna clientes de una ciudad específica."""
        return self.clientes.consultar_por_campo("ciudad", ciudad)

    # ==================== OPERACIONES DE VENTAS ====================

    def registrar_venta(
        self,
        venta_id: int,
        producto_id: int,
        cliente_id: int,
        cantidad: int
    ) -> bool:
        """
        Registra una nueva venta.

        Verifica que:
        - El producto exista y tenga stock suficiente
        - El cliente exista
        - Descuenta el stock del producto
        - Calcula el total de la venta
        """
        # Verificar que el producto existe
        producto = self.buscar_producto(producto_id)
        if producto is None:
            print(f"❌ Producto {producto_id} no encontrado")
            return False

        # Verificar que el cliente existe
        cliente = self.buscar_cliente(cliente_id)
        if cliente is None:
            print(f"❌ Cliente {cliente_id} no encontrado")
            return False

        # Verificar stock
        if not producto.tiene_stock():
            print(f"❌ Producto '{producto.nombre}' sin stock")
            return False

        if producto.stock < cantidad:
            print(f"❌ Stock insuficiente. Disponible: {producto.stock}, solicitado: {cantidad}")
            return False

        # Calcular total
        total = producto.precio * cantidad

        # Crear la venta
        venta = Venta(
            id=venta_id,
            producto_id=producto_id,
            cliente_id=cliente_id,
            cantidad=cantidad,
            total=total,
            fecha=datetime.now().isoformat()
        )

        # Registrar la venta
        if not self.ventas.insertar(venta):
            return False

        # Descontar stock
        producto.descontar_stock(cantidad)
        self.productos.actualizar(producto)

        print(f"💰 Venta registrada: {cantidad}x {producto.nombre} → ${total:.2f}")
        return True

    def listar_ventas(self) -> List[Venta]:
        """Retorna todas las ventas."""
        return self.ventas.consultar_todos()

    def ventas_por_cliente(self, cliente_id: int) -> List[Venta]:
        """Retorna todas las ventas de un cliente."""
        return self.ventas.consultar_por_campo("cliente_id", cliente_id)

    def calcular_total_ventas(self) -> float:
        """Calcula el monto total de todas las ventas."""
        ventas = self.listar_ventas()
        return sum(venta.total for venta in ventas)

    # ==================== REPORTES ====================

    def mostrar_resumen(self) -> None:
        """Muestra un resumen completo del sistema."""
        super().mostrar_resumen()

        total_productos = self.productos.contar()
        total_clientes = self.clientes.contar()
        total_ventas = self.ventas.contar()
        monto_total = self.calcular_total_ventas()

        print(f"   📦 Productos en catálogo: {total_productos}")
        print(f"   👥 Clientes registrados: {total_clientes}")
        print(f"   💰 Ventas realizadas: {total_ventas}")
        print(f"   💵 Monto total vendido: ${monto_total:.2f}")
        print(f"{'='*60}\n")

    def mostrar_inventario_bajo(self, limite: int = 5) -> None:
        """Muestra productos con stock bajo."""
        productos = self.listar_productos()
        productos_bajos = [p for p in productos if p.stock <= limite]

        if productos_bajos:
            print(f"\n⚠️  ALERTA: Productos con stock bajo (≤ {limite}):")
            for p in productos_bajos:
                print(f"   • {p.nombre}: {p.stock} unidades")
        else:
            print(f"\n✅ Todos los productos tienen stock adecuado")


# ==================== FUNCIÓN PRINCIPAL ====================

def main():
    """Función principal que demuestra el uso del sistema."""

    # Crear el sistema
    tienda = SistemaTienda()

    # ==================== POBLAR DATOS DE EJEMPLO ====================

    print("\n📥 Cargando datos de ejemplo...")

    # Agregar productos
    productos_ejemplo = [
        Producto(1, "Laptop Dell XPS", "Electrónica", 1200.00, 10),
        Producto(2, "Mouse Logitech", "Accesorios", 25.50, 50),
        Producto(3, "Teclado Mecánico", "Accesorios", 89.99, 3),
        Producto(4, "Monitor LG 27\"", "Electrónica", 350.00, 15),
        Producto(5, "Webcam HD", "Accesorios", 45.00, 2),
    ]

    for producto in productos_ejemplo:
        tienda.agregar_producto(producto)

    # Agregar clientes
    clientes_ejemplo = [
        Cliente(1, "Ana García", "ana@email.com", "555-0101", "Bogotá"),
        Cliente(2, "Carlos Ruiz", "carlos@email.com", "555-0102", "Lima"),
        Cliente(3, "María López", "maria@email.com", "555-0103", "Bogotá"),
    ]

    for cliente in clientes_ejemplo:
        tienda.agregar_cliente(cliente)

    # ==================== REALIZAR OPERACIONES ====================

    print("\n🛒 Procesando ventas...")

    # Realizar algunas ventas
    tienda.registrar_venta(1, producto_id=1, cliente_id=1, cantidad=1)  # Ana compra 1 laptop
    tienda.registrar_venta(2, producto_id=2, cliente_id=2, cantidad=2)  # Carlos compra 2 mouses
    tienda.registrar_venta(3, producto_id=3, cliente_id=3, cantidad=1)  # María compra 1 teclado
    tienda.registrar_venta(4, producto_id=5, cliente_id=1, cantidad=2)  # Ana compra 2 webcams

    # ==================== CONSULTAS Y REPORTES ====================

    # Mostrar resumen
    tienda.mostrar_resumen()

    # Listar todos los productos
    mostrar_tabla(tienda.listar_productos(), "Productos en Catálogo")

    # Productos por categoría
    print("\n🔍 Productos de categoría 'Accesorios':")
    accesorios = tienda.productos_por_categoria("Accesorios")
    for producto in accesorios:
        print(f"   • {producto.nombre} - ${producto.precio} (Stock: {producto.stock})")

    # Listar clientes
    mostrar_tabla(tienda.listar_clientes(), "Clientes Registrados")

    # Clientes por ciudad
    print("\n🔍 Clientes de Bogotá:")
    clientes_bogota = tienda.clientes_por_ciudad("Bogotá")
    for cliente in clientes_bogota:
        print(f"   • {cliente.nombre} - {cliente.email}")

    # Mostrar ventas
    mostrar_tabla(tienda.listar_ventas(), "Ventas Realizadas")

    # Ventas por cliente
    print("\n🔍 Historial de compras de Ana García:")
    ventas_ana = tienda.ventas_por_cliente(1)
    for venta in ventas_ana:
        producto = tienda.buscar_producto(venta.producto_id)
        print(f"   • {venta.cantidad}x {producto.nombre} - ${venta.total:.2f}")

    # Mostrar productos con stock bajo
    tienda.mostrar_inventario_bajo(limite=5)

    # ==================== ACTUALIZAR DATOS ====================

    print("\n🔄 Actualizando precio del Mouse...")
    tienda.actualizar_precio(2, 29.99)

    # ==================== MOSTRAR BITÁCORAS ====================

    print("\n📜 Últimas operaciones sobre productos:")
    tienda.productos.mostrar_bitacora(ultimas=5)

    print("\n📜 Últimas operaciones sobre ventas:")
    tienda.ventas.mostrar_bitacora(ultimas=5)

    # ==================== ESTADÍSTICAS ====================

    tienda.productos.mostrar_estadisticas()
    tienda.clientes.mostrar_estadisticas()
    tienda.ventas.mostrar_estadisticas()

    print("\n✅ ¡Ejemplo completado! Revisa la carpeta 'datos/tienda_ejemplo' para ver los archivos JSON generados.")


if __name__ == "__main__":
    main()
