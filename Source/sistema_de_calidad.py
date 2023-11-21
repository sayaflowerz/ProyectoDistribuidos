
import time
import asyncio
import warnings
import zmq
import zmq.asyncio

from constanstes import CALIDAD_CANAL

warnings.filterwarnings("ignore", category=RuntimeWarning, module="zmq.*")

def titulo()-> None:
    print('----- Sistema de calidad de agua -----')
    print(f'IP del sistema: {CALIDAD_CANAL["host"]}')
    print(f'Escuchando información del puerto: {CALIDAD_CANAL["port"]}')
    print('-\n')

async def go()-> None:
    titulo()

    context = zmq.asyncio.Context()
    socket = context.socket(zmq.SUB)

    socket.bind(f'tcp://*:{CALIDAD_CANAL["port"]}')
    socket.setsockopt(zmq.SUBSCRIBE, b'')

    while True:

        mensaje = await socket.recv_multipart()

        print(f"Alerta detectada {mensaje[0].decode('utf-8')}")
        print(f"Mensaje: '{mensaje[1].decode('utf-8')}'")
        timestamp = float(mensaje[2].decode('utf-8'))
        hora = time.time()
        tiempo = timestamp - hora
        print(f"Timestamp: {timestamp} - {hora} = {tiempo}\n")

def main()-> None:
    asyncio.run(go())

if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    main()   