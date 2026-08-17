import os
import sys
import logging
import subprocess

import requests

import config
import utils

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="(%(asctime)s) %(message)s")


def is_version_greater(first_version: str, second_version: str) -> bool:
    first = first_version.split(".")
    second = second_version.split(".")

    try:
        first = list(map(lambda i: int(i), first))
        second = list(map(lambda i: int(i), second))
    except ValueError:
        print("One of the versions does not match the n.n.n-like version template")
        return False

    if len(first) > len(second):
        second += [0] * (len(first) - len(second))
    elif len(second) > len(first):
        first += [0] * (len(second) - len(first))

    for first_version_number, second_version_number in zip(first, second):
        if first_version_number > second_version_number:
            return True
        elif second_version_number > first_version_number:
            return False
    return False


def check_for_bdai_updates() -> bool:
    """Checks for updates and return True if there is an available update, False otherwise"""

    try:
        latest_release_url = utils.request_with_retry("HEAD", config.BDAI_LATEST_RELEASE_PAGE_URL, allow_redirects=True)
        latest_available_version = latest_release_url.url.split("/")[-1].lstrip("v")
    except requests.RequestException as error:
        logger.error("Could not check BetterDiscordAutoInstaller version: %s", error)
        return False

    if is_version_greater(latest_available_version, config.BDAI_SCRIPT_VERSION):
        logger.info(f"A new version available ({config.BDAI_SCRIPT_VERSION} -> {latest_available_version}).")

        if config.DISABLE_BDAI_AUTOUPDATE:
            logger.info(f"To update, go to {config.BDAI_LATEST_RELEASE_PAGE_URL}\n")
        return True
    else:
        logger.info("BetterDiscordAutoInstaller is up to date.\n")
        return False


def run_updater():
    logger.info("Running updater...")
    startup_args = ["--startup"] if "--startup" in sys.argv else []

    if getattr(sys, "frozen", False):
        updater_run_command = ["updater.exe", *startup_args]
        os.chdir("../")
    else:
        updater_run_command = [sys.executable, "updater.py", *startup_args]
    subprocess.run(updater_run_command)
