import os
import subprocess


def launch_minecraft_offline():
    username = "ТвойНик"  # заменяй на нужный ник
    version = "1.21.1"

    # Путь к папке .minecraft — подставь свой!
    minecraft_dir = r"C:\Users\User\AppData\Roaming\.minecraft"

    version_dir = os.path.join(minecraft_dir, "versions", version)
    jar_path = os.path.join(version_dir, f"{version}.jar")

    if not os.path.exists(jar_path):
        print(f"Файл {jar_path} не найден")
        return

    # Собираем classpath из jar версии и библиотек
    libraries_dir = os.path.join(minecraft_dir, "libraries")
    classpath_parts = []

    for root, dirs, files in os.walk(libraries_dir):
        for file in files:
            if file.endswith(".jar"):
                classpath_parts.append(os.path.join(root, file))
    classpath_parts.append(jar_path)

    classpath = ";".join(classpath_parts)

    java_command = [
        "java",
        "-Xmx2G",
        "-cp", classpath,
        "net.minecraft.client.main.Main",
        "--username", username,
        "--version", version,
        "--gameDir", minecraft_dir,
        "--assetsDir", os.path.join(minecraft_dir, "assets")
    ]

    try:
        subprocess.Popen(java_command, cwd=version_dir)
        print("Minecraft запускается в офлайн режиме...")
    except Exception as e:
        print("Ошибка запуска:", e)


if __name__ == "__main__":
    launch_minecraft_offline()
