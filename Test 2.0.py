# =====================================
# Modern Network Utility Toolkit (B3 Polished GUI)
# =====================================

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import socket
import requests
import paramiko

# =====================================
# Remote SSH Credentials
# =====================================

REMOTE_HOST = "192.168.1.124"
REMOTE_USER = "testuser"
REMOTE_PASS = "password1"


# =====================================
# Main Application Window
# =====================================

app = tk.Tk()
app.title("Network Utility Toolkit")
app.geometry("1100x650")
app.configure(bg="#202124")
app.minsize(950, 600)


# =====================================
# Styles (Modern Look)
# =====================================

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Sidebar.TButton",
    font=("Segoe UI", 11, "bold"),
    padding=10,
    width=25,
    background="#303134",
    foreground="white"
)

style.map("Sidebar.TButton",
          background=[("active", "#424346")])

style.configure(
    "Output.TFrame",
    background="#1E1E1E"
)


# =====================================
# Layout Frames
# =====================================

# Sidebar (Left)
sidebar = tk.Frame(app, bg="#2A2B2D", width=260)
sidebar.pack(side=tk.LEFT, fill=tk.Y)

# Main Output Area (Right)
main_frame = ttk.Frame(app, style="Output.TFrame")
main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)


# =====================================
# Output Window
# =====================================

output_scroll = tk.Scrollbar(main_frame)
output_scroll.pack(side=tk.RIGHT, fill=tk.Y)

OutputBox = tk.Text(
    main_frame,
    bg="#000000",
    fg="#00FF00",
    insertbackground="white",
    font=("Consolas", 11),
    yscrollcommand=output_scroll.set
)
OutputBox.pack(fill=tk.BOTH, expand=True)

output_scroll.config(command=OutputBox.yview)


# =====================================
# Input Field (Bottom)
# =====================================

input_frame = tk.Frame(app, bg="#202124")
input_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=8)

tk.Label(
    input_frame,
    text="Input:",
    bg="#202124",
    fg="white",
    font=("Segoe UI", 11, "bold")
).pack(side=tk.LEFT, padx=5)

InputBox = tk.Entry(input_frame, width=60, font=("Segoe UI", 10))
InputBox.pack(side=tk.LEFT, padx=10)


# =====================================
# Functions
# =====================================

def show_time():
    now = datetime.now().strftime("%H:%M:%S  %d-%m-%Y")
    OutputBox.insert(tk.END, f"[TIME] {now}\n\n")


def show_ip():
    ip = socket.gethostbyname(socket.gethostname())
    OutputBox.insert(tk.END, f"[LOCAL IP] {ip}\n\n")


def list_remote_home():
    try:
        OutputBox.insert(tk.END, f"[SSH] Connecting to {REMOTE_HOST}...\n")

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(REMOTE_HOST, username=REMOTE_USER, password=REMOTE_PASS)

        stdin, stdout, stderr = ssh.exec_command("ls -la ~")

        output = stdout.read().decode()
        error = stderr.read().decode()

        if error:
            OutputBox.insert(tk.END, f"[SSH ERROR] {error}\n\n")
        else:
            OutputBox.insert(tk.END, f"\n===== HOME DIRECTORY ({REMOTE_USER}) =====\n")
            OutputBox.insert(tk.END, output)
            OutputBox.insert(tk.END, "===========================================\n\n")

        ssh.close()

    except Exception as e:
        OutputBox.insert(tk.END, f"[SSH ERROR] {e}\n\n")


def backup_remote_file():
    path = InputBox.get().strip()

    if not path:
        messagebox.showwarning("Input Needed", "Enter a remote file path first.")
        return

    try:
        OutputBox.insert(tk.END, f"[BACKUP] Backing up: {path}\n")

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(REMOTE_HOST, username=REMOTE_USER, password=REMOTE_PASS)

        backup_cmd = f"cp '{path}' '{path}.old'"
        _, stdout, stderr = ssh.exec_command(backup_cmd)

        error = stderr.read().decode()

        if error:
            OutputBox.insert(tk.END, f"[ERROR] {error}\n\n")
        else:
            OutputBox.insert(tk.END, f"[SUCCESS] Backup created → {path}.old\n\n")

        ssh.close()

    except Exception as e:
        OutputBox.insert(tk.END, f"[SSH ERROR] {e}\n\n")


def save_web_page():
    url = InputBox.get().strip()

    if not url:
        messagebox.showwarning("Input Missing", "Enter a URL first.")
        return

    try:
        OutputBox.insert(tk.END, f"[WEB] Downloading '{url}'...\n")

        response = requests.get(url, timeout=10)
        filename = "saved_page.html"

        with open(filename, "w", encoding="utf-8") as file:
            file.write(response.text)

        OutputBox.insert(tk.END, f"[SUCCESS] Web page saved → {filename}\n\n")

    except Exception as e:
        OutputBox.insert(tk.END, f"[WEB ERROR] {e}\n\n")


def quit_program():
    if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
        app.quit()


# =====================================
# Sidebar Buttons
# =====================================

def add_button(label, cmd):
    ttk.Button(sidebar, text=label, command=cmd, style="Sidebar.TButton")\
        .pack(pady=10, padx=20, fill=tk.X)


add_button("Show Date & Time", show_time)
add_button("Show Local IP", show_ip)
add_button("List Remote Home Dir", list_remote_home)
add_button("Backup Remote File", backup_remote_file)
add_button("Save Web Page", save_web_page)
add_button("Quit", quit_program)


# =====================================
# Run App
# =====================================

app.mainloop()
