@echo off
REM Instalador automático para el Curso de Desarrollo Backend con Python, Django y PostgreSQL
REM Fecha: Octubre 2025

chcp 65001 >nul 2>&1

REM Variables
set VENV_NAME=venv
set PYTHON=python
set PIP=%VENV_NAME%\Scripts\pip.exe
set PYTHON_VENV=%VENV_NAME%\Scripts\python.exe
set REQUIREMENTS=requirements.txt

REM Colores
set CYAN=[36m
set GREEN=[32m
set YELLOW=[33m
set RED=[31m
set RESET=[0m

cls
echo %CYAN%
echo   ====================================================================
echo    ____        _   _                   ____             _                  _ 
echo   ^|  _ \ _   _^| ^|_^| ^|__   ___  _ __   ^| __ )  __ _  ___^| ^| _____ _ __   __^| ^|
echo   ^| ^|_) ^| ^| ^| ^| __^| '_ \ / _ \^| '_ \  ^|  _ \ / _` ^|/ __^| ^|/ / _ \ '_ \ / _` ^|
echo   ^|  __/^| ^|_^| ^| ^|_^| ^| ^| ^| (_) ^| ^| ^| ^| ^| ^|_) ^| (_^| ^| (__^|   ^<  __/ ^| ^| ^| (_^| ^|
echo   ^|_^|    \__, ^|\__^|_^| ^|_^|\___/^|_^| ^|_^| ^|____/ \__,_^|\___ ^|_^|\_\___^|_^| ^|_^|\__,_^|
echo          ^|___/                                                               
echo   ====================================================================
echo   🚀 Instalador Automático - Entorno de Desarrollo Backend 🚀
echo   ====================================================================
echo %RESET%
echo.

REM Verificar Python
echo %YELLOW%[1/5] Verificando instalación de Python...%RESET%
%PYTHON% --version >nul 2>&1
if errorlevel 1 (
    echo %RED%❌ ERROR: Python no está instalado o no está en el PATH%RESET%
    echo %YELLOW%Por favor, instala Python desde https://www.python.org/downloads/%RESET%
    pause
    exit /b 1
)
%PYTHON% --version
echo %GREEN%✓ Python encontrado%RESET%
echo.

REM Crear entorno virtual
echo %YELLOW%[2/5] Creando entorno virtual '%VENV_NAME%'...%RESET%
if exist "%VENV_NAME%" (
    echo %YELLOW%⚠ El entorno virtual ya existe. Eliminando...%RESET%
    rmdir /s /q %VENV_NAME%
)
%PYTHON% -m venv %VENV_NAME%
if errorlevel 1 (
    echo %RED%❌ ERROR: No se pudo crear el entorno virtual%RESET%
    pause
    exit /b 1
)
echo %GREEN%✓ Entorno virtual creado correctamente%RESET%
echo.

REM Crear requirements.txt si no existe
echo %YELLOW%[3/5] Verificando archivo de dependencias...%RESET%
if not exist "%REQUIREMENTS%" (
    echo %YELLOW%Creando archivo %REQUIREMENTS%...%RESET%
    (
        echo # Requisitos para el curso de Desarrollo Backend
        echo # Fecha: %date% %time%
        echo.
        echo # Dependencias básicas
        echo Django^>=4.2.0
        echo psycopg2-binary^>=2.9.5
        echo python-dotenv^>=1.0.0
    ) > %REQUIREMENTS%
    echo %GREEN%✓ Archivo %REQUIREMENTS% creado%RESET%
) else (
    echo %GREEN%✓ Archivo %REQUIREMENTS% encontrado%RESET%
)
echo.

REM Actualizar pip
echo %YELLOW%[4/5] Actualizando pip...%RESET%
%PIP% install --upgrade pip
if errorlevel 1 (
    echo %RED%❌ ERROR: No se pudo actualizar pip%RESET%
    pause
    exit /b 1
)
echo %GREEN%✓ pip actualizado correctamente%RESET%
echo.

REM Instalar dependencias
echo %YELLOW%[5/5] Instalando dependencias desde %REQUIREMENTS%...%RESET%
echo %YELLOW%Esto puede tomar varios minutos...%RESET%
%PIP% install -r %REQUIREMENTS%
if errorlevel 1 (
    echo %RED%❌ ERROR: No se pudieron instalar las dependencias%RESET%
    pause
    exit /b 1
)
echo %GREEN%✓ Dependencias instaladas correctamente%RESET%
echo.

REM Resumen final
echo.
echo %GREEN%=====================================================================%RESET%
echo %GREEN%              ✓ INSTALACIÓN COMPLETADA EXITOSAMENTE ✓%RESET%
echo %GREEN%=====================================================================%RESET%
echo.
echo %CYAN%Para activar el entorno virtual, ejecuta:%RESET%
echo   %YELLOW%venv\Scripts\activate%RESET%
echo.
echo %CYAN%Para desactivar el entorno virtual:%RESET%
echo   %YELLOW%deactivate%RESET%
echo.
echo %CYAN%Para ejecutar un script Python:%RESET%
echo   %YELLOW%venv\Scripts\python.exe tu_script.py%RESET%
echo.
echo %GREEN%¡Listo para comenzar a desarrollar! 🎉%RESET%
echo.
pause