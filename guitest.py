import tkinter as tk
from tkinter import Label, Button, OptionMenu, StringVar
import os
from pydub import AudioSegment
from moviepy.editor import VideoFileClip
from PIL import Image

# Supported formats for conversion
audio_formats = ['mp3', 'wav', 'flac']
video_formats = ['mp4', 'mov', 'webm']
image_formats = ['png', 'jpg', 'bmp']

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

def get_conversion_options(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext in ['.mp3', '.wav', '.flac']:
        return [fmt for fmt in audio_formats if f".{fmt}" != ext]
    elif ext in ['.mp4', '.mov', '.webm']:
        return [fmt for fmt in video_formats if f".{fmt}" != ext]
    elif ext in ['.png', '.jpg', '.bmp']:
        return [fmt for fmt in image_formats if f".{fmt}" != ext]
    else:
        return []

def convert_file(file_path, target_format):
    ext = os.path.splitext(file_path)[1].lower()
    if ext in ['.mp3', '.wav', '.flac']:
        convert_audio(file_path, target_format)
    elif ext in ['.mp4', '.mov', '.webm']:
        convert_video(file_path, target_format)
    elif ext in ['.png', '.jpg', '.bmp']:
        convert_image(file_path, target_format)
    else:
        print("Unsupported file format for conversion.")

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
    selected_format.set(conversion_options[0])
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
