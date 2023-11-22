import asyncio
import uuid
import warnings
import zmq
import zmq.asyncio

from constanstes import PROXY_CANAL
from Health_helper import Suscribe_Answer, autenticacion

def titulo() ->None:
    print('--------- Proxy de sensores ---------')
    print(f'IP del proxy: {PROXY_CANAL["host"]}')
    print(f'Escuchando información del puerto: {PROXY_CANAL["publishers"]}')
    print(f'Publicando información al puerto: {PROXY_CANAL["subscribers"]}')
    print('-\n')


async def go() ->None:
    titulo()

    _id = str(uuid.uuid4())

    context = zmq.Context()

    f_socket = context.socket(zmq.XPUB)
    f_socket.bind(f'tcp://*:{PROXY_CANAL["subscribers"]}')

    b_socket = context.socket(zmq.XSUB)
    b_socket.bind(f'tcp://*:{PROXY_CANAL["publishers"]}')

    zmq.proxy(f_socket, b_socket)

    f_socket.close()
    b_socket.close()
    context.term()

def main()-> None:
    asyncio.run(go())
    

if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    main()