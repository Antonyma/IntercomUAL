import requests
import socket

def get_external_ip_and_port():
    try:
        response = requests.get('https://httpbin.org/ip')
        data = response.json()
        external_ip = data['origin']
        external_port = None  # No se puede determinar el puerto externo de esta manera.
        return external_ip, external_port
    except Exception as e:
        return None, None

if __name__ == "__main__":
    external_ip, external_port = get_external_ip_and_port()

    if external_ip:
        print(f"External IP: {external_ip}")
    else:
        print("Unable to determine external IP.")

def get_external_ip_and_port():
    try:
        external_ip = socket.gethostbyname(socket.gethostname())
        external_port = 4444  # Este es el puerto que configuraste en el reenvío de puertos.
        return external_ip, external_port
    except Exception as e:
        return None, None

if __name__ == "__main__":
    external_ip, external_port = get_external_ip_and_port()

    if external_ip and external_port:
        print(f"External IP: {external_ip}")
        print(f"External Port: {external_port}")
    else:
        print("Unable to determine external IP and port.")