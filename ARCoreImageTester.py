import os
import json
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk

APP_DIR = os.path.dirname(os.path.abspath(__file__))
ARCOREIMG = os.path.join(APP_DIR, "arcoreimg.exe")
HISTORY_FILE = os.path.join(APP_DIR, "scan_history.json")

class ARCoreImageTester(TkinterDnD.Tk):

    def __init__(self):
        super().__init__()
        self.title("ARCore Image Tester")
        self.geometry("1100x800")
        self.minsize(950, 700)
        self.configure(bg="#101216")
        self.current_image = None
        self.image_path = None
        self.history = {}    
        self.load_history()
        self.create_ui()
        self.refresh_history_list()
        self.drop_target_register(DND_FILES)
        self.dnd_bind("<<Drop>>", self.on_drop)

# HISTORY SYSTEM

    def load_history(self):

        if not os.path.exists(HISTORY_FILE):
            self.history = {}
            return

        try:

            with open(HISTORY_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            if isinstance(data, dict):
                self.history = {filename: entry
                    for filename, entry in data.items()
                    if isinstance(filename, str) and isinstance(entry, dict)}
            else:
                self.history = {}

        except Exception:
            self.history = {}


    def save_history(self):

        try:

            with open(HISTORY_FILE, "w", encoding="utf-8") as file:
                json.dump(self.history,  file, indent=4, ensure_ascii=False)

        except Exception as error:
            messagebox.showerror("History error", "Could not save scan history:\n\n" + str(error))


    def refresh_history_list(self):

        self.history_list.delete(0, tk.END)

        sorted_items = sorted(self.history.items(), key=lambda item: item[0].lower())

        for filename, data in sorted_items:

            score = data.get("score", "?")

            if isinstance(score, int):

                display = (f"{filename}" f"    |    "f"{score}/100")

            else:

                display = (f"{filename}" f"    |    ?")

            self.history_list.insert(tk.END, display)

            index = self.history_list.size() - 1

            if isinstance(score, int):

                if score >= 75: color = "#22c55e"
                elif score >= 50: color = "#eab308"
                elif score >= 25: color = "#f97316"
                else: color = "#ef4444"
                self.history_list.itemconfig(index, foreground=color)


    def on_history_select(self, event):

        selection = self.history_list.curselection()

        if not selection:
            return

        display = self.history_list.get(selection[0])
        filename = display.split("    |    ")[0]

        if filename not in self.history:
            return

        data = self.history[filename]
        path = data.get("path", "")
        score = data.get("score")

        self.filename_label.config(text=filename)

        if isinstance(score, int):
            self.show_score(score)

        if os.path.exists(path):

            self.image_path = path
            self.show_preview(path)


    def select_history_item(self, filename):

        items = self.history_list.get(0, tk.END)

        for index, item in enumerate(items):

            current_filename = item.split("    |    ")[0]

            if current_filename == filename:

                self.history_list.selection_clear(0, tk.END)
                self.history_list.selection_set(index)
                self.history_list.see(index)
                break


    def delete_selected(self):

        selection = self.history_list.curselection()

        if not selection:

            messagebox.showinfo("Nothing selected", "Select an image from the history first.")
            return

        display = self.history_list.get(selection[0])
        filename = display.split( "    |    ")[0]
        confirm = messagebox.askyesno("Delete scan", "Remove this image from the scan history?\n\n" + filename)

        if not confirm:
            return

        if filename in self.history:

            del self.history[filename]

        self.save_history()
        self.refresh_history_list()
        self.score_label.config(text="-", fg="white")
        self.rating_label.config(text="Drop an image to begin", fg="#8d95a3")
        self.filename_label.config(text="")
        self.image_path = None
        self.drop_label.config(image="", text="DROP IMAGE HERE\n\nJPG  |  JPEG  |  PNG")
        self.current_image = None

    def clear_history(self):

        if not self.history:
            return

        confirm = messagebox.askyesno("Clear history", "Are you sure you want to delete all scan history?")

        if not confirm:
            return

        self.history = {}
        self.save_history()
        self.refresh_history_list()
        self.score_label.config(text="-", fg="white")
        self.rating_label.config(text="Drop an image to begin", fg="#8d95a3")
        self.filename_label.config(text="")
        self.image_path = None
        self.drop_label.config(image="", text="DROP IMAGE HERE\n\nJPG  |  JPEG  |  PNG")
        self.current_image = None

# USER INTERFACE

    def create_ui(self):

        title = tk.Label(self,
            text="ARCore Image Tester",
            font=("Segoe UI", 24, "bold"),
            fg="white",
            bg="#101216"
        )

        title.pack(pady=(20, 5))

        subtitle = tk.Label(self,
            text="Drop an image to calculate its ARCore score",
            font=("Segoe UI", 11),
            fg="#9da3ae",
            bg="#101216"
        )

        subtitle.pack(pady=(0, 15))
        main_frame = tk.Frame(self, bg="#101216")

        main_frame.pack( fill="both", expand=True, padx=25, pady=10)

# LEFT SIDE

        left_frame = tk.Frame(main_frame, bg="#101216")

        left_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 15)
        )

        self.drop_frame = tk.Frame(
            left_frame,
            bg="#191c22",
            highlightbackground="#3a3f4b",
            highlightthickness=2
        )

        self.drop_frame.pack(fill="both", expand=True)

        self.drop_label = tk.Label(
            self.drop_frame,
            text="DROP IMAGE HERE\n\nJPG  |  JPEG  |  PNG",
            font=("Segoe UI", 18, "bold"),
            fg="#707784",
            bg="#191c22",
            justify="center"
        )

        self.drop_label.place(relx=0.5, rely=0.5, anchor="center")

        score_title = tk.Label(
            left_frame,
            text="ARCORE SCORE",
            font=("Segoe UI", 11, "bold"),
            fg="#8d95a3",
            bg="#101216"
        )

        score_title.pack(pady=(15, 0))

        self.score_label = tk.Label(
            left_frame,
            text="-",
            font=("Segoe UI", 52, "bold"),
            fg="white",
            bg="#101216"
        )

        self.score_label.pack()

        self.rating_label = tk.Label(
            left_frame,
            text="Drop an image to begin",
            font=("Segoe UI", 13, "bold"),
            fg="#8d95a3",
            bg="#101216"
        )

        self.rating_label.pack(pady=(0, 10))

        self.filename_label = tk.Label(
            left_frame,
            text="",
            font=("Segoe UI", 10),
            fg="#707784",
            bg="#101216"
        )

        self.filename_label.pack(pady=(0, 10))

