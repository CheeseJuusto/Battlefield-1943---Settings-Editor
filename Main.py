import hashlib
import os
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


class BF1943EditorApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Battlefield 1943 - Settings Editor")
        self.root.geometry("520x250")
        self.root.minsize(450, 220)

        # Ladataan ikonitiedosto PyInstaller-yhteensopivalla polulla
        try:
            icon_path = get_resource_path("app.ico")
            self.root.iconbitmap(icon_path)
        except Exception:
            pass  # Jos kuvaketta ei löydy, sovellus jatkaa normaalisti

        self.file_path = None
        self.file_bytes = bytearray()

        # Restricted search: Only Scheme1Sensitivity and AimAssist
        # Scheme1Sensitivity maximum value increased to 9.999999
        self.settings_schema = [
            ("Scheme1Sensitivity", "float", 0.0, 9.999999),
            ("AimAssist", "int", 0, 1),
        ]

        self.widget_vars = {}
        self.setup_ui()

    def setup_ui(self):
        top_frame = ttk.LabelFrame(self.root, text=" File ", padding=10)
        top_frame.pack(side="top", fill="x", padx=10, pady=5)

        self.lbl_file = ttk.Label(
            top_frame, text="No file selected", foreground="gray"
        )
        self.lbl_file.pack(side="left", fill="x", expand=True)

        btn_browse = ttk.Button(
            top_frame, text="Open File...", command=self.open_file
        )
        btn_browse.pack(side="right")

        bottom_frame = ttk.Frame(self.root, padding=10)
        bottom_frame.pack(side="bottom", fill="x")

        self.btn_save = ttk.Button(
            bottom_frame,
            text="Save Changes",
            command=self.save_file,
            state="disabled",
        )
        self.btn_save.pack(side="right")

        middle_frame = ttk.LabelFrame(self.root, text=" Settings ", padding=5)
        middle_frame.pack(side="top", fill="both", expand=True, padx=10, pady=5)

        self.canvas = tk.Canvas(middle_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            middle_frame, orient="vertical", command=self.canvas.yview
        )

        self.controls_frame = ttk.Frame(self.canvas)
        self.controls_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            ),
        )

        self.canvas.create_window((0, 0), window=self.controls_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def open_file(self):
        path = filedialog.askopenfilename(
            title="Select Profile File",
            filetypes=[
                ("All Files", "*.*"),
                ("USR-DATA", "USR-DATA*"),
                ("Profile Files", "profsave*"),
                ("DAT Files", "*.dat"),
            ],
        )
        if not path:
            return

        try:
            with open(path, "rb") as f:
                self.file_bytes = bytearray(f.read())

            self.file_path = path
            self.lbl_file.config(
                text=os.path.basename(path), foreground="black"
            )
            self.build_controls()
            self.btn_save.config(state="normal")
            messagebox.showinfo("Success", "File loaded successfully!")
        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to open file:\n{e}"
            )

    def get_setting_bounds(self, key_bytes):
        pos = self.file_bytes.find(key_bytes)
        if pos == -1:
            return None, None, None

        start_search = pos + len(key_bytes)

        start_val = start_search
        while start_val < len(self.file_bytes) and not (
            48 <= self.file_bytes[start_val] <= 57
            or self.file_bytes[start_val] == 45
        ):
            start_val += 1

        if start_val >= len(self.file_bytes):
            return None, None, None

        end_val = start_val
        while end_val < len(self.file_bytes) and (
            48 <= self.file_bytes[end_val] <= 57
            or self.file_bytes[end_val] in (46, 45)
        ):
            end_val += 1

        val_str = self.file_bytes[start_val:end_val].decode(
            "ascii", errors="ignore"
        )
        return start_val, end_val, val_str

    def build_controls(self):
        for child in self.controls_frame.winfo_children():
            child.destroy()
        self.widget_vars.clear()

        row = 0
        for key, stype, min_v, max_v in self.settings_schema:
            key_bytes = key.encode("ascii")
            start, end, val_str = self.get_setting_bounds(key_bytes)

            if start is None:
                continue

            lbl = ttk.Label(
                self.controls_frame, text=key, width=22, anchor="w"
            )
            lbl.grid(row=row, column=0, padx=5, pady=4, sticky="w")

            if stype == "float":
                try:
                    init_val = float(val_str)
                except ValueError:
                    init_val = 0.0

                var = tk.DoubleVar(value=init_val)
                entry_var = tk.StringVar(value=val_str)

                updating = False

                def on_scale_move(val, ev=entry_var, target_len=len(val_str)):
                    nonlocal updating
                    if not updating:
                        updating = True
                        dec_places = max(0, target_len - len(str(int(float(val)))) - 1)
                        ev.set(f"{float(val):.{dec_places}f}")
                        updating = False

                def on_entry_change(*args, v=var, ev=entry_var):
                    nonlocal updating
                    if not updating:
                        try:
                            val = float(ev.get())
                            updating = True
                            v.set(val)
                            updating = False
                        except ValueError:
                            pass

                entry_var.trace_add("write", on_entry_change)

                scale = ttk.Scale(
                    self.controls_frame,
                    from_=min_v,
                    to=max_v,
                    variable=var,
                    orient="horizontal",
                    length=160,
                    command=on_scale_move,
                )
                scale.grid(row=row, column=1, padx=5, pady=4)

                entry = ttk.Entry(
                    self.controls_frame, textvariable=entry_var, width=12
                )
                entry.grid(row=row, column=2, padx=5, pady=4)

                self.widget_vars[key] = (entry_var, "float")

            elif stype == "int":
                try:
                    init_val = int(val_str)
                except ValueError:
                    init_val = 0

                var = tk.IntVar(value=init_val)

                if min_v == 0 and max_v == 1:
                    chk = ttk.Checkbutton(self.controls_frame, variable=var)
                    chk.grid(
                        row=row,
                        column=1,
                        columnspan=2,
                        sticky="w",
                        padx=5,
                        pady=4,
                    )
                else:
                    spin = ttk.Spinbox(
                        self.controls_frame,
                        from_=min_v,
                        to=max_v,
                        textvariable=var,
                        width=5,
                    )
                    spin.grid(row=row, column=1, sticky="w", padx=5, pady=4)

                self.widget_vars[key] = (var, "int")

            row += 1

    def calculate_custom_md5(self, data):
        """Calculates Custom MD5 checksum according to .savepatch rules."""
        payload = bytes(data[0x000010:])
        raw_md5 = bytearray(hashlib.md5(payload).digest())

        fhash = bytearray(16)

        # Reverse bytes 0..3 (0x0000..0x0003)
        fhash[0] = raw_md5[3]
        fhash[1] = raw_md5[2]
        fhash[2] = raw_md5[1]
        fhash[3] = raw_md5[0]

        # Swap byte pairs 4..7 (0x0004..0x0007)
        fhash[4] = raw_md5[5]
        fhash[5] = raw_md5[4]
        fhash[6] = raw_md5[7]
        fhash[7] = raw_md5[6]

        # Keep bytes 8..15 as is (0x0008..0x000F)
        fhash[8:16] = raw_md5[8:16]

        return fhash

    def save_file(self):
        if not self.file_path or not self.file_bytes:
            return

        HEADER_SIZE = 16

        # 1. Update changed values in memory while preserving exact length
        for key, (var, stype) in self.widget_vars.items():
            key_bytes = key.encode("ascii")
            start, end, orig_val_str = self.get_setting_bounds(key_bytes)

            if start is None:
                continue

            target_len = end - start

            if stype == "float":
                try:
                    val_float = float(var.get())
                    dec_places = max(0, target_len - len(str(int(val_float))) - 1)
                    val_str = f"{val_float:.{dec_places}f}"
                except ValueError:
                    val_str = orig_val_str
            else:
                val_str = str(var.get())

            new_bytes = val_str.encode("ascii")

            if len(new_bytes) < target_len:
                new_bytes = (
                    new_bytes.rjust(target_len, b"0")
                    if stype == "float"
                    else new_bytes.ljust(target_len, b" ")
                )
            elif len(new_bytes) > target_len:
                new_bytes = new_bytes[:target_len]

            self.file_bytes[start : start + target_len] = new_bytes

        # 2. Calculate new custom MD5 checksum
        if len(self.file_bytes) > HEADER_SIZE:
            custom_hash = self.calculate_custom_md5(self.file_bytes)
            self.file_bytes[0:HEADER_SIZE] = custom_hash

        # 3. Save to file
        try:
            with open(self.file_path, "wb") as f:
                f.write(self.file_bytes)
            messagebox.showinfo(
                "Success",
                "File and Custom MD5 checksum saved successfully!",
            )
        except Exception as e:
            messagebox.showerror("Error", f"Save failed:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = BF1943EditorApp(root)
    root.mainloop()