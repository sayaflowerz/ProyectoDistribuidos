
from typing import TypedDict


Socket = TypedDict('Socket', {
    'host': str,
    'port': int,
})

ProxySocket = TypedDict('ProxySocket', {
    'host': str,
    'frontend_port': int,
    'backend_port': int,
})

HealthCheckSocket = TypedDict('HealthCheckSocket', {
    'host': str,
    'port_res': int,
    'port_health_check': int,
})

PROXY_SOCKET: ProxySocket = {
    'host': 'localhost', # TODO: Change this to the IP of the proxy server
    'frontend_port': 5555,
    'backend_port': 5556,
}

SYSTEM_SOCKET: Socket = {
    'host': 'localhost', # TODO: Change this to the IP of the system server
    'port': 5561,
}

DB_SOCKET: Socket = {
    'host': 'localhost', # TODO: Change this to the IP of the database server
    'port': 5558,
}

HEALTH_CHECK_SOCKET: HealthCheckSocket = {
    'host': 'localhost', # TODO: Change this to the IP of the health check server
    'port_res': 5559,
    'port_health_check': 5560,
}
