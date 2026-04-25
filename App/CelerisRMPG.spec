# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [
    (
        'Reports_Logic/globalModulesShare/.env', 
        'Reports_Logic/globalModulesShare'
    )
        ]
# KENWORTH REPORTES
binaries = [
    ('InicioSesion.pyd', '.'),
    ('Reports_Logic/globalModulesShare/kuchotsa.pyd', '.'),
    ('Reports_Logic/globalModulesShare/VersionCheck.pyd', '.'),
    # SONORA
    ('Reports_Logic/Kenworth_Sonora/Logica_Reportes/VentasOrdenesServicio.pyd', '.'),
    ('Reports_Logic/Kenworth_Sonora/Logica_Reportes/TrabajosPorEstado.pyd', '.'),
    ('Reports_Logic/Kenworth_Sonora/Logica_Reportes/ServicioDetallado.pyd', '.'),
    ('Reports_Logic/Kenworth_Sonora/Logica_Reportes/SalidasEnVale.pyd', '.'),
    ('Reports_Logic/Kenworth_Sonora/Logica_Reportes/ResultadosFinancieros.pyd', '.'),
    ('Reports_Logic/Kenworth_Sonora/Logica_Reportes/Refacciones.pyd', '.'),
    ('Reports_Logic/Kenworth_Sonora/Logica_Reportes/PagoClientes.pyd', '.'),
    ('Reports_Logic/Kenworth_Sonora/Logica_Reportes/OrdenesDeServicio.pyd', '.'),
    ('Reports_Logic/Kenworth_Sonora/Logica_Reportes/InventarioUnidades.pyd', '.'),
    ('Reports_Logic/Kenworth_Sonora/Logica_Reportes/InventarioCosteadoAndDia.pyd', '.'),
    ('Reports_Logic/Kenworth_Sonora/Logica_Reportes/Credito.pyd', '.'),
    ('Reports_Logic/Kenworth_Sonora/Logica_Reportes/Compras.pyd', '.'),
    ('Reports_Logic/Kenworth_Sonora/Logica_Reportes/BackOrder.pyd', '.'),
    # KREI
    ('Reports_Logic/KREI/Logica_Reportes/KREI_Compras.pyd', '.'),
    ('Reports_Logic/KREI/Logica_Reportes/KREI_CreditoKW.pyd', '.'),
    ('Reports_Logic/KREI/Logica_Reportes/KREI_InventarioKW.pyd', '.'),
    ('Reports_Logic/KREI/Logica_Reportes/KREI_OrdenesKW.pyd', '.'),
    ('Reports_Logic/KREI/Logica_Reportes/KREI_Refacciones.pyd', '.'),
    ('Reports_Logic/KREI/Logica_Reportes/KREI_ResultadosFinancieros.pyd', '.'),
    ('Reports_Logic/KREI/Logica_Reportes/KREI_ServicioDetallado.pyd', '.'),
    # RIO BRAVO
    ('Reports_Logic/Rio_Bravo/Logica_Reportes/Back_Order.pyd', '.'),
    ('Reports_Logic/Rio_Bravo/Logica_Reportes/Compras.pyd', '.'),
    ('Reports_Logic/Rio_Bravo/Logica_Reportes/Contabilidad.pyd', '.'),
    ('Reports_Logic/Rio_Bravo/Logica_Reportes/Credito.pyd', '.'),
    ('Reports_Logic/Rio_Bravo/Logica_Reportes/Financiero.pyd', '.'),
    ('Reports_Logic/Rio_Bravo/Logica_Reportes/InventarioCosteado.pyd', '.'),
    ('Reports_Logic/Rio_Bravo/Logica_Reportes/InventarioUnidades.pyd', '.'),
    ('Reports_Logic/Rio_Bravo/Logica_Reportes/Ordenes_Servicio.pyd', '.'),
    ('Reports_Logic/Rio_Bravo/Logica_Reportes/PagosClientes.pyd', '.'),
    ('Reports_Logic/Rio_Bravo/Logica_Reportes/Refacciones.pyd', '.'),
    ('Reports_Logic/Rio_Bravo/Logica_Reportes/Salidas_Vale.pyd', '.'),
    ('Reports_Logic/Rio_Bravo/Logica_Reportes/Servicio_Detallado.pyd', '.'),
    ('Reports_Logic/Rio_Bravo/Logica_Reportes/Trabajos_Por_Estado.pyd', '.'),
    ('Reports_Logic/Rio_Bravo/Logica_Reportes/VentasPerdidas.pyd', '.')
]

hiddenimports = [
    'Reports_Logic.globalModulesShare.WebScraping',
    'Reports_Logic.globalModulesShare.ContenedorVariables', 
    'Reports_Logic.globalModulesShare.ConcesionariosModel',
    'Reports_Logic.KenworthEste.Logica_Reportes.ServicioDetallado',
    'Reports_Logic.globalModulesShare.mensajes_alertas',
    'Reports_Logic.globalModulesShare.kuchotsa',
    'Reports_Logic.globalModulesShare.icono',
    'Reports_Logic.globalModulesShare.documentos_json',
    'Reports_Logic.Home',
    'Reports_Logic.ventanaspy.inicio_sesion',
    'Reports_Logic.globalModulesShare.resources',
    'Reports_Logic.globalModulesShare.VersionCheck',
    'Reports_Logic.globalModulesShare.Home_rutas',
    'Reports_Logic.globalModulesShare.InicialClassObjetivos',
    'Reports_Logic.ventanaspy.V_ProcesadorGeneral',
    'Reports_Logic.KenworthEste.Controller.FuncionesBalanzaComprobacionContabilidad',
    'Reports_Logic.globalModulesShare.Inicio_FechaMovimiento'
    ]
tmp_ret = collect_all('pandas')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('numpy')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('openpyxl')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('tkinter')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('subprocess')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('time')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('requests')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('beautifulsoup4')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('selenium')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('json')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('pathlib')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('PyQt6')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('dotenv')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('psutil')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('xlrd')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('lxml')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('charset_normalizer')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('fastexcel')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('xlsxwriter')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('traceback')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('shutil')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['login.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='CelerisRMPG',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icono2.ico'],
)


