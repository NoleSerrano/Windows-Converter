from pydub import AudioSegment
from moviepy.editor import VideoFileClip
from PIL import Image
import os
import sys
import winreg as reg
from tkinter import Tk, Label, Button, OptionMenu, StringVar

audio_formats = ['mp3']
# audio_formats = ['mp3', 'wav', 'flac']
# video_formats = ['mp4', 'mov', 'webm']
# image_formats = ['png', 'jpg']

# -- REGISTRY FUNCTIONS -- START
def add_to_registry():
    key_path = r"Software\Classes\*\shell\Convert"
    command = f'"{sys.executable}" "{os.path.abspath(__file__)}" "%1"'
    
    with reg.ConnectRegistry(None, reg.HKEY_CURRENT_USER) as hkey:
        with reg.CreateKey(hkey, key_path) as key:
            reg.SetValue(key, '', reg.REG_SZ, 'Convert')
            with reg.CreateKey(hkey, f"{key_path}\\command") as command_key:
                reg.SetValue(command_key, '', reg.REG_SZ, command)

    print("Registry updated successfully.")

def remove_from_registry():
    try:
        with reg.ConnectRegistry(None, reg.HKEY_CURRENT_USER) as hkey:
            reg.DeleteKey(hkey, r"Software\Classes\*\shell\Convert\command")
            reg.DeleteKey(hkey, r"Software\Classes\*\shell\Convert")
        print("Registry entries removed successfully.")
    except FileNotFoundError:
        print("The registry entries were not found.")
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

# Main Execution Logic
if __name__ == "__main__":
    if len(sys.argv) == 2:
        file_path = sys.argv[1]
        open_conversion_gui(file_path)
    else:
        # No file path provided, add to registry
        add_to_registry()  # Run this to setup or remove_from_registry() to clear old entries
