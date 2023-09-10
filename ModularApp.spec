# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('D:/Documentos/Cucei/Modular/*.h5', '.'),  # Incluye todos los archivos .h5
        ('D:/Documentos/Cucei/Modular/*.py', '.'),  # Incluye todos los archivos .py
        ('D:/Documentos/Cucei/Modular/*.npy', '.'),  # Incluye todos los archivos .npy
        ('D:/Documentos/Cucei/Modular/*.png', '.'),  # Incluye todos los archivos .png
        ('D:/Documentos/Cucei/Modular/*.jpg', '.'),  # Incluye todos los archivos .jpg
        ('D:/Documentos/Cucei/Modular/comparison', 'comparison'),  # Incluye la carpeta 'comparison'
        ('D:/Documentos/Cucei/Modular/detection', 'detection'),  # Incluye la carpeta 'detection'
        ('D:/Documentos/Cucei/Modular/gender_classification', 'gender_classification'),  # Incluye la carpeta 'gender_classification'
        ('D:/Documentos/Cucei/Modular/load', 'load'),  # Incluye la carpeta 'load'
        ('D:/Documentos/Cucei/Modular/pdfgenerator', 'pdfgenerator'),  # Incluye la carpeta 'pdfgenerator'
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ModularApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)