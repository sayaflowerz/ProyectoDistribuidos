
import zmq
 
from constanstes import PROXY_CANAL
from arguments import comando_monitor


def main():

    Beta = comando_monitor.parse_args()

    context = zmq.Context()

    socket = context.socket(zmq.SUB)
    socket.connect(f'tcp://{PROXY_CANAL["host"]}:{PROXY_CANAL["subscribers"]}') #en el codigo de alla la direccion de aca
    socket.setsockopt(zmq.SUBSCRIBE, bytes(Beta.tipo_sensor,'utf-8'))

    while True:
        message = socket.recv_multipart()
        print(f'Received: {message}')
        ...

if __name__ == "__main__":
    main()