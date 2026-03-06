# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

block_cipher = None

# 1. LISTA DE MÓDULOS OFUSCADOS
modulos_ofuscados = [
    'InicioSesion',
    'Reports_Logic.globalModulesShare.kuchotsa',
    'Reports_Logic.globalModulesShare.VersionCheck',
    'Reports_Logic.Kenworth_Sonora.Logica_Reportes.VentasOrdenesServicio',
    'Reports_Logic.Kenworth_Sonora.Logica_Reportes.TrabajosPorEstado',
    'Reports_Logic.Kenworth_Sonora.Logica_Reportes.ServicioDetallado',
    'Reports_Logic.Kenworth_Sonora.Logica_Reportes.SalidasEnVale',
    'Reports_Logic.Kenworth_Sonora.Logica_Reportes.ResultadosFinancieros',
    'Reports_Logic.Kenworth_Sonora.Logica_Reportes.Refacciones',
    'Reports_Logic.Kenworth_Sonora.Logica_Reportes.PagoClientes',
    'Reports_Logic.Kenworth_Sonora.Logica_Reportes.OrdenesDeServicio',
    'Reports_Logic.Kenworth_Sonora.Logica_Reportes.InventarioUnidades',
    'Reports_Logic.Kenworth_Sonora.Logica_Reportes.InventarioCosteadoAndDia',
    'Reports_Logic.Kenworth_Sonora.Logica_Reportes.Credito',
    'Reports_Logic.Kenworth_Sonora.Logica_Reportes.Compras',
    'Reports_Logic.Kenworth_Sonora.Logica_Reportes.BackOrder',
    'Reports_Logic.KREI.Logica_Reportes.KREI_Compras',
    'Reports_Logic.KREI.Logica_Reportes.KREI_CreditoKW',
    'Reports_Logic.KREI.Logica_Reportes.KREI_InventarioKW',
    'Reports_Logic.KREI.Logica_Reportes.KREI_OrdenesKW',
    'Reports_Logic.KREI.Logica_Reportes.KREI_Refacciones',
    'Reports_Logic.KREI.Logica_Reportes.KREI_ResultadosFinancieros',
    'Reports_Logic.KREI.Logica_Reportes.KREI_ServicioDetallado',
    'Reports_Logic.Rio_Bravo.Logica_Reportes.Back_Order',
    'Reports_Logic.Rio_Bravo.Logica_Reportes.Compras',
    'Reports_Logic.Rio_Bravo.Logica_Reportes.Contabilidad',
    'Reports_Logic.Rio_Bravo.Logica_Reportes.Credito',
    'Reports_Logic.Rio_Bravo.Logica_Reportes.Financiero',
    'Reports_Logic.Rio_Bravo.Logica_Reportes.InventarioCosteado',
    'Reports_Logic.Rio_Bravo.Logica_Reportes.InventarioUnidades',
    'Reports_Logic.Rio_Bravo.Logica_Reportes.Ordenes_Servicio',
    'Reports_Logic.Rio_Bravo.Logica_Reportes.PagosClientes',
    'Reports_Logic.Rio_Bravo.Logica_Reportes.Refacciones',
    'Reports_Logic.Rio_Bravo.Logica_Reportes.Salidas_Vale',
    'Reports_Logic.Rio_Bravo.Logica_Reportes.Servicio_Detallado',
    'Reports_Logic.Rio_Bravo.Logica_Reportes.Trabajos_Por_Estado',
    'Reports_Logic.Rio_Bravo.Logica_Reportes.VentasPerdidas',
]

a = Analysis(
    ['login.py'],
    pathex=[],
    binaries=[],
    # AQUÍ DEBE TENER SOLO 2 VALORES
    datas=[('Reports_Logic/globalModulesShare/.env', 'Reports_Logic/globalModulesShare')],
    hiddenimports=modulos_ofuscados,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# 2. RECOLECCIÓN DE LIBRERÍAS
libs = [
    'pandas', 'numpy', 'beautifulsoup4', 'PyQt6', 'selenium', 
    'requests', 'openpyxl', 'psutil', 'xlrd', 'lxml', 
    'tkinter', 'charset_normalizer'
]

for lib in libs:
    tmp_ret = collect_all(lib)
    # Agregamos los resultados asegurando que no se rompa el formato
    a.datas += tmp_ret[0]
    a.binaries += tmp_ret[1]
    a.hiddenimports += tmp_ret[2]

# --- LIMPIEZA POST-ANALYSIS PARA EL OBJETO EXE ---
# Esto asegura que todo tenga 3 elementos antes de llegar a EXE()
def ensure_3_values(lst, type_tag):
    new_lst = []
    for item in lst:
        if len(item) == 2:
            new_lst.append((item[0], item[1], type_tag))
        else:
            new_lst.append(item)
    return new_lst

a.datas = ensure_3_values(a.datas, 'DATA')
a.binaries = ensure_3_values(a.binaries, 'BINARY')

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CelerisRMPG',
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
    entitlements=None,
    icon=['icono2.ico'],
)