import tkinter as tk
from tkinter import ttk, messagebox
import os
import subprocess

LAUNCHER_VERSION = "1.0"

# Укажи путь к .minecraft
MINECRAFT_DIR = r"C:\Users\User\AppData\Roaming\.minecraft"
VERSIONS_DIR = os.path.join(MINECRAFT_DIR, "versions")

def get_versions():
    if not os.path.exists(VERSIONS_DIR):
        return []
    return [folder for folder in os.listdir(VERSIONS_DIR)
            if os.path.isdir(os.path.join(VERSIONS_DIR, folder))]

def run_hmcl():
    nickname = entry_nick.get()
    memory = combo_memory.get()
    version = combo_version.get()

    # Путь к HMCL.jar
    hmcl_path = os.path.join(os.getcwd(), "HMCL.jar")

    if not os.path.exists(hmcl_path):
        messagebox.showerror("Ошибка", f"Файл HMCL.jar не найден:\n{hmcl_path}")
        return

    command = [
        "java",
        f"-Xmx{memory}",
        "-jar",
        hmcl_path,
        "--username", nickname,
        "--version", version
    ]

    try:
        subprocess.Popen(command)
        messagebox.showinfo("Успех", f"Minecraft {version} запускается...")
    except Exception as e:
        messagebox.showerror("Ошибка запуска", str(e))

# GUI
root = tk.Tk()
root.title("Volonia Launcher")
root.geometry("360x300")

tk.Label(root, text="🧑 Никнейм:").pack(pady=(10, 5))
entry_nick = tk.Entry(root, justify="center")
entry_nick.insert(0, "Player123")
entry_nick.pack()

tk.Label(root, text="💾 Память:").pack(pady=(10, 5))
combo_memory = ttk.Combobox(root, values=["1G", "2G", "4G", "8G"], state="readonly")
combo_memory.set("2G")
combo_memory.pack()

tk.Label(root, text="🎮 Версия Minecraft:").pack(pady=(10, 5))
combo_version = ttk.Combobox(root, values=get_versions(), state="readonly")
combo_version.set("1.21.1" if "1.21.1" in get_versions() else (get_versions()[0] if get_versions() else ""))
combo_version.pack()

tk.Button(root, text="🚀 Запустить", command=run_hmcl, height=2, width=30).pack(pady=20)

root.mainloop()
