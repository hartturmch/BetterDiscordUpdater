import ctypes
import logging
import os


def show_notification(title: str, message: str, error: bool = False) -> None:
    """Show a Windows message only for a failure or an installed update."""
    logging.getLogger(__name__).info("%s: %s", title, message)
    if os.name != "nt":
        return

    icon = 0x10 if error else 0x40  # MB_ICONERROR / MB_ICONINFORMATION
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x0 | icon)


def ask_yes_no(title: str, message: str) -> bool:
    """Ask the user once whether the updater should run at Windows startup."""
    if os.name != "nt":
        return False

    result = ctypes.windll.user32.MessageBoxW(0, message, title, 0x04 | 0x20)
    return result == 6  # IDYES
