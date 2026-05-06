"""
============================================
Custom Logger Module
============================================
Provides a centralized, color-coded logger with file + console output.
All framework modules use this logger for consistent log formatting.
"""

import os
import logging
from datetime import datetime

import colorlog


# --- Ensure log directory exists ---
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reports", "logs")
os.makedirs(LOG_DIR, exist_ok=True)


def get_logger(name: str, log_level: int = logging.INFO) -> logging.Logger:
    """
    Creates and returns a configured logger instance.

    Features:
        - Color-coded console output for readability
        - File output with timestamps for audit trails
        - Per-session log files with timestamps

    Args:
        name (str): Name of the logger (usually __name__).
        log_level (int): Logging level (default: INFO).

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)

    # Prevent adding duplicate handlers on repeated calls
    if logger.handlers:
        return logger

    logger.setLevel(log_level)
    logger.propagate = False

    # --- Console Handler (Color-coded) ---
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)

    color_formatter = colorlog.ColoredFormatter(
        fmt="%(log_color)s%(asctime)s [%(levelname)-8s] %(name)s: %(message)s%(reset)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )
    console_handler.setFormatter(color_formatter)
    logger.addHandler(console_handler)

    # --- File Handler (Timestamped log file) ---
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(LOG_DIR, f"test_run_{timestamp}.log")

    file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)  # Capture everything in file

    file_formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)-8s] %(name)s | %(funcName)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger
