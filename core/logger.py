import logging
import os
from logging.handlers import RotatingFileHandler

class Logger:
    _logger_instance = None

    def __init__(self, name: str = 'app', log_file: str = 'logs/app.log', level=logging.DEBUG):
        """
        Initializes a logger instance with console and file handlers, with UTF-8 encoding.
        """
        # If logger already exists and has handlers, skip reinitialization
        existing_logger = logging.getLogger(name)
        if existing_logger.handlers:
            self.logger = existing_logger
            return

        # Ensure the log directory exists
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        self.logger = existing_logger
        self.logger.setLevel(level)

        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Console handler with UTF-8 encoding
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # File handler with rotation and UTF-8 encoding (max 5MB per file)
        file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=5, encoding='utf-8')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Prevent propagation to root logger
        self.logger.propagate = False

        Logger._logger_instance = self.logger

    @staticmethod
    def get_logger():
        """
        Returns a reusable logger instance.
        """
        if Logger._logger_instance is None:
            Logger()  # This sets _logger_instance
        return Logger._logger_instance

# Default logger setup
logger = Logger.get_logger()
