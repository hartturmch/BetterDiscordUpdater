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

## Run the packaged app

Run `updater.exe`. On its first normal run, it asks whether BetterDiscord should be checked when Windows starts.

To manage that choice later, run `v1.5.0\\startup_manager.exe` and select an option from the menu.

The updater is silent when started from Windows Startup. It creates `%APPDATA%\\BetterDiscordAutoInstaller\\logs\\updater.log` for diagnostics.

## Build from source

```powershell
python -m pip install -r requirements.txt
python setup.py build
```

The build output is written to `build/exe.win-amd64-3.14/`.

## Settings

`settings.json` is stored next to the packaged executable. It saves Discord paths, installed versions, retry limits, timeouts, and startup preference. Keep `disable_bdai_autoupdate` set to `true` for this customized build, otherwise the original self-updater can replace it.

## License

MIT. See [LICENSE](LICENSE).
