import requests
import json

# 1. Configuración de conexión
BASE_URL = "http://localhost:58000/api/v1"

USERNAME = "cisco"
PASSWORD = "class"

# 2. Obtener el Ticket de Autenticación (POST /ticket)
auth_url = f"{BASE_URL}/ticket"
auth_payload = {
    "username": USERNAME,
    "password": PASSWORD
}
headers = {
    "Content-Type": "application/json"
}

response = requests.post(auth_url, data=json.dumps(auth_payload), headers=headers)

if response.status_code in (200,201):
    ticket = response.json()["response"]["serviceTicket"]
    print(f"Autenticación exitosa. Ticket obtenido: {ticket}\n")
    
    # Agregamos el token a las cabeceras para las siguientes consultas
    headers["X-Auth-Token"] = ticket

    # 3. Consultar los dispositivos de red descubiertos (GET /network-device)
    devices_url = f"{BASE_URL}/network-device"
    dev_response = requests.get(devices_url, headers=headers)
    
    if dev_response.status_code == 200:
        devices = dev_response.json()["response"]
        print("=== DISPOSITIVOS DE RED ===")
        for dev in devices:
            hostname = dev.get("hostname", "Sin nombre")
            ip = dev.get("managementIpAddress", "Sin IP")
            status = dev.get("collectionStatus", "Desconocido")
            print(f"- {hostname} | IP: {ip} | Estado: {status}")
    else:
        print(f"Error al consultar dispositivos: {dev_response.status_code}")

    # 4. Consultar los hosts conectados (GET /host)
    hosts_url = f"{BASE_URL}/host"
    host_response = requests.get(hosts_url, headers=headers)
    
    if host_response.status_code == 200:
        hosts = host_response.json()["response"]
        print("\n=== HOSTS DETECTADOS ===")
        for host in hosts:
            ip = host.get("hostIp", "Sin IP")
            mac = host.get("hostMac", "Sin MAC")
            print(f"- IP: {ip} | MAC: {mac}")
else:
    print(f"Error de autenticación ({response.status_code}): {response.text}")
