import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import subprocess
import threading
import os
import re

class ServerManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Server Manager")
        
        self.server_processes = [None, None]
        
        # Load and resize images
        self.bg_image = Image.open('static/images/bg.png')
        self.bg_image = ImageTk.PhotoImage(self.bg_image)

        self.logo_image = Image.open('static/images/logo.png')
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
        if not self.server_processes[0]:
            self.server_processes[0] = subprocess.Popen(['python', 'app.py'], cwd=os.getcwd(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            threading.Thread(target=self.read_output, args=(0,)).start()
            self.start_button1.config(state=tk.DISABLED)
            self.stop_button1.config(state=tk.NORMAL)

    def stop_server1(self):
        if self.server_processes[0]:
            self.server_processes[0].terminate()
            self.server_processes[0] = None
            self.start_button1.config(state=tk.NORMAL)
            self.stop_button1.config(state=tk.DISABLED)

    def start_server2(self):
        if not self.server_processes[1]:
            self.server_processes[1] = subprocess.Popen(['python', 'app.py'], cwd='ms-calc', stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            threading.Thread(target=self.read_output, args=(1,)).start()
            self.start_button2.config(state=tk.DISABLED)
            self.stop_button2.config(state=tk.NORMAL)

    def stop_server2(self):
        if self.server_processes[1]:
            self.server_processes[1].terminate()
            self.server_processes[1] = None
            self.start_button2.config(state=tk.NORMAL)
            self.stop_button2.config(state=tk.DISABLED)

    def read_output(self, server_index):
        process = self.server_processes[server_index]
        output_stream = process.stdout
        error_stream = process.stderr
        while True:
            output = output_stream.readline()
            error = error_stream.readline()
            if output:
                self.display_output(server_index, output)
            if error:
                self.display_output(server_index, error)
            if process.poll() is not None and not (output or error):
                break

    def display_output(self, server_index, message):
        if server_index == 0:
            self.info_text1.insert(tk.END, message)
            self.info_text1.yview(tk.END)
        else:
            self.info_text2.insert(tk.END, message)
            self.info_text2.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ServerManagerApp(root)
    root.mainloop()
