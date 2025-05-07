from PyQt6.QtGui import QIcon, QPixmap, QMouseEvent
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6 import *
from ..globalModulesShare.ContenedorVariables import Variables
from ..ventanaspy.VendedoresVentasPerdidas import Ui_Ventas_perdidas_contenedor

class VentasPerdidasController(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Ventas_perdidas_contenedor()
        self.ui.setupUi(self)
