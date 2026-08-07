import psutil
import time
import os
import platform
import logging

# Set up logging configuration
logging.basicConfig(filename='system_monitor.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_system_info():
    system_info = {
        'platform': platform.system(),
        'platform-release': platform.release(),
        'platform-version': platform.version(),
        'architecture': platform.machine(),
        'processor': platform.processor(),
        'ram': str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB"
    }
    return system_info

def get_cpu_info():
    cpu_info = {
        'cpu-count': psutil.cpu_count(logical=False),
        'cpu-physical-count': psutil.cpu_count(logical=True),
        'cpu-frequency': psutil.cpu_freq().current,
        'cpu-usage': psutil.cpu_percent(interval=1)
    }
    return cpu_info

def get_memory_info():
    memory_info = {
        'memory-total': str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB",
        'memory-available': str(round(psutil.virtual_memory().available / (1024.0 ** 3))) + " GB",
        'memory-percent': str(psutil.virtual_memory().percent) + "%",
        'memory-used': str(round(psutil.virtual_memory().used / (1024.0 ** 3))) + " GB"
    }
    return memory_info

def get_disk_info():
    disk_info = {
        'disk-total': str(round(psutil.disk_usage('/').total / (1024.0 ** 3))) + " GB",
        'disk-available': str(round(psutil.disk_usage('/').free / (1024.0 ** 3))) + " GB",
        'disk-percent': str(psutil.disk_usage('/').percent) + "%",
        'disk-used': str(round(psutil.disk_usage('/').used / (1024.0 ** 3))) + " GB"
    }
    return disk_info

def get_network_info():
    network_info = {
        'bytes-sent': str(psutil.net_io_counters().bytes_sent),
        'bytes-received': str(psutil.net_io_counters().bytes_recv),
        'packets-sent': str(psutil.net_io_counters().packets_sent),
        'packets-received': str(psutil.net_io_counters().packets_recv)
    }
    return network_info

def main():
    while True:
        system_info = get_system_info()
        cpu_info = get_cpu_info()
        memory_info = get_memory_info()
        disk_info = get_disk_info()
        network_info = get_network_info()

        logging.info("System Info: " + str(system_info))
        logging.info("CPU Info: " + str(cpu_info))
        logging.info("Memory Info: " + str(memory_info))
        logging.info("Disk Info: " + str(disk_info))
        logging.info("Network Info: " + str(network_info))

        print("System Info: " + str(system_info))
        print("CPU Info: " + str(cpu_info))
        print("Memory Info: " + str(memory_info))
        print("Disk Info: " + str(disk_info))
        print("Network Info: " + str(network_info))

        time.sleep(5)

if __name__ == "__main__":
    main()