import urllib.request
import os
import sys
import time
import shutil

URL = "https://твоя_ссылка/VoloniaLauncher.exe"  # заменишь на свой линк
NEW_FILE = "VoloniaLauncher_new.exe"
FINAL_FILE = "VoloniaLauncher.exe"

def download_new_version():
    print("Скачиваем новую версию...")
    urllib.request.urlretrieve(URL, NEW_FILE)
    print("Скачано.")

def replace_and_restart():
    time.sleep(1)  # Дать время завершиться главному лаунчеру
    if os.path.exists(FINAL_FILE):
        os.remove(FINAL_FILE)
    shutil.move(NEW_FILE, FINAL_FILE)
    print("Запуск новой версии...")
    os.startfile(FINAL_FILE)
    sys.exit()

if __name__ == "__main__":
    download_new_version()
    replace_and_restart()
