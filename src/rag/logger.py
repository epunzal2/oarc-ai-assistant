import logging
import os
from logging.handlers import RotatingFileHandler

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure logging
log_file = "logs/app.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler(log_file, maxBytes=10485760, backupCount=5), # 10MB per file, 5 backup files
        logging.StreamHandler() # Also print to console
    ]
)

def get_logger(name):
    """
    Returns a logger with the specified name.
    """
    return logging.getLogger(name)