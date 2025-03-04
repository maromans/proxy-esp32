# ESP32 D-STAR Proxy para Icom IC-705

Este proyecto permite a un ESP32, programado en MicroPython, actuar como un proxy de paquetes UDP para el Icom IC-705, redirigiendo las conexiones D-STAR a distintos reflectores en función de la selección realizada en el display del IC-705.

## 📌 Características
- **Captura paquetes UDP** enviados por el Icom IC-705 en la red WiFi.
- **Modifica los destinos** de los paquetes para redirigirlos a diferentes reflectores D-STAR.
- **Tabla de redirección configurable**, basada en nombres de reflectores.
- **Resolución DNS integrada** para obtener direcciones IP de los reflectores.
- **Conexión WiFi con IP fija**, asegurando estabilidad en la comunicación.

## 🎯 Objetivo
El ESP32 actúa como un puente inteligente entre el IC-705 y la red D-STAR, permitiendo cambiar de reflector dinámicamente sin necesidad de modificar la configuración de red del radio. Captura los paquetes enviados por el IC-705 y los redirige al reflector adecuado según una tabla de mapeo predefinida.

## ⚙️ Funcionamiento
1. El ESP32 se conecta a la red WiFi con una IP fija.
2. Escucha en el puerto UDP 20001, donde el IC-705 envía sus paquetes D-STAR.
3. Intercepta los paquetes y analiza si contienen la identificación de un reflector conocido.
4. Si el reflector está en la tabla de redirección, resuelve su IP y reenvía el paquete al destino correcto.
5. Si no se encuentra una coincidencia, el paquete no es reenviado.

## 🛠️ Configuración y Uso
1. **Configurar los parámetros WiFi** en el código fuente:
   ```python
   WIFI_SSID = "TuRedWiFi"
   WIFI_PASSWORD = "TuContraseña"
   ESP32_IP = "192.168.0.110"
   ```
2. **Definir la tabla de redirección de reflectores** en el código:
   ```python
   reflector_map = {
       b"XLX015S": "server5.dstar.es",
       b"REF030C": "ref030.dns.net",
   }
   ```
3. **Subir el código al ESP32** usando MicroPython.
4. **Encender el IC-705** y conectarlo a la misma red WiFi.
5. **El ESP32 capturará y reenviará los paquetes automáticamente.**

## 🚀 Mejoras Futuras
- Captura bidireccional de paquetes para permitir respuestas desde los reflectores.
- Interfaz web o serie para modificar la tabla de redirección dinámicamente.
- Soporte para más protocolos relacionados con D-STAR.

## 📝 Notas
Este proyecto está en desarrollo, y pueden requerirse ajustes dependiendo de la red y la configuración del IC-705.

