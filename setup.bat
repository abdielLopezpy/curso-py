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

REM Habilitar secuencias de escape ANSI en Windows 10+
for /f "tokens=4-5 delims=. " %%i in ('ver') do set VERSION=%%i.%%j
if "%VERSION%" geq "10.0" (
    REM Activar soporte de ANSI
    reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1
)

REM Colores ANSI (corregidos)
set "CYAN=[96m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "RED=[91m"
set "RESET=[0m"

cls
echo.
echo %CYAN%=====================================================================%RESET%
echo %CYAN%   ____        _   _                   ____             _                  _ %RESET%
echo %CYAN%  ^| __ \ _   _^| ^|_^| ^|__   ___  _ __   ^| __ )  __ _  ___^| ^| _____ _ __   __^| ^|%RESET%
echo %CYAN%  ^|  ^|_) ^| ^| ^| ^| __^| '_ \ / _ \^| '_ \  ^|  _ \ / _` ^|/ __^| ^|/ / _ \ '_ \ / _` ^|%RESET%
echo %CYAN%  ^|  __/^| ^|_^| ^| ^|_^| ^| ^| ^| (_) ^| ^| ^| ^| ^| ^|_) ^| (_^| ^| (__^|   ^<  __/ ^| ^| ^| (_^| ^|%RESET%
echo %CYAN%  ^|_^|    \__, ^|\__^|_^| ^|_^|\___/^|_^| ^|_^| ^|____/ \__,_^|\___ ^|_^|\_\___^|_^| ^|_^|\__,_^|%RESET%
echo %CYAN%         ^|___/                                                               %RESET%
echo %CYAN%=====================================================================%RESET%
echo %CYAN%   Instalador Automatico - Entorno de Desarrollo Backend%RESET%
echo %CYAN%=====================================================================%RESET%
echo.

REM Verificar Python
echo %YELLOW%[1/5] Verificando instalacion de Python...%RESET%
%PYTHON% --version >nul 2>&1
if %errorlevel% neq 0 (
    echo %RED%ERROR: Python no esta instalado o no esta en el PATH%RESET%
    echo %YELLOW%Por favor, instala Python desde https://www.python.org/downloads/%RESET%
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('%PYTHON% --version 2^>^&1') do set PYTHON_VERSION=%%i
echo %GREEN%OK Python encontrado: %PYTHON_VERSION%%RESET%
echo.

REM Crear entorno virtual
echo %YELLOW%[2/5] Creando entorno virtual '%VENV_NAME%'...%RESET%
if exist "%VENV_NAME%" (
    echo %YELLOW%El entorno virtual ya existe. Eliminando...%RESET%
    rmdir /s /q %VENV_NAME% >nul 2>&1
    timeout /t 1 /nobreak >nul
)

%PYTHON% -m venv %VENV_NAME%
if %errorlevel% neq 0 (
    echo %RED%ERROR: No se pudo crear el entorno virtual%RESET%
    echo %YELLOW%Intenta instalar: %PYTHON% -m pip install virtualenv%RESET%
    echo.
    pause
    exit /b 1
)
echo %GREEN%OK Entorno virtual creado correctamente%RESET%
echo.

REM Crear requirements.txt si no existe
echo %YELLOW%[3/5] Verificando archivo de dependencias...%RESET%
if not exist "%REQUIREMENTS%" (
    echo %YELLOW%Creando archivo %REQUIREMENTS%...%RESET%
    (
        echo # Requisitos para el curso de Desarrollo Backend
        echo # Fecha: %date% %time%
        echo.
        echo # Framework web
        echo Django^>=4.2.0,^<5.0.0
        echo.
        echo # Base de datos
        echo psycopg2-binary^>=2.9.5
        echo.
        echo # Variables de entorno
        echo python-dotenv^>=1.0.0
        echo.
        echo # Herramientas de desarrollo
        echo django-extensions^>=3.2.0
        echo.
        echo # API REST ^(opcional^)
        echo djangorestframework^>=3.14.0
    ) > %REQUIREMENTS%
    echo %GREEN%OK Archivo %REQUIREMENTS% creado%RESET%
) else (
    echo %GREEN%OK Archivo %REQUIREMENTS% encontrado%RESET%
)
echo.

REM Actualizar pip
echo %YELLOW%[4/5] Actualizando pip...%RESET%
call %PIP% install --upgrade pip --quiet
if %errorlevel% neq 0 (
    echo %RED%ADVERTENCIA: No se pudo actualizar pip, continuando...%RESET%
) else (
    echo %GREEN%OK pip actualizado correctamente%RESET%
)
echo.

REM Instalar dependencias
echo %YELLOW%[5/5] Instalando dependencias desde %REQUIREMENTS%...%RESET%
echo %YELLOW%Esto puede tomar varios minutos, por favor espera...%RESET%
echo.

call %PIP% install -r %REQUIREMENTS%
if %errorlevel% neq 0 (
    echo.
    echo %RED%ERROR: No se pudieron instalar todas las dependencias%RESET%
    echo %YELLOW%Revisa el archivo %REQUIREMENTS% y tu conexion a internet%RESET%
    echo.
    pause
    exit /b 1
)
echo.
echo %GREEN%OK Dependencias instaladas correctamente%RESET%
echo.

REM Resumen final
echo.
echo %GREEN%=====================================================================%RESET%
echo %GREEN%         INSTALACION COMPLETADA EXITOSAMENTE%RESET%
echo %GREEN%=====================================================================%RESET%
echo.
echo %CYAN%Para ACTIVAR el entorno virtual:%RESET%
echo   %YELLOW%%VENV_NAME%\Scripts\activate%RESET%
echo.
echo %CYAN%Para DESACTIVAR el entorno virtual:%RESET%
echo   %YELLOW%deactivate%RESET%
echo.
echo %CYAN%Para ejecutar Django:%RESET%
echo   %YELLOW%python manage.py runserver%RESET%
echo.
echo %CYAN%Para crear un proyecto Django:%RESET%
echo   %YELLOW%django-admin startproject mi_proyecto .%RESET%
echo.
echo %GREEN%Listo para comenzar a desarrollar!%RESET%
echo.
echo %CYAN%Presiona cualquier tecla para salir...%RESET%
pause >nul