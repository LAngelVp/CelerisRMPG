from PyQt6.QtGui import QIcon, QPixmap, QMouseEvent, QStandardItemModel
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6 import *
from ..globalModulesShare.ContenedorVariables import Variables
from ..globalModulesShare.documentos_json import creacion_json
from ..ventanaspy.VendedoresVentasPerdidas import Ui_Ventas_perdidas_contenedor

class VentasPerdidasController(QWidget):
    def __init__(self):
        super().__init__()
        self.variables = Variables()
        self.ui = Ui_Ventas_perdidas_contenedor()
        self.ui.setupUi(self)
        self.tabla_mostrar_datos()
        
    def leer_documento_vendedores(self):
        pass
    def comprobacion_existencia_documento(self):
        nombre_documento = self.variables.departamentos_vendedores_ventas_perdidas
        ruta_archivos_configuracion = self.variables.help_directory
        datos_json = creacion_json(ruta = ruta_archivos_configuracion, nombre = nombre_documento).comprobar_existencia
        return datos_json
    
    def tabla_mostrar_datos(self):
        datos = self.comprobacion_existencia_documento()
        model = QStandardItemModel()
        if not datos:
            model.setHorizontalHeaderLabels(["Nombre del Vendedor", "Departamento"])
        self.ui.tabla_ventasperdidas.setModel(model)
        