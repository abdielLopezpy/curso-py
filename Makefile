# Makefile para el Curso de Desarrollo Backend con Python, Django y PostgreSQL
# Autor: Copilot
# Fecha: Abril 22, 2025

# Variables
VENV_NAME := venv
PYTHON := python3
PIP := $(VENV_NAME)/bin/pip
PYTHON_VENV := $(VENV_NAME)/bin/python
REQUIREMENTS := requirements.txt

# Colores para mensajes
CYAN := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RESET := \033[0m

# Mensaje ASCII Art divertido
define MEME
$(CYAN)
  ____        _   _                   ____             _                  _ 
 |  _ \ _   _| |_| |__   ___  _ __   | __ )  __ _  ___| | _____ _ __   __| |
 | |_) | | | | __| '_ \ / _ \| '_ \  |  _ \ / _` |/ __| |/ / _ \ '_ \ / _` |
 |  __/| |_| | |_| | | | (_) | | | | | |_) | (_| | (__|   <  __/ | | | (_| |
 |_|    \__, |\__|_| |_|\___/|_| |_| |____/ \__,_|\___|_|\_\___|_| |_|\__,_|
        |___/                                                               

 🚀 ¡Bienvenido a tu asistente de desarrollo backend! 🚀
$(RESET)

endef
export MEME

# Objetivos falsos (no corresponden a archivos)
.PHONY: all help setup venv clean run test requirements show-meme

# Mostrar mensaje de ayuda por defecto
all: help

# Muestra los comandos disponibles
help:
	@echo "$$MEME"
	@echo "$(GREEN)Comandos disponibles:$(RESET)"
	@echo "  $(YELLOW)make setup$(RESET)        - Configura el entorno virtual e instala dependencias"
	@echo "  $(YELLOW)make venv$(RESET)         - Crea solo el entorno virtual"
	@echo "  $(YELLOW)make requirements$(RESET) - Instala las dependencias en el entorno virtual"
	@echo "  $(YELLOW)make run SCRIPT=ruta$(RESET) - Ejecuta el script Python especificado"
	@echo "  $(YELLOW)make clean$(RESET)        - Elimina el entorno virtual y archivos temporales"
	@echo "  $(YELLOW)make show-meme$(RESET)    - Muestra el mensaje de bienvenida"
	@echo ""
	@echo "$(GREEN)Ejemplo de uso:$(RESET)"
	@echo "  $(YELLOW)make run SCRIPT=Semana_1/Clase_1/hola_mundo.py$(RESET)"

# Muestra solo el meme
show-meme:
	@echo "$$MEME"

# Configura todo el entorno
setup: venv requirements
	@echo "$(GREEN)¡Entorno configurado correctamente!$(RESET)"
	@echo "$(YELLOW)Para activar el entorno virtual manualmente:$(RESET)"
	@echo "  source $(VENV_NAME)/bin/activate"

# Crea el entorno virtual
venv:
	@echo "$(YELLOW)Creando entorno virtual '$(VENV_NAME)'...$(RESET)"
	@if [ ! -d "$(VENV_NAME)" ]; then \
		$(PYTHON) -m venv $(VENV_NAME); \
		echo "$(GREEN)Entorno virtual creado con éxito.$(RESET)"; \
	else \
		echo "$(YELLOW)El entorno virtual '$(VENV_NAME)' ya existe.$(RESET)"; \
	fi

# Crea un archivo requirements.txt si no existe
$(REQUIREMENTS):
	@echo "$(YELLOW)Creando archivo de requisitos vacío...$(RESET)"
	@echo "# Requisitos para el curso de Desarrollo Backend" > $(REQUIREMENTS)
	@echo "# Fecha: $$(date)" >> $(REQUIREMENTS)
	@echo "" >> $(REQUIREMENTS)
	@echo "# Dependencias básicas" >> $(REQUIREMENTS)
	@echo "Django>=4.2.0" >> $(REQUIREMENTS)
	@echo "psycopg2-binary>=2.9.5" >> $(REQUIREMENTS)
	@echo "python-dotenv>=1.0.0" >> $(REQUIREMENTS)
	@echo "$(GREEN)Archivo $(REQUIREMENTS) creado.$(RESET)"

# Instala las dependencias
requirements: venv $(REQUIREMENTS)
	@echo "$(YELLOW)Instalando dependencias...$(RESET)"
	$(PIP) install --upgrade pip
	$(PIP) install -r $(REQUIREMENTS)
	@echo "$(GREEN)Dependencias instaladas correctamente.$(RESET)"

# Ejecuta un script Python
run:
	@if [ -z "$(SCRIPT)" ]; then \
		echo "$(YELLOW)Por favor, especifica un script para ejecutar:$(RESET)"; \
		echo "  make run SCRIPT=ruta/al/script.py"; \
	elif [ ! -f "$(SCRIPT)" ]; then \
		echo "$(YELLOW)Error: El script '$(SCRIPT)' no existe.$(RESET)"; \
	else \
		echo "$(YELLOW)Ejecutando '$(SCRIPT)'...$(RESET)"; \
		$(PYTHON_VENV) $(SCRIPT); \
	fi

# Limpia el entorno
clean:
	@echo "$(YELLOW)Limpiando entorno...$(RESET)"
	@rm -rf $(VENV_NAME) __pycache__ */__pycache__ */*/__pycache__ */*/*/__pycache__
	@find . -name "*.pyc" -delete
	@echo "$(GREEN)¡Limpieza completa!$(RESET)"