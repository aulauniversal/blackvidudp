# BlackvidUDP - UDP DDoS Attack Tool

## Project Description

BlackvidUDP is an advanced tool for performing Distributed Denial of Service (DDoS) attacks over the UDP protocol.

It allows launching large volumes of traffic to IPs or domains, using port rotation, random packets, or complex patterns to evade basic protections.

Includes:

* Automatic detection of active devices on the internal network (ARP scanning).
* Basic IP spoofing to simulate multiple attackers.
* Real-time attack monitoring (CPU, memory, bandwidth, packets).
* Dynamic attack control (pause/resume/stop).
* Automatic thread adjustment based on CPU usage.
* Logging results to an `attack_summary.log` file.

---

## Requirements

Before using BlackvidUDP, install the dependencies by running:

```
pip install -r requirements.txt
```

**Required dependencies:**

* psutil
* colorama
* netifaces
* scapy
* ifaddr
* matplotlib (optional for graphical monitoring)

---

## Instructions for Use

1. Clone the repository:

```
git clone https://github.com/aulauniversal/blackvidudp.git
cd blackvidudp
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Run the script:

```
sudo python BlackvidUDP.py
```

4. Execution flow:

* Scan the local network or manually enter an IP/Domain.
* Configure:

* Destination ports (can be randomly rotated).
* Packet size.
* Number of sends.
* Timeout between packets.
* Number of threads.
* During the attack:

* Press `p` to pause or resume.
* Press `s` to stop.

5. Upon completion:

* The `attack_summary.log` file is generated with all statistics.

---

## Feature Highlights

* Local network scan (ARP scan).
* Mass UDP attack.
* Random IP spoofing.
* Port rotation.
* Real-time monitoring.
* Automatic thread tuning.
* Detailed logging.
* (Optional) Graphical CPU and network monitoring.

---

## Legal Disclaimer

> This project is for educational purposes and testing in controlled environments. >
> Using this tool against systems without prior authorization is illegal and may result in severe criminal and civil penalties.
>
> The author is not responsible for any misuse of this tool.
# BlackvidUDP - UDP DDoS Attack Tool

## Descripción del Proyecto

BlackvidUDP es una herramienta avanzada para realizar ataques de Denegación de Servicio Distribuidos (DDoS) sobre el protocolo UDP.

Permite lanzar grandes volúmenes de tráfico hacia IPs o dominios, usando rotación de puertos, paquetes aleatorios o patrones complejos para evadir algunas protecciones básicas.

Incluye:

* Detección automática de dispositivos activos en la red interna (escaneo ARP).
* Spoofing básico de IP para simular múltiples atacantes.
* Monitoreo en tiempo real del ataque (CPU, memoria, ancho de banda, paquetes).
* Control dinámico del ataque (pausar/reanudar/detener).
* Ajuste automático de hilos basado en el uso de CPU.
* Registro de resultados en un archivo `attack_summary.log`.

---

## Requisitos

Antes de usar BlackvidUDP, instala las dependencias ejecutando:

```
pip install -r requirements.txt
```

**Dependencias necesarias:**

* psutil
* colorama
* netifaces
* scapy
* ifaddr
* matplotlib (opcional para monitoreo gráfico)

---

## Instrucciones de Uso

1. Clonar el repositorio:

```
git clone https://github.com/aulauniversal/blackvidudp.git
cd blackvidudp
```

2. Instalar dependencias:

```
pip install -r requirements.txt
```

3. Ejecutar el script:

```
sudo python BlackvidUDP.py
```

4. Flujo de ejecución:

* Escanear la red local o introducir manualmente una IP/Dominio.
* Configurar:

  * Puertos de destino (se pueden rotar aleatoriamente).
  * Tamaño de paquetes.
  * Cantidad de envíos.
  * Tiempo de espera entre paquetes.
  * Número de hilos.
* Durante el ataque:

  * Presiona `p` para pausar o reanudar.
  * Presiona `s` para detener.

5. Al finalizar:

* Se genera el archivo `attack_summary.log` con todas las estadísticas.

---

## Funcionalidades destacadas

* Escaneo de red local (ARP Scan).
* Ataque UDP masivo.
* IP Spoofing aleatorio.
* Rotación de puertos.
* Control en tiempo real.
* Ajuste automático de hilos.
* Logging detallado.
* (Opcional) Monitoreo gráfico de CPU y red.

---

## Advertencia Legal

> Este proyecto tiene fines educativos y de pruebas en entornos controlados.
>
> El uso de esta herramienta contra sistemas sin autorización previa es ilegal y puede conllevar sanciones penales y civiles graves.
>
> El autor no se hace responsable del mal uso de esta herramienta.

---


