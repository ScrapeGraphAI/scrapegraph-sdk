import logging
import logging.handlers
from typing import Dict, Optional

# Emoji mappings for different log levels
LOG_EMOJIS: Dict[int, str] = {
    logging.DEBUG: "🐛",
    logging.INFO: "💬",
    logging.WARNING: "⚠️",
    logging.ERROR: "❌",
    logging.CRITICAL: "🚨",
}


class EmojiFormatter(logging.Formatter):
    """Custom formatter that adds emojis to log messages"""

    def format(self, record: logging.LogRecord) -> str:
        # Add emoji based on log level
        emoji = LOG_EMOJIS.get(record.levelno, "")
        record.emoji = emoji
        return super().format(record)


def get_logger(
    name: str = "scrapegraph",
    level: str = "INFO",
    log_file: Optional[str] = None,
    log_format: Optional[str] = None,
) -> logging.Logger:
    """
    Get a configured logger instance with emoji support.

    Args:
        name: Name of the logger (default: 'scrapegraph')
        level: Logging level (default: 'INFO')
        log_file: Optional file path to write logs to
        log_format: Optional custom log format string

    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)

    # Return existing logger if already configured
    if logger.handlers:
        return logger

    # Set log level
    level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(level)

    # Default format if none provided
    if not log_format:
        log_format = "%(levelname)-6s %(asctime)-15s %(message)s"

    formatter = EmojiFormatter(log_format)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler if log_file specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


# Default sgai logger instance
sgai_logger = get_logger()
