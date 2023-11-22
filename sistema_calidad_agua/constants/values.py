
from enum import Enum


class SensorValues(Enum):
    VALORES_CORRECTOS = 'Valores correctos'
    VALORES_FUERA_RANGO = 'Valores fuera del rango'
    ERRORES = 'Errores'

class SensorType(Enum):
    TEMPERATURA = 'Temperatura'
    PH = 'PH'
    OXIGENO_DISUELTO = 'Oxigeno'

RANGES: dict[SensorType, tuple[float, float]] = {
    SensorType.TEMPERATURA: (68, 89),
    SensorType.PH: (6.0, 8.0),
    SensorType.OXIGENO_DISUELTO: (2, 11),
}
