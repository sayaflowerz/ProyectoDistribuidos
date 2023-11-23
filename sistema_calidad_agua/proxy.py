
import asyncio
import uuid
import warnings

import zmq
import zmq.asyncio

from .constants import PROXY_SOCKET
from .helpers import health_check, auth


warnings.filterwarnings("ignore", category=RuntimeWarning, module="zmq.*")


def print_title() -> None:
    print('--------- Proxy de sensores ---------')
    print(f'IP del proxy: {PROXY_SOCKET["host"]}')
    print(f'Escuchando información del puerto: {PROXY_SOCKET["backend_port"]}')
    print(f'Publicando información al puerto: {PROXY_SOCKET["frontend_port"]}')
    print('-------------------------------------\n')


async def run() -> None:
    print_title()

    _id = str(uuid.uuid4())

    context = zmq.Context()

    # await auth(context, _id, 'proxy')

    # asyncio.create_task(health_check(context, _id))

    frontend_socket = context.socket(zmq.XPUB)
    frontend_socket.bind(f'tcp://*:{PROXY_SOCKET["frontend_port"]}')

    backend_socket = context.socket(zmq.XSUB)
    backend_socket.bind(f'tcp://*:{PROXY_SOCKET["backend_port"]}')

    zmq.proxy(frontend_socket, backend_socket)

    frontend_socket.close()
    backend_socket.close()
    context.term()


def main() -> None:
    asyncio.run(run())


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    main()
