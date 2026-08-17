import os
import glob
import logging
import shutil
from datetime import datetime

import requests

import config
import utils

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="(%(asctime)s) %(message)s")


def get_asar_path(is_ci: bool) -> str:
    return utils.backslash_path(config.BD_CI_ASAR_PATH if is_ci else config.BD_ASAR_PATH)


def get_require_line(is_ci: bool) -> str:
    return f'require("{get_asar_path(is_ci)}");\n'


def get_release_tag(is_ci: bool) -> str:
    return "CI" if is_ci else "Stable"


def is_bd_injected(discord_path: str, is_ci: bool) -> bool:
    core_path_pattern = os.path.join(discord_path, "modules/discord_desktop_core-*/discord_desktop_core")
    core_paths = glob.glob(core_path_pattern)

    if not core_paths:
        logger.warning("Discord core path not found when checking BetterDiscord injection.")
        return False

    index_js_path = os.path.join(core_paths[0], "index.js")
    if not os.path.exists(index_js_path):
        logger.warning("Discord index.js not found.")
        return False

    with open(index_js_path, "r", encoding="utf-8") as f:
        content = f.read()

    return f'require("{get_asar_path(is_ci)}");' in content


def update_bd_asar_only(is_ci: bool):
    if is_ci:
        if update_bd_ci_asar():
            logger.info("BetterDiscord CI has been updated successfully.")
            return

        logger.info("BetterDiscord CI update failed.")
        return

    os.makedirs(os.path.dirname(config.BD_ASAR_PATH), exist_ok=True)

    try:
        logger.info("Downloading BetterDiscord Stable asar...")
        response = utils.request_with_retry("GET", config.BD_ASAR_URL)
        backup_asar(config.BD_ASAR_PATH)
        with open(config.BD_ASAR_PATH, "wb") as f:
            f.write(response.content)
        logger.info("BetterDiscord Stable asar downloaded successfully.")

    except requests.RequestException as error:
        logger.error("Failed to download BetterDiscord Stable asar: %s", error)
        return

    config.LAST_INSTALLED_BD_VERSION = fetch_latest_bd_release()
    config.dump_settings()


def inject_patch(discord_path: str, is_ci: bool):
    core_path_pattern = os.path.join(discord_path, "modules/discord_desktop_core-*/discord_desktop_core")
    core_paths = glob.glob(core_path_pattern)

    if not core_paths:
        raise FileNotFoundError(f"No matching discord_desktop_core-* folder found in: {discord_path}")

    index_js_path = os.path.join(core_paths[0], "index.js")

    with open(index_js_path, "r", encoding="utf-8") as f:
        content = f.readlines()

    require_line = get_require_line(is_ci)
    other_release_require_line = get_require_line(not is_ci)
    release_tag = get_release_tag(is_ci)
    other_release_tag = get_release_tag(not is_ci)

    if any(other_release_require_line.strip() in line for line in content):
        logger.info(f"Found BetterDiscord {other_release_tag} injection. Removing it.")
        content = utils.remove_item_from_list(other_release_require_line, content)

    if any(require_line.strip() in line for line in content):
        logger.info(f"BetterDiscord {release_tag} is already injected. Skipping patch.")
        return

    content.insert(0, require_line)

    with open(index_js_path, "w", encoding="utf-8") as f:
        f.writelines(content)

    logger.info(f"Patched {index_js_path} to include BetterDiscord {release_tag}.")


def fetch_latest_bd_release() -> str:
    logger.info("Fetching latest BetterDiscord Stable version.")
    try:
        latest_release_url = utils.request_with_retry("HEAD", config.BD_LATEST_RELEASE_PAGE_URL, allow_redirects=True)
        return latest_release_url.url.split("/")[-1]
    except requests.RequestException as error:
        logger.error("Could not check BetterDiscord version: %s", error)
        return config.LAST_INSTALLED_BD_VERSION


def check_for_bd_updates(is_ci: bool) -> bool:
    """Checks for updates and return True if there is an available update, False otherwise"""
    logger.info("Checking for BetterDiscord updates...")
    if is_ci:
        return check_for_bd_ci_updates()

    latest_version = fetch_latest_bd_release()
    return latest_version is not None and latest_version != config.LAST_INSTALLED_BD_VERSION


def check_for_bd_ci_updates() -> bool:
    """Checks for updates and return True if there is an available update, False otherwise"""
    return utils.get_artifacts_from_successful_run(
        config.BD_CI_WORKFLOWS_RUNS_URL,
        config.BD_CI_WORKFLOW_REPO,
        config.BD_CI_WORKFLOW_AUTHOR
    ).run_id != config.LAST_INSTALLED_BD_CI_VERSION


def update_bd_ci_asar() -> bool:
    """Updates BD CI and returns False if there is any error, True otherwise"""

    release_meta = utils.get_artifacts_from_successful_run(config.BD_CI_WORKFLOWS_RUNS_URL, config.BD_CI_WORKFLOW_REPO, config.BD_CI_WORKFLOW_AUTHOR)
    if not release_meta:
        logger.info(f"Failed to fetch BetterDiscord CI artifacts from workflow run.")
        return False

    artifact = utils.find_artefact(release_meta.artifacts)
    if not artifact:
        logger.info(f"Failed to find BetterDiscord CI artifact ({release_meta.run_id}).")
        return False

    success = utils.download_artifact(artifact)
    if not success:
        return False

    config.LAST_INSTALLED_BD_CI_VERSION = release_meta.run_id
    config.dump_settings()
    return True


def backup_asar(asar_path: str) -> None:
    """Keep three timestamped BetterDiscord asar backups before replacing one."""
    if not os.path.exists(asar_path):
        return

    os.makedirs(config.BACKUP_DIRECTORY, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = os.path.join(
        config.BACKUP_DIRECTORY,
        f"{os.path.basename(asar_path)}.{timestamp}.bak"
    )
    shutil.copy2(asar_path, backup_path)
    logger.info("Backed up BetterDiscord asar to %s", backup_path)

    backups = sorted(
        glob.glob(os.path.join(config.BACKUP_DIRECTORY, f"{os.path.basename(asar_path)}.*.bak")),
        key=os.path.getmtime,
        reverse=True
    )
    for old_backup in backups[3:]:
        os.remove(old_backup)
