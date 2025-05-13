import os
from ..globalModulesShare.resources import *
import pandas as pd
from PyQt6.QtGui import QIcon, QPixmap, QMouseEvent, QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QHeaderView, QMessageBox, QWidget
from PyQt6.QtCore import *
from PyQt6 import *
from ..globalModulesShare.ContenedorVariables import Variables
from ..globalModulesShare.documentos_json import creacion_json
from ..ventanaspy.ADMIN_CLIENTES_FINANCIERO_ui import Ui_clientes_financiero_contenedor
from ..globalModulesShare.mensajes_alertas import Mensajes_Alertas

class ClientesFinancierController(QWidget):
    def __init__(self):
        super().__init__()
        self.variables = Variables()
        self.ui = Ui_clientes_financiero_contenedor()
        self.ui.setupUi(self)
        self.setWindowTitle("Admin. Clientes Financiero")
        self.setWindowIcon(QIcon(":/Source/LOGO_KREI_3.ico"))
        self.obtener_clientes_para_tabla()
        
        self.ui.btn_agregar.clicked.connect(self.agregar)
        self.ui.btn_eliminar.clicked.connect(self.eliminar)
        self.ui.btn_actualizar.clicked.connect(self.actualizar)
        self.ui.txt_buscador.returnPressed.connect(self.buscar)
    
    def buscar(self):
        dato_buscar =  self.ui.txt_buscador.text().strip()
        if dato_buscar == "":
            return
        
        if not self.documento.empty:
            documento = self.documento
            data_filtrada = documento[documento["NombreCteAsignatario"].str.contains(dato_buscar, case=False)]
            self.tabla_mostrar_datos(dataframe=data_filtrada)
    
    def obtener_datos_de_campos(self):
        nombre = self.ui.txt_nombrecliente.text().strip()
        ciudad = self.ui.txt_ciudadcliente.text().strip()
        estado = self.ui.txt_estadocliente.text().strip()
        return nombre, estado, ciudad
    
    def agregar(self):
        nombre, estado, ciudad  = self.obtener_datos_de_campos()
        if nombre == "" or estado == "" or ciudad == "":
             Mensajes_Alertas(
                    "INFORMATIVO",
                    f"El nombre del vendedor no puede ser vacio",
                    QMessageBox.Icon.Warning,
                    None,
                    botones=[
                        ("Aceptar", self.Aceptar_callback)
                    ]
                ).mostrar
             return
         
        objeto = {
            "NombreCteAsignatario" : nombre,
            "Ciudad": ciudad,
            "Estado" : estado
        }
        creacion_json(self.variables.help_directory, self.variables.clientes_financiero, objeto).agregar_json
        self.tabla_mostrar_datos()
        self.ui.txt_nombrecliente.clear()
        self.ui.txt_ciudadcliente.clear()
        self.ui.txt_estadocliente.clear()
        self.id_elemento = None
    
    def eliminar(self):
        if self.id_elemento is None:
            QMessageBox.information(self, "Id de la fila seleccionada", "No se ha seleccionado ningun elemento de la tabla")
            return
        elemento_a_eliminar = {
            "id": self.id_elemento
        }
        try:
            creacion_json(self.variables.help_directory, self.variables.clientes_financiero, elemento_a_eliminar).eliminar_datos_json
            QMessageBox.information(self, "Exito", "Operación exitosa")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se logro eliminar el elemento: {e}")
        self.tabla_mostrar_datos()
        self.ui.txt_nombrecliente.clear()
        self.ui.txt_ciudadcliente.clear()
        self.ui.txt_estadocliente.clear()
        self.id_elemento = None
        
    def actualizar(self):
        if self.id_elemento is None:
            QMessageBox.information(self, "Id de la fila seleccionada", "No se ha seleccionado ningun elemento de la tabla")
            return
        elemento_a_actualizar = {
            "id": self.id_elemento
        }
        nombre_nuevo, estado_nueva, ciudad_nueva = self.obtener_datos_de_campos()
        
        if nombre_nuevo == "":
            QMessageBox.information(self, "Datos incompletos", "Debes de colocar un nombre de vendedor")
            return
        
        datos_anteriores = creacion_json(self.variables.help_directory, self.variables.clientes_financiero,elemento_a_actualizar).obtener_datos_json_por_id
        
        if datos_anteriores:
            datos_nuevos = {
                "id" : elemento_a_actualizar["id"],
                "NombreCteAsignatario": nombre_nuevo,
                "Ciudad" : ciudad_nueva,
                "Estado" : estado_nueva
            }
            creacion_json(self.variables.help_directory, self.variables.clientes_financiero,elemento_a_actualizar).actualizar_datos(datos_nuevos)
        self.tabla_mostrar_datos()
        self.ui.txt_nombrecliente.clear()
        self.ui.txt_ciudadcliente.clear()
        self.ui.txt_estadocliente.clear()
        self.id_elemento = None
    
    def obtener_clientes(self):
        clientes_json = creacion_json(self.variables.help_directory, self.variables.clientes_financiero).comprobar_existencia
        self.documento =  pd.DataFrame(clientes_json)
        return self.documento
    
    def obtener_clientes_para_tabla(self):
        datos = self.obtener_clientes()
        self.tabla_mostrar_datos(datos)
    
    def tabla_mostrar_datos(self, dataframe=None):     
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Id", "Nombre del Cliente", "Ciudad", "Estado"])

        if dataframe is None or dataframe.empty:
            dataframe = self.obtener_clientes()  # Solo si no se pasó un DataFrame válido

        if dataframe.empty:
            self.ui.tabla_clientes.setModel(model)
            return

        for indice, fila in dataframe.iterrows():
            items = [
                QStandardItem(str(fila["id"])),
                QStandardItem(str(fila["NombreCteAsignatario"])),
                QStandardItem(str(fila["Ciudad"])),
                QStandardItem(str(fila["Estado"]))
            ]
            model.appendRow(items)

        self.ui.tabla_clientes.setModel(model)
        # Ajustar columnas al contenido
        self.ui.tabla_clientes.resizeColumnsToContents()

        # Estirar todas las columnas proporcionalmente (PYQT6)
        self.ui.tabla_clientes.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)      

        self.ui.tabla_clientes.clicked.connect(self.mostrar_id_fila_seleccionada)
        
    def mostrar_id_fila_seleccionada(self, indice):
        fila = indice.row()
        if fila < 0:
            return
        try:
            self.id_elemento = self.documento.iloc[fila]["id"]
            nombre = self.documento.iloc[fila]["NombreCteAsignatario"]
            ciudad_actual = self.documento.iloc[fila]["Ciudad"] 
            estado_actual = self.documento.iloc[fila]["Estado"] 
            
            self.ui.txt_nombrecliente.setText(nombre)
            self.ui.txt_ciudadcliente.setText(ciudad_actual)
            self.ui.txt_estadocliente.setText(estado_actual)
            
        except (IndexError, KeyError):
            QMessageBox.warning(self, "Error", "No se encontró un id o departamento para esta fila.")