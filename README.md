# Simulador de Procesamiento Concurrente - NovaTech 🛒

Este proyecto es una aplicación de consola desarrollada en Python que simula el procesamiento concurrente de pedidos para la tienda tecnológica NovaTech. Demuestra el uso de hilos reales, manejo de secciones críticas y protección de recursos compartidos para evitar condiciones de carrera.

## 🛠️ Tecnologías y Dependencias
* **Lenguaje:** Python 3.x (Probado en Python 3.10+)
* **Dependencias:** El proyecto utiliza únicamente bibliotecas estándar de Python. No requiere instalación de paquetes externos.
  * `threading`: Para la creación y sincronización de hilos.
  * `queue`: Para el manejo seguro de la cola de pedidos.
  * `time`: Para la simulación de trabajo y control del monitor.
  * `random`: Para generar tiempos de procesamiento variables.

##  Cómo ejecutar el proyecto
1. Abre una terminal (o la consola integrada de tu editor de código).
2. Navega hasta el directorio donde se encuentra el archivo `simulador_novatech.py`.
3. Ejecuta el siguiente comando:
   ```bash
   python simulador_novatech.py