# Battlefield 1943 Settings Editor v1.0

A lightweight GUI tool written in Python/Tkinter for modifying profile setting values in **Battlefield 1943** PS3 save files (`USR-DATA`). The editor includes automatic custom MD5 checksum recalculation to ensure save files remain valid and accepted by the game or emulator (RPCS3).

## Features

* **Complete Game Settings Support:** Access and tweak all profile options available in the game menus (Controls and Settings tabs).
* **Sensitivity Unlock:** Adjust mouse/stick sensitivity (`Scheme1Sensitivity`) beyond standard boundaries up to `9.999999` with the **Unlock** toggle.
* **Full Control Mapping & Inversion:** Configure soldier, vehicle, and plane control schemes, along with vertical axis inversions.
* **Audio & Display Adjustments:** Fine-tune Master, Music, and Dialogue volumes, sound system output types, voiceover languages, and brightness levels.
* **Automatic Custom MD5 Checksum:** Recalculates and patches the game's modified 16-byte header hash upon saving, preventing save corruption errors.
* **Tab-Based Interface:** Cleanly categorized into **Controls** and **Settings** with quick **Default** reset buttons for each category.
* **Standalone Executable Support:** Fully compatible with PyInstaller bundling (includes dynamic `_MEIPASS` resource handling for app icons).

## Supported Settings

### Controls Tab
| Setting Name | Internal Key | Allowed Values / Options |
| :--- | :--- | :--- |
| **Sensitivity** | `Scheme1Sensitivity` | `0.0` - `1.0` (Expandable to `9.999999` via Unlock) |
| **Vertical Look** | `Scheme1FlipY` | `Standard axis` (0), `Invert axis` (1) |
| **Vertical Vehicle** | `Scheme4FlipY` | `Standard axis` (0), `Invert axis` (1) |
| **Vertical Fly** | `Scheme3FlipY` | `Standard axis` (0), `Invert axis` (1) |
| **Soldier Controls** | `Scheme1InputType` | `Normal` (0), `Southpaw` (1), `Lefty` (2), `Lefty Southpaw` (3) |
| **Land/Boat Controls**| `Scheme2InputType` | `Normal` (0), `Stickdrive` (1), `Southpaw` (2), `Southpaw Stickd.` (3) |
| **Plane Controls** | `Scheme3InputType` | `Normal` (0), `Southpaw` (1), `Lefty` (2), `Lefty Southpaw` (3) |
| **Aim Assist** | `AimAssist` | `No` (0), `Yes` (1) |
| **Vibration** | `Vibration` | `No` (0), `Low` (1), `High` (2) |

### Settings Tab
| Setting Name | Internal Key | Allowed Values / Options |
| :--- | :--- | :--- |
| **Voiceover Language**| `VOLanguage` | `Localized` (0), `Original` (1) |
| **Your Sound System** | `SoundSystemSize` | `TV` (0), `HI-FI` (1), `Home Cinema` (2) |
| **Master Volume** | `Volume` | `0.00` - `1.00` |
| **Music Volume** | `MusicVolume` | `0.00` - `1.00` |
| **Dialogue Volume** | `DialogueVolume` | `0.00` - `1.00` |
| **Telemetry** | `Telemetry` | `No` (0), `Yes` (1) |
| **Brightness** | `Brightness` | `0.00` - `1.00` |
| **Car Radio** | `CarRadio` | `No` (0), `Yes` (1) |

## Usage

1. **Launch** the application executable or python script (`Main.py`).
2. Click **Open file...** and navigate to your save data directory:
   * **RPCS3 Path Example:** `dev_hdd0/home/00000001/savedata/NPEB00092-PROF_SAVE/USR-DATA`
3. Adjust your preferred control schemes, sliders, or dropdown options.
4. Click **Save file**.
5. **Restart the game** for the modified settings to take effect.
