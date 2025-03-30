import os
import sys
import webbrowser
from threading import Timer
import subprocess
import sqlite3
import shutil
from pathlib import Path

# Establecer la variable PYTHONPATH para encontrar módulos 
# cuando se ejecuta como aplicación empaquetada
if getattr(sys, 'frozen', False):
    # Ajustar el path para encontrar los módulos en la aplicación empaquetada
    bundle_dir = os.path.dirname(sys.executable)
    sys.path.insert(0, bundle_dir)
    os.chdir(bundle_dir)  # Cambiar al directorio de la aplicación

# Configuración de directorios y rutas
def get_app_dir():
    """Obtiene el directorio de la aplicación para guardar datos"""
    if getattr(sys, 'frozen', False):
        # Si estamos en una aplicación empaquetada con PyInstaller
        app_dir = os.path.dirname(sys.executable)
    else:
        # Si estamos en desarrollo
        app_dir = os.path.dirname(os.path.abspath(__file__))
    
    return app_dir

def ensure_data_dir():
    """Asegura que exista el directorio de datos"""
    app_dir = get_app_dir()
    data_dir = os.path.join(app_dir, 'data')
    
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Asegurarse de que exista una base de datos SQLite
    db_path = os.path.join(data_dir, 'lallosa.db')
    
    # Establecer la variable de entorno para la base de datos ANTES de cualquier importación
    os.environ['DATABASE_URL'] = f'sqlite:///{db_path}'
    
    # Si no existe el archivo de base de datos, lo creamos
    if not os.path.exists(db_path):
        print(f"Creando nueva base de datos en {db_path}")
        conn = sqlite3.connect(db_path)
        conn.close()
        
        try:
            # Importar después de configurar las variables de entorno
            import models
            from app import db, app
            
            with app.app_context():
                db.create_all()
                print("Base de datos inicializada con éxito")
        except Exception as e:
            print(f"Error al inicializar la base de datos: {e}")
    
    # Verificar/copiar directorios de recursos en el ejecutable empaquetado
    if getattr(sys, 'frozen', False):
        for dirname in ['static', 'templates', 'attached_assets']:
            src_dir = os.path.join(app_dir, dirname)
            if not os.path.exists(src_dir):
                # Buscar en directorio actual o relativo
                os.makedirs(src_dir, exist_ok=True)
                if os.path.exists(dirname):  # Solo copiar si existe en desarrollo
                    try:
                        print(f"Copiando directorio {dirname} a {src_dir}")
                        shutil.copytree(dirname, src_dir, dirs_exist_ok=True)
                    except Exception as e:
                        print(f"Error al copiar recursos: {e}")
    
    return data_dir

def open_browser():
    """Abre el navegador predeterminado con la aplicación"""
    try:
        webbrowser.open('http://localhost:5000')
    except Exception as e:
        print(f"Error al abrir navegador: {e}")

def main():
    try:
        # Configurar el entorno
        data_dir = ensure_data_dir()
        print(f"Directorio de datos: {data_dir}")
        
        # Importar después de configurar el entorno
        from app import app
        
        # Abrir el navegador después de 1 segundo
        Timer(1, open_browser).start()
        
        # Ejecutar la aplicación Flask
        print("Iniciando servidor web en http://localhost:5000")
        app.run(host='localhost', port=5000, debug=False)
    except Exception as e:
        print(f"Error crítico: {e}")
        input("Presione ENTER para cerrar...")

if __name__ == '__main__':
    main()