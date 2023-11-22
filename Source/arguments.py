
from argparse import ArgumentParser

comando_sensor = ArgumentParser(description='Sensor')
comando_monitor = ArgumentParser(description='Monitor')

#Sensor patron

comando_sensor.add_argument(
    '-s',
    '--tipo-sensor',
    type=str,
    help='Tipo sensor',
    required=True
)

comando_sensor.add_argument(
    '-t',
    '--tiempo',
    type=int,
    help='Cada cuanto se enviara informacion',
    required=True
)

comando_sensor.add_argument(
    '-c',
    '--config',
    type=str,
    help='Archivo de configuracion',
    required=True
)

comando_monitor.add_argument(
    '-s',
    '--tipo-monitor',
    type=str,
    help='Tipo de monitor',
    required=True
)