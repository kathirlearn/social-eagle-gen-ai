import os
import shutil
import pyautogui
import time

# Safety first
pyautogui.FAILSAFE = True

# Get Desktop path (macOS)
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# File organization rules
folders = {
    "Images": [".png", ".jpg", ".jpeg"],
    "Documents": [".pdf", ".docx", ".txt"],
    "Videos": [".mp4", ".mov"],
    "Archives": [".zip", ".rar"]
}

# Create folders if they don't exist
for folder in folders:
    folder_path = os.path.join(desktop_path, folder)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

# Organize desktop files
for file in os.listdir(desktop_path):
    file_path = os.path.join(desktop_path, file)

    if os.path.isfile(file_path):
        for folder, extensions in folders.items():
            if file.lower().endswith(tuple(extensions)):
                shutil.move(file_path, os.path.join(desktop_path, folder, file))
                break

# Visual refresh (Finder)
time.sleep(1)
pyautogui.hotkey('command', 'option', 'escape')  # Open Force Quit (visual cue)
time.sleep(1)
pyautogui.press('esc')  # Close it

print("✅ Desktop cleanup completed on macOS!")
