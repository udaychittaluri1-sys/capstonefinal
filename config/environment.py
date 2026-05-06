"""
============================================
Environment Configuration Module
============================================
Handles environment-specific settings (dev, staging, prod).
Allows dynamic switching between environments via CLI or env vars.
"""

import os
from enum import Enum


class Environment(Enum):
    """Supported test environments."""
    DEV = "dev"
    STAGING = "staging"
    PRODUCTION = "production"


# --- Environment-specific URL mappings ---
ENV_CONFIG = {
    Environment.DEV: {
        "base_url": "https://practice.expandtesting.com/notes/app",
        "api_base_url": "https://practice.expandtesting.com/notes/api",
    },
    Environment.STAGING: {
        "base_url": "https://practice.expandtesting.com/notes/app",
        "api_base_url": "https://practice.expandtesting.com/notes/api",
    },
    Environment.PRODUCTION: {
        "base_url": "https://practice.expandtesting.com/notes/app",
        "api_base_url": "https://practice.expandtesting.com/notes/api",
    },
}


def get_environment() -> Environment:
    """
    Determines the current test environment.
    Priority: CLI arg > Environment variable > Default (DEV).

    Returns:
        Environment: The active environment enum value.
    """
    env_name = os.getenv("TEST_ENV", "dev").lower()
    try:
        return Environment(env_name)
    except ValueError:
        print(f"[WARNING] Unknown environment '{env_name}', defaulting to DEV")
        return Environment.DEV


def get_env_config() -> dict:
    """
    Returns the configuration dictionary for the active environment.

    Returns:
        dict: URL and settings for the current environment.
    """
    env = get_environment()
    return ENV_CONFIG[env]
