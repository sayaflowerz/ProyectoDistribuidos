import time
import random
from zmq import Context, PUB
from read import leer_archivo_config
from arguments import comando_sensor

# Configuración del canal de comunicación
context = Context()
socket = context.socket(PUB)
socket.connect("tcp://localhost:5559")

# Función para simular un sensor
def simular_sensor(tipo_sensor, tiempo, config_file):
    while True:
        # Leer las probabilidades desde el archivo de configuración
        probabilidades = leer_archivo_config(config_file)
        
        # Generar lectura aleatoria basada en las probabilidades
        lectura = generar_lectura_aleatoria(probabilidades)
        
        # Obtener la hora actual
        hora_actual = time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Publicar lectura en el canal
        mensaje = f"{tipo_sensor}: {lectura} @ {hora_actual}"
        socket.send_string(mensaje)
        
        # Esperar el tiempo especificado antes de enviar la siguiente lectura
        time.sleep(tiempo)

# Función para generar una lectura aleatoria basada en probabilidades
def generar_lectura_aleatoria(probabilidades):
    valor = random.random()
    if valor < probabilidades[0]:
        # Valor dentro del rango
        return random.uniform(0, 100)  # Modificar el rango según tus necesidades
    elif valor < probabilidades[0] + probabilidades[1]:
        # Valor fuera del rango
        return random.uniform(101, 200)  # Modificar el rango según tus necesidades
    else:
        # Valor erróneo
        return -1

if __name__ == "__main__":
    # Obtener argumentos de línea de comandos
    args = comando_sensor.parse_args()
    
    # Llamar a la función para simular el sensor
    simular_sensor(args.tipo_sensor, args.tiempo, args.config)
