
import random

from ..constants import SensorValues, SensorType, RANGES


def get_sensor_value(sensorType: SensorType, config: dict[SensorValues, float]) -> float:
    probability = random.random()

    min, max = RANGES[sensorType]

    if probability < config[SensorValues.VALORES_CORRECTOS]:
        return random.uniform(min, max)

    elif probability < config[SensorValues.VALORES_CORRECTOS] + config[SensorValues.VALORES_FUERA_RANGO]:
        probability = random.random()
        if probability < 0.5:
            return random.uniform(0, min)
        else:
            return random.uniform(max, max + min)
    else:
        return random.uniform(-min, 0)


def is_in_range(sensorType: SensorType, value: float) -> bool:
    min, max = RANGES[sensorType]

    return min <= value <= max
