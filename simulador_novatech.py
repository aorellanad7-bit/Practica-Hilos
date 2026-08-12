import threading
import queue
import time
import random

# --------------------------------------------------------
# 1. RECURSOS COMPARTIDOS Y CONFIGURACIÓN INICIAL
# --------------------------------------------------------

# Inventario inicial según los datos mínimos del escenario
inventario = {
    "P001": {"nombre": "Teclado mecánico", "existencia": 12},
    "P002": {"nombre": "Mouse inalámbrico", "existencia": 18},
    "P003": {"nombre": "Audífonos USB", "existencia": 10},
    "P004": {"nombre": "Cámara web", "existencia": 8},
    "P005": {"nombre": "Monitor de 24 pulgadas", "existencia": 6}
}

# Candado (Mutex/Lock) para proteger el inventario y los contadores
lock_inventario = threading.Lock()

# Contadores globales para el resumen final
resultados = {
    "procesados": 0,
    "aprobados": 0,
    "rechazados": 0,
    "errores": 0
}