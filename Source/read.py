

def leer_archivo_config(file : str):

    Values: list[float] = []

    with open(file, "r") as f:
        Values = list(map(float,f.readlines()))

    return Values
    
