"""Package logger configuration."""

import logging


def get_logger(name: str = "minipixel") -> logging.Logger:
    """Return a named logger without configuring global logging handlers."""
    return logging.getLogger(name)
