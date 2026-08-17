import os
import sys

import winshell

import config


SHORTCUT_NAME = "BetterDiscordAutoInstaller.lnk"


def get_shortcut_path() -> str:
    return os.path.join(
        os.getenv("appdata"),
        "Microsoft",
        "Windows",
        "Start Menu",
        "Programs",
        "Startup",
        SHORTCUT_NAME
    )


def enable_autostart() -> None:
    """Create a per-user Startup shortcut that runs the updater silently."""
    if os.name != "nt":
        raise OSError("Autostart is only available on Windows.")

    if getattr(sys, "frozen", False):
        target = os.path.join(config.APPLICATION_ROOT, "updater.exe")
        arguments = "--run --startup"
        working_directory = config.APPLICATION_ROOT
    else:
        target = sys.executable
        arguments = f'"{os.path.join(config.APPLICATION_ROOT, "updater.py")}" --run --startup'
        working_directory = config.APPLICATION_ROOT

    with winshell.shortcut(get_shortcut_path()) as shortcut:
        shortcut.path = target
        shortcut.arguments = arguments
        shortcut.working_directory = working_directory
        shortcut.description = "Checks for BetterDiscord updates when Windows starts"


def disable_autostart() -> bool:
    shortcut_path = get_shortcut_path()
    if not os.path.exists(shortcut_path):
        return False
    os.remove(shortcut_path)
    return True
