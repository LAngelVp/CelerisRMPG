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
        
#señales:
        self.ui.tabla_vendedoresrefacciones.itemClicked.connect(self.click_celda_tabla_refacciones)
        self.ui.tabla_vendedoresrefacciones_servicio.itemClicked.connect(self.click_celda_tabla_servicio)
        
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
        
    def click_celda_tabla_refacciones(self, elemento):
        if self.ui.rb_agregar.isChecked():
            return
        fila = elemento.row()
        columna = elemento.column()
        if columna == 0:
            id_elemento = self.ui.tabla_vendedoresrefacciones.item(fila, columna - 0).text()
        else:
            pass
        try:
            self.ui.ledit_idrefacciones.setText(id_elemento)
            id_objeto = {"id":id_elemento}
            elementos = creacion_json(self.variables.help_directory, self.variables.nombre_documento_clasificacion_vendedores_refacciones_sonora, id_objeto).obtener_datos_json_por_id
            self.ui.ledit_nombrevendedor.setText(elementos["vendedor"])
            self.ui.ledit_sucursal.setText(elementos["sucursal"])
            self.ui.ledit_cargo.setText(elementos["jerarquia"])
            self.ui.ledit_depaventa.setText(elementos["depto venta"])
            self.ui.ledit_depa.setText(elementos["departamento"])
        except:
            pass
    def click_celda_tabla_servicio(self, elemento):
        if (self.ui.rb_agregar_servicio.isChecked()):
            return
        fila = elemento.row()
        columna = elemento.column()
        if columna == 0:
            id = self.ui.tabla_vendedoresrefacciones_servicio.item(fila, columna - 0).text()
        else:
            pass
        try:
            self.ui.ledit_idservicio.setText(id)
            id_objeto = {"id" : id}
            elementos = creacion_json(self.variables.help_directory, self.variables.nombre_documento_clasificacion_vendedores_servicio_kwe,id_objeto).obtener_datos_json_por_id
            self.ui.ledit_nombrevendedor_servicio.setText(elementos["Vendedor"])
            self.ui.ledit_depaventa_servicio.setText(elementos["Depa_Venta"])
            self.ui.ledit_depa_servicio.setText(elementos["Depa"])
        except:
            pass
    def obtener_ventana_activa(self):
        ventana_activa = self.ui.Vendedores_Refacciones.currentIndex()
        return ventana_activa
        
    def funcion_aceptar(self):
        ventana_activa = self.obtener_ventana_activa()
        
    def actualizar_vendedores_refacciones(self):
        pass
    def agregar_vendedores_refacciones(self):
        pass
    def eliminar_vendedores_refacciones(self):
        pass
    def actualizar_vendedores_servicio(self):
        pass
    def agregar_vendedores_servicio(self):
        pass
    def eliminar_vendedores_servicio(self):
        pass
        