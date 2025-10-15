"""
Logging utilities for the ScrapeGraphAI SDK.

This module provides a custom logging system with emoji support and
configurable output for debugging and monitoring SDK operations.

The logger can be enabled/disabled dynamically and supports both
console and file output with customizable formatting.

Example:
    Enable logging:
        >>> from scrapegraph_py.logger import sgai_logger
        >>> sgai_logger.set_logging(level="DEBUG", log_file="scraping.log")

    Disable logging:
        >>> sgai_logger.disable()
"""
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
    """
    Custom log formatter that adds emojis to log messages.

    This formatter enhances log messages by prepending relevant emojis
    based on the log level, making logs more visually distinctive.

    The emoji is added to the log record before formatting.
    """

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record with an emoji prefix.

        Args:
            record: The log record to format

        Returns:
            Formatted log string with emoji prefix
        """
        # Add emoji based on log level
        emoji = LOG_EMOJIS.get(record.levelno, "")
        record.emoji = emoji
        return super().format(record)


class ScrapegraphLogger:
    """
    Singleton logger manager for the ScrapeGraphAI SDK.

    This class manages SDK-wide logging configuration, providing methods
    to enable, disable, and configure logging behavior. It implements the
    singleton pattern to ensure consistent logging across the SDK.

    Attributes:
        logger (logging.Logger): The underlying Python logger instance
        enabled (bool): Whether logging is currently enabled

    Example:
        >>> logger = ScrapegraphLogger()
        >>> logger.set_logging(level="INFO", log_file="api.log")
        >>> logger.info("Starting API request")
    """

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
        """
        Disable all logging.

        Clears all handlers and sets enabled flag to False, effectively
        silencing all log output from the SDK.
        """
        self.logger.handlers.clear()
        self.enabled = False

    def debug(self, message: str) -> None:
        """
        Log debug message if logging is enabled.

        Args:
            message: The debug message to log
        """
        if self.enabled:
            self.logger.debug(message)

    def info(self, message: str) -> None:
        """
        Log info message if logging is enabled.

        Args:
            message: The info message to log
        """
        if self.enabled:
            self.logger.info(message)

    def warning(self, message: str) -> None:
        """
        Log warning message if logging is enabled.

        Args:
            message: The warning message to log
        """
        if self.enabled:
            self.logger.warning(message)

    def error(self, message: str) -> None:
        """
        Log error message if logging is enabled.

        Args:
            message: The error message to log
        """
        if self.enabled:
            self.logger.error(message)

    def critical(self, message: str) -> None:
        """
        Log critical message if logging is enabled.

        Args:
            message: The critical message to log
        """
        if self.enabled:
            self.logger.critical(message)


# Default logger instance
sgai_logger = ScrapegraphLogger()
