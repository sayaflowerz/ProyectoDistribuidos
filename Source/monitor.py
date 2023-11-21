
import sys
import time
import asyncio
import uuid
import warnings
import json
import zmq,zmq.asyncio

 
from constanstes import PROXY_CANAL, DB_CANAL, CALIDAD_CANAL
from arguments import comando_monitor
from operaciones import en_rango
from Health_helper import autenticacion, Suscribe_Answer



warnings.filterwarnings("ignore", category=RuntimeWarning, module="zmq.*")


def titulo(tipo:str) -> None:
    print(f'----- Monitor de {tipo}: -----')
    print(f'Escuchando información de los sensores: {PROXY_CANAL["host"]}:{PROXY_CANAL["subscribers"]}')
    print(f'Publicando información a la base de datos: {DB_CANAL["host"]}:{DB_CANAL["port"]}')
    print(f'Publicando información al sistema: {CALIDAD_CANAL["host"]}:{CALIDAD_CANAL["port"]}')
    print('-\n')


async def go() ->None:

    args = comando_monitor.parse_args()
    tipo = args.tipo_monitor
    _id = str(uuid.uuid4())

    titulo(tipo)

    context = zmq.asyncio.Context()

    await autenticacion(context, _id, tipo)

#Proxy

    socket_sensores = context.socket(zmq.SUB)
    socket_sensores.connect(f'tcp//{PROXY_CANAL["host"]}:{PROXY_CANAL["subscribers"]}')
    socket_sensores.setsockopt(zmq.SUBSCRIBE, bytes (tipo, 'utf-8'))

#Sistema

    socket_sistema = context.socket(zmq.SUB)
    socket_sistema.connect(f'tcp://{CALIDAD_CANAL["host"]}:{CALIDAD_CANAL["port"]}')

    while True:

        mensaje = await socket_sensores.recv_multipart()

        valor = float(mensaje[0].decode('uft-8').split()[1])
        hora = float(mensaje[0].decode('uft-8').split()[2])

        socket_base = context.socket(zmq.REQ)
        socket_base.connect(f'tcp://{DB_CANAL["host"]}:{DB_CANAL["port"]}')

        print(f'Enviando informacion a la base de datos: {valor} {tipo}')
        socket_base.send_json({
            'Tipo_sensor' : tipo,
            'dato' : valor,
            'time' : hora
        })

        res = await socket_base.recv_multipart()

        json_obj = json.loads(res[0])

        assert isinstance(json_obj, dict)

        if json_obj['status'] == 'ok':
            if not en_rango(tipo,valor):
                socket_sistema.send_multipart([
                    bytes(tipo, 'utf-8'),
                    bytes(f'Valor fuera de rango: {valor}', 'utf-8'),
                    bytes(str(hora), 'utf-8')
                ])
        else:
            print(f'Error : {json_obj["message"]}')

    ...

def main():
    asyncio.run(go())


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    main()