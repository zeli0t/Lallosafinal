# LA LLOSA MOTORS - Sistema de Gestión de Presupuestos
## Instrucciones de Instalación y Uso

Este documento describe las diferentes opciones para ejecutar el sistema de gestión de presupuestos de LA LLOSA MOTORS en equipos Windows.

## Requisitos del sistema

- Windows 7, 8, 10 o 11
- Conexión a Internet para la primera instalación (opcional)
- 100 MB de espacio libre en disco

## Opciones de instalación

Hay tres formas de ejecutar la aplicación:

### Opción 1: Ejecutable empaquetado con PyInstaller (recomendado para usuarios finales)

Esta opción genera un ejecutable independiente que no requiere ninguna instalación adicional en el equipo del usuario. Es la opción más sencilla para usuarios finales.

**Para crear el ejecutable:**

1. Asegúrate de tener Python 3.7 o superior instalado en el equipo que usarás para crear el ejecutable
2. Abre una terminal de comandos y navega hasta la carpeta del proyecto
3. Ejecuta:
   ```
   python build_windows.py
   ```
4. Espera a que termine el proceso de compilación
5. La carpeta `dist` contendrá el ejecutable `LA_LLOSA_MOTORS.exe` y los archivos necesarios

**Para instalar en el equipo del usuario final:**

1. Copia la carpeta `dist` completa al equipo del usuario
2. Renombra la carpeta `dist` a `LA_LLOSA_MOTORS` (opcional)
3. Crea un acceso directo al archivo `LA_LLOSA_MOTORS.exe` en el escritorio
4. La primera vez que se ejecute, Windows puede mostrar una advertencia de seguridad; haz clic en "Más información" y luego en "Ejecutar de todas formas"

**Solución de problemas:**

Si aparece un error sobre "No se encuentra el ordinal 380 en la biblioteca de vínculos dinámicos", necesitarás incluir las bibliotecas de Microsoft Visual C++ Redistributable:

1. Descarga e instala Microsoft Visual C++ Redistributable (x86 y x64) desde la página oficial de Microsoft
2. Coloca las DLLs `msvcp140.dll` y `vcruntime140.dll` en la misma carpeta que el ejecutable

### Opción 2: Archivo por lotes con instalación automática de dependencias

Esta opción utiliza Python, pero se encarga automáticamente de instalar las dependencias necesarias.

**Requisitos:**
- Python 3.7 o superior instalado en el equipo (la primera vez pedirá al usuario instalarlo si no lo tiene)
- Conexión a Internet para la primera ejecución

**Pasos:**
1. Copia toda la carpeta del proyecto al equipo del usuario
2. Haz doble clic en `LA_LLOSA_MOTORS.bat`
3. Si es la primera vez, el script instalará automáticamente las dependencias necesarias
4. La aplicación se abrirá en el navegador predeterminado

### Opción 3: Ejecución directa desde Python (para desarrolladores)

Esta opción es la más flexible y permite realizar modificaciones al código.

**Requisitos:**
- Python 3.7 o superior instalado
- Conocimientos básicos de línea de comandos

**Pasos:**
1. Abre una terminal de comandos y navega hasta la carpeta del proyecto
2. Instala las dependencias manualmente (solo la primera vez):
   ```
   pip install flask flask-sqlalchemy gunicorn
   ```
3. Ejecuta la aplicación:
   ```
   python main.py
   ```
   
## Estructura de datos y archivos

- La aplicación guarda los datos en una base de datos SQLite ubicada en la carpeta `data`
- Los servicios y presupuestos se exportan también como archivos JSON en `static/data`
- Todos los archivos de datos se crean automáticamente al iniciar la aplicación por primera vez

## Solución de problemas

1. **La aplicación no abre en el navegador automáticamente:**
   - Abre manualmente el navegador y accede a http://localhost:5000

2. **Mensaje "Python no está instalado":**
   - Descarga e instala Python desde https://www.python.org/downloads/
   - Marca la opción "Add Python to PATH" durante la instalación

3. **Errores de permisos en Windows:**
   - Ejecuta la aplicación como administrador la primera vez
   - Asegúrate de que la carpeta donde está instalada la aplicación tenga permisos de escritura

4. **La base de datos no guarda los cambios:**
   - Verifica que la carpeta `data` tenga permisos de escritura
   - Asegúrate de cerrar correctamente la aplicación (con Ctrl+C en la ventana de comandos)

## Contacto y soporte

Para obtener asistencia técnica, contacta con:
[Información de contacto]