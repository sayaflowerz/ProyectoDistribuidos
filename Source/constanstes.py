
from typing import TypedDict


DB_PATH = 'ProyectoDistribuidos/Source/db.json'

Canal = TypedDict('Canal', {
    'host' : str,
    'subscribers' : int,
    'publishers' : int,
})

Socket = TypedDict('Socket', {
    'host' : str,
    'port' : int,
})

Health = TypedDict('Health', {
    'host' : str,
    'respuesta' : int,
    'entrada' : int,
})

#//--------------------------------------------------------------------------------------------------------//

PROXY_CANAL: Canal = {
    'host' : 'localhost',
    'subscribers' : 5555,
    'publishers' : 5556,
}

CALIDAD_CANAL: Socket = {
    'host' : 'localhost',
    'port' : 5561    
}

DB_CANAL: Socket = {
    'host' : 'localhost', #IP donde ira la base de datos
    'port' : 5558
}

HEALTH_CHECK_CANAL: Health = {
    'host' : 'localhost',
    'respuesta' : 5559,
    'entrada' : 5560
}

RANGOS: dict [str,tuple[float,float]] = {
    'Temperatura' : (68,89),
    'PH' : (6.0,8.0),
    'Oxigeno' : (2,11)
}