import os
import sys
import webbrowser
import sqlite3
import time
import platform
from threading import Timer

# Determinar si estamos ejecutando en modo desarrollo
def is_development():
    return os.environ.get("REPLIT_ENVIRONMENT") is not None

# Obtener el directorio base de la aplicación
def get_base_dir():
    return os.path.dirname(os.path.abspath(__file__))

def abrir_navegador():
    """Abre el navegador predeterminado con la aplicación"""
    try:
        time.sleep(2)  # Esperar a que la aplicación esté lista
        webbrowser.open('http://localhost:5000')
        print("Navegador abierto. Si no se ha abierto automáticamente, acceda a: http://localhost:5000")
    except Exception as e:
        print(f"No se pudo abrir el navegador automáticamente: {e}")
        print("Por favor, abra manualmente http://localhost:5000 en su navegador.")

# Configurar el entorno antes de importar la aplicación
def configurar_entorno():
    # Asegurarse de que estamos en el directorio correcto
    base_dir = get_base_dir()
    os.chdir(base_dir)
    
    # Crear directorio de datos si no existe
    data_dir = os.path.join(base_dir, 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Crear directorio para JSON si no existe
    json_dir = os.path.join(base_dir, 'static', 'data')
    if not os.path.exists(json_dir):
        os.makedirs(json_dir)
    
    # Configurar la base de datos SQLite
    db_path = os.path.join(data_dir, 'lallosa.db')
    os.environ['DATABASE_URL'] = f'sqlite:///{db_path}'
    
    # Configurar una clave secreta para Flask
    os.environ["SESSION_SECRET"] = "lallosa_motors_secreto"
    
    # Si la base de datos no existe, crearla
    if not os.path.exists(db_path):
        print("Creando nueva base de datos...")
        conn = sqlite3.connect(db_path)
        conn.close()

# Configurar el entorno al importar este módulo
configurar_entorno()

# Importar la aplicación Flask
from app import app

def main():
    try:
        print("="*60)
        print("   LA LLOSA MOTORS - Sistema de Gestión de Presupuestos")
        print("="*60)
        print(f"Sistema operativo: {platform.system()} {platform.release()}")
        print(f"Directorio de datos: {os.path.join(get_base_dir(), 'data')}")
        
        # Abrir el navegador automáticamente
        if not is_development():
            Timer(2, abrir_navegador).start()
        
        # Iniciar el servidor Flask
        print("Iniciando servidor web...")
        app.run(host='0.0.0.0', port=5000, debug=is_development())
        
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        # Imprimir detalles técnicos
        import traceback
        traceback.print_exc()
        print("\nSi el problema persiste, por favor contacte al soporte técnico.")
        # Mantener la ventana abierta
        input("\nPresione ENTER para cerrar...")

if __name__ == '__main__':
    main()