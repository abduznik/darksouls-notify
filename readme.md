# Dark Souls Notification - Python

![Example Notification](sources/example.jpg)

A background Python script that brings the iconic Dark Souls notification banners to your Windows desktop. It listens to system events—like saving a file or switching windows—and triggers a "BONFIRE LIT" style popup with sound.

## Features
* **Progress Saved:** Triggers when you press **Ctrl+S** in supported apps (VS Code, Notepad, Blender, etc.).
* **Area Discovered:** Triggers when you switch active windows.
* **Humanity Restored:** Triggers when you switch specifically to a coding IDE.
* **System Tray:** Runs silently in the background with a tray icon to Quit.
* **Non-Intrusive:** Notifications are click-through and fade in/out smoothly without stealing focus.

## Setup & Running

1.  **Clone the repository.**
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the script:**
    ```bash
    cd src
    python main.py
    ```

## Building the Executable (.exe)

To create a standalone portable `.exe` file that works on any Windows machine without Python installed:

1.  **Install build tools:**
    ```bash
    pip install -r requirements-dev.txt
    ```
2.  **Run the build script:**
    ```bash
    python build.py
    ```
3.  **Find your App:**
    The generic executable will be located in the `dist/` folder.

## Configuration

You can customize which apps trigger the "Progress Saved" notification by editing `src/options.py`.

```python
# src/options.py
WATCHED_APPS = [
    "VS Code",
    "Blender",
    "Unity",
    # Add your apps here...
]

```

## Contributing

I am looking for more creative triggers! If you have ideas for system events to track (e.g., battery low, specific time of day, git push), please contribute.

* **`src/options.py`**: Adjust probabilities, colors, and text.
* **`src/triggers.py`**: Add your own logic to the `EventManager` class.

## Project Structure

```text
/
├── build.py           # One-click build script
├── requirements.txt   # Runtime dependencies
├── requirements-dev.txt # Build dependencies
├── readme.md
└── src/
    ├── assets/        # Font, Icon, and Sound files
    ├── main.py        # Entry point
    ├── tray.py        # System Tray logic
    ├── notifier.py    # UI / Animation Logic
    ├── options.py     # Settings & App Lists
    └── triggers.py    # Event listeners (Keyboard & Window hooks)

```
