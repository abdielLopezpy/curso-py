# Guía para crear un entorno virtual

Sigue estas instrucciones según tu sistema operativo para crear y activar un entorno virtual en este proyecto.

## Requisitos previos

- Contar con Python 3.8 o superior instalado.
- Tener pip instalado (se incluye por defecto en las instalaciones recientes de Python).

## Windows

1. Verifica la instalación de Python:
   ```powershell
   py --version
   ```
2. Crea el entorno virtual (puedes cambiar `venv` por el nombre que prefieras):
   ```powershell
   py -m venv venv
   ```
3. Activa el entorno virtual:
   - PowerShell:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - Símbolo del sistema (CMD):
     ```cmd
     .\venv\Scripts\activate.bat
     ```
4. Instala las dependencias del proyecto:
   ```powershell
   pip install -r requirements.txt
   ```
5. Para desactivar el entorno virtual:
   ```powershell
   deactivate
   ```

## macOS y Linux

1. Verifica la instalación de Python:
   ```bash
   python3 --version
   ```
2. Crea el entorno virtual:
   ```bash
   python3 -m venv venv
   ```
3. Activa el entorno virtual:
   ```bash
   source venv/bin/activate
   ```
4. Instala las dependencias del proyecto:
   ```bash
   pip install -r requirements.txt
   ```
5. Para desactivar el entorno virtual:
   ```bash
   deactivate
   ```

## Notas adicionales

- Usa siempre el entorno virtual activado antes de ejecutar scripts o instalar paquetes.
- Si necesitas recrear el entorno, elimina la carpeta `venv` y repite los pasos anteriores.
- Evita commitear la carpeta `venv` al repositorio.
