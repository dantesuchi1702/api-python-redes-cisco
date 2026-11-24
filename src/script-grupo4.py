import csv
import json
from datetime import datetime
import requests

# Configuración de conexión al Network Controller
BASE_URL = "http://localhost:58000/api/v1"
USERNAME = "cisco"
PASSWORD = "class"


def obtener_ticket():
    """Autentica contra el controlador y devuelve el serviceTicket."""
    url = f"{BASE_URL}/ticket"
    headers = {"Content-Type": "application/json"}
    payload = {"username": USERNAME, "password": PASSWORD}

    resp = requests.post(url, data=json.dumps(payload), headers=headers)
    if resp.status_code in (200, 201):
        return resp.json()["response"]["serviceTicket"]
    raise Exception(f"Error de autenticación ({resp.status_code}): {resp.text}")


def exportar_dispositivos_csv(headers, fecha_ejecucion):
    """Consulta los dispositivos de red, filtra los administrados y los guarda en CSV."""
    resp = requests.get(f"{BASE_URL}/network-device", headers=headers)
    resp.raise_for_status()
    dispositivos = resp.json().get("response", [])

    archivo_csv = "inventario_dispositivos.csv"
    columnas = [
        "Fecha_Relevamiento",
        "Hostname",
        "IP_Administracion",
        "Familia",
        "Modelo",
        "Numero_Serie",
        "Version_IOS",
        "Estado"
    ]

    administrados = 0
    with open(archivo_csv, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(columnas)

        for dev in dispositivos:
            estado = dev.get("collectionStatus", "Desconocido")
            if estado == "Managed":
                administrados += 1
            writer.writerow([
                fecha_ejecucion,
                dev.get("hostname", "Sin nombre"),
                dev.get("managementIpAddress", "N/A"),
                dev.get("family", "N/A"),
                dev.get("platformId", "N/A"),
                dev.get("serialNumber", "N/A"),
                dev.get("softwareVersion", "N/A"),
                estado
            ])

    return archivo_csv, len(dispositivos), administrados


def exportar_hosts_csv(headers, fecha_ejecucion):
    """Consulta los equipos finales (hosts) conectados y los exporta a CSV."""
    resp = requests.get(f"{BASE_URL}/host", headers=headers)
    resp.raise_for_status()
    hosts = resp.json().get("response", [])

    archivo_csv = "inventario_hosts.csv"
    columnas = [
        "Fecha_Relevamiento",
        "IP_Host",
        "Direccion_MAC",
        "Tipo_Conexion",
        "Switch_Conectado",
        "Interfaz_Switch",
        "VLAN"
    ]

    with open(archivo_csv, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(columnas)

        for host in hosts:
            writer.writerow([
                fecha_ejecucion,
                host.get("hostIp", "N/A"),
                host.get("hostMac", "N/A"),
                host.get("hostType", "N/A"),
                host.get("connectedNetworkDeviceIpAddress", "N/A"),
                host.get("connectedInterfaceName", "N/A"),
                host.get("vlanId", "N/A")
            ])

    return archivo_csv, len(hosts)


def main():
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Conectando con el Network Controller...")

    ticket = obtener_ticket()
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": ticket
    }

    arch_dev, total_dev, total_managed = exportar_dispositivos_csv(headers, fecha_actual)
    arch_hosts, total_hosts = exportar_hosts_csv(headers, fecha_actual)

    print("\n=== REPORTE GENERADO CON ÉXITO ===")
    print(f"- Fecha y hora: {fecha_actual}")
    print(f"- Dispositivos exportados en '{arch_dev}': {total_dev} totales ({total_managed} Managed)")
    print(f"- Hosts exportados en '{arch_hosts}': {total_hosts} equipos finales")


if __name__ == "__main__":
    main()

