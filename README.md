# Simulador de Procesamiento de Pedidos y Control de Inventario en Tiempo Real (NovaTech)

Este proyecto es una solución multihilo en Python que simula un sistema de procesamiento de pedidos e inventario concurrente, resolviendo problemas de **condiciones de carrera (*race conditions*)** mediante el uso de exclusión mutua (**Mutex Locks**) y colas seguras para hilos (**Thread-safe Queues**).

##  Tecnologías y Primitivas Utilizadas

* **Lenguaje:** Python 3.10+
* **Concurrencia y Sincronización:**
  * `threading.Thread`: Creación y gestión de hilos independientes (Workers y Monitor).
  * `threading.Lock`: Cerrojo Mutex para garantizar exclusión mutua en la sección crítica del inventario.
  * `threading.Event`: Bandera de sincronización para la parada limpia del hilo monitor.
  * `queue.Queue`: Cola FIFO segura para hilos que implementa el patrón **Productor-Consumidor**.

---

##  Arquitectura del Sistema

El simulador se compone de:
1. **Queue Compartida:** Almacena la lista de 20 pedidos simulados.
2. **3 Hilos Trabaljadores (Workers):** Extraen pedidos de la cola en paralelo, procesan el pago/simulación fuera del bloqueo y solicitan acceso exclusivo al inventario para descontar el stock.
3. **1 Hilo Monitor:** Observa y reporta periódicamente las métricas globales del sistema sin bloquear la ejecución.
4. **Sección Crítica Protegida:** Uso de `with lock_inventario:` para evitar la sobreventa de productos como el monitor P005.

---

##  Casos de Prueba Evaluados

| ID | Tipo de Prueba | Descripción |
| :--- | :--- | :--- |
| **CP-01** | Flujo Normal | Solicitudes de productos válidos con existencias suficientes. |
| **CP-02** | Contención Extrema | Múltiples hilos compitiendo por el producto P005 (Monitor). |
| **CP-03** | Stock Insuficiente | Pedidos que superan el stock disponible sin alterar el inventario. |
| **CP-04** | Datos Inválidos | Manejo de errores (productos inexistentes, cantidades negativas o cero). |

---

##  Métricas de Ejecución

* **Total de Pedidos:** 20
* **Tiempo Secuencial Teórico ($T_1$):** ~21.25 s
* **Tiempo Concurrente Real ($T_p$):** ~9.02 s
* **Aceleración (*Speedup*):** 2.36x
* **Eficiencia Multihilo:** 78.7%

---

##  Instrucciones de Ejecución

1. Clonar el repositorio:
   ```bash
   git clone [https://github.com/aorellanad7-bit/Practica-Hilos.git](https://github.com/aorellanad7-bit/Practica-Hilos.git)
   cd Practica-Hilos

2. ejecutar el simulador
   python simulador_novatech.py

     
