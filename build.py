import PyInstaller.__main__
import os
import shutil

APP_NAME = "DarkSoulsNotify"
ENTRY_POINT = "src/main.py"
ICON_PATH = "src/assets/icon.png"

ASSETS = [
    ("src/assets", "assets") 
]

def clean_build_folders():
    folders = ["build", "dist"]
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)
    
    spec_file = f"{APP_NAME}.spec"
    if os.path.exists(spec_file):
        os.remove(spec_file)

def build():
    print("--- STARTING BUILD ---")
    clean_build_folders()

    args = [
        ENTRY_POINT,
        f"--name={APP_NAME}",
        "--onefile",
        "--noconsole",
        f"--icon={ICON_PATH}",
        "--clean",
        # We removed the watchdog hidden import :)
    ]

    for source, dest in ASSETS:
        args.append(f"--add-data={source};{dest}")

    PyInstaller.__main__.run(args)
    print(f"\n[Success] Build complete! Check 'dist/{APP_NAME}.exe'")

if __name__ == "__main__":
    build()