
import sys
import time
import asyncio

import zmq
import zmq.asyncio
from argparse import Namespace

from .constants import sensor_parser, SensorType, SensorValues, PROXY_SOCKET
from .helpers import read_config_file, get_sensor_value


def print_title(sensor_type: SensorType) -> None:
    print(f'----- Sensor de calidad de agua: {sensor_type.value} -----')
    print(f'Publicando información a la dirección: {PROXY_SOCKET["host"]}:{PROXY_SOCKET["backend_port"]}')
    print('--------------------------------------\n')


def get_args(args: Namespace) -> tuple[str, int, dict[SensorValues, float]]:
    tipo_sensor: SensorType

    try:
        tipo_sensor = SensorType(args.tipo_sensor)
    except ValueError:
        print(f"Tipo de sensor '{args.tipo_sensor}' inválido")
        sys.exit(1)

    print_title(tipo_sensor)

    tiempo: int = args.tiempo
    config = read_config_file(args.config)

    return tipo_sensor.value, tiempo, config


async def run() -> None:
    tipo_sensor, tiempo, config = get_args(sensor_parser.parse_args())

    context = zmq.asyncio.Context()
    socket = context.socket(zmq.PUB)
    socket.connect(
        f'tcp://{PROXY_SOCKET["host"]}:{PROXY_SOCKET["backend_port"]}')

    while True:
        sensor_value = get_sensor_value(SensorType(tipo_sensor), config)
        socket.send(bytes(f'{tipo_sensor} {sensor_value} {time.time()}', 'utf-8'))
        print(f'Enviando: {tipo_sensor} {sensor_value} {time.time()}')
        time.sleep(tiempo)


def main() -> None:
    asyncio.run(run())


if __name__ == '__main__':
    main()
