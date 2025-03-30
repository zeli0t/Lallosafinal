
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['iniciar_app.py'],
    pathex=[r'F:\lallosa\LaLLosaMotors'],
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
    hooksconfig={},
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
    icon=r'F:\lallosa\LaLLosaMotors\static\img\logo.jpg',
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
