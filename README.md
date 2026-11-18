# Trabajo Práctico Integrador - Redes de Computadoras

## Integrantes del Grupo 4
* **Dante Segovia**
* **Tobías Caba**
* **Lautaro Villafañe**
* **Santiago Granero**
* **Emanuel Barreto**

## Script del Grupo (`src/`)
### Funcionalidad
El script automatiza la consulta del inventario de red a través de la API REST del **Network Controller** de Cisco Packet Tracer:
1. **Autenticación (`POST /api/v1/ticket`):** Obtiene dinámicamente el `serviceTicket` y lo inyecta en la cabecera `X-Auth-Token`.
2. **Consulta y filtrado de dispositivos (`GET /api/v1/network-device`):** Obtiene los switches y routers de la topología, filtrando exclusivamente aquellos en estado `Managed` para evitar excepciones por equipos externos o inaccesibles, y extrae `hostname`, `managementIpAddress`, `serialNumber` y `softwareVersion`.
3. **Consulta de hosts (`GET /api/v1/host`):** Lista las terminales conectadas mostrando su dirección IP y dirección MAC.
4. **Visualización estructurada:** Presenta los resultados en consola mediante tablas formateadas con la librería `tabulate`.

### Ejecución
Con el entorno virtual activado y el **Network Controller** habilitado con *Real World Access* en el puerto `58000`:
```bash
python src/import requests-grupo.py
```

---

