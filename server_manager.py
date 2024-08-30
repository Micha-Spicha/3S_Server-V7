import tkinter as tk
from tkinter import messagebox
import subprocess
import os

class ServerManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Server Manager")
        self.root.geometry("400x300")
        
        self.process1 = None
        self.process2 = None

        self.create_widgets()

    def create_widgets(self):
        # Use absolute path for background image
        script_dir = os.path.dirname(os.path.abspath(__file__))
        bg_image_path = os.path.join(script_dir, 'static', 'images', 'bg.png')

        try:
            bg_image = tk.PhotoImage(file=bg_image_path)
            bg_label = tk.Label(self.root, image=bg_image)
            bg_label.place(relwidth=1, relheight=1)
            # Keep a reference to the image to prevent garbage collection
            bg_label.image = bg_image
        except tk.TclError:
            print(f"Error: Unable to open image file '{bg_image_path}'")

        # Scoring Server Button
        self.scoring_server_button = tk.Button(self.root, text="Start Scoring Server", command=self.toggle_scoring_server)
        self.scoring_server_button.pack(pady=10)

        # MS Calc Server Button
        self.ms_calc_server_button = tk.Button(self.root, text="Start MS Calc Server", command=self.toggle_ms_calc_server)
        self.ms_calc_server_button.pack(pady=10)

        # Status
        self.status_label = tk.Label(self.root, text="Server Status: Scoring Server OFF | MS Calc Server OFF")
        self.status_label.pack(pady=10)

    def toggle_scoring_server(self):
        if self.process1 is None:
            self.process1 = subprocess.Popen(['python', 'app.py'], cwd=os.path.dirname(os.path.abspath(__file__)))
            self.scoring_server_button.config(text="Stop Scoring Server")
            self.update_status()
        else:
            self.process1.terminate()
            self.process1 = None
            self.scoring_server_button.config(text="Start Scoring Server")
            self.update_status()

    def toggle_ms_calc_server(self):
        if self.process2 is None:
            self.process2 = subprocess.Popen(['python', 'ms-calc/app.py'], cwd=os.path.dirname(os.path.abspath(__file__)))
            self.ms_calc_server_button.config(text="Stop MS Calc Server")
            self.update_status()
        else:
            self.process2.terminate()
            self.process2 = None
            self.ms_calc_server_button.config(text="Start MS Calc Server")
            self.update_status()

    def update_status(self):
        scoring_server_status = "ON" if self.process1 is not None else "OFF"
        ms_calc_server_status = "ON" if self.process2 is not None else "OFF"
        self.status_label.config(text=f"Server Status: Scoring Server {scoring_server_status} | MS Calc Server {ms_calc_server_status}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ServerManagerApp(root)
    root.mainloop()
