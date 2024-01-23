from pydub import AudioSegment
from moviepy.editor import VideoFileClip
from PIL import Image
import os
import sys
import reg

audio_formats = ['mp3', 'wav', 'flac']
video_formats = ['mp4', 'mov', 'webm']
image_formats = ['png', 'jpg']

# -- REGISTRY FUNCTIONS -- START
def add_conversion_options(media_formats):
    with reg.ConnectRegistry(None, reg.HKEY_LOCAL_MACHINE) as hkey:
        for format in media_formats:
            key_path = rf"SOFTWARE\Classes\SystemFileAssociations\.{format}\shell\Convert"
            with reg.CreateKey(hkey, key_path) as convert_key:
                for target_format in media_formats:
                    sub_key_path = f"{key_path}\\{target_format}"
                    with reg.CreateKey(hkey, sub_key_path) as subkey:
                        command = f'"{sys.executable}" "{os.path.abspath(__file__)}" "%1" {target_format}'
                        reg.SetValue(subkey, '', reg.REG_SZ, command)
                        print(f"Added context menu option for .{format} to convert to {target_format}")

def remove_conversion_options(media_formats):
    with reg.ConnectRegistry(None, reg.HKEY_LOCAL_MACHINE) as hkey:
        for format in media_formats:
            key_path = rf"SOFTWARE\Classes\SystemFileAssociations\.{format}\shell\Convert"
            for target_format in media_formats:
                sub_key_path = f"{key_path}\\{target_format}"
                try:
                    reg.DeleteKey(hkey, sub_key_path)
                    print(f"Removed context menu option for .{format} to convert to {target_format}")
                except FileNotFoundError:
                    print(f"No entry exists for .{format} to {target_format}")
            try:
                reg.DeleteKey(hkey, key_path)
            except FileNotFoundError:
                pass


def add_to_registry():
    add_conversion_options(audio_formats)
    add_conversion_options(video_formats)
    add_conversion_options(image_formats)
    print("Registry updated successfully.")

def remove_from_registry():
    remove_conversion_options(audio_formats)
    remove_conversion_options(video_formats)
    remove_conversion_options(image_formats)
    print("Registry entries removed successfully.")
# -- REGISTRY FUNCTIONS -- END

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

if __name__ == "__main__":
    if len(sys.argv) == 3:
        file_path = sys.argv[1]
        target_format = sys.argv[2]

        file_extension = os.path.splitext(file_path)[1].lower().strip('.')
        if file_extension in audio_formats:
            convert_audio(file_path, target_format)
        elif file_extension in video_formats:
            convert_video(file_path, target_format)
        elif file_extension in image_formats:
            convert_image(file_path, target_format)
        else:
            print("Unsupported file type or conversion.")
    else:
        add_to_registry()