# BUTTONS

        button_frame = tk.Frame(left_frame, bg="#101216")
        button_frame.pack(pady=(0, 10))

        self.select_button = tk.Button(
            button_frame,
            text="Select Image",
            command=self.select_image,
            font=("Segoe UI", 10, "bold"),
            fg="white",
            bg="#2563eb",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=9,
            cursor="hand2"
        )

        self.select_button.pack(side="left", padx=5)

        self.rescan_button = tk.Button(
            button_frame,
            text="Rescan Selected",
            command=self.rescan_selected,
            font=("Segoe UI", 10, "bold"),
            fg="white",
            bg="#374151",
            activebackground="#4b5563",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=9,
            cursor="hand2"
        )

        self.rescan_button.pack(side="left", padx=5)

# RIGHT SIDE - HISTORY

        right_frame = tk.Frame(main_frame, bg="#191c22", width=370)
        right_frame.pack(side="right", fill="y")
        right_frame.pack_propagate(False)

        history_title = tk.Label(
            right_frame,
            text="SCAN HISTORY",
            font=("Segoe UI", 13, "bold"),
            fg="white",
            bg="#191c22"
        )

        history_title.pack(
            anchor="w",
            padx=18,
            pady=(18, 2)
        )

        history_subtitle = tk.Label(
            right_frame,
            text="One result per image",
            font=("Segoe UI", 9),
            fg="#707784",
            bg="#191c22"
        )

        history_subtitle.pack(anchor="w", padx=18, pady=(0, 10))

# HISTORY LIST

        list_frame = tk.Frame(right_frame, bg="#191c22")
        list_frame.pack(fill="both", expand=True, padx=12)
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self.history_list = tk.Listbox(
            list_frame,
            bg="#111318",
            fg="#d1d5db",
            selectbackground="#2563eb",
            selectforeground="white",
            activestyle="none",
            font=("Segoe UI", 10),
            borderwidth=0,
            highlightthickness=0,
            yscrollcommand=scrollbar.set
        )

        self.history_list.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.history_list.yview)
        self.history_list.bind("<<ListboxSelect>>", self.on_history_select)

# HISTORY BUTTONS

        history_buttons = tk.Frame(right_frame, bg="#191c22")
        history_buttons.pack(fill="x", padx=15, pady=15)

        self.delete_button = tk.Button(
            history_buttons,
            text="Delete Selected",
            command=self.delete_selected,
            font=("Segoe UI", 9, "bold"),
            fg="white",
            bg="#7f1d1d",
            activebackground="#991b1b",
            activeforeground="white",
            relief="flat",
            padx=12,
            pady=8,
            cursor="hand2"
        )

        self.delete_button.pack(side="left", padx=(0, 5))

        self.clear_button = tk.Button(
            history_buttons,
            text="Clear History",
            command=self.clear_history,
            font=("Segoe UI", 9, "bold"),
            fg="white",
            bg="#374151",
            activebackground="#4b5563",
            activeforeground="white",
            relief="flat",
            padx=12,
            pady=8,
            cursor="hand2"
        )

        self.clear_button.pack(side="right")

