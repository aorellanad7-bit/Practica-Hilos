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
    {"id": "ORD-010", "cliente": "Diana Paz", "producto": "P002", "cantidad": 2},
    {"id": "ORD-011", "cliente": "Jorge M.", "producto": "P001", "cantidad": 4},
    {"id": "ORD-012", "cliente": "Lucía H.", "producto": "P003", "cantidad": 5},
    {"id": "ORD-013", "cliente": "Víctor R.", "producto": "P001", "cantidad": 2},
    {"id": "ORD-014", "cliente": "Marta L.", "producto": "P004", "cantidad": 3},
    {"id": "ORD-015", "cliente": "Hugo C.", "producto": "P002", "cantidad": 1},
    {"id": "ORD-016", "cliente": "Inés B.", "producto": "P003", "cantidad": 4},
    {"id": "ORD-017", "cliente": "Omar F.", "producto": "P001", "cantidad": 3},
    {"id": "ORD-018", "cliente": "Rosa N.", "producto": "P002", "cantidad": 6},
    {"id": "ORD-019", "cliente": "Tito V.", "producto": "P004", "cantidad": 2},
    {"id": "ORD-020", "cliente": "Alma Z.", "producto": "P005", "cantidad": 1}
]

# --------------------------------------------------------
# 3. CONFIGURACIÓN DE LA COLA COMPARTIDA
# --------------------------------------------------------
cola_pedidos = queue.Queue()

# Llenamos la cola con los pedidos que creamos arriba (RF-02)
for pedido in lista_pedidos:
    cola_pedidos.put(pedido)
    
    # Evento para avisarle al monitor cuándo detenerse (CP-05)
evento_fin_monitor = threading.Event()

# --------------------------------------------------------
# 4. LÓGICA DE LOS TRABAJADORES (WORKERS)
# --------------------------------------------------------
def trabajador(id_trabajador):
    while not cola_pedidos.empty():
        try:
            # Extraemos un pedido de forma segura
            pedido = cola_pedidos.get_nowait()
        except queue.Empty:
            break  # Si ya no hay pedidos, el hilo termina
        
          # CP-04: Capturar errores de pedidos mal formados sin detener el programa
        if "producto" not in pedido or "cantidad" not in pedido or pedido["cantidad"] <= 0 or pedido["producto"] not in inventario:
            print(f"[WORKER-{id_trabajador}] {pedido.get('id', 'ERROR')} FALLÓ | Pedido inválido.")
            with lock_inventario:
                resultados["errores"] += 1
                resultados["procesados"] += 1
            cola_pedidos.task_done()
            continue
        
            print(f"[{time.strftime('%H:%M:%S')}] [WORKER-{id_trabajador}] Inicia pedido {pedido['id']} | Cliente: {pedido['cliente']}")
        
        # RF-04: Simular tiempo de procesamiento FUERA de la sección crítica (0.5 a 2 seg)
        tiempo_simulacion = random.uniform(0.5, 2.0)
        time.sleep(tiempo_simulacion)
        
          # RF-05 y CP-02: SECCIÓN CRÍTICA - Validación y descuento atómico
       
        with lock_inventario:
            producto = pedido["producto"]
            cantidad_solicitada = pedido["cantidad"]
            
            if inventario[producto]["existencia"] >= cantidad_solicitada:
                # Hay stock: Aprobamos y descontamos
                inventario[producto]["existencia"] -= cantidad_solicitada
                resultados["aprobados"] += 1
                print(f"[{time.strftime('%H:%M:%S')}] [WORKER-{id_trabajador}] {pedido['id']} APROBADO | {producto}: -{cantidad_solicitada} unidades")
            else:
                # No hay stock: Rechazamos sin tocar inventario (CP-03)
                resultados["rechazados"] += 1
                print(f"[{time.strftime('%H:%M:%S')}] [WORKER-{id_trabajador}] {pedido['id']} RECHAZADO | Stock insuficiente {producto}")
            
            resultados["procesados"] += 1   
            
               # Le avisamos a la cola que terminamos con este pedido
        cola_pedidos.task_done()
        
        # --------------------------------------------------------
# 5. LÓGICA DEL MONITOR
# --------------------------------------------------------
def monitor():
    # Se ejecutará hasta que el evento_fin_monitor sea activado
    while not evento_fin_monitor.is_set():
        pendientes = cola_pedidos.qsize()
  
