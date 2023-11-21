
import json
import time
import uuid
from typing import Any
import asyncio
import warnings

import zmq
import zmq.asyncio

from Health_helper import autenticacion,Suscribe_Answer
from constanstes import DB_PATH,DB_CANAL

warnings.filterwarnings("ignore", category=RuntimeWarning, module="zmq.*")

def titulo() -> None:
    print('------ Gestor de base de datos ------')
    print(f'IP de la base de datos: {DB_CANAL["host"]}')
    print(f'Escuchando información en el puerto: {DB_CANAL["port"]}')
    print('-\n')

def escribir(data:dict[str,Any])-> None:
    
    with open(DB_PATH,'w') as e:
        json.dump(data,e)

def leer()->dict[str,Any]:

    with open(DB_PATH,'r') as l:
        return json.load(l) 
    
def infovalida(tipo: str, valor: float, hora: float = time.time())->None:

    if valor < 0:
        raise ValueError(f'Valor invalido: {valor}')
    
    data = leer()

    data[tipo].append({
        'dato' : valor,
        'time' : hora
    })

    escribir(data)


async def go()-> None:

    titulo()

    context = zmq.asyncio.Context()

    socket = context.socket(zmq.REQ)

    socket.bind(f'tcp://*:{DB_CANAL["port"]}')

    while True:

        res = await socket.recv_multipart()

        json_obj = json.loads(res[0])

        try:
            assert isinstance(json_obj,dict)

            infovalida(json_obj['Tipo_sensor'], json_obj['dato'],json_obj['time'])

            socket.send_json({'status' : 'ok'})

        except Exception as e:
            print(f'Error: {e}')
            socket.send_json({'status:': 'error', 'mensaje':str(e)})

def main()-> None:
    asyncio.run(go())

if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    main() 
    
 