# FILE SELECTION

    def select_image(self):

        path = filedialog.askopenfilename(title="Select an image",
            filetypes=
            [
                ("Image files", "*.jpg *.jpeg *.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("PNG files", "*.png"),
                ("All files", "*.*")
            ]
        )

        if path:
            self.evaluate_image(path)

# DRAG AND DROP

    def on_drop(self, event):

        files = self.tk.splitlist(event.data)
        if not files: return
        path = files[0]
        if os.path.isfile(path): self.evaluate_image(path)

# IMAGE EVALUATION

    def evaluate_image(self, image_path):

        if not os.path.exists(ARCOREIMG):

            messagebox.showerror("arcoreimg.exe not found", "Could not find arcoreimg.exe in:\n\n"
                + ARCOREIMG + "\n\n" "Make sure arcoreimg.exe is in the same folder as this program.")
            return

        extension = os.path.splitext(image_path)[1].lower()

        if extension not in [".jpg", ".jpeg", ".png"]:

            messagebox.showerror("Unsupported image", "Please use a JPG, JPEG, or PNG image.")
            return

        self.image_path = image_path
        self.show_preview(image_path)
        self.filename_label.config(text=os.path.basename(image_path))
        self.rating_label.config(text="Analyzing...", fg="#8d95a3")
        self.score_label.config(text="...", fg="white")
        self.update()

        try:

            result = subprocess.run(
                [
                    ARCOREIMG,
                    "eval-img",
                    "--input_image_path=" + image_path
                ],
                capture_output=True, text=True, timeout=30
            )

            output = result.stdout.strip()

            if result.returncode != 0:

                error = result.stderr.strip()

                messagebox.showerror("ARCore error", error
                    if error
                    else "arcoreimg returned an error."
                )

                self.score_label.config(text="-")

                self.rating_label.config(text="Evaluation failed", fg="#ef4444")

                return

            try:

                score = int(output)

            except ValueError:

                messagebox.showerror("Unexpected output", "arcoreimg returned:\n\n" + output)

                return

 # DISPLAY SCORE

            self.show_score(score)

# SAVE TO HISTORY
#
# Same filename = replace old result

            filename = os.path.basename(image_path)

            self.history[filename] = {"score": score, "path": os.path.abspath(image_path),
                "scanned_at": datetime.now().isoformat(timespec="seconds")}

            self.save_history()
            self.refresh_history_list()
            self.select_history_item(filename)

        except subprocess.TimeoutExpired:

            messagebox.showerror(
                "Timeout",
                "arcoreimg took too long to evaluate "
                "the image."
            )

            self.score_label.config(text="-")
            self.rating_label.config(text="Evaluation timed out", fg="#ef4444")

        except Exception as error:

            messagebox.showerror("Error", str(error))

# IMAGE PREVIEW

    def show_preview(self, image_path):

        try:

            image = Image.open(image_path)
            max_width = 560
            max_height = 430
            image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            self.current_image = ImageTk.PhotoImage(image)
            self.drop_label.config(image=self.current_image, text="")

        except Exception:

            self.drop_label.config(image="", text="Unable to preview image")

# SCORE DISPLAY

    def show_score(self, score):

        self.score_label.config(text=str(score) + " / 100")

        if score >= 75:

            self.score_label.config(fg="#22c55e")
            self.rating_label.config(text="EXCELLENT - Great ARCore target", fg="#22c55e")

        elif score >= 50:

            self.score_label.config(fg="#eab308")
            self.rating_label.config(text="FAIR - Could be improved", fg="#eab308")

        elif score >= 25:

            self.score_label.config(fg="#f97316")
            self.rating_label.config(text="POOR - Consider improving the image",fg="#f97316")

        else:

            self.score_label.config(fg="#ef4444")
            self.rating_label.config( text="VERY POOR - Difficult ARCore target", fg="#ef4444")

# RESCAN CURRENT IMAGE
  
    def rescan_selected(self):

         if not self.image_path:

                messagebox.showinfo("No image selected", "Select or drop an image first.")
                return

         if not os.path.exists(self.image_path):

                messagebox.showerror("Image not found", "The selected image no longer exists:\n\n" + self.image_path)
                return

         self.evaluate_image(self.image_path)

# START APPLICATION

if __name__ == "__main__":

    app = ARCoreImageTester()
    app.mainloop()