import os
import sys

import config
import utils


def show_versions():
    config.load_settings()
    print("\nInstalled versions:")
    editions = {
        config.DiscordEdition.STABLE: config.DISCORD_PARENT_PATH,
        config.DiscordEdition.CANARY: config.DISCORD_CANARY_PARENT_PATH,
        config.DiscordEdition.PTB: config.DISCORD_PTB_PARENT_PATH
    }

    for edition, path in editions.items():
        if not path:
            continue
        try:
            version = utils.get_latest_installed_discord_folder_name(path)
        except (FileNotFoundError, OSError):
            version = "not found"
        print(f"- {edition}: {version}")

    betterdiscord_version = config.LAST_INSTALLED_BD_CI_VERSION if config.USE_BD_CI_RELEASES else config.LAST_INSTALLED_BD_VERSION
    print(f"- BetterDiscord: {betterdiscord_version or 'not detected'}")


def main():
    if os.name != "nt":
        input(
            "Your system is not supported to use this script\n"
            "\n"
            "Press ENTER to exit."
        )
        sys.exit(0)

    print(f"BetterDiscordAutoInstaller v{config.BDAI_SCRIPT_VERSION} (startup_manager)")

    while True:
        command = input(
            "\n"
            "[0] -- Exit\n"
            "[1] -- Enable checks when Windows starts\n"
            "[2] -- Disable checks when Windows starts\n"
            "[3] -- Show installed versions\n"
            "\n"
            "> "
        )
        print()

        if command == "0":
            print("Exiting...")
            break
        elif command == "1":
            try:
                utils.enable_autostart()
                print("Automatic BetterDiscord checks are enabled for Windows startup.")

            except PermissionError:
                print("Permission denied. Please run the script with administrator privileges.")
            except Exception as e:
                print(f"An error occurred while adding the shortcut: {e}")
        elif command == "2":
            try:
                if utils.disable_autostart():
                    print("Automatic BetterDiscord checks were removed from Windows startup.")
                else:
                    print("The shortcut does not exist in the startup folder.")
            except Exception as e:
                print(f"An error occurred while removing the shortcut: {e}")
        elif command == "3":
            show_versions()
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
