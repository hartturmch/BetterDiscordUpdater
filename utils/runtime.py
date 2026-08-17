import logging
import os
import time
from logging.handlers import RotatingFileHandler

import requests

import config


def configure_logging(silent: bool) -> None:
    """Write every run to a bounded log, optionally keeping console output."""
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    file_handler = RotatingFileHandler(
        config.LOG_PATH,
        maxBytes=config.LOG_MAX_BYTES,
        backupCount=config.LOG_BACKUP_COUNT,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    if not silent:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)


def request_with_retry(method: str, url: str, **kwargs) -> requests.Response:
    """Request with bounded retries so a temporary network failure does not abort BDAI."""
    logger = logging.getLogger(__name__)
    attempts = max(1, config.NETWORK_RETRY_ATTEMPTS)
    kwargs.setdefault("timeout", config.NETWORK_TIMEOUT_SECONDS)

    for attempt in range(1, attempts + 1):
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as error:
            if attempt == attempts:
                raise
            logger.warning(
                "Network request failed (%s/%s): %s. Retrying in %ss.",
                attempt,
                attempts,
                error,
                config.NETWORK_RETRY_DELAY_SECONDS
            )
            time.sleep(config.NETWORK_RETRY_DELAY_SECONDS)
