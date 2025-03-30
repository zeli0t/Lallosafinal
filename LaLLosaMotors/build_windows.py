"""
Script para compilar la aplicación como un ejecutable de Windows (.exe)
que incluye todas las dependencias necesarias (incluido Python).
"""
import os
import sys
import subprocess
import shutil
import platform

def main():
    print("Compilando LA LLOSA MOTORS para Windows...")
    
    # Verificar que estamos en Windows
    if platform.system() != "Windows":
        print("Este script debe ejecutarse en Windows.")
        return
    
    # Instalar PyInstaller si no está instalado
    try:
        import PyInstaller
        print("PyInstaller ya está instalado.")
    except ImportError:
        print("Instalando PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    # Asegurarse de que todas las dependencias estén instaladas
    print("Asegurando que todas las dependencias estén instaladas...")
    dependencies = [
        "flask", 
        "flask-sqlalchemy", 
        "sqlalchemy", 
        "webbrowser", 
        "jinja2", 
        "werkzeug", 
        "itsdangerous", 
        "click", 
        "colorama",
        "markupsafe"
    ]
    
    for dep in dependencies:
        print(f"Verificando {dep}...")
        try:
            __import__(dep.replace("-", "_"))
            print(f"  ✓ {dep} ya está instalado")
        except ImportError:
            print(f"  ✗ Instalando {dep}...")
            subprocess.run([sys.executable, "-m", "pip", "install", dep], check=True)
    
    # Crear directorio dist si no existe
    if not os.path.exists("dist"):
        os.makedirs("dist")
    
    # Directorio actual
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Crear un archivo spec personalizado para un mejor control
    spec_content = f"""
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['iniciar_app.py'],
    pathex=[r'{current_dir}'],
    binaries=[],
    datas=[
        ('static', 'static'),
        ('templates', 'templates'),
    ],
    hiddenimports=[
        'sqlalchemy.sql.default_comparator',
        'flask',
        'jinja2.ext',
        'sqlalchemy.ext.baked',
        'sqlalchemy.ext.declarative',
        'sqlalchemy.ext.indexable',
        'sqlalchemy.ext.instrumentation',
        'sqlalchemy.ext.hybrid',
        'sqlalchemy.ext.serializer',
        'sqlalchemy.ext.horizontal_shard',
        'sqlalchemy.dialects.sqlite',
        'sqlalchemy.dialects.sqlite.base',
        'sqlalchemy.dialects.sqlite.pysqlite',
        'werkzeug.datastructures',
        'werkzeug.exceptions',
        'werkzeug.http',
        'werkzeug.local',
        'werkzeug.routing',
        'werkzeug.utils',
        'werkzeug.wsgi',
        'markupsafe',
        'sqlite3',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='LA_LLOSA_MOTORS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Sin ventana de consola
    icon=r'{os.path.join(current_dir, "static", "img", "logo.jpg")}',
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
"""

    # Guardar el archivo spec
    spec_file = os.path.join(current_dir, "LA_LLOSA_MOTORS.spec")
    with open(spec_file, 'w') as f:
        f.write(spec_content)
    
    # Compilar con PyInstaller usando el archivo .spec
    print("\nCompilando aplicación con PyInstaller...")
    subprocess.run([
        "pyinstaller",
        "--clean",  # Limpiar caché antes de compilar
        "LA_LLOSA_MOTORS.spec"
    ], check=True)
    
    print("\nCreando estructura de directorios para la aplicación...")
    
    # Crear directorios de datos en dist
    dist_dir = os.path.join(current_dir, "dist")
    data_dir = os.path.join(dist_dir, "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Copiar datos iniciales si existen
    static_data_dir = os.path.join(current_dir, "static", "data")
    if os.path.exists(static_data_dir):
        for file in os.listdir(static_data_dir):
            if file.endswith('.json'):
                src = os.path.join(static_data_dir, file)
                dst = os.path.join(data_dir, file)
                shutil.copy2(src, dst)
    
    # Crear un archivo batch de inicio
    batch_file = os.path.join(dist_dir, "Iniciar LA LLOSA MOTORS.bat")
    with open(batch_file, 'w') as f:
        f.write('@echo off\n')
        f.write('echo Iniciando LA LLOSA MOTORS...\n')
        f.write('start LA_LLOSA_MOTORS.exe\n')
    
    print("\n¡Compilación completada!")
    print(f"El ejecutable se encuentra en: {os.path.join(dist_dir, 'LA_LLOSA_MOTORS.exe')}")
    print(f"Para usar la aplicación, ejecuta: {os.path.join(dist_dir, 'Iniciar LA LLOSA MOTORS.bat')}")
    print("\nNOTA IMPORTANTE: Si hay errores de DLL faltantes como 'No se encuentra el ordinal 380'")
    print("es posible que necesites incluir las DLLs del sistema Microsoft Visual C++ Redistributable en el mismo directorio.")
    print("Puedes descargar el instalador de Microsoft Visual C++ Redistributable (x86 y x64) y distribuirlo con tu aplicación.")

if __name__ == "__main__":
    main()