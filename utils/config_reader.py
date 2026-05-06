"""
============================================
Configuration Reader Module
============================================
Reads and provides access to config.yaml settings.
Implements singleton pattern to avoid repeated file reads.
"""

import os
import yaml
from utils.logger import get_logger

logger = get_logger(__name__)

# --- Path to config file ---
CONFIG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "config",
    "config.yaml",
)

# --- Singleton cache ---
_config_cache = None


def load_config(config_path: str = None) -> dict:
    """
    Loads and caches the YAML configuration file.

    Args:
        config_path (str, optional): Custom path to config file.

    Returns:
        dict: Parsed configuration dictionary.
    """
    global _config_cache

    if _config_cache is not None:
        return _config_cache

    path = config_path or CONFIG_PATH

    if not os.path.exists(path):
        logger.error(f"Configuration file not found: {path}")
        raise FileNotFoundError(f"Configuration file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        _config_cache = yaml.safe_load(f)
        logger.info(f"Configuration loaded from: {path}")

    return _config_cache


def get_config_value(section: str, key: str, default=None):
    """
    Retrieves a specific configuration value.

    Args:
        section (str): Top-level config section (e.g., 'app', 'browser').
        key (str): Key within the section.
        default: Default value if key is not found.

    Returns:
        The configuration value or the default.
    """
    config = load_config()
    try:
        value = config[section][key]
        return value
    except KeyError:
        logger.warning(f"Config key '{section}.{key}' not found, using default: {default}")
        return default


def get_browser_config() -> dict:
    """Returns the browser configuration section."""
    return load_config().get("browser", {})


def get_api_config() -> dict:
    """Returns the API configuration section."""
    return load_config().get("api", {})


def get_app_config() -> dict:
    """Returns the application URL configuration section."""
    return load_config().get("app", {})


def get_test_user() -> dict:
    """Returns the test user credentials."""
    return load_config().get("test_user", {})
