import sys
import time
import asyncio

import zmq
import zmq.asyncio

from argparse import Namespace 
from constanstes import PROXY_CANAL
from arguments import comando_sensor
from operaciones import probabilidad
from read import leer_archivo_config


def titulo(tipo: str)-> None:
    print(f'----- Sensor de calidad de agua: {tipo} -----')
    print(f'Publicando información a la dirección: {PROXY_CANAL["host"]}:{PROXY_CANAL["publishers"]}')
    print('-\n')

async def go()-> None:
    
    args = comando_sensor.parse_args()
    tipo = args.tipo_sensor
    config = leer_archivo_config(args.config)
    tiempo = args.tiempo

    titulo(tipo)

    context = zmq.asyncio.Context()

    socket = context.socket(zmq.PUB)
    socket.connect(f'tcp://{PROXY_CANAL["host"]}:{PROXY_CANAL["publishers"]}')

    while True:

        chances = probabilidad(config,tipo)
        socket.send(bytes(f'{tipo} {chances} {time.time()}', 'utf-8'))
        print(f'Enviando al proxy... {tipo} {chances} {time.time()}')
        time.sleep(tiempo)




def main():
    asyncio.run(go())

if __name__ == "__main__":
    main()