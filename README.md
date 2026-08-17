# BetterDiscord Updater

Windows updater for [BetterDiscord](https://betterdiscord.app/) and Discord Stable, PTB, and Canary installations.

## What it does

- Checks the installed Discord and BetterDiscord versions.
- Waits for Discord to finish its own update before applying a patch.
- Downloads the current BetterDiscord release, with network retries.
- Creates a timestamped `app.asar` backup before modifying it.
- Keeps a small rotating log and only shows Windows notifications for errors or updates.
- Starts Discord after the checks when it is closed, even when everything is already up to date.
- Offers to run silently when Windows starts. The option creates a shortcut in the current user's Startup folder; it does not change the Windows registry.
- Includes `startup_manager.exe` to enable or disable startup checks and view detected versions.

## Install

Download the latest `BetterDiscordUpdater-Setup-vX.Y.Z.exe` release and run it. The installer places the application in your local AppData folder and opens the updater after installation. Administrator permission is not required.

On its first normal run, the updater asks whether BetterDiscord should be checked when Windows starts.

To manage that choice later, run `startup_manager.exe` in the installed `v1.5.0` folder and select an option from the menu.

The updater is silent when started from Windows Startup. It creates `%APPDATA%\\BetterDiscordAutoInstaller\\logs\\updater.log` for diagnostics.

## License

MIT. See [LICENSE](LICENSE).
