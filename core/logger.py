import logging
import os
from logging.handlers import RotatingFileHandler

class Logger:
    def __init__(self, name: str = 'app', log_file: str = 'logs/app.log', level=logging.DEBUG):
        """
        Initializes a logger instance with console and file handlers.
        
        :param name: Name of the logger
        :param log_file: Path to the log file
        :param level: Log level (default is DEBUG)
        """
        # Ensure the log directory exists
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        # Create the logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Define formatter
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # File handler with rotation (max 5MB per file)
        file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=5)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Prevent log duplication
        self.logger.propagate = False

    def get_logger(self):
        """
        Returns the logger instance.
        """
        return self.logger

# Default logger setup
logger = Logger().get_logger()
