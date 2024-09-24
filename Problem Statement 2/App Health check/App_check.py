import requests
import time
import logging
import os

app_url = ""
CHECK_INTERVAL = 10
RETRY_COUNT = 3
RETRY_DELAY = 2

log_dir = r'C:\Users\91636\Downloads\Assessment2\App Health check\Logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, 'app_health.log')
logging.basicConfig(filename=log_file, 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def check_application_health():
    retry_attempts = 0
    while retry_attempts < RETRY_COUNT:
        try:
            start_time = time.time()
            response = requests.get(app_url, timeout=5)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                logging.info(f"Application is UP. Status code: {response.status_code}, Response time: {response_time:.2f} seconds")
                print(f"Application is UP. Status code: {response.status_code}, Response time: {response_time:.2f} seconds")
            else:
                logging.warning(f"Application is DOWN. Status code: {response.status_code}")
                print(f"Application is DOWN. Status code: {response.status_code}")
            break
        except requests.exceptions.RequestException as e:
            logging.error(f"ERROR! Application is DOWN. Error: {e}. Retrying... ({retry_attempts + 1}/{RETRY_COUNT})")
            print(f"ERROR! Application is DOWN. Error: {e}. Retrying... ({retry_attempts + 1}/{RETRY_COUNT})")
            retry_attempts += 1
            time.sleep(RETRY_DELAY)
    if retry_attempts == RETRY_COUNT:
        logging.error(f"Application is DOWN after {RETRY_COUNT} retries.")
        print(f"Application is DOWN after {RETRY_COUNT} retries.")

while True:
    check_application_health()
    time.sleep(CHECK_INTERVAL)
