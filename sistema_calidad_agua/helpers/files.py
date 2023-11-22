
from ..constants import SensorValues


def read_config_file(file: str) -> dict[SensorValues, float]:

    res: dict[SensorValues, float] = {}

    lines: list[str] = []

    with open(file, "r") as f:
        lines = f.readlines()

    for line in lines:
        if line.strip() == '':
            continue

        words = line.split()

        val = float(words[0])
        name = (' '.join(words[1:])).strip()
        try:
            name = SensorValues(name)
        except ValueError:
            raise ValueError(
                f"Nombre '{name}' inválido en archivo de configuración")

        if name in res:
            raise ValueError(
                f"Nombre '{name}' duplicado en archivo de configuración")

        res[name] = val

    if not SensorValues.VALORES_CORRECTOS in res:
        raise ValueError(
            f"Nombre '{SensorValues.VALORES_CORRECTOS.value}' no encontrado en archivo de configuración")
    if not SensorValues.VALORES_FUERA_RANGO in res:
        raise ValueError(
            f"Nombre '{SensorValues.VALORES_FUERA_RANGO.value}' no encontrado en archivo de configuración")
    if not SensorValues.ERRORES in res:
        raise ValueError(
            f"Nombre '{SensorValues.ERRORES.value}' no encontrado en archivo de configuración")

    return res
