# Battlefield 1943 Settings Editor

A lightweight Python/Tkinter tool for modifying profile setting values in **Battlefield 1943** save files (e.g. `USR-DATA`). The editor features custom recalculation for the game's modified MD5 checksums to ensure file validity.

## Features

* **Sensitivity Unlock:** Adjust `Scheme1Sensitivity` beyond normal limits (up to `9.999999`).
* **Aim Assist Toggle:** Easily modify the `AimAssist` setting.
* **Custom MD5 Checksum:** Automatically recalculates and patches the modified 16-byte header hash required by Battlefield 1943 upon saving.
* **Stand-Alone Executable:** Pre-configured for PyInstaller bundling with dynamic resource path resolving (`_MEIPASS`).

## Usage

1. Launch the application.
2. Click **Open File...** and select your profile save file (e.g., `USR-DATA`).
3. Adjust the **Scheme1Sensitivity** slider/entry or toggle **AimAssist**.
4. Click **Save Changes** to write the update and automatically apply the custom MD5 header hash.
