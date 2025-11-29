"""
Logging configuration for AccessibleAI project.
Sets up structured logging with both file and console output.
"""
import logging
import sys
from pathlib import Path


def setup_logging(log_level="INFO"):
    """
    Configure logging for the entire project.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Logger instance
    """
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Configure logging format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'

    # Set up handlers
    handlers = [
        # File handler - saves to logs/accessible_ai.log
        logging.FileHandler(log_dir / 'accessible_ai.log', mode='a'),
        # Console handler - prints to stdout
        logging.StreamHandler(sys.stdout)
    ]

    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        datefmt=date_format,
        handlers=handlers
    )

    # Create and return logger
    logger = logging.getLogger(__name__)
    logger.info("=" * 60)
    logger.info("AccessibleAI Logging System Initialized")
    logger.info(f"Log level: {log_level}")
    logger.info("=" * 60)

    return logger


# Create global logger instance
logger = setup_logging()
