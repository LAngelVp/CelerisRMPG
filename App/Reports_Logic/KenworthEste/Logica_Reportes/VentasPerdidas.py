import os
import pandas as pd
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios
import locale
from time import sleep

class VentasPerdidas(Variables):
    def __init__(self):
        self.concesionario = Concesionarios().concesionarioEste
        self.variables = Variables()
        self.df_final = pd.DataFrame()

        self.documentos_ventasperdidas_sucursal = [
            {"archivo":"VPMATRIZ.xls","sucursal":"Matriz Cordoba"},
            {"archivo":"VPTREBOL.xls","sucursal":"Trebol"},
            {"archivo":"VPVERACRUZ.xls","sucursal":"Veracruz"},
            {"archivo":"VPORIZABA.xls","sucursal":"Orizaba"},
            {"archivo":"VPTEHUACAN.xls","sucursal":"Tehuacan"},
            {"archivo":"VPVILLAHERMOSA.xls","sucursal":"Villahermosa"},
            {"archivo":"VPCOATZACOALCOS.xls","sucursal":"Coatzacoalcos"},
            {"archivo":"VPMERIDA.xls","sucursal":"Merida"},
            {"archivo":"VPOAXACA.xls","sucursal":"Oaxaca"},
            {"archivo":"VPTUXTLA1.xls","sucursal":"Tuxtla1"},
            {"archivo":"VPTUXTLA2.xls","sucursal":"Tuxtla2"},
        ]
        
        # Asegúrate de que 'ruta_ventasperdidas' sea una propiedad de la clase
        self.ruta_ventasperdidas = None
        # Obtener la ruta base donde se almacenan los archivos
        self.ruta_base = self.variables.ruta_Trabajos_kwe
        
    
            
    def venta_perdida_matriz(self):
        if self.df_final.empty:
            self.comprobar_existencia_ventasperdidas()
        documento = "VPMATRIZ.xls"
        self.comprobar_documento(documento)
        self.guardar_todo()
    def venta_perdida_trebol(self):
        if self.df_final.empty:
            self.comprobar_existencia_ventasperdidas()
        documento = "VPTR  EBOL.xls"
        self.comprobar_documento(documento)
        self.guardar_todo()
    def venta_perdida_veracruz(self):
        if self.df_final.empty:
            self.comprobar_existencia_ventasperdidas()
        documento = "VPVERACRUZ.xls"
        self.comprobar_documento(documento)
        self.guardar_todo()
    def venta_perdida_orizaba(self):
        if self.df_final.empty:
            self.comprobar_existencia_ventasperdidas()
        documento = "VPORIZABA.xls"
        self.comprobar_documento(documento)
        self.guardar_todo()
    def venta_perdida_tehuacan(self):
        if self.df_final.empty:
            self.comprobar_existencia_ventasperdidas()
        documento = "VPTEHUACAN.xls"
        self.comprobar_documento(documento)
        self.guardar_todo()
    def venta_perdida_villahermosa(self):
        if self.df_final.empty:
            self.comprobar_existencia_ventasperdidas()
        documento = "VPVILLAHERMOSA.xls"
        self.comprobar_documento(documento)
        self.guardar_todo()
    def venta_perdida_coatzacoalcos(self):
        if self.df_final.empty:
            self.comprobar_existencia_ventasperdidas()
        documento = "VPCOATZACOALCOS.xls"
        self.comprobar_documento(documento)
        self.guardar_todo()
    def venta_perdida_merida(self):
        if self.df_final.empty:
            self.comprobar_existencia_ventasperdidas()
        documento = "VPMERIDA.xls"
        self.comprobar_documento(documento)
        self.guardar_todo()
    def venta_perdida_oaxaca(self):
        if self.df_final.empty:
            self.comprobar_existencia_ventasperdidas()
        documento = "VPOAXACA.xls"
        self.comprobar_documento(documento)
        self.guardar_todo()
    def venta_perdida_tuxtla1(self):
        if self.df_final.empty:
            self.comprobar_existencia_ventasperdidas()
        documento = "VPTUXTLA1.xls"
        self.comprobar_documento(documento)
        self.guardar_todo()
    def venta_perdida_tuxtla2(self):
        if self.df_final.empty:
            self.comprobar_existencia_ventasperdidas()
        documento = "VPTUXTLA2.xls"
        self.comprobar_documento(documento)
        self.guardar_todo()
        
    def proceso(self, nombre_documento):
        self.nombre_doc = nombre_documento
        path = os.path.join(self.variables.ruta_Trabajos_kwe, self.nombre_doc)

        # Leer el archivo Excel
        df = pd.read_excel(path, sheet_name=0)

        if df.empty:
            sucursal = next((item["sucursal"] for item in self.documentos_ventasperdidas_sucursal if item["archivo"] == nombre_documento), None)
            if sucursal:
                print(f"El archivo {nombre_documento} está vacío. Se generarán filas en cero para la sucursal: {sucursal}")
                fila_en_cero = self.creacion_filas_en_cero(documento_con_contenido=False, sucursal=sucursal)
                return fila_en_cero, True, []

        # Reemplazar los puntos y comas por guiones
        df = df.replace(to_replace=";", value="-", regex=True)
        df = df.drop(df.index[-1])  # Eliminar la última fila

        # Convertir la columna "Hora" a formato adecuado
        hora = pd.to_datetime(df["Hora"])
        df["Hora"] = hora.dt.strftime('%I:%M:%S %p').astype(str)

        # Procesar las columnas de fechas
        for column_name in df.columns:
            if "fecha" in column_name.lower():
                df = self.variables.global_date_format_america(df, column_name)

        df["Mes"] = df["Fecha"].apply(lambda x:self.variables.nombre_mes_completo_base_columna(x))
        
        df["Año"] = df["Fecha"].apply(lambda x:self.variables.nombre_año_completo_base_columna(x))
        
        df.insert(0, "VP", 1, allow_duplicates=False)

        # Concatenar la columna "Venta Perdida"
        col_venta_perdida_concat = "VP-" + df["Venta Perdida"].astype(int).astype(str)
        df["Venta Perdida"] = col_venta_perdida_concat

        # Cargar la información de vendedores
        vendedores = pd.read_json(os.path.join(self.variables.help_directory, "VendedoresVP.json"))
        df.insert(12, column="Departamento", value="", allow_duplicates=False)

        # Mapear los departamentos
        df["Departamento"] = df['Usuario'].map(vendedores.set_index('Usuario')['Departamento'])

        # Reconvertir las fechas
        for column_name in df.columns:
            if "fecha" in column_name.lower():
                df = self.variables.global_date_format_dmy_mexican(df, column_name)

        # Convertir columnas booleanas a texto
        columnas_bol = df.select_dtypes(include=bool).columns.tolist()
        df[columnas_bol] = df[columnas_bol].astype(str)
        departamentos_presentes = df["Departamento"].unique().tolist()
        return df, False, departamentos_presentes
    
    def comprobar_documento(self, documento):
        ruta_completa = os.path.join(self.ruta_base, documento)
        if not os.path.exists(ruta_completa):
            print(f"El documento {documento} no existe")
            return

        df, es_fila_en_cero, departamentos = self.proceso(documento)

        if df is None or df.empty:
            return

        sucursal = df["Sucursal"].iloc[0]

        # Eliminar filas en cero según departamento
        for depto in departamentos:
            self.df_final = self.df_final[~(
                (self.df_final["Sucursal"] == sucursal) & 
                (self.df_final["Departamento"] == depto) &
                (self.df_final["VP"] == 0)
            )]

        self.df_final = pd.concat([self.df_final, df], ignore_index=True)
        print(f"Documento procesado y agregado: {documento}")
        
    def comprobar_existencia_ventasperdidas(self):
        # Buscar si ya existe un archivo con ventas perdidas
        self.df_final = None
        for archivo in os.listdir(self.variables.ruta_exitosos_kwe):
            if "ventasperdidas" in archivo:
                self.ruta_ventasperdidas = os.path.join(self.variables.ruta_exitosos_kwe, archivo)

        # Si ya existe, lo carga
        if self.ruta_ventasperdidas and os.path.exists(self.ruta_ventasperdidas):
            self.df_final = pd.read_excel(self.ruta_ventasperdidas)
            print("Archivo 'ventasperdidas' encontrado y abierto.")
        else:
            # Si no existe, crear filas en cero para todas las sucursales
            df_filas_cero = []
            for item in self.documentos_ventasperdidas_sucursal:
                sucursal = item["sucursal"]
                fila = self.creacion_filas_en_cero(documento_con_contenido=False, sucursal=sucursal)
                df_filas_cero.append(fila)
            self.df_final = pd.concat(df_filas_cero, ignore_index=True)
            print("Se crearon filas en cero para todas las sucursales.")

    def creacion_filas_en_cero(self, documento_con_contenido, sucursal):
        def crear_fila(departamento):
            fecha = Variables().date_movement_config_document()
            return pd.DataFrame({
                "VP": [0],
                "Venta Perdida": ["-"],
                "Id. Cliente": [0],
                "Nombre Cliente": ["-"],
                "Núm. Artículo": ["-"],
                "Artículo": ["-"],
                "Motivo": ["NO EXIST EN SUCURSAL (MOVTO)"],
                "Cantidad": [0],
                "Fecha": [fecha],
                "Hora": [fecha],
                "Comentario": ["-"],
                "Usuario": ["-"],
                "Departamento": [departamento],
                "Sucursal": [sucursal],
                "Programa": ["Ventas Perdidas"],
                "Tipo de Inventario": [departamento],
                "Precio": [0],
                "Clasificación": ["E"],
                "Desc. Clasificación": ["Sin Eventos"],
                "Costo": [0],
                "Total": [0],
                "Id. Competidor": [0],
                "Competidor": ["-"],
                "Precio Competidor": [0],
                "Moneda Competidor": ["-"]
            })

        departamentos = ["Refacciones", "Servicio"]
        dfs = [crear_fila(dep) for dep in departamentos]

        fila_dataframe = pd.concat(dfs, ignore_index=True)
        fila_dataframe["Mes"] = fila_dataframe["Fecha"].apply(lambda x: self.variables.nombre_mes_completo_base_columna(x))
        fila_dataframe["Año"] = fila_dataframe["Fecha"].apply(lambda x: self.variables.nombre_año_completo_base_columna(x))
        hora = pd.to_datetime(fila_dataframe["Hora"])
        fila_dataframe["Hora"] = hora.dt.strftime('%I:%M:%S %p').astype(str)

        for column_name in fila_dataframe.columns:
            if "fecha" in column_name.lower():
                fila_dataframe = self.variables.global_date_format_dmy_mexican(fila_dataframe, column_name)

        return fila_dataframe
    
    def guardar_todo(self):
        if not self.df_final.empty:
            self.variables.guardar_xls("ventasperdidas.xls", self.df_final, self.concesionario)
            print("Archivo final de ventas perdidas guardado correctamente.")
        else:
            print("No hay datos para guardar.")