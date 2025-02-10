#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import sys
import os
import json
from PyQt6.QtGui import QIcon, QPixmap, QMouseEvent
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6 import *
from ..globalModulesShare.resources import *
from ..globalModulesShare.ContenedorVariables import Variables
from ..ventanaspy.IU_VENDEDORES import *
from ..globalModulesShare.documentos_json import*
from ..globalModulesShare.mensajes_alertas import *

class VendedoresSonoraController(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Formulario_Vendedores()
        self.ui.setupUi(self)
        self.setWindowTitle("Clasificación de vendedores Sonora")
        self.setWindowIcon(QIcon(":/Source/LOGO_KREI_3.ico"))
        self.ui.tabla_vendedoresrefacciones.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.ui.tabla_vendedoresrefacciones_servicio.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
#comment: Botones
        self.ui.btn_aceptar_vendedores.clicked.connect(self.funcion_aceptar)
        
#comment: Variables locales
        self.acciones_por_pestaña = {
            0 : {
                "actualizar" : self.actualizar_vendedores_refacciones,
                "agregar" : self.agregar_vendedores_refacciones,
                "eliminar" : self.eliminar_vendedores_refacciones,
            },
            1 : {
                "actualizar" : self.actualizar_vendedores_servicio,
                "agregar" : self.agregar_vendedores_servicio,
                "eliminar" : self.eliminar_vendedores_servicio,
            },
        }
        
        
    def obtener_ventana_activa(self):
        ventana_activa = self.ui.Vendedores_Refacciones.currentIndex()
        return ventana_activa
        
    def funcion_aceptar(self):
        ventana_activa = self.obtener_ventana_activa()
        