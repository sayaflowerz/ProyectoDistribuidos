
import subprocess,threading
import asyncio
from typing import Optional, Any
import json
import warnings

import zmq, zmq.asyncio

from constanstes import HEALTH_CHECK_CANAL

warnings.filterwarnings("ignore", category=RuntimeWarning, module="zmq.*")

monitores: list[dict[str,Any]] = []

def titulo() -> None:
    print('----- Health check server -----')
    print(f'IP del health check server: {HEALTH_CHECK_CANAL["host"]}')
    print(f'Escuchando información en el puerto: {HEALTH_CHECK_CANAL["respuesta"]}')
    print(f'Publicando información en el puerto: {HEALTH_CHECK_CANAL["entrada"]}')
    print('-------------------------------\n')

async def escuchar_aut(context: zmq.asyncio.Context) -> None:
    
    socket_a = context.socket(zmq.REP)

    socket_a.bind(f'tcp://*:{HEALTH_CHECK_CANAL['respuesta']}')

    while True:
        res = await socket_a.recv_multipart()

        json_obj = json.loads(res[0])

        assert isinstance(json_obj, dict)

        if json_obj['req'] == 'auth':
            json_obj.pop('req')
            json_obj['status'] = 'ok'

            monitores.append(json_obj)
            print(f'Monitor con id: {json_obj[id]} creado')
        
            socket_a.send(b'OK')

        elif json_obj['req'] == 'health_check':
            _id = json_obj['id']

            monitores_f = list(filter(lambda x:x['id'] == _id, monitores))

            assert len(monitores_f) == 1

            monitores_f[0]['status'] = 'ok'

            print(f'El monitor {_id} ha funcionado')

            socket_a.send(b'OK')
        
def crear_monitor(Tipo: str) -> None:
    command = f'python ProyectoDistribuidos/Source/monitor.py -s {Tipo}'

    threading.Thread(target=lambda: subprocess.run(command)).start()


async def go() -> None:
    titulo()

    context = zmq.asyncio.Context()

    asyncio.create_task(escuchar_aut(context))

    socket_hc = context.socket(zmq.PUB)

    socket_hc.bind(f'tcp//*:{HEALTH_CHECK_CANAL["entrada"]}')

    while True:

        for m in monitores:

            if m['status'] != 'ok':
                print(f'El monitor {m['id']} ha fallado')
                print(f'Creando un nuevo monitor de {m['Tipo_s']}como respaldo...')
                monitores.remove(m)
                crear_monitor(m['Tipo_s'])



def main() -> None:
    asyncio.run(go())



if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    main()





