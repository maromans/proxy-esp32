import network
import socket

# ===== CONFIGURACIÓN DE LA RED Wi-Fi ===== la misma red a la que se conecta el icom 705
WIFI_SSID = ""         # Cambia esto con el nombre de tu red Wi-Fi
WIFI_PASSWORD = "" # Cambia esto con tu contraseña Wi-Fi

# Configuración de IP fija del ESP32
ESP32_IP = "192.168.0.110"
GATEWAY = "192.168.0.1"
SUBNET_MASK = "255.255.255.0"
DNS_SERVER = "8.8.8.8"  # Se corrigió el error levanta por google dns

def configurar_wifi():
    """ Configura el ESP32 con una IP fija y lo conecta a Wi-Fi """
    wlan = network.WLAN(network.STA_IF)  # Modo estación (cliente Wi-Fi)
    wlan.active(True)  # Activa la interfaz Wi-Fi

    # Asigna la IP fija antes de conectarse
    wlan.ifconfig((ESP32_IP, SUBNET_MASK, GATEWAY, DNS_SERVER))  

    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    # Espera hasta que se conecte
    while not wlan.isconnected():
        pass  # Esperar conexión

    print("✅ Conectado a Wi-Fi. IP:", wlan.ifconfig())

# ===== TABLA DE REDIRECCIÓN DE REFLECTORES =====
reflector_map = {
    b"XLX015S": "server5.dstar.es",
    b"REF030C": "ref030.dns.net",
}

def get_redirected_ip(request_data):
    """
    Busca en los datos recibidos si hay un reflector en la tabla de redirección.
    Si lo encuentra, devuelve la dirección IP correspondiente.
    """
    for key in reflector_map:
        if key in request_data:
            try:
                # Resolver el nombre de dominio a una IP
                addr_info = socket.getaddrinfo(reflector_map[key], 20001, socket.AF_INET, socket.SOCK_DGRAM)
                ip_address = addr_info[0][4][0]  # Extraer la IP de la primera tupla
                print(f"🌐 {reflector_map[key]} resuelto a {ip_address}")
                return ip_address
            except:
                print(f"⚠️ No se pudo resolver {reflector_map[key]}")
                return None
    return None  # No se encontró en la tabla

# ===== SERVIDOR PROXY UDP =====
def udp_proxy():
    """
    Captura los paquetes UDP enviados por el IC-705 y los redirige al reflector correcto.
    """
    listen_port = 20001  # Puerto en el que escucha el IC-705 para D-STAR
    buffer_size = 1024   # Tamaño máximo del paquete

    # Crear socket UDP para recibir datos del IC-705
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", listen_port))  # Escucha en todas las interfaces de red

    print(f"🎧 ESP32 escuchando en {ESP32_IP}:{listen_port}")

    while True:
        data, addr = sock.recvfrom(buffer_size)  # Recibe datos del IC-705
        print(f"📡 Solicitud recibida desde {addr}: {data}")

        # Buscar la IP del reflector en la solicitud
        new_ip = get_redirected_ip(data)

        if new_ip:
            print(f"🔀 Redirigiendo tráfico a {new_ip}")

            try:
                # Reenviar el paquete al nuevo destino
                forward_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                forward_sock.sendto(data, (new_ip, 20001))
                forward_sock.close()
                print(f"✅ Paquete enviado a {new_ip}")
            except:
                print(f"⚠️ Error enviando paquete a {new_ip}")
        else:
            print("⚠️ Reflector no encontrado o no resolvió IP.")

# ===== INICIAR EL PROGRAMA =====
configurar_wifi()  # Conectar a Wi-Fi con IP fija
udp_proxy()        # Iniciar el proxy UDP
