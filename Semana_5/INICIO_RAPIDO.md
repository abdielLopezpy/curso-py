# 🚀 Inicio Rápido - Semana 5

**¡Bienvenido a la Semana 5!** Esta es tu guía de inicio rápido.

---

## 📋 ¿Por Dónde Empiezo?

### Si eres nuevo aquí:

#### ✅ PASO 1: Lee la Documentación Principal (10 min)
📖 [README_SEMANA_5.md](README_SEMANA_5.md)

Lee al menos estas secciones:
- ¿Qué es JSON?
- JSON en Python
- Framework de Gestión de Datos JSON

#### ✅ PASO 2: Aprende sobre @dataclass (15 min)
📖 [CONCEPTOS_CLAVE.md](CONCEPTOS_CLAVE.md)

Lee la sección de **@dataclass** para entender cómo crear clases simples.

#### ✅ PASO 3: Ejecuta el Ejemplo (5 min)

```bash
# Desde la raíz del curso
python3 Semana_5/ejemplo/ejemplo_tienda.py
```

**Observa**:
- La salida en consola
- Los archivos JSON creados en `framework/datos/tienda_ejemplo/`

#### ✅ PASO 4: Estudia el Ejemplo (30 min)
👀 [ejemplo/ejemplo_tienda.py](ejemplo/ejemplo_tienda.py)

Lee el código línea por línea para entender:
- Cómo se definen las entidades
- Cómo se crea el sistema
- Cómo se relacionan las entidades

#### ✅ PASO 5: Lee las Instrucciones del Desafío (15 min)
📋 [desafio/DESAFIO_README.md](desafio/DESAFIO_README.md)

Comprende qué se te pide hacer.

#### ✅ PASO 6: ¡Hazlo! (2-3 horas)
✏️ [desafio/DESAFIO.py](desafio/DESAFIO.py)

Crea tu propio sistema con 3 entidades.

---

## 📁 Estructura del Proyecto

```
Semana_5/
│
├── 📖 README_SEMANA_5.md          ← Documentación completa
├── 🚀 INICIO_RAPIDO.md            ← Este archivo
├── 📚 CONCEPTOS_CLAVE.md          ← Explicación de conceptos de Python
│
├── framework/                     ← 🔧 Infraestructura (NO tocar)
│   └── database_framework.py
│
├── ejemplo/                       ← 👀 Ejemplo para estudiar
│   └── ejemplo_tienda.py
│
├── desafio/                       ← ✏️ Tu trabajo va aquí
│   ├── DESAFIO_README.md          ← Instrucciones paso a paso
│   └── DESAFIO.py                 ← Archivo donde trabajarás
│
└── datos/                         ← 💾 Datos guardados (se genera automáticamente)
```

---

## 🎯 ¿Qué voy a hacer en el Desafío?

Vas a crear un **sistema completo de gestión** como:

- 🏥 Sistema Hospitalario (Doctores, Pacientes, Citas)
- 📚 Sistema de Biblioteca (Libros, Usuarios, Préstamos)
- 🍕 Sistema de Restaurante (Platillos, Ingredientes, Pedidos)
- 🏨 Sistema Hotelero (Habitaciones, Huéspedes, Reservas)
- 🎓 Sistema Educativo (Estudiantes, Profesores, Cursos)

**O cualquier otro que se te ocurra**.

Tu sistema debe:
1. ✅ Tener 3 entidades relacionadas
2. ✅ Guardar datos en archivos JSON
3. ✅ Realizar operaciones CRUD
4. ✅ Relacionar las entidades entre sí

---

## ⚡ Comandos Rápidos

### Ejecutar el ejemplo:
```bash
python3 Semana_5/ejemplo/ejemplo_tienda.py
```

### Ejecutar tu desafío:
```bash
python3 Semana_5/desafio/DESAFIO.py
```

### Ver archivos JSON generados:
```bash
# Del ejemplo
ls -la Semana_5/framework/datos/tienda_ejemplo/
cat Semana_5/framework/datos/tienda_ejemplo/productos.json

# De tu desafío (después de ejecutarlo)
ls -la Semana_5/datos/[tu_sistema]/
```

---

## 📚 Documentos Clave

