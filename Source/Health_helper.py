
from typing import Optional

import zmq
import zmq.asyncio

from constanstes import HEALTH_CHECK_CANAL

async def autenticacion(context: zmq.asyncio.Context, uuid: str, Tipo_s:str ) -> None:

    autenticacion_socket = context.socket(zmq.REQ)
    autenticacion_socket.connect(f'tcp://{HEALTH_CHECK_CANAL["host"]}:{HEALTH_CHECK_CANAL["respuesta"]}')

    autenticacion_socket.send_json({'id': uuid, 'req': 'auth', 'Tipo_s': Tipo_s})

    await autenticacion_socket.recv()
    print('Atuntenticacion exitosa')


async def Suscribe_Answer(context: zmq.asyncio.Context, uuid: str)-> None:

    print('Escuchando a health check')
    subscribe_socket = context.socket(zmq.SUB)
    subscribe_socket.connect(f'tcp://{HEALTH_CHECK_CANAL["host"]}:{HEALTH_CHECK_CANAL["entrada"]}')

    subscribe_socket.setsockopt(zmq.SUBSCRIBE, bytes('','utf-8'))

    while True:

        await subscribe_socket.recv()
        print('Health check recibido')

        answer_socket = context.socket(zmq.REQ)
        answer_socket.connect(f'tcp://{HEALTH_CHECK_CANAL["host"]}:{HEALTH_CHECK_CANAL["respuesta"]}')
        
        answer_socket.send_json({'id': uuid, 'req' : 'health_check'})
