
from typing import TypedDict


Canal = TypedDict('Canal', {
    'host' : str,
    'subscribers' : int,
    'publishers' : int,
})

PROXY_CANAL: Canal = {
    'host' : 'localhost',
    'subscribers' : 5555,
    'publishers' : 5556,
}

RANGOS: dict [str,tuple[float,float]] = {
    'Temperatura' : (68,89),
    'PH' : (6.0,8.0),
    'Oxigeno' : (2,11)
}