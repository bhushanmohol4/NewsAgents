import logging
import os
from datetime import datetime
import streamlit as st

class Logger:
    def __init__(self):
        # Create Logs directory if it doesn't exist
        self.logs_dir = "Logging/Logs"
        os.makedirs(self.logs_dir, exist_ok=True)
        
        # Set up the logger
        self.logger = logging.getLogger('PodcastCreator')
        self.logger.setLevel(logging.INFO)
        
        # Create a file handler for today's log
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = os.path.join(self.logs_dir, f'{today}.log')
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create formatters and add them to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add the handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message):
        self.logger.info(message)
    
    def error(self, message):
        self.logger.error(message)
    
    def warning(self, message):
        self.logger.warning(message)
    
    def debug(self, message):
        self.logger.debug(message)

# Create a singleton instance
logger = Logger()