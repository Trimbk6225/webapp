import logging
from flask import request
from functools import wraps
import os
from dotenv import load_dotenv

load_dotenv()
def setup_logger():
    logger = logging.getLogger('webapp')
    logger.setLevel(logging.DEBUG)
    
    
    stream_handler = logging.StreamHandler()
    stream_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(stream_formatter)
    
   
    log_file = os.getenv("LOG")
    if not log_file:
        log_file = "/var/log/webapp/webapp.log"

   
    file_handler = logging.FileHandler(log_file)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    
    # Add handlers to logger
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    
    return logger

webapp_logger = setup_logger()


def log_request(func):
    """Decorator to log incoming requests and responses."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        
        webapp_logger.info(f"Request: {request.method} {request.url}")
        
        
        response = func(*args, **kwargs)
        
       
        if isinstance(response, tuple):
            status_code = response[1]
        else:
            status_code = response.status_code
            
        if 400 <= status_code < 600:
            webapp_logger.error(f"Response: {status_code} - {request.method} {request.url}")
        else:
            webapp_logger.info(f"Response: {status_code} - {request.method} {request.url}")
        
        return response
    return wrapper