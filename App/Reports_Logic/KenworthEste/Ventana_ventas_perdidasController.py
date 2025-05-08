import pandas as pd
from PyQt6.QtGui import QIcon, QPixmap, QMouseEvent, QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6 import *
from ..globalModulesShare.ContenedorVariables import Variables
from ..globalModulesShare.documentos_json import creacion_json
from ..ventanaspy.VendedoresVentasPerdidas import Ui_Ventas_perdidas_contenedor
from ..globalModulesShare.mensajes_alertas import Mensajes_Alertas

class VentasPerdidasController(QWidget):
    def __init__(self):
        super().__init__()
        self.variables = Variables()
        self.ui = Ui_Ventas_perdidas_contenedor()
        self.ui.setupUi(self)
        self.tabla_mostrar_datos()
        self.id_elemento = None
        
        self.setWindowTitle("Administración de vendedores")
        
        self.ui.btn_agreagar.clicked.connect(self.agregar)
        self.ui.btn_actualizar.clicked.connect(self.actualizar)
        self.ui.btn_eliminar.clicked.connect(self.eliminar)
    
    def Aceptar_callback(self):
        pass
    
    def comprobacion_existencia_documento(self):
        nombre_documento = self.variables.departamentos_vendedores_ventas_perdidas
        ruta_archivos_configuracion = self.variables.help_directory
        datos_json = creacion_json(ruta = ruta_archivos_configuracion, nombre = nombre_documento).comprobar_existencia
        return datos_json
    
    def tabla_mostrar_datos(self):
        datos = self.comprobacion_existencia_documento()
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Id", "Nombre del Vendedor", "Departamento"])
        
        if not datos:
            self.ui.tabla_ventasperdidas.setModel(model)
            return
        self.documento =  pd.DataFrame(datos)
        for indice, fila in self.documento.iterrows():
            items = [
                QStandardItem(str(fila["id"])),
                QStandardItem(str(fila["Usuario"])),
                QStandardItem(str(fila["Departamento"]))
            ]
            model.appendRow(items)
        self.ui.tabla_ventasperdidas.setModel(model)
        self.ui.tabla_ventasperdidas.resizeColumnsToContents()
        self.ui.tabla_ventasperdidas.clicked.connect(self.mostrar_id_fila_seleccionada)
        
    def mostrar_id_fila_seleccionada(self, indice):
        fila = indice.row()
        if fila < 0:
            return
        try:
            self.id_elemento = self.documento.iloc[fila]["id"]
            nombre = self.documento.iloc[fila]["Usuario"]
            departamento_actual = self.documento.iloc[fila]["Departamento"] 
            combo = self.ui.listaseleccion_departamentos
            departamentos = [combo.itemText(i) for i in range(combo.count())]

            if departamento_actual in departamentos:
                departamentos.remove(departamento_actual)
            departamentos.insert(0, departamento_actual)

            combo.clear()
            combo.addItems(departamentos)
            
            self.ui.txt_nombrevendedor.setText(nombre)
            
        except (IndexError, KeyError):
            QMessageBox.warning(self, "Error", "No se encontró un id o departamento para esta fila.")
            
    def obtener_datos_de_campos(self):
        nombre = self.ui.txt_nombrevendedor.text()
        departamento = self.ui.listaseleccion_departamentos.currentText()
        return nombre, departamento
    
    def agregar(self):
        nombre, departamento = self.obtener_datos_de_campos()
        if nombre.strip() == "":
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
            "Usuario" : nombre,
            "Departamento": departamento
        }
        creacion_json(self.variables.help_directory, self.variables.departamentos_vendedores_ventas_perdidas, objeto).agregar_json
        self.tabla_mostrar_datos()
        self.ui.txt_nombrevendedor.clear()
        self.id_elemento = None
    
    def eliminar(self):
        if self.id_elemento is None:
            QMessageBox.information(self, "Id de la fila seleccionada", "No se ha seleccionado ningun elemento de la tabla")
            return
        elemento_a_eliminar = {
            "id": self.id_elemento
        }
        try:
            creacion_json(self.variables.help_directory, self.variables.departamentos_vendedores_ventas_perdidas, elemento_a_eliminar).eliminar_datos_json
            QMessageBox.information(self, "Exito", "Operación exitosa")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se logro eliminar el elemento: {e}")
        self.tabla_mostrar_datos()
        self.ui.txt_nombrevendedor.clear()
        self.id_elemento = None
    def actualizar(self):
        if self.id_elemento is None:
            QMessageBox.information(self, "Id de la fila seleccionada", "No se ha seleccionado ningun elemento de la tabla")
            return
        elemento_a_actualizar = {
            "id": self.id_elemento
        }
        nombre_nuevo, departamento_nuevo = self.obtener_datos_de_campos()
        
        if nombre_nuevo.strip() == "":
            QMessageBox.information(self, "Datos incompletos", "Debes de colocar un nombre de vendedor")
            return
        
        datos_anteriores = creacion_json(self.variables.help_directory, self.variables.departamentos_vendedores_ventas_perdidas,elemento_a_actualizar).obtener_datos_json_por_id
        
        if datos_anteriores:
            datos_nuevos = {
                "id" : elemento_a_actualizar["id"],
                "Usuario": nombre_nuevo,
                "Departamento" : departamento_nuevo
            }
            creacion_json(self.variables.help_directory, self.variables.departamentos_vendedores_ventas_perdidas,elemento_a_actualizar).actualizar_datos(datos_nuevos)
        self.tabla_mostrar_datos()
        self.ui.txt_nombrevendedor.clear()
        self.id_elemento = None