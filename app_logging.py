import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from constants import ASSETS_DIR


def handle_logging():
    """
    Set up logging configuration with RotatingFileHandler.

    Args:
        None

    Returns:
        None
    """
    # Define the logging format
    log_format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'

    # Define the path to the log file: ASSETS_DIR/Logs/app.log
    log_file = ASSETS_DIR / "Logs" / "app.log"

    try:
        # Ensure the directory for log files exists, create if not
        log_file.parent.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        # If directory creation fails, log the error to a temporary default location
        temp_log_file = Path("./log_dir_error.log")
        logging.basicConfig(filename=temp_log_file,
                            level=logging.ERROR, format=log_format)
        logging.error(f"Error creating log directory: {e}")
        return

    # Calculate the maximum size of each log file (10 MB)
    max_bytes = 10 * 1024 * 1024  # 10 MB

    # Specify the number of backup log files to keep (5)
    backup_count = 5  # Keep up to 5 backup log files

    # Create a RotatingFileHandler instance to handle log rotation
    handler = RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count)

    # Configure the root logger with the specified handler
    logging.basicConfig(level=logging.INFO,
                        format=log_format, handlers=[handler])
