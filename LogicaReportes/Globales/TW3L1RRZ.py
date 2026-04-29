"""
DESARROLLADOR
LUIS A. PEREZ
"""
import sys
from tkinter import messagebox
from PyQt6 import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from Reports_Logic.globalModulesShare.VersionCheck import VersionCheckController
from Reports_Logic.globalModulesShare.resources import *
from Reports_Logic.globalModulesShare import *
from dotenv import load_dotenv
from Front.inicio_sesion import UI_Inicio_Sesion
from Reports_Logic.globalModulesShare.mensajes_alertas import Mensajes_Alertas
from Reports_Logic.globalModulesShare.kuchotsa import *
from Reports_Logic.Home import PrincipalWindow
import Reports_Logic.globalModulesShare.icono as icono
from Reports_Logic.globalModulesShare.ContenedorVariables import *
from Reports_Logic.globalModulesShare.documentos_json import *
from Reports_Logic.globalModulesShare.R9T2FG5Y import *
import os

class InicioSesion(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.variables = Variables()
        
        domains='Reports_Logic/globalModulesShare'
        self.ui = UI_Inicio_Sesion()
        self.ui.setupUi(self) 
        self.setWindowTitle("Inicio de Sesión")
        self.setWindowIcon(QIcon(":/Source/LOGO_KREI_3.ico"))
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.ui.label_2.setPixmap(QPixmap(":/Source/DevRous2.png"))
        self.ui.label_2.setScaledContents(True)
        dotenv_path = os.path.join(os.path.dirname(__file__), domains, '.env')
        self.ui.btn_manejoventana_2.setIcon(QIcon(":Source/Icon_Close.png"))
        load_dotenv(dotenv_path)
        print(os.path.dirname(__file__))
        self.ui.btn_manejoventana.setIcon(QIcon(":Source/Icon_Minimize.png"))
        self.ui.label.setStyleSheet("font-weight: bold;")
        self.ui.w_login.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=45, xOffset=0, yOffset=0))
        self.__User__ = os.getenv('USERNAME')
        self.__Password__ = os.getenv('APP_PASSWORD')
        self.ui.btn_aceptar_ingreso.clicked.connect(self.ingresar)
        self.ui.btn_manejoventana_2.clicked.connect(self.cerrar)
        self.ui.btn_manejoventana.clicked.connect(self.minimizar)
        self.ui.txt_usuario.setStyleSheet("color:#000000;")
        self.ui.txt_usuarioPassword.setStyleSheet("color:#000000;")
        self.ui.label.setStyleSheet("color:#000000;")
        if not os.path.exists(self.variables.help_directory):
            os.makedirs(self.variables.help_directory, exist_ok=True)
        else:
            pass
        self.comprobateVersion()

    def cerrar(self, checked=False):
        self.close()

    def minimizar(self, checked=False):
        self.showMinimized()

    def Aceptar_callback(self, clicked=False):
        pass

    def mousePressEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.drag_start_position = event.globalPosition() - QPointF(self.pos())
    
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            if self.drag_start_position is not None:
                new_pos = event.globalPosition() - self.drag_start_position
                self.move(new_pos.toPoint())
        
    def ingresar(self, checked=False):
        user = self.ui.txt_usuario.text().strip()
        password = self.ui.txt_usuarioPassword.text().strip()
        if all((user, password)):
            respuesta = verificar_acceso(user, password)
            if respuesta['estado'] == True:
                if respuesta['disponible'] == False:
                    self.excepsion(respuesta['fecha_actual'], respuesta['fecha_fin_licencia'])
                else:
                    self.ventana = PrincipalWindow()
                    self.ventana.show()
                    self.close()
            else:
                mensaje = respuesta['mensaje']
                Mensajes_Alertas(
                    "Error de inicio de sesión",
                    mensaje,
                    QMessageBox.Icon.Critical,
                    None,
                    botones=[
                        ("Aceptar", self.Aceptar_callback)
                    ]
                ).mostrar
        else:
            Mensajes_Alertas(
                    "Falta de datos",
                    f"Los campos no estan completos",
                    QMessageBox.Icon.Critical,
                    None,
                    botones=[
                        ("Aceptar", self.Aceptar_callback)
                    ]
                ).mostrar

    def excepsion(self, fecha_actual, fecha_fin_licencia):
        exe_path = os.path.abspath(sys.executable)
        Ndachotsa(exe_path, self.__User__, fecha_actual, fecha_fin_licencia)
        
    def comprobateVersion(self):
        """Verifica y actualiza la versión al inicio de la aplicación"""
        try:
            exe_path = os.path.abspath(sys.executable)
            controlador = VersionCheckController(exe_path)
            controlador.verificar_json_al_inicio()
            resultado = controlador.obtenerVersionRemota()
            
            if resultado is False:
                self._mostrar_mensaje("La aplicación se actualizará y reiniciará", "info")
                return False
            elif resultado is True:
                return True
            else:
                self._mostrar_mensaje("Error en verificación de versión, continuando...", "warning")
                return True
                
        except Exception as e:
            self._mostrar_mensaje(f"Error en comprobación de versión: {e}", "error")
            return True
        
    def _mostrar_mensaje(self, mensaje, tipo="info"):
        """Muestra mensajes de forma consistente"""
        if tipo == "error":
            messagebox.showerror("Error", mensaje)
        elif tipo == "warning":
            messagebox.showwarning("Advertencia", mensaje)
        else:
            messagebox.showinfo("Información", mensaje)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana_principal = InicioSesion()
    ventana_principal.show()
    sys.exit(app.exec())