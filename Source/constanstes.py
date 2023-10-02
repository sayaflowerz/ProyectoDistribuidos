
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
