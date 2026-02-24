"""
DESARROLLADOR
LUIS A. PEREZ
"""
import traceback
import sys
import os
import shutil
from .Logica_Reportes.Back_Order import BackOrder
from .Logica_Reportes.Compras import Compras
from .Logica_Reportes.Credito import Credito
from .Logica_Reportes.Ordenes_Servicio import OrdenesServicio
from .Logica_Reportes.PagosClientes import PagosClientes
from .Logica_Reportes.Refacciones import Refacciones
from .Logica_Reportes.Salidas_Vale import SalidasVale
from .Logica_Reportes.Servicio_Detallado import ServioDetallado
from .Logica_Reportes.Trabajos_Por_Estado import TrabajosPorEstado
from .Logica_Reportes.InventarioCosteado import InventarioCosteado
from .Logica_Reportes.InventarioUnidades import InventarioUnidades
from .Logica_Reportes.Financiero import ResultadosFinancieros
from .Logica_Reportes.Contabilidad import ContabilidadAnalisis
from .Logica_Reportes.VentasPerdidas import VentasPerdidas

class KenworthConnect():
    def SalidasEnVale(self):
        SalidasVale()
    def Refacciones(self):
        Refacciones()
    def OrdenesDeServicio(self):
        OrdenesServicio()
    def ServicioDetallado(self):
        ServioDetallado()
    def BackOrder(self):
        BackOrder()
    def ComprasDetallado(self):
        Compras()
    def Credito(self):
        Credito()
    def TrabajosPorEstado(self):
        TrabajosPorEstado()
    def PagosClientes(self):
        PagosClientes()
    def InventarioCosteado(self):
        InventarioCosteado()
    def InventarioDeUnidades(self):
        InventarioUnidades()
    def ResultadosFinancieros(self):
        ResultadosFinancieros()
    def ContabilidadConector(self):
        ContabilidadAnalisis().anexos_moimientos_gastos()
    def VentasPerdidasNuevoLaredoMatriz(self):
        VentasPerdidas().venta_perdida_nuevo_laredo_matriz()
    def VentasPerdidasReynosa(self):
        VentasPerdidas().venta_perdida_reynosa()
    def VentasPerdidasMatamoros(self):
        VentasPerdidas().venta_perdida_matamoros()
    def VentasPerdidasPiedrasNegras(self):
        VentasPerdidas().venta_perdida_piedras_negras()
    def VentasPerdidasNuevoLaredoAeropuerto(self):
        VentasPerdidas().venta_perdida_nuevo_laredo_aeropuerto()
    def VentasPerdidasPozaRica(self):
        VentasPerdidas().venta_perdida_poza_rica()
    def VentasPerdidasValleHermoso(self):
        VentasPerdidas().venta_perdida_valle_hermoso()
    def VentasPerdidasTrpNava(self):
        VentasPerdidas().venta_perdida_trp_nava()
    def VentasPerdidasTrpReynosa(self):
        VentasPerdidas().venta_perdida_trp_reynosa()
    def VentasPerdidasTrpNuevoLaredo(self):
        VentasPerdidas().venta_perdida_trp_nuevo_laredo()
    def VentasPerdidasTrpAcuña(self):
        VentasPerdidas().venta_perdida_trp_acuña()