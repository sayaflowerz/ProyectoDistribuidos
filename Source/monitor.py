from zmq import Context, SUB
from arguments import comando_monitor

# Configuración del canal de comunicación
context = Context()
socket = context.socket(SUB)
socket.connect("tcp://localhost:5560")

# Función para simular un monitor
def simular_monitor(tipo_sensor):
    socket.subscribe(tipo_sensor.encode())  # Suscripción al tipo de sensor
    while True:
        mensaje = socket.recv_string()
        tipo, lectura, hora = mensaje.split(": ")
        validar_y_almacenar_lectura(tipo, float(lectura), hora)


# Función para validar y almacenar la lectura
def validar_y_almacenar_lectura(tipo_sensor, lectura, hora):
    # Aquí implementar la lógica para validar la lectura y almacenarla en una base de datos o archivo
    
    # Si la lectura está fuera del rango, generar una alarma
    if lectura < 0 or lectura > 100:
        generar_alarma(tipo_sensor, lectura, hora)

# Función para generar una alarma
def generar_alarma(tipo_sensor, lectura, hora):
    # Aquí  implementar la lógica para generar y registrar una alarma
    print(f"Alarma en {tipo_sensor} a las {hora}: Lectura fuera del rango: {lectura}")

if __name__ == "__main__":
    # Obtener argumentos de línea de comandos
    args = comando_monitor.parse_args()
    
    # Llamar a la función para simular el monitor
    simular_monitor(args.tipo_sensor)
