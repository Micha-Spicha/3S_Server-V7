import os
import sys
import subprocess
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk

# Function to get the path to the resources directory
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores paths in `_MEIPASS`
        base_path = sys._MEIPASS
    except AttributeError:
        # PyCharm and other dev environments
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

class ServerManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Server Manager")

        self.server_processes = [None, None]

        # Load and resize images
        self.bg_image = Image.open(resource_path('static/images/bg.png'))
        self.bg_image = ImageTk.PhotoImage(self.bg_image)

        self.logo_image = Image.open(resource_path('static/images/logo.png'))
        self.logo_image = self.logo_image.resize((50, 50), Image.Resampling.LANCZOS)
        self.logo_image = ImageTk.PhotoImage(self.logo_image)

        # Set background image
        self.bg_label = tk.Label(root, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)

        # Create and place widgets
        self.start_button1 = tk.Button(root, text="Start Scoring Server", command=self.start_server1)
        self.start_button1.grid(row=0, column=0, padx=10, pady=10)
        
        self.stop_button1 = tk.Button(root, text="Stop Scoring Server", command=self.stop_server1, state=tk.DISABLED)
        self.stop_button1.grid(row=0, column=1, padx=10, pady=10)
        
        self.start_button2 = tk.Button(root, text="Start MS Calc Server", command=self.start_server2)
        self.start_button2.grid(row=1, column=0, padx=10, pady=10)
        
        self.stop_button2 = tk.Button(root, text="Stop MS Calc Server", command=self.stop_server2, state=tk.DISABLED)
        self.stop_button2.grid(row=1, column=1, padx=10, pady=10)

        self.info_text1 = scrolledtext.ScrolledText(root, width=40, height=10, wrap=tk.WORD)
        self.info_text1.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        self.info_text1.insert(tk.END, "Scoring Server Output:\n")
        
        self.info_text2 = scrolledtext.ScrolledText(root, width=40, height=10, wrap=tk.WORD)
        self.info_text2.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        self.info_text2.insert(tk.END, "MS Calc Server Output:\n")

        # Port information
        self.port_info = tk.Label(root, text="Ports:\nScoring Server: 55807\nMS Calc Server: 5000", bg='white')
        self.port_info.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Set logo in header
        self.logo_label = tk.Label(root, image=self.logo_image)
        self.logo_label.grid(row=0, column=2, padx=10, pady=10)

    def start_server1(self):
        """ Start Scoring Server """
        if self.server_processes[0] is None:
            try:
                self.server_processes[0] = subprocess.Popen(
                    ["python", "app.py"], cwd=os.path.abspath("корневая папка"),
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                self.start_button1.config(state=tk.DISABLED)
                self.stop_button1.config(state=tk.NORMAL)
                self.update_output(self.info_text1, self.server_processes[0])
            except FileNotFoundError:
                print("Error: Scoring server script not found.")
            except NotADirectoryError:
                print("Error: Directory for Scoring server is invalid.")

    def stop_server1(self):
        """ Stop Scoring Server """
        if self.server_processes[0] is not None:
            self.server_processes[0].terminate()
            self.server_processes[0] = None
            self.start_button1.config(state=tk.NORMAL)
            self.stop_button1.config(state=tk.DISABLED)

    def start_server2(self):
        """ Start MS Calc Server """
        if self.server_processes[1] is None:
            try:
                self.server_processes[1] = subprocess.Popen(
                    ["python", "app.py"], cwd=os.path.abspath("ms-calc"),
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                self.start_button2.config(state=tk.DISABLED)
                self.stop_button2.config(state=tk.NORMAL)
                self.update_output(self.info_text2, self.server_processes[1])
            except FileNotFoundError:
                print("Error: MS Calc server script not found.")
            except NotADirectoryError:
                print("Error: Directory for MS Calc server is invalid.")

    def stop_server2(self):
        """ Stop MS Calc Server """
        if self.server_processes[1] is not None:
            self.server_processes[1].terminate()
            self.server_processes[1] = None
            self.start_button2.config(state=tk.NORMAL)
            self.stop_button2.config(state=tk.DISABLED)

    def update_output(self, text_widget, process):
        """ Update the output of the server in the text widget """
        def read_output():
            for line in iter(process.stdout.readline, b''):
                text_widget.insert(tk.END, line.decode())
                text_widget.yview(tk.END)
        self.root.after(100, read_output)

if __name__ == "__main__":
    root = tk.Tk()
    app = ServerManagerApp(root)
    root.mainloop()
