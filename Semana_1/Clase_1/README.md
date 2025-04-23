# Clase 1: Introducción al desarrollo backend

## Contenido de la clase

- Ecosistema de desarrollo backend y el rol de Python
- Responsabilidades del desarrollador backend
- Configuración del entorno: Python, pip, entornos virtuales
- Introducción a la línea de comandos y control de versiones con Git
- Ejercicio práctico: Configuración del entorno y primer script Python

## Recursos

### Instalación del entorno

1. **Instalación de Python**:
   - Descargar Python desde [python.org](https://www.python.org/downloads/)
   - Verificar instalación: `python --version` o `python3 --version`

2. **Instalación de pip** (gestor de paquetes):
   - Verificar si ya está instalado: `pip --version` o `pip3 --version`
   - Si no está instalado: [Instrucciones de instalación](https://pip.pypa.io/en/stable/installation/)

3. **Creación de entornos virtuales**:
   ```bash
   # Instalación de virtualenv
   pip install virtualenv
   
   # Crear un entorno virtual
   virtualenv venv
   
   # Activación en Windows
   venv\Scripts\activate
   
   # Activación en Linux/Mac
   source venv/bin/activate
   ```

### Control de versiones con Git

1. **Instalación de Git**:
   - Descargar desde [git-scm.com](https://git-scm.com/downloads)
   - Verificar instalación: `git --version`

2. **Configuración básica**:
   ```bash
   git config --global user.name "Tu Nombre"
   git config --global user.email "tu@email.com"
   ```

3. **Comandos básicos**:
   ```bash
   git init            # Iniciar un repositorio
   git add .           # Añadir todos los archivos al staging
   git commit -m "Mensaje"  # Confirmar cambios
   git status          # Ver estado del repositorio
   git log             # Ver historial de cambios
   ```

## Ejercicio práctico

1. Configurar el entorno de desarrollo
2. Crear un script Python simple: `hola_mundo.py`
3. Inicializar un repositorio Git y hacer el primer commit

Revisa el archivo `hola_mundo.py` para ver un ejemplo de script Python básico.