| Documento | ¿Qué contiene? | ¿Cuándo leerlo? |
|-----------|----------------|-----------------|
| [README_SEMANA_5.md](README_SEMANA_5.md) | Documentación completa de la semana | Al inicio |
| [CONCEPTOS_CLAVE.md](CONCEPTOS_CLAVE.md) | Explicación de @dataclass, herencia, etc. | Cuando tengas dudas sobre conceptos |
| [desafio/DESAFIO_README.md](desafio/DESAFIO_README.md) | Instrucciones paso a paso del desafío | Antes de empezar el desafío |

---

## 🤔 Preguntas Frecuentes

### ¿Qué es @dataclass?
Es una forma fácil de crear clases para almacenar datos. Lee la sección en [CONCEPTOS_CLAVE.md](CONCEPTOS_CLAVE.md#qué-es-dataclass).

### ¿Tengo que modificar el framework?
**NO**. El framework ya está completo y funcional. Solo tienes que:
1. Importar las clases del framework
2. Definir tus entidades
3. Crear tu sistema

### ¿Qué archivos debo modificar?
Solo trabaja en: [desafio/DESAFIO.py](desafio/DESAFIO.py)

### ¿Puedo usar el ejemplo como referencia?
**¡SÍ!** De hecho, es recomendado. Estudia [ejemplo/ejemplo_tienda.py](ejemplo/ejemplo_tienda.py) para ver cómo se hace.

### Mi programa no crea archivos JSON, ¿por qué?
Revisa:
1. ¿Estás llamando a `.insertar()` en los repositorios?
2. ¿Tus datos pasan las validaciones?
3. ¿Ejecutas desde la raíz del curso?

### Error: "ModuleNotFoundError: No module named 'database_framework'"
**Solución**: Ejecuta desde la raíz del curso:
```bash
# ✅ Correcto
python3 Semana_5/desafio/DESAFIO.py

# ❌ Incorrecto
cd Semana_5/desafio
python3 DESAFIO.py
```

---

## 📊 Checklist Rápido

Antes de empezar, asegúrate de:

- [ ] Ejecuté y vi funcionar el ejemplo
- [ ] Entiendo qué es JSON
- [ ] Entiendo qué es @dataclass (al menos básicamente)
- [ ] Leí las instrucciones del desafío
- [ ] Decidí qué sistema voy a crear

Durante el desarrollo:

- [ ] Definí mis 3 entidades
- [ ] Cada entidad tiene al menos 4 campos
- [ ] Implementé validaciones
- [ ] Creé mi sistema con los 3 repositorios
- [ ] Implementé métodos básicos (agregar, listar, buscar)
- [ ] Creé UN método que relacione las entidades
- [ ] Agregué datos de ejemplo en main()

Al terminar:

- [ ] El programa se ejecuta sin errores
- [ ] Se crean archivos JSON
- [ ] Los archivos JSON tienen datos válidos
- [ ] Todo está bien documentado

---

## 💡 Tips Finales

1. **No te abrumes**: Empieza simple, agrega complejidad después
2. **Usa el ejemplo**: Copia la estructura y adáptala a tu sistema
3. **Prueba frecuentemente**: Ejecuta tu código cada vez que agregues algo nuevo
4. **Lee los errores**: Python te dice exactamente qué está mal
5. **Pide ayuda**: Si te atascas, revisa la documentación o pregunta

---

## 🎓 Ruta de Aprendizaje Resumida

```
DÍA 1-2:
  → Leer documentación
  → Entender conceptos básicos
  → Ejecutar y estudiar el ejemplo

DÍA 3-4:
  → Decidir qué sistema crear
  → Definir las 3 entidades
  → Crear el sistema base

DÍA 5-6:
  → Implementar operaciones básicas
  → Implementar relaciones entre entidades
  → Probar que funcione

DÍA 7:
  → Pulir y documentar
  → Verificar checklist
  → ¡Entregar!
```

---

## 🆘 ¿Necesitas Ayuda?

1. 📖 Revisa [CONCEPTOS_CLAVE.md](CONCEPTOS_CLAVE.md) para dudas sobre Python
2. 👀 Estudia [ejemplo/ejemplo_tienda.py](ejemplo/ejemplo_tienda.py) para ver cómo se hace
3. 📋 Lee [desafio/DESAFIO_README.md](desafio/DESAFIO_README.md) para instrucciones detalladas
4. 💬 Pregunta a tu instructor

---

**¡Mucha suerte! 🚀**

Recuerda: El objetivo no es crear el sistema más complejo, sino **aprender a trabajar con JSON y estructurar datos**.

---

**Última actualización**: 2025
