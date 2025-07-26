import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import zipfile

# Пути
MINECRAFT_DIR = r"C:\vlm\.minecraft"
VERSIONS_DIR = os.path.join(MINECRAFT_DIR, "versions")
LIBRARIES_DIR = os.path.join(MINECRAFT_DIR, "libraries")

# Получение списка версий
def get_versions():
    if not os.path.exists(VERSIONS_DIR):
        return []
    return [v for v in os.listdir(VERSIONS_DIR) if os.path.isdir(os.path.join(VERSIONS_DIR, v))]

# Распаковка natives
def extract_natives(version):
    natives_path = os.path.join(VERSIONS_DIR, version, "natives")
    if os.path.exists(natives_path) and os.listdir(natives_path):
        return natives_path  # Уже распаковано

    os.makedirs(natives_path, exist_ok=True)

    for root, dirs, files in os.walk(LIBRARIES_DIR):
        for file in files:
            if "natives" in file and file.endswith(".jar"):
                jar_path = os.path.join(root, file)
                try:
                    with zipfile.ZipFile(jar_path, 'r') as zip_ref:
                        for member in zip_ref.namelist():
                            if member.endswith(".dll") or member.endswith(".so"):
                                zip_ref.extract(member, natives_path)
                except Exception as e:
                    print(f"Ошибка при распаковке {file}: {e}")
    return natives_path

# Запуск Minecraft
def launch_minecraft():
    nick = entry_nick.get().strip()
    version = version_combo.get().strip()

    if not nick:
        messagebox.showerror("Ошибка", "Введите ник.")
        return
    if not version:
        messagebox.showerror("Ошибка", "Выберите версию.")
        return

    jar = os.path.join(VERSIONS_DIR, version, f"{version}.jar")
    if not os.path.exists(jar):
        messagebox.showerror("Ошибка", f"Файл {version}.jar не найден:\n{jar}")
        return

    # Собираем classpath
    classpath = [jar]
    for root, dirs, files in os.walk(LIBRARIES_DIR):
        for file in files:
            if file.endswith(".jar"):
                classpath.append(os.path.join(root, file))
    classpath_str = ";".join(classpath)

    # Распаковка natives
    native_path = extract_natives(version)

    # Команда запуска
    command = [
        "java",
        "-Xmx2G",
        f"-Djava.library.path={native_path}",
        "-cp", classpath_str,
        "net.minecraft.client.main.Main",
        "--username", nick,
        "--version", version,
        "--accessToken", "0",
        "--gameDir", MINECRAFT_DIR,
        "--assetsDir", os.path.join(MINECRAFT_DIR, "assets"),
        "--assetIndex", version,
        "--uuid", "0",
        "--userType", "legacy"
    ]

    try:
        proc = subprocess.Popen(command, cwd=os.path.join(VERSIONS_DIR, version),
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        out, err = proc.communicate(timeout=20)
        print("stdout:", out)
        print("stderr:", err)

        if proc.returncode != 0:
            messagebox.showerror("Ошибка запуска", err)
        else:
            messagebox.showinfo("Успех", f"Minecraft {version} запускается...")
    except subprocess.TimeoutExpired:
        messagebox.showinfo("Успех", f"Minecraft {version} запущен.")
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

# Интерфейс GUI
root = tk.Tk()
root.title("Volonia Launcher")
root.geometry("340x200")

tk.Label(root, text="Введите ник:").pack(pady=(10, 0))
entry_nick = tk.Entry(root)
entry_nick.pack(pady=5, fill="x", padx=10)

tk.Label(root, text="Выберите версию:").pack()
version_combo = ttk.Combobox(root, values=get_versions(), state="readonly")
version_combo.pack(pady=5, fill="x", padx=10)

btn_launch = tk.Button(root, text="🚀 Запустить Minecraft", command=launch_minecraft)
btn_launch.pack(pady=15)

tk.Label(root, text=f".minecraft путь:\n{MINECRAFT_DIR}", font=("Arial", 8)).pack(pady=(0, 10))

root.mainloop()





