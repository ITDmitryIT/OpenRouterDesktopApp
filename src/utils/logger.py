import logging
from datetime import datetime

def setup_logger():
    logger = logging.getLogger("AIChat")
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        handler = logging.FileHandler("logs/app.log")
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger