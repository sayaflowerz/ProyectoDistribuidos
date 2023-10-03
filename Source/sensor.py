
import time
import zmq
 
from constanstes import PROXY_CANAL
from arguments import comando_sensor
from operaciones import probabilidad
from read import leer_archivo_config


def main():

    Alpha = comando_sensor.parse_args()

    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.connect(f'tcp://{PROXY_CANAL["host"]}:{PROXY_CANAL["publishers"]}')

    while True:
        mensaje = Alpha.tipo_sensor + ',' +  str(probabilidad(leer_archivo_config(Alpha.config),Alpha.tipo_sensor)) #wtf
        socket.send(bytes(mensaje,'utf-8'))
        time.sleep(Alpha.tiempo)

if __name__ == "__main__":
    main()