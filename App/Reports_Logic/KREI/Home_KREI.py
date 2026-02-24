"""
DESARROLLADOR
LUIS A. PEREZ
"""
import sys
import os
import shutil
from ..globalModulesShare.resources import *
from PyQt6.QtWidgets import QWidget
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QPixmap, QBrush, QColor
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QPointF
from webbrowser import *
from ..globalModulesShare.ContenedorVariables import Variables
from ..globalModulesShare.Inicio_FechaMovimiento import *
from .KenworthConnect import *
from ..ventanaspy.V_KREI import *
from ..globalModulesShare.mensajes_alertas import Mensajes_Alertas
import subprocess
import traceback

class Home_KREI(QMainWindow, QDialog):
    closed = pyqtSignal()
    def __init__(self):
        super(Home_KREI,self).__init__()
        self.variables = Variables()
        Icon_Cerrar = QIcon(":/Source/Icon_Close.png")
        Icon_Minimizar = QIcon(":/Source/Icon_Minimize.png")
        Icon_Help = QIcon(":/Source/Icon_Help.png")
        Icon_Delete = QIcon(":/Source/Icon_Delete.png")
        Icon_Proccess = QIcon(":/Source/Icon_Proccess.png")
        Icon_Upload = QIcon(":/Source/Icon_Upload.png")
        logo = QPixmap(":/Source/LOGOKREI.png")
        self.setWindowIcon(QIcon(":/Source/LOGO_KREI_3.ico"))
        
        self.Creacion_Carpetas()
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.Ventana = Ui_Kenworth_KREI()
        self.Ventana.setupUi(self)
        self.Ventana.lblLogoKWKREI.setPixmap(logo)
        self.Ventana.btc_btc_Cerrar.setIcon(Icon_Cerrar)
        self.Ventana.btc_btc_Minimizar.setIcon(Icon_Minimizar)
        self.Ventana.btn_btn_Ayuda.setIcon(Icon_Help)
        self.Ventana.btn_btn_Eliminar.setIcon(Icon_Delete)
        self.Ventana.btn_btn_Eliminar.setIconSize(QtCore.QSize(24, 24))
        self.Ventana.btn_btn_Comenzar.setIcon(Icon_Proccess)
        self.Ventana.btn_btn_Comenzar.setIconSize(QtCore.QSize(24, 24))
        self.Ventana.btn_btn_Subir.setIcon(Icon_Upload)
        self.Ventana.btn_btn_Subir.setIconSize(QtCore.QSize(24, 24))
        self.Hilo = trabajohilo()
        self.Ventana.btn_btn_Subir.clicked.connect(self.Cargar)
        self.Ventana.btn_btn_Comenzar.clicked.connect(self.ComenzarProceso)
        self.Ventana.btn_btn_Eliminar.clicked.connect(self.RemoveProcessed)
        self.Ventana.btn_btn_Ayuda.clicked.connect(self.Ayuda)
        self.Ventana.btc_btc_Cerrar.clicked.connect(self.Cerrar)
        self.Ventana.btc_btc_Minimizar.clicked.connect(self.Minimizar)
        self.Ventana.btn_btn_Errores.clicked.connect(self.abrir_ruta_errores)
        self.Ventana.btn_btn_Originales.clicked.connect(self.abrir_ruta_originales)
        self.Ventana.btn_btn_Procesados.clicked.connect(self.abrir_ruta_procesados)

        self.Ventana.actionFechaMovimiento.triggered.connect(self.FechaMovimiento)

        self.Hilo.signal.connect(self.mensajeTrabajoTerminado)
        self.Hilo.signalDocumentosErroneos.connect(self.mensajeArchivoErroneo)
        self.Hilo.signalNombreArchivo.connect(self.nombreArchivoTrabajando)
        self.Hilo.signalShowTrabajos.connect(self.Show_Data_Trabajos)
        self.Hilo.signalShowProcesados.connect(self.Show_Data_Procesado)
        
        self.variables.actualizar_fecha_movimiento()
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()
        
    def closeEvent(self, event):
        super().closeEvent(event)
        self.closed.emit()
        
    def FechaMovimiento(self):
        self.ventana_obj = Home_DateMovement()
        self.ventana_obj.show()

    def abrir_ruta_errores(self):
        self.Creacion_Carpetas()
        options = QFileDialog().options()
        options |= QFileDialog.Option.ReadOnly
        file_path, _ = QFileDialog.getOpenFileNames(self, 'Abrir Archivo Excel', self.variables.ruta_errores_krei, 'Excel Archivos (*.xlsx);; CSV Archivos (*.csv)',options=options)
        
        if file_path:
            try:
                for path in file_path:
                    subprocess.Popen(['start', 'excel', path], shell=True)
            except Exception as e:
                Mensajes_Alertas(
                    "Error",
                    f"Error al abrir el documento.\n{e}",
                    QMessageBox.Icon.Warning,
                    None,
                    botones=[
                        ("Aceptar", self.Aceptar_callback)
                    ]
                ).mostrar
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()
    def abrir_ruta_originales(self):
        self.Creacion_Carpetas()
        options = QFileDialog().options()
        options |= QFileDialog.Option.ReadOnly
        file_path, _ = QFileDialog.getOpenFileNames(self, 'Abrir Archivo Excel', self.variables.ruta_original_krei, 'Excel Archivos (*.xlsx);; CSV Archivos (*.csv)',options=options)
        
        if file_path:
            try:
                for path in file_path:
                    subprocess.Popen(['start', 'excel', path], shell=True)
            except Exception as e:
                Mensajes_Alertas(
                    "Error",
                    f"Error al abrir el documento.\n{e}",
                    QMessageBox.Icon.Warning,
                    None,
                    botones=[
                        ("Aceptar", self.Aceptar_callback)
                    ]
                ).mostrar
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()
    def abrir_ruta_procesados(self):
        self.Creacion_Carpetas()
        options = QFileDialog().options()
        options |= QFileDialog.Option.ReadOnly
        file_path, _ = QFileDialog.getOpenFileNames(self, 'Abrir Archivo Excel', self.variables.ruta_exitosos_krei, 'Excel Archivos (*.xlsx);; CSV Archivos (*.csv)',options=options)
        
        if file_path:
            try:
                for path in file_path:
                    subprocess.Popen(['start', 'excel', path], shell=True)
            except Exception as e:
                Mensajes_Alertas(
                    "Error",
                    f"Error al abrir el documento.\n{e}",
                    QMessageBox.Icon.Warning,
                    None,
                    botones=[
                        ("Aceptar", self.Aceptar_callback)
                    ]
                ).mostrar
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()

    def mensajeTrabajoTerminado(self):
        Mensajes_Alertas(
            "Trabajos Terminados",
            "Todos los trabajos que se comenzaron fueron insertados por el proceso lógico del sistema.",
            QMessageBox.Icon.Information,
            None,
            botones=[
                ("Aceptar", self.Aceptar_callback)
            ]
        ).mostrar
        textoVacio =""
        self.nombreArchivoTrabajando(textoVacio)
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()

    def mensajeArchivoErroneo(self, mensaje = None, detalle = None):
        if detalle is None:
            Mensajes_Alertas(
                "Errores durante el proceso",
                f'Los documentos que no se lograron procesar son:\n{mensaje}\nLa ruta de los errores es:\n {self.variables.ruta_errores_krei}',
                QMessageBox.Icon.Critical,
                f"Cuando el sistema muestra un error como este, existen algunos factores que se tienen que tomar en cuenta:\n1.- El nombre del documento no tiene la nomenclatura correcta.\n2.- El documento original no contiene las columnas a trabajar o su contendo es incorrecto.\n3.- EL documento no es el correcto o esta corrupto.",
                botones=[
                    ("Aceptar", self.Aceptar_callback)
                ]
            ).mostrar
        else:
            Mensajes_Alertas(
                "Errores durante el proceso",
                f'Los documentos que no se lograron procesar son:\n{mensaje}\nLa ruta de los errores es:\n {self.variables.ruta_errores_krei}',
                QMessageBox.Icon.Critical,
                f"Cuando el sistema muestra un error como este, existen algunos factores que se tienen que tomar en cuenta:\n1.- El nombre del documento no tiene la nomenclatura correcta.\n2.- El documento original no contiene las columnas a trabajar o su contendo es incorrecto.\n3.- EL documento no es el correcto o esta corrupto.\nDetalles del error:\n{detalle}",
                botones=[
                    ("Aceptar", self.Aceptar_callback)
                ]
            ).mostrar
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()

    def nombreArchivoTrabajando(self, nombre):
        if (nombre != ""):
            self.Ventana.lbl_TrabajandoCon.setText(f'Trabajando Con:')
            self.Ventana.lbl_NombreReporte.setText(f'{nombre}')
        else:
            self.Ventana.lbl_TrabajandoCon.setText(f'TERMINADO')
            self.Ventana.lbl_NombreReporte.setText(f'')
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()

    def mousePressEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.drag_start_position = event.globalPosition() - QPointF(self.pos())
    
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            if self.drag_start_position is not None:
                new_pos = event.globalPosition() - self.drag_start_position
                self.move(new_pos.toPoint())
    def Show_Data_Trabajos(self):
        archivos_para_mostrar = os.listdir(self.variables.ruta_Trabajos_krei)
        self.Ventana.Tabla_Cola.setRowCount(len(archivos_para_mostrar))
        self.Ventana.Tabla_Cola.setColumnCount(1)
        self.Ventana.Tabla_Cola.setHorizontalHeaderLabels(["Nombre del archivo"])
        self.Ventana.Tabla_Cola.setStyleSheet("color:#000000;")
        for fila, archivo in enumerate(archivos_para_mostrar):
            elemento = QTableWidgetItem(archivo)
            elemento.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)  # Bloqueamos la edición
            elemento.setForeground(QBrush(QColor(0, 0, 0)))
            self.Ventana.Tabla_Cola.setItem(fila, 0, elemento)
        header = self.Ventana.Tabla_Cola.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setStyleSheet("background-color:#4096d8; color:#FFFFFF;")

        verticalHeader = self.Ventana.Tabla_Cola.verticalHeader()
        verticalHeader.setStyleSheet("background-color:#4096d8; color:#FFFFFF;")

    def Show_Data_Procesado(self):
        archivos_para_mostrar = os.listdir(self.variables.ruta_exitosos_krei)
        self.Ventana.Tabla_Procesado.setRowCount(len(archivos_para_mostrar))
        self.Ventana.Tabla_Procesado.setColumnCount(1)
        self.Ventana.Tabla_Procesado.setHorizontalHeaderLabels(["Nombre del archivo"])
        self.Ventana.Tabla_Procesado.setStyleSheet("color:#000000;")
        for fila, archivo in enumerate(archivos_para_mostrar):
            elemento = QTableWidgetItem(archivo)
            elemento.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
            elemento.setForeground(QBrush(QColor(0, 0, 0)))
            self.Ventana.Tabla_Procesado.setItem(fila, 0, elemento)
        header = self.Ventana.Tabla_Procesado.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setStyleSheet("background-color:#4096d8; color:#FFFFFF;")

        verticalHeader = self.Ventana.Tabla_Procesado.verticalHeader()
        verticalHeader.setStyleSheet("background-color: #4096d8; color:#FFFFFF;")


    def Creacion_Carpetas(self):
        rutas_a_verificar = [
            self.variables.ruta_Trabajos_krei,
            self.variables.ruta_original_krei,
            self.variables.ruta_errores_krei,
            self.variables.ruta_exitosos_krei
        ]
        
        todas_existen = all(os.path.exists(ruta) for ruta in rutas_a_verificar)
        
        if todas_existen:
            pass
        else:
            for ruta in rutas_a_verificar:
                if not os.path.exists(ruta):
                    os.makedirs(ruta, exist_ok=True)
            

    def Cerrar(self):
        self.close()
    def Minimizar(self):
        self.showMinimized()
    
    def Cargar(self):
        self.Creacion_Carpetas()
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()
        ubicacion_carga = os.chdir(self.variables.route_kwkrei)
        options = QFileDialog().options()
        options |= QFileDialog.Option.ReadOnly
        options |= QFileDialog.Option.HideNameFilterDetails
        options |= QFileDialog.Option.DontResolveSymlinks

        selected_filter = "Hojas de Excel (*.xlsx);;Todos los archivos (*)"
        
        if os.path.isdir(self.variables.ruta_Trabajos_krei) == True:
            try:
                file_names, filter_selected = QFileDialog.getOpenFileNames(
                    self,
                    "Selecciona archivo(s)",
                    "",
                    selected_filter,
                    options=options
                )
                for nombre_archivo in file_names:
                    shutil.move(nombre_archivo, self.variables.ruta_Trabajos_krei)
            except:
                pass
        else:
            os.makedirs(self.variables.ruta_Trabajos_krei)
            try:
                file_names, filter_selected = QFileDialog.getOpenFileNames(
                    self,
                    "Selecciona archivo(s)",
                    "",
                    selected_filter,
                    options=options
                )
                for nombre_archivo in file_names:
                    shutil.move(nombre_archivo, self.variables.ruta_Trabajos_krei)
            except:
                pass
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()

    def ComenzarProceso(self):
        if self.Hilo.isRunning():
            self.Hilo.requestInterruption()
        else:
            self.Hilo.start()

    def eliminar(self):
        carpeta_contenido_eliminar = os.listdir(self.variables.ruta_exitosos_krei)
        for archivo in carpeta_contenido_eliminar:
            if (len(carpeta_contenido_eliminar) != 0):
                try:
                    archivo_completo = os.path.join(self.variables.ruta_exitosos_krei, archivo)
                    os.remove(archivo_completo)
                except:
                    pass
            else:
                pass
    def RemoveProcessed(self):
        self.Creacion_Carpetas()
        ruta_trabajos_procesados = os.listdir(self.variables.ruta_exitosos_krei)
        if (len(ruta_trabajos_procesados) == 0):
            Mensajes_Alertas(None,None,None,None,botones=[("Aceptar", self.Aceptar_callback)]).Eliminar_vacio
        else:
            Mensajes_Alertas(None,None,None,None,botones=[("Eliminar", self.eliminar)]).Eliminar_lleno
        self.Show_Data_Trabajos()
        self.Show_Data_Procesado()

    def Ayuda(self):
        Mensajes_Alertas(
            "Información de Ayuda",
            'Si tienes problemas con la aplicación debido a que no sabes como guardar tus archivos de excel para que puedan ser transformados.\nPuedes ver el manual de usuario dando click en el boton de "Ver"',
            QMessageBox.Icon.Information,
            None,
            botones = [
                ("Aceptar", self.Aceptar_callback),
                ("Ver", self.Ayuda_callback)
            ]
        ).Apartado_Ayuda
    def Aceptar_callback(self):
        pass
    def Ayuda_callback(self):
        open_new(self.variables.pdf)

