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


class ScrapegraphLogger:
    """Class to manage Scrapegraph logging configuration"""

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ScrapegraphLogger, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.logger = logging.getLogger("scrapegraph")
            self.logger.setLevel(logging.INFO)
            self.enabled = False
            self._initialized = True

    def set_logging(
        self,
        level: Optional[str] = None,
        log_file: Optional[str] = None,
        log_format: Optional[str] = None,
    ) -> None:
        """
        Configure logging settings. If level is None, logging will be disabled.

        Args:
            level: Logging level (e.g., 'DEBUG', 'INFO'). None to disable logging.
            log_file: Optional file path to write logs to
            log_format: Optional custom log format string
        """
        # Clear existing handlers
        self.logger.handlers.clear()

        if level is None:
            # Disable logging
            self.enabled = False
            return

        # Enable logging with specified level
        self.enabled = True
        level = getattr(logging, level.upper(), logging.INFO)
        self.logger.setLevel(level)

        # Default format if none provided
        if not log_format:
            log_format = "%(emoji)s %(asctime)-15s %(message)s"

        formatter = EmojiFormatter(log_format)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # File handler if log_file specified
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def disable(self) -> None:
        """Disable all logging"""
        self.logger.handlers.clear()
        self.enabled = False

    def debug(self, message: str) -> None:
        """Log debug message if logging is enabled"""
        if self.enabled:
            self.logger.debug(message)

    def info(self, message: str) -> None:
        """Log info message if logging is enabled"""
        if self.enabled:
            self.logger.info(message)

    def warning(self, message: str) -> None:
        """Log warning message if logging is enabled"""
        if self.enabled:
            self.logger.warning(message)

    def error(self, message: str) -> None:
        """Log error message if logging is enabled"""
        if self.enabled:
            self.logger.error(message)

    def critical(self, message: str) -> None:
        """Log critical message if logging is enabled"""
        if self.enabled:
            self.logger.critical(message)


# Default logger instance
sgai_logger = ScrapegraphLogger()
