# Semana 5: Objetos JSON y simulación de almacenamiento

Esta semana está dedicada a comprender qué es un objeto JSON, cómo se utiliza en aplicaciones backend y de qué forma podemos simular el proceso de persistir información en una base de datos usando este formato.

## 1. ¿Qué es JSON?

JSON (JavaScript Object Notation) es un formato de texto ligero para el intercambio de datos. Se basa en pares clave-valor y listas ordenadas, por lo que resulta ideal para representar objetos o colecciones de objetos.

```json
{
  "id": 101,
  "nombre": "Ana",
  "activo": true,
  "roles": ["admin", "auditor"],
  "perfil": {
    "pais": "Argentina",
    "email": "ana@example.com"
  }
}
```

### Ventajas
- Es legible para humanos y máquinas.
- Es independiente del lenguaje pero compatible con prácticamente todos.
- Es perfecto para APIs, archivos de configuración y almacenamiento ligero.

## 2. ¿Dónde se usa y se guarda?

1. **APIs REST y GraphQL**: los servidores envían y reciben objetos JSON.
2. **Archivos `.json`**: sirven como configuración, catálogos, "semillas" de datos, etc.
3. **Colas y eventos**: RabbitMQ, Kafka y otros brokers transportan mensajes en JSON.
4. **Bases NoSQL**: MongoDB, DynamoDB y Firestore almacenan documentos JSON.
5. **Logs estructurados**: facilitar la observabilidad y el análisis automatizado.

En disco bastará con crear un archivo de texto con extensión `.json`. En memoria, trabajamos con diccionarios y listas (Python) que luego serializamos (convertimos a texto JSON) cuando queremos persistirlos o enviarlos.

## 3. Guardar y leer archivos JSON en Python

```python
import json
from pathlib import Path

clientes = [
    {"id": 1, "nombre": "Ana", "saldo": 125.5},
    {"id": 2, "nombre": "Luis", "saldo": 98.0},
]

ruta_archivo = Path("Semana_5/datos/clientes.json")
ruta_archivo.parent.mkdir(parents=True, exist_ok=True)

# Guardar (serializar)
with ruta_archivo.open("w", encoding="utf-8") as archivo:
    json.dump(clientes, archivo, ensure_ascii=False, indent=2)

# Leer (deserializar)
with ruta_archivo.open(encoding="utf-8") as archivo:
    clientes_desde_archivo = json.load(archivo)

print(clientes_desde_archivo)
```

## 4. Simulación de proceso de guardado en base de datos

Para entender cómo llegarían estos datos a una base real crearemos un **repositorio simulado**:

1. El módulo `json_db_simulator.py` expone la clase `JsonDatabase`, que actúa como un adaptador.
2. Al llamar a `insertar_registro`, el objeto Python se transforma en JSON, se agrega a una colección en memoria y se sincroniza con un archivo `.json` (nuestro "disco").
3. El método `consultar` filtra esa colección y muestra cómo podríamos ejecutar una query sencilla.
4. Registramos un historial de operaciones que simula un log transaccional.

Este flujo imita lo que sucede en una base de datos real:

```
Entrada Python -> Validación -> Serialización JSON -> Persistencia
```

## 5. Archivos principales de la semana

| Archivo | Descripción |
| --- | --- |
| `README_SEMANA_5.md` | Este documento con la teoría clave. |
| `json_basics.py` | Script interactivo con ejemplos de creación, serialización y lectura de JSON. |
| `json_db_simulator.py` | Simula un motor de almacenamiento basado en archivos JSON. |
| `datos/` | Carpeta donde se depositan los archivos generados durante los ejemplos. |

## 6. Laboratorio sugerido

1. Ejecuta `python Semana_5/json_basics.py` y experimenta con tus propios objetos.
2. Luego corre `python Semana_5/json_db_simulator.py` e inserta varios registros.
3. Abre el archivo `Semana_5/datos/registros.json` para verificar que el contenido coincide con lo mostrado en consola.
4. Modifica el método `consultar` para aceptar filtros dinámicos (por ejemplo, `campo="ciudad", valor="Bogotá"`).

