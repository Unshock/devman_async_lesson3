import logging

from archive_downloader.settings import LOG_LEVEL, LOG_SHOW_STATE

LOG_LEVEL_MAP = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}


def setup_logger():
    logger = logging.getLogger('archive_downloader')

    if not LOG_SHOW_STATE:
        logger.setLevel(logging.CRITICAL + 1)
        return logger

    if not logger.handlers:
        log_level = LOG_LEVEL_MAP.get(LOG_LEVEL.lower(), logging.INFO)
        logger.setLevel(log_level)

        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
    return logger
