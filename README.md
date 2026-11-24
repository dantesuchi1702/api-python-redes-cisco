# Trabajo Práctico Integrador - Redes de Computadoras

## Integrantes del Grupo 4
* **Dante Segovia**
* **Tobías Caba**
* **Lautaro Villafañe**
* **Santiago Granero**
* **Emanuel Barreto**

## Script del Grupo (`src/exportar_inventario_csv.py`)

Automatiza el relevamiento de la red consultando la API REST del **Network Controller** (`POST /ticket`, `GET /network-device` y `GET /host`). Procesa los datos agregando marca de tiempo, métricas de disponibilidad y correlación de puerto/VLAN para cada terminal, exportando dos reportes persistentes listos para Excel (`inventario_dispositivos.csv` e `inventario_hosts.csv`).

### Ejecución
```bash
python src/exportar_inventario_csv.py
```
---

