import psutil
import time
import logging
import os

CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 80
DISK_THRESHOLD = 80

log_dir = r'C:\Users\91636\Downloads\Assessment2\Logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, 'system_health.log')

logging.basicConfig(filename=log_file,
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def check_system_health():
    cpu_usage = psutil.cpu_percent(interval=1)
    if cpu_usage > CPU_THRESHOLD:
        logging.warning(f"ALERT! CPU usage is high: {cpu_usage}%")
    else:
        logging.info(f"CPU usage: {cpu_usage}%")

    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent
    if memory_usage > MEMORY_THRESHOLD:
        logging.warning(f"ALERT! Memory usage is high: {memory_usage}%")
    else:
        logging.info(f"Memory usage: {memory_usage}%")

    disk_info = psutil.disk_usage('/')
    disk_usage = disk_info.percent
    if (disk_usage > DISK_THRESHOLD):
        logging.warning(f"ALERT! Disk usage is high: {disk_usage}%")
    else:
        logging.info(f"Disk usage: {disk_usage}%")

    process_count = len(psutil.pids())
    logging.info(f"Number of running processes: {process_count}")

while True:
    check_system_health()
    time.sleep(10)
