📝 BlackvidUDP - UDP DDoS Attack Tool
📜 Descripción del Proyecto

BlackvidUDP es una herramienta avanzada para realizar ataques de Denegación de Servicio Distribuidos (DDoS) sobre el protocolo UDP.
Permite lanzar grandes volúmenes de tráfico hacia IPs o dominios, usando rotación de puertos, paquetes aleatorios o patrones complejos para evadir algunas protecciones básicas.

Incluye:

    Detección automática de dispositivos activos en la red interna (escaneo ARP).

    Spoofing básico de IP para simular múltiples atacantes.

    Monitoreo en tiempo real del ataque (CPU, memoria, ancho de banda, paquetes).

    Control dinámico del ataque (pausar/reanudar/detener).

    Ajuste automático de hilos basados en el uso de CPU.

    Registro de resultados en un archivo attack_summary.log.

⚙️ Requisitos

Antes de usar BlackvidUDP, asegúrate de tener instalado:

pip install -r requirements.txt

Dependencias necesarias:

    psutil

    colorama

    netifaces

    scapy

    ifaddr

    (opcional para gráficos) matplotlib
   🚀 Instrucciones de uso

    Clonar el repositorio:

git clone https://github.com/tu_usuario/blackvidudp.git
cd blackvidudp

    Instalar dependencias:

pip install -r requirements.txt

    Ejecutar el script:

python BlackvidUDP.py

    Flujo de ejecución:

        Al iniciar, el sistema te preguntará si deseas escanear la red local.

        Si no quieres escanear, puedes:

            Introducir un objetivo manualmente (IP/Dominio).

            Cargar una lista de objetivos desde un archivo de texto.

        Luego configurará:

            Puertos para atacar (rotando aleatoriamente).

            Tamaño de paquetes.

            Cantidad de envíos.

            Delay entre envíos (segundos).

            Número de hilos (ajustable en función del rendimiento de tu máquina).

        Durante el ataque:

            Presiona p para pausar/reanudar.

            Presiona s para detener el ataque completamente.

    Resumen y estadísticas:

        Al finalizar, se genera automáticamente un archivo attack_summary.log con:

            IPs atacadas exitosamente.

            IPs con errores.

            Total de paquetes enviados y fallidos.

            Ancho de banda utilizado.

            Puertos usados y rotados.

📈 Funcionalidades destacadas

    Escaneo de Red Local (ARP Scan)

    Detección de IPs activas

    Ataque UDP masivo

    IP Spoofing aleatorio

    Rotación de puertos en ataque

    Control del ataque en tiempo real

    Ajuste automático de hilos basado en CPU

    Sistema de logging

    (Opcional) Monitorización gráfica en tiempo real

⚠️ Advertencia Legal

    Este proyecto tiene fines educativos y de pruebas en entornos controlados.
    El uso de esta herramienta contra sistemas sin autorización previa es ilegal y puede conllevar sanciones penales y civiles graves.
    El autor no se hace responsable del mal uso de esta herramienta. 
