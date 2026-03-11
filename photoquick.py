import sys
import os
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import threading
import time
import webbrowser
from PIL import Image, ImageTk, ImageOps

# --- EXE RESOURCE HANDLING ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- THEME & COLOR CONFIGURATION ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class Theme:
    BG_DARK      = "#050505"
    BG_LIGHT     = "#F2F2F7"
    ACCENT       = "#00E5FF"
    TEXT_DIM     = "#888888"
    BORDER_DARK  = "#222222"
    LABEL_TEXT   = ("#333333", "#FFFFFF")
    SUB_TEXT     = ("#666666", "#888888")

class Config:
    VALID_EXTENSIONS = (
        '.jpg', '.jpeg', '.png', '.bmp', '.webp', '.heic',
        '.cr2', '.nef', '.arw', '.dng', '.orf', 
        '.mp4', '.mov', '.avi'
    )

# --- LOGIC ENGINE ---
class SearchEngine:
    def __init__(self, update_status_callback, finish_callback):
        self.update_status = update_status_callback
        self.finish = finish_callback
        # Track which SOURCE files have been copied (full paths)
        self.copied_sources = set()

    def run_search(self, id_list, target_folder):
        try:
            out_dir = os.path.join(target_folder, "PhotoQuick_Export")
            if not os.path.exists(out_dir): os.makedirs(out_dir)

            self.update_status(f"Scanning directory...")
            matches = 0
            
            files = [f for f in os.listdir(target_folder) if os.path.isfile(os.path.join(target_folder, f))]

            for f in files:
                if not f.lower().endswith(Config.VALID_EXTENSIONS): continue
                for target_id in id_list:
                    if target_id in f:
                        matches += 1
                        src_path = os.path.join(target_folder, f)
                        copied = self._copy_file(src_path, out_dir, f)
                        if copied:
                            self.update_status(f"FOUND: {f}")
                        break 

            msg = f"Operation Complete.\nAssets recovered: {matches}"
            self.finish(True, msg)
        except Exception as e:
            self.finish(False, str(e))

    def _copy_file(self, src, folder, fname):
        """
        Copy file to destination. 
        Returns True if copied, False if skipped (already exists in output).
        """
        dst = os.path.join(folder, fname)
        
        # Check if file already exists in output folder (by name)
        # This handles the case where user deleted files and wants to recopy
        if os.path.exists(dst):
            self.update_status(f"EXISTS (skipping): {fname}")
            return False
        
        # Also check if this exact source was copied to a different name (timestamped)
        # by checking if source is in our tracking set AND the destination exists
        if src in self.copied_sources:
            # Check if any file with this source's base name exists in output
            base_name = os.path.splitext(fname)[0]
            for existing_file in os.listdir(folder):
                if existing_file.startswith(base_name):
                    self.update_status(f"EXISTS (skipping): {fname}")
                    return False
        
        # If filename exists in output, create unique name with timestamp
        # (This shouldn't happen now due to above check, but keep as safety)
        if os.path.exists(dst):
            base, ext = os.path.splitext(fname)
            timestamp = int(time.time())
            dst = os.path.join(folder, f"{base}_{timestamp}{ext}")
        
        # Copy the file
        shutil.copy2(src, dst)
        # Mark this source as copied
        self.copied_sources.add(src)
        return True

# --- UI COMPONENTS ---
class AboutWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("About PhotoQuick")
        self.geometry("500x600")
        self.resizable(False, False)
        self.attributes('-topmost', True)
        self.center_relative_to_parent(parent, 500, 600)
        self._set_window_icon()
        
        mode = ctk.get_appearance_mode()
        bg_col = Theme.BG_DARK if mode == "Dark" else Theme.BG_LIGHT
        self.configure(fg_color=bg_col)

        ctk.CTkLabel(self, text="PHOTOQUICK", font=("Segoe UI", 24, "bold"), text_color=Theme.ACCENT).pack(pady=(30, 5))
        ctk.CTkLabel(self, text="Professional Asset Management Tool", font=("Segoe UI", 12), text_color=Theme.SUB_TEXT).pack(pady=(0, 20))
        ctk.CTkFrame(self, height=1, width=400, fg_color=Theme.BORDER_DARK).pack()

        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.pack(fill="both", expand=True, padx=40, pady=20)

        details = [
            ("Creator", "Mohammed Fadel"),
            ("Origin Year", "2022"),
            ("Last Update", "2026.2"),
            ("Region", "Beirut, Lebanon"),
            ("contact", "+964 788 490 8775")
        ]

        for label, value in details:
            row = ctk.CTkFrame(info_frame, fg_color="transparent")
            row.pack(fill="x", pady=8)
            ctk.CTkLabel(row, text=f"{label}:", font=("Segoe UI", 12, "bold"), text_color=Theme.SUB_TEXT).pack(side="left")
            ctk.CTkLabel(row, text=value, font=("Segoe UI", 12), text_color=Theme.LABEL_TEXT).pack(side="right")

        ctk.CTkButton(self, text="Visit Official Website", fg_color=Theme.ACCENT, text_color="black", hover_color="#00B8D4", 
                      command=lambda: webbrowser.open("https://photoquick.unaux.com/")).pack(pady=(10, 0))
        ctk.CTkButton(self, text="Contact via WhatsApp", fg_color="#25D366", text_color="white", hover_color="#128C7E", 
                      command=lambda: webbrowser.open("https://wa.me/9647884908775")).pack(pady=20)
        
        ctk.CTkLabel(self, text="PhotoQuick is a high-performance utility designed in Lebanon\nfor professional photographers and data management.", 
                     font=("Segoe UI", 10), text_color=Theme.SUB_TEXT, justify="center").pack(pady=(0, 20))
    
    def center_relative_to_parent(self, parent, width, height):
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def _set_window_icon(self):
        try:
            icon_path = resource_path("icon.ico")
            if os.path.exists(icon_path):
                self.wm_iconbitmap(icon_path)
            else:
                icon_path = resource_path("icon.png")
                if os.path.exists(icon_path):
                    img = Image.open(icon_path)
                    photo = ImageTk.PhotoImage(img)
                    self.wm_iconphoto(True, photo)
        except Exception:
            pass

