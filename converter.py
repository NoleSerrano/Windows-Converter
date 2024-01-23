from pydub import AudioSegment
from moviepy.editor import VideoFileClip
from PIL import Image
import os
import sys
import reg

audio_formats = ['mp3', 'wav', 'flac']
video_formats = ['mp4', 'mov', 'webm']
image_formats = ['png', 'jpg']

# -- REGISTRY SETUP -- START
def add_conversion_options(media_formats, media_type):
    for format in media_formats:
        key_path = rf"Software\Classes\SystemFileAssociations\.{format}\shell"
        for target_format in media_formats:
            if target_format != format:
                sub_key_path = f"{key_path}\Convert to {target_format}"
                command = f'"{sys.executable}" "{os.path.abspath(__file__)}" "%1" {target_format}'
                reg.SetValue(reg.HKEY_CLASSES_ROOT, sub_key_path + r'\command', reg.REG_SZ, command)
                print(f"Added context menu option for .{format} to convert to {target_format}")

def add_to_registry():
    add_conversion_options(audio_formats, "audio")
    add_conversion_options(video_formats, "video")
    add_conversion_options(image_formats, "image")
    print("Registry updated successfully.")
# -- REGISTRY SETUP -- END

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
