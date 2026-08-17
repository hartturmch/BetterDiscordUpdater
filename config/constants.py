import os
import sys

import config

APPDATA = os.getenv("appdata")
LOCALAPPDATA = os.getenv("localappdata")
USERPROFILE = os.getenv("userprofile")


def get_application_root() -> str:
    """Return folder that contains settings, logs and updater.exe."""
    if getattr(sys, "frozen", False):
        executable_directory = os.path.dirname(sys.executable)
        if os.path.basename(sys.executable).lower() == "updater.exe":
            return executable_directory
        return os.path.abspath(os.path.join(executable_directory, ".."))
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

BDAI_SCRIPT_VERSION = "1.5.0"
BDAI_LATEST_RELEASE_PAGE_URL = "https://github.com/Zwylair/BetterDiscordAutoInstaller/releases/latest"
BDAI_RAW_RELEASE_URL_TEMPLATE = "https://github.com/Zwylair/BetterDiscordAutoInstaller/archive/refs/tags/{tag}.zip"
BDAI_RELEASE_URL_TEMPLATE = "https://github.com/Zwylair/BetterDiscordAutoInstaller/releases/download/{tag}/BetterDiscordAutoInstaller-{tag}.zip"
APPLICATION_ROOT = get_application_root()
SETTINGS_PATH = os.path.join(APPLICATION_ROOT, "settings.json")
GITHUB_TOKEN_FILE_PATH = os.path.join(APPLICATION_ROOT, "github_token")
LOG_PATH = os.path.join(APPLICATION_ROOT, "updater.log")
BACKUP_DIRECTORY = os.path.join(APPDATA, "BetterDiscord", "backups")

BD_LATEST_RELEASE_PAGE_URL = "https://github.com/rauenzi/BetterDiscordApp/releases/latest"
BD_ASAR_URL = "https://github.com/rauenzi/BetterDiscordApp/releases/latest/download/betterdiscord.asar"
BD_ASAR_PATH = os.path.join(APPDATA, "BetterDiscord", "data", "betterdiscord.asar")
BD_CI_ASAR_PATH = os.path.join(APPDATA, "BetterDiscord", "data", "betterdiscord-ci.asar")
BD_CI_WORKFLOW_AUTHOR = "BetterDiscord CI"
BD_CI_WORKFLOW_REPO = "BetterDiscord/BetterDiscord"
BD_CI_WORKFLOWS_RUNS_URL = f"https://api.github.com/repos/{BD_CI_WORKFLOW_REPO}/actions/workflows/ci.yml/runs"

DISCORD_POSSIBLE_PATHS = {
    config.DiscordEdition.STABLE: [os.path.join(LOCALAPPDATA, "Discord")],
    config.DiscordEdition.CANARY: [os.path.join(LOCALAPPDATA, "DiscordCanary")],
    config.DiscordEdition.PTB: [os.path.join(LOCALAPPDATA, "DiscordPTB")],
}
