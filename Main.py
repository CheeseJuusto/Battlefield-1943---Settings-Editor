import hashlib
import os
import re
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def get_resource_path(relative_path):
    """Hakee absoluuttisen polun resurssiin (toimii sekä .py- koodina että PyInstaller .exe-tiedostona)."""
    try:
        # PyInstaller luo väliaikaisen kansion osoitteeseen _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Standardiasetukset (Vakioarvot palautusta varten)
DEFAULT_SETTINGS = {
    # Controls
    "Scheme1Sensitivity": "0.500000",
    "Scheme1FlipY": "0",
    "Scheme4FlipY": "0",
    "Scheme3FlipY": "1",
    "Scheme1InputType": "0",
    "Scheme2InputType": "0",
    "Scheme3InputType": "0",
    "AimAssist": "1",
    "Vibration": "2",
    # Settings
    "VOLanguage": "1",
    "SoundSystemSize": "1",
    "Volume": "1.000000",
    "MusicVolume": "0.700000",
    "DialogueVolume": "0.700000",
    "Telemetry": "1",
    "Brightness": "0.500000",
    "CarRadio": "1",
}

# Pudotusvalikoiden vaihtoehdot (Teksti <-> Arvo tiedostossa)
OPTIONS_MAP = {
    "Scheme1FlipY": {"Standard axis": "0", "Invert axis": "1"},
    "Scheme3FlipY": {"Standard axis": "0", "Invert axis": "1"},
    "Scheme4FlipY": {"Standard axis": "0", "Invert axis": "1"},
    "Scheme1InputType": {
        "Normal": "0",
        "Southpaw": "1",
        "Lefty": "2",
        "Lefty Southpaw": "3",
    },
    "Scheme2InputType": {
        "Normal": "0",
        "Stickdrive": "1",
        "Southpaw": "2",
        "Southpaw Stickd.": "3",
    },
    "Scheme3InputType": {
        "Normal": "0",
        "Southpaw": "1",
        "Lefty": "2",
        "Lefty Southpaw": "3",
    },
    "AimAssist": {"No": "0", "Yes": "1"},
    "Vibration": {"No": "0", "Low": "1", "High": "2"},
    "VOLanguage": {"Localized": "0", "Original": "1"},
    "SoundSystemSize": {"TV": "0", "HI-FI": "1", "Home Cinema": "2"},
    "Telemetry": {"No": "0", "Yes": "1"},
    "CarRadio": {"No": "0", "Yes": "1"},
}


class ConfigEditorApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Battlefield 1943 Settings Editor")
        self.root.geometry("560x560")
        
        # Ladataan ikonitiedosto PyInstaller-yhteensopivalla polulla
        try:
            icon_path = get_resource_path("app.ico")
            self.root.iconbitmap(icon_path)
        except Exception:
            pass  # Jos kuvaketta ei löydy, sovellus jatkaa normaalisti

        self.file_path = None
        self.file_bytes = b""

        # UI muuttujat ja elementit
        self.vars = {}
        self.widgets = {}
        self.sensitivity_unlocked = tk.BooleanVar(value=False)

        self.setup_ui()

    def setup_ui(self):
        # Yläpalkki tiedoston valinnalle
        top_frame = ttk.Frame(self.root, padding=10)
        top_frame.pack(fill="x")

        btn_open = ttk.Button(
            top_frame, text="Open file...", command=self.open_file
        )
        btn_open.pack(side="left", padx=5)

        self.lbl_file = ttk.Label(
            top_frame, text="File not found", foreground="gray"
        )
        self.lbl_file.pack(side="left", padx=10)

        # Notebook välilehdet
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill="both", padx=10, pady=5)

        self.tab_controls = ttk.Frame(notebook)
        self.tab_settings = ttk.Frame(notebook)

        notebook.add(self.tab_controls, text="  Controls  ")
        notebook.add(self.tab_settings, text="  Settings  ")

        self.build_controls_tab()
        self.build_settings_tab()

        # Tallenna-painike alapalkkiin
        self.btn_save = ttk.Button(
            self.root,
            text="Save file",
            command=self.save_file,
            state="disabled",
        )
        self.btn_save.pack(pady=10)

    def open_file(self):
        path = filedialog.askopenfilename(
            title="Select USR-DATA file",
            filetypes=[("All files", "*.*"), ("USR-DATA", "USR-DATA*")],
        )
        if not path:
            return

        try:
            with open(path, "rb") as f:
                self.file_bytes = f.read()
            self.file_path = path
            self.lbl_file.config(
                text=os.path.basename(path), foreground="black"
            )
            self.btn_save.config(state="normal")
            self.update_ui_from_file()
        except Exception as e:
            messagebox.showerror(
                "Virhe", f"Tiedoston avaaminen epäonnistui:\n{e}"
            )

    def get_value(self, key):
        """Etsii avaimen arvon suoraan tiedostosta."""
        if not self.file_bytes:
            return DEFAULT_SETTINGS.get(key, "0")

        key_b = key.encode("utf-8")
        pos = self.file_bytes.find(key_b)
        if pos != -1:
            sub = self.file_bytes[pos + len(key_b) : pos + len(key_b) + 30]
            match = re.search(rb"[0-9\.]+", sub)
            if match:
                return match.group(0).decode("utf-8")
        return DEFAULT_SETTINGS.get(key, "0")

    def build_controls_tab(self):
        frame = ttk.Frame(self.tab_controls, padding=10)
        frame.pack(fill="both", expand=True)

        controls_schema = [
            ("Sensitivity", "Scheme1Sensitivity", "slider_sens", None),
            ("Vertical Look", "Scheme1FlipY", "dropdown", None),
            ("Vertical Vehicle", "Scheme4FlipY", "dropdown", None),
            ("Vertical Fly", "Scheme3FlipY", "dropdown", None),
            ("Soldier Controls", "Scheme1InputType", "dropdown", None),
            ("Land/Boat Controls", "Scheme2InputType", "dropdown", None),
            ("Plane Controls", "Scheme3InputType", "dropdown", None),
            ("Aim Assist", "AimAssist", "dropdown", None),
            ("Vibration", "Vibration", "dropdown", None),
        ]

        self.create_widgets(frame, controls_schema)

        btn_default = ttk.Button(
            frame,
            text="Default Controls",
            command=lambda: self.reset_to_default(controls_schema),
        )
        btn_default.pack(pady=15, anchor="e")

    def build_settings_tab(self):
        frame = ttk.Frame(self.tab_settings, padding=10)
        frame.pack(fill="both", expand=True)

        settings_schema = [
            ("Voiceover Language", "VOLanguage", "dropdown", None),
            ("Your Sound System", "SoundSystemSize", "dropdown", None),
            ("Master Volume", "Volume", "slider", 1.0),
            ("Music Volume", "MusicVolume", "slider", 1.0),
            ("Dialogue Volume", "DialogueVolume", "slider", 1.0),
            ("Telemetry", "Telemetry", "dropdown", None),
            ("Brightness", "Brightness", "slider", 1.0),
            ("Car Radio", "CarRadio", "dropdown", None),
        ]

        self.create_widgets(frame, settings_schema)

        btn_default = ttk.Button(
            frame,
            text="Default Settings",
            command=lambda: self.reset_to_default(settings_schema),
        )
        btn_default.pack(pady=15, anchor="e")

    def create_widgets(self, parent, schema):
        for label_text, key, widget_type, max_val in schema:
            row = ttk.Frame(parent)
            row.pack(fill="x", pady=5)

            lbl = ttk.Label(row, text=label_text, width=20, anchor="w")
            lbl.pack(side="left")

            val = float(DEFAULT_SETTINGS.get(key, "0"))

            if widget_type == "slider_sens":
                var = tk.DoubleVar(value=val)
                self.vars[key] = var

                scale = ttk.Scale(
                    row, from_=0.0, to=1.0, variable=var, orient="horizontal"
                )
                scale.pack(side="left", fill="x", expand=True, padx=5)

                val_lbl = ttk.Label(row, text=f"{val:.2f}", width=5)
                val_lbl.pack(side="right")

                chk = ttk.Checkbutton(
                    row,
                    text="Unlock",
                    variable=self.sensitivity_unlocked,
                    command=self.toggle_sensitivity_unlock,
                )
                chk.pack(side="right", padx=5)

                # Riippuvuudet tallennetaan päivityksiä varten
                self.widgets[key] = {
                    "scale": scale,
                    "label": val_lbl,
                    "type": "slider_sens",
                }
                var.trace_add(
                    "write",
                    lambda *args, v=var, l=val_lbl: self.on_sensitivity_change(
                        v, l
                    ),
                )

            elif widget_type == "slider":
                var = tk.DoubleVar(value=val)
                self.vars[key] = var

                max_limit = max_val if max_val is not None else 1.0
                scale = ttk.Scale(
                    row,
                    from_=0.0,
                    to=max_limit,
                    variable=var,
                    orient="horizontal",
                )
                scale.pack(side="left", fill="x", expand=True, padx=5)

                val_lbl = ttk.Label(row, text=f"{val:.2f}", width=5)
                val_lbl.pack(side="right")

                self.widgets[key] = {
                    "scale": scale,
                    "label": val_lbl,
                    "type": "slider",
                }
                var.trace_add(
                    "write",
                    lambda *args, v=var, l=val_lbl: l.config(
                        text=f"{v.get():.2f}"
                    ),
                )

            elif widget_type == "dropdown":
                options = OPTIONS_MAP[key]
                current_text = list(options.keys())[0]

                var = tk.StringVar(value=current_text)
                self.vars[key] = var

                dropdown = ttk.OptionMenu(
                    row, var, current_text, *options.keys()
                )
                dropdown.pack(side="right", fill="x", expand=True)

                self.widgets[key] = {"dropdown": dropdown, "type": "dropdown"}

    def toggle_sensitivity_unlock(self):
        """Käsitellään Unlock-täppä. Jos se poistetaan, asteikko palaa 0-1 välille liikutettaessa."""
        scale = self.widgets["Scheme1Sensitivity"]["scale"]
        if self.sensitivity_unlocked.get():
            scale.config(to=9.999999)
        else:
            # Jos arvo on jo alle 1.0, asetetaan asteikon maksimiksi heti 1.0
            if self.vars["Scheme1Sensitivity"].get() <= 1.0:
                scale.config(to=1.0)

    def on_sensitivity_change(self, var, label):
        scale = self.widgets["Scheme1Sensitivity"]["scale"]
        # Jos unlock ei ole päällä, mutta asteikkoa liikutetaan, pakotetaan maksimi 1.0:aan
        if not self.sensitivity_unlocked.get():
            scale.config(to=1.0)

        label.config(text=f"{var.get():.2f}")

    def update_ui_from_file(self):
        """Päivittää käyttöliittymän arvot ladatun tiedoston mukaisesti."""
        for key in self.vars:
            val_str = self.get_value(key)
            val_num = float(val_str)

            if key == "Scheme1Sensitivity":
                # Tarkistetaan ylittääkö arvo 1.0 -> Aktivoidaan unlock automaattisesti
                if val_num > 1.0:
                    self.sensitivity_unlocked.set(True)
                    self.widgets[key]["scale"].config(to=9.999999)
                else:
                    self.sensitivity_unlocked.set(False)
                    self.widgets[key]["scale"].config(to=1.0)

                self.vars[key].set(val_num)

            elif self.widgets[key]["type"] in ["slider"]:
                self.vars[key].set(val_num)

            elif self.widgets[key]["type"] == "dropdown":
                options = OPTIONS_MAP[key]
                val_int_str = str(int(val_num))
                current_text = next(
                    (k for k, v in options.items() if v == val_int_str),
                    list(options.keys())[0],
                )
                self.vars[key].set(current_text)

    def reset_to_default(self, schema):
        """Palauttaa tietyn välilehden asetukset vakioarvoihin."""
        for _, key, widget_type, _ in schema:
            if key in DEFAULT_SETTINGS:
                def_val = DEFAULT_SETTINGS[key]
                if widget_type in ["slider", "slider_sens"]:
                    self.vars[key].set(float(def_val))
                    if key == "Scheme1Sensitivity":
                        self.sensitivity_unlocked.set(False)
                        self.widgets[key]["scale"].config(to=1.0)
                elif widget_type == "dropdown":
                    options = OPTIONS_MAP[key]
                    text = next(
                        (k for k, v in options.items() if v == def_val), ""
                    )
                    self.vars[key].set(text)

    def calculate_custom_md5(self, data):
        """Laskee BF1943 Custom MD5 -tarkistussumman peliä varten."""
        payload = bytes(data[0x000010:])
        raw_md5 = bytearray(hashlib.md5(payload).digest())

        fhash = bytearray(16)

        # Tavut 0..3 käänteiseen järjestykseen
        fhash[0] = raw_md5[3]
        fhash[1] = raw_md5[2]
        fhash[2] = raw_md5[1]
        fhash[3] = raw_md5[0]

        # Tavuparit 4..7 vaihdetaan keskenään (5,4,7,6)
        fhash[4] = raw_md5[5]
        fhash[5] = raw_md5[4]
        fhash[6] = raw_md5[7]
        fhash[7] = raw_md5[6]

        # Tavut 8..15 pidetään sellaisenaan
        fhash[8:16] = raw_md5[8:16]

        return fhash

    def save_file(self):
        """Kirjoittaa muutetut arvot tiedostoon ja päivittää Custom MD5 otsakkeeseen."""
        if not self.file_path or not self.file_bytes:
            messagebox.showerror("Virhe", "Ei ladattua tiedostoa!")
            return

        data = bytearray(self.file_bytes)

        # 1. Päivitetään muuttuneet arvot
        for key, var in self.vars.items():
            key_b = key.encode("utf-8")
            pos = data.find(key_b)

            if pos != -1:
                sub_start = pos + len(key_b)
                sub = data[sub_start : sub_start + 30]
                match = re.search(rb"[0-9\.]+", sub)

                if match:
                    val_start = sub_start + match.start()
                    val_end = sub_start + match.end()

                    if key in OPTIONS_MAP:
                        raw_val = OPTIONS_MAP[key][var.get()]
                    else:
                        raw_val = f"{var.get():.6f}"

                    target_len = val_end - val_start
                    new_bytes = raw_val.encode("utf-8")

                    if len(new_bytes) < target_len:
                        new_bytes = new_bytes.ljust(target_len, b"0")
                    elif len(new_bytes) > target_len:
                        new_bytes = new_bytes[:target_len]

                    data[val_start:val_end] = new_bytes

        # 2. Lasketaan uusi Custom MD5 ja kirjoitetaan otsakkeeseen (0x00..0x0F)
        if len(data) > 16:
            custom_hash = self.calculate_custom_md5(data)
            data[0:16] = custom_hash

        # 3. Tallennetaan tiedosto levylle
        try:
            with open(self.file_path, "wb") as f:
                f.write(data)
            messagebox.showinfo(
                "Saving successful",
                "Restart the game to apply changes!",
            )
            self.file_bytes = bytes(data)
        except Exception as e:
            messagebox.showerror(
                "Virhe", f"Tiedoston tallennus epäonnistui:\n{e}"
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigEditorApp(root)
    root.mainloop()
