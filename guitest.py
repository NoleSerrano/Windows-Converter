import tkinter as tk
from tkinter import Label, Button, OptionMenu, StringVar
import os

# Supported formats for conversion
audio_formats = ['mp3', 'wav', 'flac']
video_formats = ['mp4', 'mov', 'webm']
image_formats = ['png', 'jpg', 'bmp']

def get_conversion_options(file_path):
    """ Determine the file type and return the appropriate conversion options """
    ext = os.path.splitext(file_path)[1].lower()
    if ext in ['.mp3', '.wav', '.flac']:
        return [fmt for fmt in audio_formats if fmt != ext]
    elif ext in ['.mp4', '.mov', '.webm']:
        return [fmt for fmt in video_formats if fmt != ext]
    elif ext in ['.png', '.jpg', '.bmp']:
        return [fmt for fmt in image_formats if fmt != ext]
    else:
        return []  # No conversion options available for this file type

def convert_file(file_path, target_format):
    # Placeholder for conversion logic
    print(f"Converting {file_path} to {target_format}...")
    # Implement actual conversion code here

def open_conversion_gui(file_path):
    root = tk.Tk()
    root.title("Convert File")

    conversion_options = get_conversion_options(file_path)

    if not conversion_options:
        label = tk.Label(root, text="No available formats for conversion.")
        label.pack()
        return

    label = tk.Label(root, text="Choose format to convert to:")
    label.pack()

    selected_format = StringVar(root)
    selected_format.set(conversion_options[0])  # Set default value

    format_menu = OptionMenu(root, selected_format, *conversion_options)
    format_menu.pack()

    def on_convert():
        convert_file(file_path, selected_format.get())
        root.destroy()

    convert_button = tk.Button(root, text="Convert", command=on_convert)
    convert_button.pack()

    root.mainloop()

# Example file path for testing
test_file_path = 'input.mp3'  # Replace with the actual file path
open_conversion_gui(test_file_path)
