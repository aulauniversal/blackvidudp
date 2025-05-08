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
python BlackvidUDP.py
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


