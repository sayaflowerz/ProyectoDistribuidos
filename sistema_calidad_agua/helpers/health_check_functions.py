
from typing import Optional

import zmq
import zmq.asyncio

from ..constants import HEALTH_CHECK_SOCKET


async def auth(context: zmq.asyncio.Context, uuid: str, node_type: str, flags: Optional[dict[str, str]] = None) -> None:
    auth_socket = context.socket(zmq.REQ)
    auth_socket.connect(
        f'tcp://{HEALTH_CHECK_SOCKET["host"]}:{HEALTH_CHECK_SOCKET["port_res"]}')

    auth_socket.send_json({'id': uuid, 'type': node_type,
                          'req': 'auth', 'flags': flags})
    await auth_socket.recv()
    print('Autenticación exitosa')


async def health_check(context: zmq.asyncio.Context, uuid: str) -> None:
    print('Escuchando health check')
    sub_socket = context.socket(zmq.SUB)
    sub_socket.connect(
        f'tcp://{HEALTH_CHECK_SOCKET["host"]}:{HEALTH_CHECK_SOCKET["port_health_check"]}')
    sub_socket.setsockopt(zmq.SUBSCRIBE, bytes('', 'utf-8'))

    while True:
        await sub_socket.recv()
        print(f'Health check recibido')

        res_socket = context.socket(zmq.REQ)
        res_socket.connect(
            f'tcp://{HEALTH_CHECK_SOCKET["host"]}:{HEALTH_CHECK_SOCKET["port_res"]}')
        res_socket.send_json({'id': uuid, 'req': 'health_check'})