## 7. Recursos

- [Documentación oficial del módulo `json`](https://docs.python.org/3/library/json.html)
- [JSON Schema](https://json-schema.org/) para validar la estructura.
- [MongoDB vs. Postgres JSON](https://www.postgresql.org/docs/current/datatype-json.html) para conocer opciones en bases reales.

> "JSON es el puente entre tu código Python y el mundo exterior; dominarlo significa hablar el idioma universal del intercambio de datos." — Equipo del curso

## 8. Guía autodidacta paso a paso

### json_basics.py

1. **Explora la estructura**: abre el archivo y ubica las funciones `crear_objeto_python`, `convertir_a_json`, `guardar_clientes_registro`, `leer_clientes_registro` y `registrar_evento`. Cada una representa una etapa real de trabajo con JSON.
2. **Ejecución básica**:
   ```bash
   python3 Semana_5/json_basics.py
   ```
   El script imprime el objeto Python original, su versión serializada y los registros recién guardados.
3. **Lecturas guiadas**:
   - Observa cómo `guardar_clientes_registro` usa `Path` para asegurar que la carpeta exista.
   - Sigue el flujo hasta `registrar_evento`: convierte eventos en una lista persistida en `datos/eventos.json`.
   - Repite la ejecución cambiando valores en la lista `clientes` para reforzar el ciclo editar → correr → validar.
4. **Verificación manual**: abre los archivos JSON generados y confirma que coinciden con lo mostrado en consola; esta práctica simula una auditoría de datos previa a subir información a una base real.

### json_db_simulator.py

1. **Entiende la arquitectura**:
   - `Cliente` es una dataclass que actúa como DTO (objeto de transferencia de datos).
   - `JsonDatabase` encapsula las operaciones (insertar, consultar, persistir, registrar eventos).
2. **Simulación guiada**:
   ```bash
   python3 Semana_5/json_db_simulator.py
   ```
   - La primera ejecución pobla la “base” con tres clientes y deja rastros en `registros.json` y `bitacora.json`.
   - La segunda ejecución detecta que ya existen registros y evita duplicarlos automáticamente.
3. **Investigación autodidacta**:
   - Modifica el método `consultar` para aceptar operadores distintos (`>`, `<`, `in`) y evalúa cómo se reflejan los cambios en las consultas.
   - Añade un nuevo método `actualizar_registro` siguiendo el patrón de persistencia y valida que la bitácora también se actualice.
4. **Checklist de persistencia** (repite cada vez que cambies la lógica):
   - ¿Se validó que el `id` sea único?
   - ¿La bitácora registra la operación con fecha y payload?
   - ¿El archivo `registros.json` refleja el nuevo estado?

## 9. Referencia rápida de funciones y clases

| Archivo | Elemento | Descripción de uso autodidacta |
| --- | --- | --- |
| `json_basics.py` | `crear_objeto_python()` | Punto de partida para comparar formatos Python vs. JSON. |
| `json_basics.py` | `convertir_a_json(data)` | Úsalo para practicar serialización con distintas estructuras anidadas. |
| `json_basics.py` | `registrar_evento(tipo, payload)` | Simula logs históricos cada vez que interactúas con datos. |
| `json_db_simulator.py` | `Cliente` | Representa una fila de la tabla `clientes`; modifica atributos y vuelve a ejecutar. |
| `json_db_simulator.py` | `JsonDatabase.insertar_registro` | Replica la operación INSERT y deja constancia en bitácora. |
| `json_db_simulator.py` | `JsonDatabase.consultar` | Realiza filtros simples; ideal para extender con nuevas condiciones. |

Con estas guías puedes experimentar sin supervisión: cambia los datos, vuelve a ejecutar los scripts, analiza los archivos JSON generados y registra lo aprendido para reforzar el proceso de persistencia basado en archivos.
