
import random
from constanstes import RANGOS

def probabilidad(lista: list[float],tipo:str):

    x=random.random()

    min,max = RANGOS[tipo]
 
    if x <= lista[0]: #menores que 6
        return random.uniform(min,max)
    elif x<lista[0]+lista[1] : #mayores que 6 menores que 9
        y = random.random()
        if y < 0.5:
            return random.uniform(max,max+min)
        else: 
            return random.uniform(0,min)
    else:
        return random.uniform(-10,-1)
    
def en_rango(Sensor: str, value: float ) -> bool:

        min,max = RANGOS[Sensor]
        return min<=value<=max