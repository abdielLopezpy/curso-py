# Copyright 2025 Abdiel Lopez
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     https://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from dataclasses import dataclass
from typing import List, TypeVar, Generic

# Definir un tipo genérico
T = TypeVar('T')


class Repo(Generic[T]):
    def __init__(self):
        self.contenido: List[T] = []

    def agregar(self, item: T) -> None:
        self.contenido.append(item)

    def obtener_todos(self) -> List[T]:
        return self.contenido
    

@dataclass
class Usuario:
    id: int
    nombre: str

@dataclass
class Producto:
    id: int
    nombre: str
    precio: float

@dataclass
class Tren:
    id: int
    ruta: str
    precio: float
    
@dataclass
class Carro:
    id: int
    marca: str
    model: str

@dataclass
class Celular:
    id: int
    marca: str
    precio: int
    modelo: str


@dataclass
class Cafe:
    id:int
    marca:str
    precio: float
       

# Crear repositorios específicos para Usuario y Producto
repo_usuarios = Repo[Usuario]()
repo_productos = Repo[Producto]()


repo_tren = Repo[Tren]()
repo_carro = Repo[Carro]()
repo_celular = Repo[Celular]()
repo_Cafe = Repo [Cafe] ()

# Agregar usuarios al repositorio de usuarios
repo_usuarios.agregar(Usuario(id=1, nombre="Alice"))
repo_usuarios.agregar(Usuario(id=2, nombre="Bob"))

# Agregar productos al repositorio de productos
repo_productos.agregar(Producto(id=1, nombre="Laptop", precio=999.99))
repo_productos.agregar(Producto(id=2, nombre="Smartphone", precio=499.99))


repo_tren.agregar(Tren(id=1, ruta='Agua fria', precio=10.00))
repo_tren.agregar(Tren(id=2, ruta='David', precio=40.00))
repo_tren.agregar(Tren(id=3, ruta='Chorrera', precio=12.00))

repo_carro.agregar(Carro(id=1, marca='toyota', model='yaris'))
repo_carro.agregar(Carro(id=2, marca='nissan', model='versa'))
repo_carro.agregar(Carro(id=3, marca='honda', model='civic'))

repo_celular.agregar(Celular(id=1, marca='Honor',precio=600,modelo='200pro'))
repo_celular.agregar(Celular(id=2, marca='Samsung',precio=10000,modelo='fold2'))


repo_Cafe.agregar(Cafe(id=1, marca='Duran', precio+))

# Obtener y mostrar todos los usuarios
usuarios = repo_usuarios.obtener_todos()
print("Usuarios en el repositorio:")
for usuario in usuarios:
    print(usuario)  

# Obtener y mostrar todos los productos
productos = repo_productos.obtener_todos()
print("\nProductos en el repositorio:")
for producto in productos:
    print(producto)


trenes = repo_tren.obtener_todos()
print("\nTrenes:")
for tren in trenes:
    print (tren)
    
carros = repo_carro.obtener_todos()
print("\nCarros en el Repositorio")
for carro in carros:
    print (carro)
    
celular = repo_celular.obtener_todos()
print("\nCelular")
for celular in celular:
    print (celular)