#Logging in Python is a built-in way to record (log) messages from your code — useful for debugging, tracking errors, or understanding how your program runs over time.
import logging
import os
from datetime import datetime
from from_root import from_root

# Create a timestamped log file name
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Create the full path for the logs directory inside project root
log_dir = os.path.join(from_root(), "logs")
os.makedirs(log_dir, exist_ok=True)  # ✅ create logs folder inside project

# Full log file path
logs_path = os.path.join(log_dir, LOG_FILE)

# Configure logging
logging.basicConfig(
    filename=logs_path,
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)

logging.info("Logger initialized successfully.")
