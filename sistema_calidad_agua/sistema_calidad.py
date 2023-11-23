
import time
import asyncio
import warnings
import zmq
import zmq.asyncio

from sistema_calidad_agua.constants import SYSTEM_SOCKET
from .constants import SensorType,RANGES


warnings.filterwarnings("ignore", category=RuntimeWarning, module="zmq.*")


def titulo() -> None:
    print('----- Sistema de calidad de agua -----')
    print(f'IP del sistema: {SYSTEM_SOCKET["host"]}')
    print(f'Escuchando información del puerto: {SYSTEM_SOCKET["port"]}')
    print('--------------------------------------\n')


async def run() -> None:
    titulo()

    context = zmq.asyncio.Context()
    socket = context.socket(zmq.SUB)

    socket.bind(f'tcp://*:{SYSTEM_SOCKET["port"]}')
    socket.setsockopt(zmq.SUBSCRIBE, b'')

    while True:
        mensaje = await socket.recv_multipart()

        tipo = mensaje[0].decode('utf-8')

        cambio = SensorType(tipo)

        min,max = RANGES[cambio]

        print(f"Alerta recibida de {mensaje[0].decode('utf-8')}")
        print(f'Valores normales entre: {min} y {max}')
        print(f"Mensaje: '{mensaje[1].decode('utf-8')}'")
        timestamp = float(mensaje[2].decode('utf-8'))
        timestamp_actual = time.time()
        tiempo = timestamp - timestamp_actual
        print(f"Timestamp: {timestamp} - {timestamp_actual} = {tiempo}\n")


def main() -> None:
    asyncio.run(run())


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    main()
