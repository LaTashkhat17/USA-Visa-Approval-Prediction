import logging
import os
from datetime import datetime
from from_root import from_root

# Create logs directory dynamically
LOG_DIR = os.path.join(from_root(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Create timestamped log file
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE)

# Create UTF-8 safe file handler manually
file_handler = logging.FileHandler(LOG_FILE_PATH, mode='a', encoding='utf-8')

# Configure basic logging (no unsupported args)
logging.basicConfig(
    level=logging.INFO,
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    handlers=[file_handler, logging.StreamHandler()]  # both file + console
)

logging.info(f"Logging setup complete. Log file: {LOG_FILE_PATH}")
