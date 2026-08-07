import speedtest
import time
import logging
import os
import platform
import psutil
import socket
import netifaces as ni

# Set up logging
logging.basicConfig(filename='speedtest.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_network_info():
    # Get network interface information
    net_info = {}
    for interface in ni.interfaces():
        try:
            ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
            net_info[interface] = ip
        except (KeyError, IndexError):
            pass
    return net_info

def get_system_info():
    # Get system information
    system_info = {}
    system_info['platform'] = platform.system()
    system_info['platform_release'] = platform.release()
    system_info['platform_version'] = platform.version()
    system_info['architecture'] = platform.machine()
    system_info['processor'] = platform.processor()
    return system_info

def get_memory_info():
    # Get memory information
    memory_info = {}
    memory_info['virtual_memory'] = psutil.virtual_memory()
    memory_info['swap_memory'] = psutil.swap_memory()
    return memory_info

def get_disk_info():
    # Get disk information
    disk_info = {}
    for disk in psutil.disk_partitions():
        disk_info[disk.mountpoint] = psutil.disk_usage(disk.mountpoint)
    return disk_info

def get_network_speed():
    # Get network speed
    s = speedtest.Speedtest()
    s.get_servers()
    s.get_best_server()
    download_speed = s.download() / (1024 * 1024)  # Convert to MB/s
    upload_speed = s.upload() / (1024 * 1024)  # Convert to MB/s
    ping = s.results.ping
    return download_speed, upload_speed, ping

def main():
    # Get network information
    net_info = get_network_info()
    logging.info('Network Information:')
    for interface, ip in net_info.items():
        logging.info(f'Interface: {interface}, IP: {ip}')

    # Get system information
    system_info = get_system_info()
    logging.info('\nSystem Information:')
    for key, value in system_info.items():
        logging.info(f'{key}: {value}')

    # Get memory information
    memory_info = get_memory_info()
    logging.info('\nMemory Information:')
    for key, value in memory_info['virtual_memory'].items():
        logging.info(f'{key}: {value}%')
    for key, value in memory_info['swap_memory'].items():
        logging.info(f'{key}: {value}%')

    # Get disk information
    disk_info = get_disk_info()
    logging.info('\nDisk Information:')
    for mountpoint, usage in disk_info.items():
        logging.info(f'Mountpoint: {mountpoint}')
        logging.info(f'Total: {usage.total / (1024 * 1024 * 1024)} GB')
        logging.info(f'Used: {usage.used / (1024 * 1024 * 1024)} GB')
        logging.info(f'Free: {usage.free / (1024 * 1024 * 1024)} GB')
        logging.info(f'Percentage: {usage.percent}%')

    # Get network speed
    download_speed, upload_speed, ping = get_network_speed()
    logging.info('\nNetwork Speed:')
    logging.info(f'Download Speed: {download_speed} MB/s')
    logging.info(f'Upload Speed: {upload_speed} MB/s')
    logging.info(f'Ping: {ping} ms')

if __name__ == '__main__':
    main()
    time.sleep(10)  # Wait for 10 seconds before exiting
    os._exit(0)