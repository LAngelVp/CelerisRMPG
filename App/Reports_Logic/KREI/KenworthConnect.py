"""
DESARROLLADOR
LUIS A. PEREZ
"""
from .Logica_Reportes.KREI_OrdenesKW import *
from .Logica_Reportes.KREI_CreditoKW import *
from .Logica_Reportes.KREI_InventarioKW import *
from .Logica_Reportes.KREI_Refacciones import *
from .Logica_Reportes.KREI_ServicioDetallado import *
from .Logica_Reportes.KREI_ResultadosFinancieros import *
from .Logica_Reportes.KREI_Compras import *

class KenworthConnect():
    def OrdenesServicioKREIKWESTE(self):
        OrdenesServicioKWESTEKREI().OrdenesKWESTE_KREI()
    
    def OrdenesServicioKREIKWSUR(self):
        OrdenesServicioKWESTEKREI().OrdenesKWSUR_KREI()
    
    def CreditoKREIKWSUR(self):
        CreditoKWESTEKREI().CreditoKWSUR_KREI()
    
    def CreditoKREIKWESTE(self):
        CreditoKWESTEKREI().CreditoKWESTE_KREI()

    def InventarioKREIKWSUR(self):
        InventarioKWESTEKREI().InventarioKWSUR_KREI()
    
    def InventarioKREIKWESTE(self):
        InventarioKWESTEKREI().InventarioKWESTE_KREI()
        
    def RefaccionesKREIKWSUR(self):
        RefaccionesKWESTEKREI().RefaccionesKWSUR_KREI()
    
    def RefaccionesKREIKWESTE(self):
        RefaccionesKWESTEKREI().RefaccionesKWESTE_KREI()

    def ServicioDetalladoKREIKWSUR(self):
        ServicioDetalladoKWESTEKREI().ServicioDetalladoKWSUR_KREI()
    
    def ServicioDetalladoKREIKWESTE(self):
        ServicioDetalladoKWESTEKREI().ServicioDetalladoKWESTE_KREI()

    def ResultadosFinancierosEsteKREI(self):
        ResultadosFinancierosKREI().ReporteFinancieroKWESTE_KREI()
        
    def ResultadosFinancierosSurKREI(self):
        ResultadosFinancierosKREI().ReporteFinancieroKWSUR_KREI()
    
    def ComprasDetalladoSurKREI(self):
        ComprasKREI().ComprasSur()