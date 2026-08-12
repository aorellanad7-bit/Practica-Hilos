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

# --------------------------------------------------------
# 2. CASOS DE PRUEBA (Mínimo 20 pedidos)
# --------------------------------------------------------
# Diseñados para cubrir CP-01 (Normal), CP-02 (Contención), 
# CP-03 (Stock Insuficiente) y CP-04 (Inválidos).

lista_pedidos = [
    {"id": "ORD-001", "cliente": "Ana López", "producto": "P001", "cantidad": 2},   # Normal
    {"id": "ORD-002", "cliente": "Mario Pérez", "producto": "P002", "cantidad": 5}, # Normal
    {"id": "ORD-003", "cliente": "Luis Gómez", "producto": "P005", "cantidad": 3},  # Contención por el P005 (solo hay 6)
    {"id": "ORD-004", "cliente": "Carmen Ruiz", "producto": "P005", "cantidad": 2}, # Contención por el P005
    {"id": "ORD-005", "cliente": "José Díaz", "producto": "P005", "cantidad": 2},   # Contención por el P005 (Este debería ser rechazado por CP-02)
    {"id": "ORD-006", "cliente": "Elena Soto", "producto": "P003", "cantidad": 15},
    {"id": "ORD-007", "cliente": "Pablo O.", "producto": "P008", "cantidad": 1},
    {"id": "ORD-008", "cliente": "Sara Vega", "producto": "P004", "cantidad": -1},
    {"id": "ORD-009", "cliente": "Raúl Gil", "producto": "P004", "cantidad": 0},
    {"id": "ORD-010", "cliente": "Diana Paz", "producto": "P002", "cantidad": 2}
]