class LiquidSplashScreen(ctk.CTkToplevel):
    def __init__(self, parent, image_path):
        super().__init__(parent)
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        self._set_window_icon()
        
        tr_key = "#010101" 
        self.configure(fg_color=tr_key)
        self.wm_attributes("-transparentcolor", tr_key)

        w, h = 600, 320
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

        self.main_frame = ctk.CTkFrame(self, fg_color=Theme.BG_DARK, corner_radius=25, border_width=1, border_color=Theme.ACCENT)
        self.main_frame.pack(fill="both", expand=True)

        ctk.CTkLabel(self.main_frame, text="Photo\nQuick", font=("Segoe UI Display", 48, "bold"), text_color="white", justify="left").place(x=40, y=40)
        ctk.CTkLabel(self.main_frame, text="Precision Search Core", font=("Segoe UI", 14), text_color=Theme.ACCENT).place(x=45, y=160)
        
        self.prog = ctk.CTkProgressBar(self.main_frame, height=4, width=200, fg_color="#222", progress_color=Theme.ACCENT)
        self.prog.place(x=45, y=250)
        self.prog.start()

        self.img_frame = ctk.CTkFrame(self.main_frame, width=260, height=280, corner_radius=15, fg_color="black")
        self.img_frame.place(x=315, y=20)
        self.img_frame.grid_propagate(False)

        try:
            img_full_path = resource_path(image_path)
            pil_img = Image.open(img_full_path)
            pil_img = ImageOps.fit(pil_img, (260, 280))
            self.img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(260, 280))
            ctk.CTkLabel(self.img_frame, text="", image=self.img).pack(fill="both", expand=True)
        except Exception as e:
            ctk.CTkLabel(self.img_frame, text=f"IMAGE NOT FOUND\n({image_path})", text_color="white").pack(expand=True)
    
    def _set_window_icon(self):
        try:
            icon_path = resource_path("icon.ico")
            if os.path.exists(icon_path):
                self.wm_iconbitmap(icon_path)
            else:
                icon_path = resource_path("icon.png")
                if os.path.exists(icon_path):
                    img = Image.open(icon_path)
                    photo = ImageTk.PhotoImage(img)
                    self.wm_iconphoto(True, photo)
        except Exception:
            pass

class PhotoQuickApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.withdraw()
        self._set_window_icon()
        self.title("PhotoQuick")
        self.center_window(1150, 650)
        
        self.engine = SearchEngine(self.update_status, self.on_finish)
        self.target_folder = ""

        self.splash = LiquidSplashScreen(self, "i.png")
        self.after(3000, self.reveal)

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _set_window_icon(self):
        try:
            icon_path = resource_path("icon.ico")
            if os.path.exists(icon_path):
                self.wm_iconbitmap(icon_path)
                return
        except Exception:
            pass
        
        try:
            icon_path = resource_path("icon.png")
            if os.path.exists(icon_path):
                img = Image.open(icon_path)
                small_img = img.resize((16, 16), Image.Resampling.LANCZOS)
                large_img = img.resize((32, 32), Image.Resampling.LANCZOS)
                small_photo = ImageTk.PhotoImage(small_img)
                large_photo = ImageTk.PhotoImage(large_img)
                self.wm_iconphoto(False, large_photo, small_photo)
        except Exception:
            pass

    def reveal(self):
        if self.splash:
            self.splash.destroy()
        self.deiconify()
        self.setup_ui()

    def setup_ui(self):
        self.nav_bar = ctk.CTkFrame(self, height=45, corner_radius=0)
        self.nav_bar.pack(fill="x", side="top")
        
        btn_opt = {"font": ("Segoe UI", 12), "fg_color": "transparent", "height": 35, "width": 100, "text_color": Theme.LABEL_TEXT}
        ctk.CTkButton(self.nav_bar, text="Dark Mode", command=lambda: ctk.set_appearance_mode("Dark"), **btn_opt).pack(side="left", padx=5)
        ctk.CTkButton(self.nav_bar, text="Light Mode", command=lambda: ctk.set_appearance_mode("Light"), **btn_opt).pack(side="left", padx=5)
        ctk.CTkButton(self.nav_bar, text="About", command=self.show_about, **btn_opt).pack(side="right", padx=15)

        self.body = ctk.CTkFrame(self, fg_color="transparent")
        self.body.pack(fill="both", expand=True)
        self.body.grid_columnconfigure((0,1,2), weight=1)
        self.body.grid_rowconfigure(0, weight=1)

        self.col1 = ctk.CTkFrame(self.body, corner_radius=0)
        self.col1.grid(row=0, column=0, sticky="nsew", padx=1)
        ctk.CTkLabel(self.col1, text="1. INPUT SEQUENCE", font=("Segoe UI", 14, "bold"), text_color=Theme.SUB_TEXT).pack(padx=20, pady=(30, 10), anchor="w")
        self.txt_ids = ctk.CTkTextbox(self.col1, font=("Consolas", 12), text_color=Theme.LABEL_TEXT)
        self.txt_ids.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.col2 = ctk.CTkFrame(self.body, corner_radius=0)
        self.col2.grid(row=0, column=1, sticky="nsew", padx=1)
        ctk.CTkLabel(self.col2, text="2. DIRECTORY", font=("Segoe UI", 14, "bold"), text_color=Theme.SUB_TEXT).pack(padx=20, pady=(30, 40), anchor="w")
        self.btn_browse = ctk.CTkButton(self.col2, text="SELECT FOLDER", height=60, border_width=1, border_color=Theme.ACCENT, fg_color="transparent", text_color=Theme.ACCENT, command=self.browse)
        self.btn_browse.pack(fill="x", padx=40, pady=20)
        self.lbl_path = ctk.CTkLabel(self.col2, text="No directory selected", wraplength=250, text_color=Theme.LABEL_TEXT)
        self.lbl_path.pack(padx=20, pady=10)

        self.col3 = ctk.CTkFrame(self.body, corner_radius=0)
        self.col3.grid(row=0, column=2, sticky="nsew", padx=1)
        ctk.CTkLabel(self.col3, text="3. STATUS", font=("Segoe UI", 14, "bold"), text_color=Theme.SUB_TEXT).pack(padx=20, pady=(30, 40), anchor="w")
        self.lbl_status = ctk.CTkLabel(self.col3, text="READY", font=("Consolas", 16, "bold"), text_color=Theme.ACCENT)
        self.lbl_status.pack(pady=(20, 10))
        self.prog = ctk.CTkProgressBar(self.col3, height=4, progress_color=Theme.ACCENT)
        self.prog.pack(pady=(0, 40), padx=40, fill="x")
        self.prog.set(0)
        self.btn_run = ctk.CTkButton(self.col3, text="START EXTRACTION", height=60, fg_color=Theme.ACCENT, text_color="black", font=("Segoe UI", 15, "bold"), command=self.start_process)
        self.btn_run.pack(fill="x", padx=40, pady=20)

    def show_about(self):
        AboutWindow(self)

    def browse(self):
        p = filedialog.askdirectory()
        if p:
            self.target_folder = p
            self.lbl_path.configure(text=p)

    def start_process(self):
        raw = self.txt_ids.get("1.0", "end").replace('\n', ' ').replace(',', ' ')
        ids = [x.strip() for x in raw.split(' ') if x.strip()]
        if not ids or not self.target_folder: return messagebox.showwarning("Incomplete Data", "Identification list or directory path is missing.")
        self.btn_run.configure(state="disabled", text="PROCESSING")
        self.prog.start()
        threading.Thread(target=self.engine.run_search, args=(ids, self.target_folder), daemon=True).start()

    def update_status(self, msg):
        self.after(0, lambda: self.lbl_status.configure(text=msg))

    def on_finish(self, success, msg):
        self.after(0, lambda: self._finalize(success, msg))

    def _finalize(self, success, msg):
        self.prog.stop()
        self.prog.set(1 if success else 0)
        self.btn_run.configure(state="normal", text="START EXTRACTION")
        if success: messagebox.showinfo("Process Complete", msg)
        else: messagebox.showerror("System Error", msg)

if __name__ == "__main__":
    app = PhotoQuickApp()
    app.mainloop()
