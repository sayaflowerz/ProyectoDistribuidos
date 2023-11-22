
import subprocess
import threading
import asyncio
from typing import Optional, Any
import json
import warnings

import zmq
import zmq.asyncio

from .constants import HEALTH_CHECK_SOCKET


warnings.filterwarnings("ignore", category=RuntimeWarning, module="zmq.*")

nodes: list[dict[str, Any]] = []


def print_title() -> None:
    print('----- Health check server -----')
    print(f'IP del health check server: {HEALTH_CHECK_SOCKET["host"]}')
    print(f'Escuchando información en el puerto: {HEALTH_CHECK_SOCKET["port_res"]}')
    print(f'Publicando información en el puerto: {HEALTH_CHECK_SOCKET["port_health_check"]}')
    print('-------------------------------\n')


async def listen_auth(context: zmq.asyncio.Context) -> None:
    socket_auth = context.socket(zmq.REP)

    socket_auth.bind(f'tcp://*:{HEALTH_CHECK_SOCKET["port_res"]}')

    while True:
        res = await socket_auth.recv_multipart()

        json_obj = json.loads(res[0])

        assert isinstance(json_obj, dict)

        if json_obj['req'] == 'auth':
            json_obj.pop('req')
            json_obj['status'] = 'ok'

            assert json_obj['type'] in ['monitor', 'proxy', 'db_manager']

            nodes.append(json_obj)
            print(f'Nodo {json_obj["id"]} de tipo {json_obj["type"]} creado')

            socket_auth.send(b'OK')
        elif json_obj['req'] == 'health_check':
            _id = json_obj['id']

            filtered_nodes = list(
                filter(lambda node: node['id'] == _id, nodes))

            assert len(filtered_nodes) == 1

            filtered_nodes[0]['status'] = 'ok'

            print(f'Nodo {_id} funcionando correctamente')

            socket_auth.send(b'OK')


def create_node(node_type: str, flags: Optional[dict[str, str]] = None) -> None:
    command = f'poetry run {node_type}'
    
    if flags:
        for flag, value in flags.items():
            command += f' {flag} {value}'
    
    threading.Thread(target=lambda: subprocess.run(command)).start()


async def run() -> None:
    print_title()

    context = zmq.asyncio.Context()

    asyncio.create_task(listen_auth(context))

    socket_health_check = context.socket(zmq.PUB)

    socket_health_check.bind(f'tcp://*:{HEALTH_CHECK_SOCKET["port_health_check"]}')


    while True:
        for node in nodes:
            node['status'] = 'not ok'

        print('Revisando nodos...')
        socket_health_check.send_json({
            'req': 'health_check',
        })

        await asyncio.sleep(10)

        for node in nodes:
            if node['status'] != 'ok':
                print(f'El nodo {node["id"]} no está funcionando correctamente')
                print(f'Creando nodo {node["type"]}...')
                nodes.remove(node)
                create_node(node['type'], node.get('flags'))

def main() -> None:
    asyncio.run(run())


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    main()
