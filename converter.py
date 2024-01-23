from pydub import AudioSegment
from moviepy.editor import VideoFileClip
from PIL import Image
import os
import sys
import winreg as reg
from tkinter import Tk, Label, Button, OptionMenu, StringVar
import tkinter as tk

audio_formats = ['mp3']
video_formats = []
image_formats = []

# audio_formats = ['mp3', 'wav', 'flac']
# video_formats = ['mp4', 'mov', 'webm']
# image_formats = ['png', 'jpg']
# Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Classes\SystemFileAssociations\.mp3

# -- REGISTRY FUNCTIONS -- START
def add_to_registry():
    for media_type in (audio_formats + video_formats + image_formats):
        key_path = rf"SOFTWARE\Classes\SystemFileAssociations\.{media_type}\shell\Convert"
        command = f'"{sys.executable}" "{os.path.abspath(__file__)}" "%1"'
        
        with reg.ConnectRegistry(None, reg.HKEY_LOCAL_MACHINE) as hkey:
            with reg.CreateKey(hkey, key_path) as key:
                reg.SetValue(key, '', reg.REG_SZ, 'Convert')
                with reg.CreateKey(hkey, f"{key_path}\\command") as command_key:
                    reg.SetValue(command_key, '', reg.REG_SZ, command)

    print("Registry updated successfully.")

def remove_from_registry():
    for media_type in (audio_formats + video_formats + image_formats):
        try:
            with reg.ConnectRegistry(None, reg.HKEY_LOCAL_MACHINE) as hkey:
                reg.DeleteKey(hkey, rf"SOFTWARE\Classes\SystemFileAssociations\.{media_type}\shell\Convert\command")
                reg.DeleteKey(hkey, rf"SOFTWARE\Classes\SystemFileAssociations\.{media_type}\shell\Convert")
            print(f"Registry entries removed for .{media_type}")
        except FileNotFoundError:
            print(f"No registry entries found for .{media_type}")
# -- REGISTRY FUNCTIONS -- END

def convert_file(file_path, target_format):
    print(f"Converting {file_path} to {target_format}")
    # Add your conversion logic here

# Tkinter GUI for Conversion
def open_conversion_gui(file_path):
    root = Tk()
    root.title("Convert File")

    Label(root, text="Choose format to convert to:").pack()

    # Combine all formats and remove the original format from the list
    all_formats = list(set(audio_formats))
    original_format = os.path.splitext(file_path)[1].lstrip('.').lower()
    try:
        all_formats.remove(original_format)
    except ValueError:
        pass  # Original format is not in the list

    # StringVar to hold the selected format
    selected_format = StringVar(root)
    selected_format.set(all_formats[0])  # default value

    # Dropdown menu for format selection
    OptionMenu(root, selected_format, *all_formats).pack()

    # Function to call conversion logic and close GUI
    def on_convert():
        convert_file(file_path, selected_format.get())
        root.destroy()

    # Convert button
    Button(root, text="Convert", command=on_convert).pack()

    root.mainloop()



# old conversion functions
def convert_audio(file_path, target_format):
    audio = AudioSegment.from_file(file_path)
    output_file = f"{os.path.splitext(file_path)[0]}.{target_format}"
    audio.export(output_file, format=target_format)
    print(f"Audio file converted successfully: {output_file}")

def convert_video(file_path, target_format):
    video = VideoFileClip(file_path)
    output_file = f"{os.path.splitext(file_path)[0]}.{target_format}"
    video.write_videofile(output_file)
    print(f"Video file converted successfully: {output_file}")

def convert_image(file_path, target_format):
    image = Image.open(file_path)
    output_file = f"{os.path.splitext(file_path)[0]}.{target_format}"
    image.save(output_file)
    print(f"Image file converted successfully: {output_file}")

# TEST function so know code is working
def touch(file_path):
    os.utime(file_path)

def on_button_click():
    label.config(text="Button clicked!")

def gui():
    # Create the main window
    root = tk.Tk()
    root.title("GUI Test")

    # Create a label
    global label
    label = tk.Label(root, text="Hello, Tkinter!")
    label.pack()

    # Create a button
    button = tk.Button(root, text="Click Me", command=on_button_click)
    button.pack()

    # Start the event loop
    root.mainloop()

# Main Execution Logic
if __name__ == "__main__":
    if len(sys.argv) == 2:
        file_path = sys.argv[1]
        touch(file_path)
        # open_conversion_gui(file_path)
        gui()
    else:
        # No file path provided, add to registry
        add_to_registry()  # Run this to setup or remove_from_registry() to clear old entries
