import sys
import os

# --- IMPORTS FANTASMA PARA PYINSTALLER ---
# Esto asegura que las librerías de tu requirements.txt se incluyan
import pandas
import numpy
import openpyxl
import requests
import bs4
import selenium
import lxml
import tkinter
from tkinter import messagebox
import charset_normalizer
# -----------------------------------------

from PyQt6.QtWidgets import QApplication
# 'InicioSesion' ya debe estar ofuscado como InicioSesion.pyd en la misma carpeta
try:
    from InicioSesion import InicioSesion 
except ImportError as e:
    # Esto ayuda a depurar si el .pyd tiene problemas de dependencias
    print(f"Error al cargar el módulo ofuscado: {e}")
    sys.exit(1)

def main():
    app = QApplication(sys.argv)
    login_window = InicioSesion()
    login_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()