class trabajohilo(QThread):
    signal = pyqtSignal()
    signalDocumentosErroneos = pyqtSignal(str, str)
    signalShowTrabajos = pyqtSignal()
    signalShowProcesados = pyqtSignal()
    signalNombreArchivo =  pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.variables = Variables()
        self.mensaje_del_error = None

    def run(self):
        array_errores = []
        diccionario_archivos = {
            "OSEKREI.xlsx" : KenworthConnect().OrdenesServicioKREIKWESTE,
            "OSSKREI.xlsx" : KenworthConnect().OrdenesServicioKREIKWSUR,
            "CEKREI.xlsx" : KenworthConnect().CreditoKREIKWESTE,
            "CSKREI.xlsx" : KenworthConnect().CreditoKREIKWSUR,
            "ICEKREI.xlsx" : KenworthConnect().InventarioKREIKWESTE,
            "ICSKREI.xlsx" :KenworthConnect().InventarioKREIKWSUR,
            "REKREI.xlsx" : KenworthConnect().RefaccionesKREIKWESTE,
            "RSKREI.xlsx" : KenworthConnect().RefaccionesKREIKWSUR,
            "SDEKREI.xlsx" : KenworthConnect().ServicioDetalladoKREIKWESTE,
            "SDSKREI.xlsx" : KenworthConnect().ServicioDetalladoKREIKWSUR,
            "RFEKREI.xlsx" : KenworthConnect().ResultadosFinancierosEsteKREI,
            "RFSKREI.xlsx" : KenworthConnect().ResultadosFinancierosSurKREI

        }
        while True:
            carpeta_de_trabajos = os.listdir(self.variables.ruta_Trabajos_krei)
            if not carpeta_de_trabajos:
                nombre_documento = ""
                self.signalNombreArchivo.emit(nombre_documento)
                return
            else:
                for nombre_archivo in carpeta_de_trabajos:
                    if (nombre_archivo in diccionario_archivos):
                        try:
                            self.signalNombreArchivo.emit(nombre_archivo)
                            Metodo = diccionario_archivos[nombre_archivo]
                            Metodo()
                            self.Comprobacion_Originales(nombre_archivo)
                            self.signalShowTrabajos.emit()
                            self.signalShowProcesados.emit()
                        except Exception as e:
                            array_errores.append(nombre_archivo)
                            self.Comprobacion_Errores(nombre_archivo)
                            self.mensaje_del_error = traceback.format_exc()
                            self.signalShowTrabajos.emit()
                            self.signalShowProcesados.emit()
                            continue
                    else:
                        nombre_archivo_error = nombre_archivo
                        array_errores.append(nombre_archivo_error)
                        self.Comprobacion_Errores(nombre_archivo)
                        self.signalShowTrabajos.emit()
                        self.signalShowProcesados.emit()
                        continue
                self.signalShowTrabajos.emit()
                self.signalShowProcesados.emit()
            if array_errores:
                mensaje = ""
                x = 1
                for i in array_errores:
                    mensaje += f'{x}.-{i}\n'
                    x += 1
                if self.mensaje_del_error is not None:
                    self.signalDocumentosErroneos.emit(mensaje, self.mensaje_del_error)
                else:
                    self.signalDocumentosErroneos.emit(mensaje, None)
                continue
            self.signalShowTrabajos.emit()
            self.signalShowProcesados.emit()

    def Comprobacion_Originales(self, file_name):
        ruta_origen = os.path.join(self.variables.ruta_Trabajos_krei, file_name)
        destino_archivoOriginal = os.path.join(self.variables.ruta_original_krei, file_name)
        if not os.path.exists(destino_archivoOriginal):
            shutil.move(ruta_origen, self.variables.ruta_original_krei)
        else:
            os.remove(destino_archivoOriginal)
            shutil.move(ruta_origen, self.variables.ruta_original_krei)

    def Comprobacion_Errores(self, file_name):
        ruta_origen = os.path.join(self.variables.ruta_Trabajos_krei, file_name)
        destino_archivoOriginal = os.path.join(self.variables.ruta_errores_krei, file_name)
        if not os.path.exists(destino_archivoOriginal):
            shutil.move(ruta_origen, self.variables.ruta_errores_krei)
        else:
            os.remove(destino_archivoOriginal)
            shutil.move(ruta_origen, self.variables.ruta_errores_krei)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Ventana = Home_KREI()
    Ventana.show()
    sys.exit(app.exec_())