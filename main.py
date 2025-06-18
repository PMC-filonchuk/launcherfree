import tkinter as tk
import subprocess
import os

# Укажи путь к HMCL (проверь, где у тебя лежит HMCL.jar)
HMCL_PATH = r"C:\Users\User\Downloads\HMCL-3.5.9.262.exe"  # или .jar, если ты качал .jar

def launch_hmcl():
    try:
        subprocess.Popen(HMCL_PATH, shell=True)
        print("HMCL запущен.")
    except Exception as e:
        print("Ошибка запуска:", e)

# GUI
root = tk.Tk()
root.title("Лаунчер Minecraft")

tk.Label(root, text="Нажми кнопку для запуска HMCL").pack(pady=10)
tk.Button(root, text="🚀 Запустить HMCL", command=launch_hmcl).pack(pady=10)

root.mainloop()
