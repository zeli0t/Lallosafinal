@echo off
echo ******************************************
echo *                                        *
echo *          LA LLOSA MOTORS               *
echo *   Sistema de Gestion de Presupuestos   *
echo *                                        *
echo ******************************************
echo.

rem Verificar si Python está instalado
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python no esta instalado en este sistema.
    echo.
    echo Por favor, descarga e instala Python 3.7 o superior desde:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANTE: Marca la opcion "Add Python to PATH" durante la instalacion.
    echo.
    pause
    exit /b 1
)

rem Verificar directorio de datos
if not exist "data" (
    echo Creando directorio de datos...
    mkdir data
)

rem Verificar si los requisitos están instalados
echo Verificando dependencias...
python -c "import flask" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Instalando dependencias necesarias. Esto solo se realizara una vez.
    echo Por favor espere...
    python -m pip install flask flask-sqlalchemy gunicorn
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: No se pudieron instalar las dependencias.
        pause
        exit /b 1
    )
    echo Dependencias instaladas correctamente.
)

echo.
echo Iniciando LA LLOSA MOTORS...
echo La aplicacion se abrira en su navegador en unos segundos.
echo Si no se abre automaticamente, abra su navegador y visite: http://localhost:5000
echo.
echo Presione CTRL+C en esta ventana para cerrar la aplicacion cuando termine.
echo.

python iniciar_app.py
pause