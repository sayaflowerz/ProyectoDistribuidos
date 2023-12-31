
import json
import time
import uuid
from typing import Any
import asyncio
import warnings

import zmq
import zmq.asyncio

from .helpers import auth, health_check
from .constants import DB_PATH, DB_SOCKET


warnings.filterwarnings("ignore", category=RuntimeWarning, module="zmq.*")


def print_title() -> None:
    print('------ Gestor de base de datos ------')
    print(f'IP de la base de datos: {DB_SOCKET["host"]}')
    print(f'Escuchando información en el puerto: {DB_SOCKET["port"]}')
    print('--------------------------------------\n')


def write_to_db(data: dict[str, Any]) -> None:
    '''Write data to database.'''

    with open(DB_PATH, 'w') as f:
        json.dump(data, f)


def read_from_db() -> dict[str, Any]:
    '''Read data from database.'''

    with open(DB_PATH, 'r') as f:
        return json.load(f)


def write_valid_info(type_sensor: str, value: float, timestamp: float = time.time()) -> None:
    '''Write valid data to database.'''

    if value < 0:
        raise ValueError(f'Valor inválido: {value}')

    data = read_from_db()

    data[type_sensor].append({
        'value': value,
        'timestamp': timestamp
    })

    write_to_db(data)


async def run() -> None:
    _id = str(uuid.uuid4())

    print_title()

    context = zmq.asyncio.Context()

    await auth(context, _id, 'db_manager')

    asyncio.create_task(health_check(context, _id))

    socket = context.socket(zmq.REP)

    socket.bind(f'tcp://*:{DB_SOCKET["port"]}')

    while True:
        res = await socket.recv_multipart()

        json_obj = json.loads(res[0])

        try:
            assert isinstance(json_obj, dict)

            write_valid_info(json_obj['type_sensor'],
                             json_obj['value'], json_obj['timestamp'])

            socket.send_json({'status': 'ok'})

        except Exception as e:
            print(f'Error: {e}')
            socket.send_json({'status': 'error', 'message': str(e)})


def main() -> None:
    asyncio.run(run())


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    main()
