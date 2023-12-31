
# Antes de ejecutar, asegurarse de tener configurado:

- Las IPs y los puertos (opcional) de los nodos en el archivo `./sistema_calidad_agua/constants/net.py`
- Tener el archivo de configuración de los sensores creado (pueden usar el del enunciado en `./sistema_calidad_agua/config/ejemplo.txt`)

# Comandos

## Comandos de configuración:

### Instalar dependencias
```bash
poetry install
```

## Ejecutar nodos:

### Ejecutar sensor
Los tipos de sensor son: `Temperatura`, `PH`, `Oxigeno` (Cuidado con las mayúsculas)
El tiempo entre medidas es en segundos
```bash
poetry run sensor -s <tipo-sensor> -t <tiempo-entre-medidas> -c <path-archivo-configuracion>
```

### Ejecutar monitor
Los tipos de sensor son: `Temperatura`, `PH`, `Oxigeno` (Cuidado con las mayúsculas)
```bash
poetry run monitor -s <tipo-sensor>
```

### Ejecutar proxy
```bash
poetry run proxy
```

### Ejecutar db_manager
```bash
poetry run db_manager
```

### Ejecutar health_check
```bash
poetry run health_check
```

### Ejecutar sistema_calidad_agua
```bash
poetry run sistema_calidad_agua
```
