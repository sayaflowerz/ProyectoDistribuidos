
import asyncio
import uuid
import warnings

import zmq
import zmq.asyncio

from .constants import PROXY_SOCKET
from .helpers import health_check, auth


warnings.filterwarnings("ignore", category=RuntimeWarning, module="zmq.*")


def titulo() -> None:
    print('--------- Proxy de sensores ---------')
    print(f'IP del proxy: {PROXY_SOCKET["host"]}')
    print(f'Escuchando información del puerto: {PROXY_SOCKET["backend_port"]}')
    print(f'Publicando información al puerto: {PROXY_SOCKET["frontend_port"]}')
    print('-------------------------------------\n')


async def run() -> None:
    titulo()

    _id = str(uuid.uuid4())

    context = zmq.Context()

    socket_front = context.socket(zmq.XPUB)
    socket_front.bind(f'tcp://*:{PROXY_SOCKET["frontend_port"]}')

    socket_back = context.socket(zmq.XSUB)
    socket_back.bind(f'tcp://*:{PROXY_SOCKET["backend_port"]}')

    zmq.proxy(socket_front, socket_back)

    socket_front.close()
    socket_back.close()
    context.term()


def main() -> None:
    asyncio.run(run())


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    main()
