import PyInstaller.__main__
import os
import shutil
import sys

APP_NAME = "DarkSoulsNotify"
ENTRY_POINT = "src/main.py"
ICON_PATH = "src/assets/icon.png"

ASSETS = [
    ("src/assets", "assets")
]

EXE_SUFFIX = ".exe" if sys.platform.startswith("win") else ""

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
        "--clean",
    ]

    # PyInstaller only accepts .ico on Windows and .icns on macOS;
    # the bundled icon is a .png, so only use it on Windows.
    if sys.platform.startswith("win"):
        args.append(f"--icon={ICON_PATH}")

    for source, dest in ASSETS:
        args.append(f"--add-data={source}{os.pathsep}{dest}")

    PyInstaller.__main__.run(args)
    print(f"\n[Success] Build complete! Check 'dist/{APP_NAME}{EXE_SUFFIX}'")

if __name__ == "__main__":
    build()
