import os
import sys
import webbrowser
import sqlite3
from threading import Timer

# Determinar si estamos ejecutando en modo congelado (PyInstaller)
def is_frozen():
    return getattr(sys, 'frozen', False)

# Obtener el directorio base de la aplicación
def get_base_dir():
    if is_frozen():
        # Estamos ejecutando desde un .exe compilado
        return os.path.dirname(sys.executable)
    else:
        # Estamos ejecutando desde el código fuente
        return os.path.dirname(os.path.abspath(__file__))

# Asegurarse de que estamos en el directorio correcto
base_dir = get_base_dir()
os.chdir(base_dir)

# Crear directorio de datos si no existe
data_dir = os.path.join(base_dir, 'data')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Configurar la base de datos SQLite
db_path = os.path.join(data_dir, 'lallosa.db')
os.environ['DATABASE_URL'] = f'sqlite:///{db_path}'

# Configurar una clave secreta para Flask
os.environ["SESSION_SECRET"] = "lallosa_motors_secreto"

# Configurar las rutas de los recursos cuando se ejecuta desde PyInstaller
if is_frozen():
    # Crear una variable de entorno para indicar que estamos en modo congelado
    os.environ["PYINSTALLER_FROZEN"] = "1"

def abrir_navegador():
    """Abre el navegador predeterminado con la aplicación"""
    webbrowser.open('http://localhost:5000')
    print("Navegador abierto. Si no se ha abierto automáticamente, acceda a: http://localhost:5000")

def main():
    try:
        print("Iniciando LA LLOSA MOTORS...")
        print(f"Directorio de datos: {data_dir}")
        print(f"Base de datos: {db_path}")
        
        # Si la base de datos no existe, crearla
        if not os.path.exists(db_path):
            print("Creando nueva base de datos...")
            conn = sqlite3.connect(db_path)
            conn.close()
        
        # Abrir el navegador después de 2 segundos
        Timer(2, abrir_navegador).start()
        
        # Iniciar el servidor Flask
        print("Iniciando servidor web...")
        from app import app
        app.run(host='localhost', port=5000, debug=False)
        
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        input("Presione ENTER para cerrar...")

if __name__ == '__main__':
    main()