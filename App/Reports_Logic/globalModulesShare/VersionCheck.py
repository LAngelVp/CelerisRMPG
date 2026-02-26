"""
DESARROLLADOR
LUIS A. PEREZ
"""
import requests
import json
import os
import sys
import subprocess
import tempfile
import zipfile
from pathlib import Path
from packaging import version
from datetime import datetime
from .documentos_json import creacion_json
from .ContenedorVariables import Variables
from .kuchotsa import Ndachotsa
import tkinter as tk
from tkinter import ttk, messagebox
from PyQt6.QtWidgets import QApplication, QProgressDialog, QMessageBox, QStyle
from PyQt6.QtCore import Qt

class VersionCheckController:
    def __init__(self, path):
        self.dueño_repositorio = "LAngelVp"
        self.repositorio = "ProcesadorGlobalVp"
        self.rutaEjecutable = path
        self.variables = Variables()
        self.github_api_url = f"https://api.github.com/repos/{self.dueño_repositorio}/{self.repositorio}/releases/latest"
        self.assets = None
        self.ruta_nueva_version = None
        self.nombre_nueva_version = None
        
    def _comparar_versiones(self, datos_remotos):
        """Compara versiones locales y remotas, actualiza JSON si es necesario"""
        try:
            datos_locales = creacion_json(
                self.variables.help_directory, 
                self.variables.rutaDatosVersionVp
            ).comprobar_existencia
            
            if not datos_locales:
                self._mostrar_mensaje("JSON corrupto. Recreando...", "info")
                self.construirVersionLocal(datos_remotos)
                return False
            
            version_local = datos_locales[0].get("tag_name", "")
            version_remota = datos_remotos.get("tag_name", "")
            
            if version_local == version_remota:
                self._mostrar_mensaje("La versión actual está actualizada", "info")
                return True
            else:
                self._mostrar_mensaje(f"Nueva versión disponible: {version_remota}", "info")
                self.construirVersionLocal(datos_remotos)
                return False
                
        except Exception as e:
            self._mostrar_mensaje(f"Error al procesar JSON: {e}", "error")
            self.construirVersionLocal(datos_remotos)
            return False
    
    def _procesar_actualizacion(self, datos):
        """Maneja el proceso completo de actualización cuando hay una nueva versión"""
        self.construirVersionLocal(datos)
        
        if not self._descargar_actualizacion(datosVersionRemota = datos):
            self._mostrar_mensaje("No se pudo descargar la actualización", "error")
            return True
        
        self._mostrar_mensaje("Descarga completada. Iniciando actualización...", "info")
        
        Ndachotsa(path=self.rutaEjecutable, user=None).directEliminate(
            ruta_nueva_version=self.ruta_nueva_version, 
            nombre_nueva_version=self.nombre_nueva_version
        )
        return False
    
    def obtenerVersionRemota(self):
        """Obtiene y compara la versión remota"""
        datos_remotos = self._obtener_datos_remotos()
        if not datos_remotos:
            self._mostrar_mensaje("No se obtuvieron datos del repositorio remoto", "error")
            return None
        
        if not self._comparar_versiones(datos_remotos):
            return self._procesar_actualizacion(datos_remotos)
        else:
            return True
        
    def construirVersionLocal(self, datos):
        """Construye el JSON de versión local"""
        objeto = {
            'tag_name': datos["tag_name"],
            'version': datos["version"],
            'titulo': datos["titulo"],
            'descripcion': datos["descripcion"],
            'fecha_publicacion': datos["fecha_publicacion"],
            'fecha_actualizacion': datos["fecha_actualizacion"],
            'autor_login': datos["autor_login"]
        }
        creacion_json(
            self.variables.help_directory, 
            self.variables.rutaDatosVersionVp, 
            objeto
        ).agregar_json_unico_dato
        
    def _obtener_datos_remotos(self):
        """Obtiene datos de la versión remota desde GitHub"""
        try:
            response = requests.get(self.github_api_url, timeout=15)
            response.raise_for_status()
            datos = response.json()
            
            if not datos:
                return None
            
            informacion_detallada = {
                'tag_name': datos.get('tag_name', ''),
                'version': datos.get('tag_name', '').lstrip('v'),
                'titulo': datos.get('name', ''),
                'descripcion': datos.get('body', ''),
                'fecha_publicacion': datos.get('published_at', ''),
                'fecha_actualizacion': datos.get('updated_at', ''),
                'assets': datos.get('assets', []),
                'autor_login': datos.get('author', {}).get('login', '')
            }
            
            self.assets = informacion_detallada["assets"]
            return informacion_detallada
            
        except requests.RequestException as e:
            self._mostrar_mensaje(f"Error de conexión: {e}", "error")
            return None
        except json.JSONDecodeError:
            self._mostrar_mensaje("Error en formato de respuesta", "error")
            return None
        except Exception as e:
            self._mostrar_mensaje(f"Error inesperado: {e}", "error")
            return None
    
    def _descargar_actualizacion(self, datosVersionRemota):
        """Descarga la nueva versión del ejecutable con diálogo de progreso"""
        try:
            if not self.assets:
                self._mostrar_mensaje("No hay archivos disponibles para descargar", "error")
                return False
            
            archivo_exe = next(
                (asset for asset in self.assets if asset["name"].endswith('.exe')), 
                None
            )
            
            if not archivo_exe:
                self._mostrar_mensaje("No se encontró archivo ejecutable", "error")
                return False
            
            temp_dir = os.path.join(os.environ['TEMP'], 'actualizacion_kweste')
            os.makedirs(temp_dir, exist_ok=True)
            ruta_descarga = os.path.join(temp_dir, archivo_exe['name'])
            
            self._mostrar_dialogo_progreso(
                titulo="Descargando Actualización",
                mensaje=f"Descargando: {archivo_exe['name']}\n\n"
                    f"Autor: {datosVersionRemota['autor_login']}\n"
                    f"Título: {datosVersionRemota['titulo']}\n"
                    f"Detalles: {datosVersionRemota['descripcion']}",
                max_progress=100
            )
            
            response = requests.get(archivo_exe['browser_download_url'], stream=True, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(ruta_descarga, 'wb') as archivo:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        archivo.write(chunk)
                        downloaded += len(chunk)
                        
                        if total_size > 0:
                            progress = int((downloaded / total_size) * 100)
                            self._actualizar_progreso(progress)
            self._cerrar_dialogo_progreso()
            self.ruta_nueva_version = ruta_descarga
            self.nombre_nueva_version = archivo_exe['name']
            
            return True
            
        except Exception as e:
            self._cerrar_dialogo_progreso()
            self._mostrar_mensaje(f"Error en descarga: {e}", "error")
            return False

    def _mostrar_dialogo_progreso(self, titulo, mensaje, max_progress=100):
        """Muestra un diálogo de progreso modal"""
        app = QApplication.instance()
        
        self.progress_dialog = QProgressDialog(mensaje, "Cancelar", 0, max_progress, None)
        self.progress_dialog.setWindowTitle(titulo)
        icono = app.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload)
        self.progress_dialog.setWindowIcon(icono)
        self.progress_dialog.setMinimumWidth(500)
        self.progress_dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.progress_dialog.setCancelButton(None)
        self.progress_dialog.setMinimumDuration(0)
        self.progress_dialog.show()
        
        if app:
            app.processEvents()

    def _actualizar_progreso(self, valor):
        """Actualiza el valor del progreso"""
        if hasattr(self, 'progress_dialog') and self.progress_dialog:
            self.progress_dialog.setValue(valor)
            app = QApplication.instance()
            if app:
                app.processEvents()

    def _cerrar_dialogo_progreso(self):
        """Cierra el diálogo de progreso"""
        if hasattr(self, 'progress_dialog') and self.progress_dialog:
            self.progress_dialog.close()

    def verificar_json_al_inicio(self):
        """Verifica y crea el JSON de versión al inicio de la aplicación"""
        ruta_json = os.path.join(self.variables.help_directory, self.variables.rutaDatosVersionVp)
        
        if not os.path.exists(ruta_json):
            datos_remotos = self._obtener_datos_remotos()
            if datos_remotos:
                self.construirVersionLocal(datos_remotos)
                self._mostrar_mensaje(f"Version del programa establecida.\nVersion: {datos_remotos['tag_name']}", "info")
            else:
                self._mostrar_mensaje("No se pudieron obtener datos", "warning")
    
    def _mostrar_mensaje(self, mensaje, tipo="info"):
        """Muestra mensajes de forma consistente"""
        if tipo == "error":
            messagebox.showerror("Error", mensaje)
        elif tipo == "warning":
            messagebox.showwarning("Advertencia", mensaje)
        else:
            messagebox.showinfo("Información", mensaje)