
import sys
import time
import asyncio
import uuid
import warnings
import json

import zmq
import zmq.asyncio

from .helpers import is_in_range, auth, health_check

from .constants import monitor_parser, SensorType, PROXY_SOCKET, DB_SOCKET, SYSTEM_SOCKET


warnings.filterwarnings("ignore", category=RuntimeWarning, module="zmq.*")


def titulo(sensor_type: SensorType) -> None:
    print(f'----- Monitor de calidad de agua: {sensor_type.value} -----')
    print(f'Escuchando información de los sensores: {PROXY_SOCKET["host"]}:{PROXY_SOCKET["frontend_port"]}')
    print(f'Publicando información a la base de datos: {DB_SOCKET["host"]}:{DB_SOCKET["port"]}')
    print(f'Publicando información al sistema: {SYSTEM_SOCKET["host"]}:{SYSTEM_SOCKET["port"]}')
    print('--------------------------------------\n')


async def run() -> None:
    args = monitor_parser.parse_args()
    tipo_sensor: SensorType
    _id = str(uuid.uuid4())

    try:
        tipo_sensor = SensorType(args.tipo_sensor)
    except ValueError:
        print(f"Tipo de sensor '{args.tipo_sensor}' inválido")
        sys.exit(1)

    titulo(tipo_sensor)

    context = zmq.asyncio.Context()

    await auth(context, _id, 'monitor', {'-s': tipo_sensor.value})

    asyncio.create_task(health_check(context, _id))

    socket_sensors = context.socket(zmq.SUB)
    socket_sensors.connect(
        f'tcp://{PROXY_SOCKET["host"]}:{PROXY_SOCKET["frontend_port"]}')
    socket_sensors.setsockopt(zmq.SUBSCRIBE, bytes(tipo_sensor.value, 'utf-8'))

    socket_system = context.socket(zmq.PUB)
    socket_system.connect(
        f'tcp://{SYSTEM_SOCKET["host"]}:{SYSTEM_SOCKET["port"]}')

    while True:
        message = await socket_sensors.recv_multipart()

        value = float(message[0].decode('utf-8').split()[1])
        timestamp = float(message[0].decode('utf-8').split()[2])
        
        socket_db = context.socket(zmq.REQ)
        socket_db.connect(
            f'tcp://{DB_SOCKET["host"]}:{DB_SOCKET["port"]}')

        print(f'Enviando datos a la base de datos: {value} {tipo_sensor.value}')
        socket_db.send_json({
            'type_sensor': tipo_sensor.value,
            'value': value,
            'timestamp': timestamp
        })

        res = await socket_db.recv_multipart()

        json_obj = json.loads(res[0])

        assert isinstance(json_obj, dict)

        if json_obj['status'] == 'ok':
            if not is_in_range(tipo_sensor, value):
                socket_system.send_multipart([
                    bytes(tipo_sensor.value, 'utf-8'),
                    bytes(f'Valor fuera de rango: {value}', 'utf-8'),
                    bytes(str(timestamp), 'utf-8')
                ])
        else:
            print(f'Error: {json_obj["message"]}')


def main() -> None:
    asyncio.run(run())


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    main()
