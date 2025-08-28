# Logging is essential for monitoring, debugging, and tracking the execution of code.

import logging
import os
import sys
from datetime import datetime

LOGS_DIR = "logs"
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

logs_path = os.path.join(os.getcwd(), LOGS_DIR, LOG_FILE)
os.makedirs(logs_path, exist_ok = True)

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

logging.basicConfig(
    filename = LOG_FILE_PATH,
    format = "[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s", 
    level = logging.INFO
)

if __name__ == "__main__":
    logging.info("Logger initialized successfully.")