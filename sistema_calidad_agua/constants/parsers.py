
from argparse import ArgumentParser


# * Declarando parsers:

sensor_parser = ArgumentParser(description='Sensor')
monitor_parser = ArgumentParser(description='Monitor')


# * Declarando argumentos:

# ** Argumentos para parser:
sensor_parser.add_argument(
    '-s',
    '--tipo-sensor',
    type=str,
    help='Tipo de sensor',
    required=True
)

sensor_parser.add_argument(
    '-t',
    '--tiempo',
    type=int,
    help='Cada cuanto tiempo se envia la informacion',
    required=True
)

sensor_parser.add_argument(
    '-c',
    '--config',
    type=str,
    help='Archivo de configuracion',
    required=True
)

# ** Argumentos para monitor:

monitor_parser.add_argument(
    '-s',
    '--tipo-sensor',
    type=str,
    help='Tipo de sensor',
    required=True
)
