from pydub import AudioSegment
from moviepy.editor import VideoFileClip
from PIL import Image
import os
import sys
import winreg as reg
from tkinter import Tk, Label, Button, OptionMenu, StringVar
import tkinter as tk

# audio_formats = ['mp3']
# video_formats = []
# image_formats = []
# Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Classes\SystemFileAssociations\.mp3

audio_formats = ['mp3', 'wav', 'flac']
video_formats = ['mp4', 'mov', 'webm']
image_formats = ['png', 'jpg', 'bmp']

def get_unique_filename(base_path, ext):
    counter = 1
    new_path = f"{base_path} ({counter}).{ext}"
    while os.path.exists(new_path):
        counter += 1
        new_path = f"{base_path} ({counter}).{ext}"
    return new_path

def get_output_filename(file_path, target_format):
    base = os.path.splitext(file_path)[0]
    output_file = f"{base}.{target_format}"
    # If the target file already exists, create a unique filename
    if os.path.exists(output_file):
        return get_unique_filename(base, target_format)

    return output_file
    
def convert_audio(file_path, target_format, output_file):
    audio = AudioSegment.from_file(file_path)
    audio.export(output_file, format=target_format)
    print(f"Audio file converted successfully: {output_file}")

def convert_video(file_path, target_format, output_file):
    video = VideoFileClip(file_path)
    video.write_videofile(output_file)
    print(f"Video file converted successfully: {output_file}")

def convert_image(file_path, target_format, output_file):
    image = Image.open(file_path)
    image.save(output_file)
    print(f"Image file converted successfully: {output_file}")

def convert_file(file_path, target_format):
    ext = os.path.splitext(file_path)[1].lower()
    output_file = get_output_filename(file_path, target_format)
    print(output_file)
    if ext in ['.mp3', '.wav', '.flac']:
        convert_audio(file_path, target_format, output_file)
    elif ext in ['.mp4', '.mov', '.webm']:
        convert_video(file_path, target_format, output_file)
    elif ext in ['.png', '.jpg', '.bmp']:
        convert_image(file_path, target_format, output_file)
    else:
        print("Unsupported file format for conversion.")

def open_conversion_gui(file_path):
    root = tk.Tk()
    root.title("Convert File")

    # Determine the file type based on its extension
    ext = os.path.splitext(file_path)[1].lower().lstrip('.')
    if ext in audio_formats:
        conversion_options = audio_formats
    elif ext in video_formats:
        conversion_options = video_formats
    elif ext in image_formats:
        conversion_options = image_formats
    else:
        label = tk.Label(root, text="Unsupported file format for conversion.")
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

# TEST function so know code is working
def touch(file_path):
    os.utime(file_path)

# Main Execution Logic
if __name__ == "__main__":
    if len(sys.argv) == 2:
        file_path = sys.argv[1]
        # touch(file_path)
        # open_conversion_gui(file_path)
        open_conversion_gui(file_path)
