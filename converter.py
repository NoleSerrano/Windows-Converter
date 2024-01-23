from pydub import AudioSegment
from moviepy.editor import VideoFileClip
from PIL import Image
import os
import sys
import winreg as reg

audio_formats = ['mp3', 'wav']
# audio_formats = ['mp3', 'wav', 'flac']
# video_formats = ['mp4', 'mov', 'webm']
# image_formats = ['png', 'jpg']

# -- REGISTRY FUNCTIONS -- START
def add_conversion_options(media_formats):
    with reg.ConnectRegistry(None, reg.HKEY_LOCAL_MACHINE) as hkey:
        for format in media_formats:
            # Set up the 'Convert' submenu
            key_path = rf"SOFTWARE\Classes\SystemFileAssociations\.{format}\shell\Convert"
            with reg.CreateKey(hkey, key_path) as convert_key:
                # Set the default value for the submenu (displayed verb)
                reg.SetValue(convert_key, '', reg.REG_SZ, 'Convert')
                # Indicate that this key has subcommands
                reg.SetValue(convert_key, 'subcommands', reg.REG_SZ, '')

                # Set up the conversion options
                for target_format in media_formats:
                    # Create a key for the subcommand
                    sub_key_path = f"{key_path}\\shell\\to{target_format.upper()}"
                    with reg.CreateKey(hkey, sub_key_path) as subkey:
                        # Create the command key and set the command
                        command_key_path = f"{sub_key_path}\\command"
                        with reg.CreateKey(hkey, command_key_path) as command_key:
                            command = f'"{sys.executable}" "{os.path.abspath(__file__)}" "%1" {target_format}'
                            reg.SetValue(command_key, '', reg.REG_SZ, command)
                            print(f"Added context menu option for .{format} to convert to {target_format}")


def remove_conversion_options(media_formats):
    with reg.ConnectRegistry(None, reg.HKEY_LOCAL_MACHINE) as hkey:
        for format in media_formats:
            # Define the base path for the 'Convert' submenu
            convert_key_path = rf"SOFTWARE\Classes\SystemFileAssociations\.{format}\shell\Convert"

            # Attempt to remove subcommands for each target format
            for target_format in media_formats:
                sub_key_path = f"{convert_key_path}\\shell\\to{target_format.upper()}"
                command_key_path = f"{sub_key_path}\\command"
                try:
                    # Remove the 'command' subkey
                    reg.DeleteKey(hkey, command_key_path)
                except FileNotFoundError:
                    print(f"No command key to remove for {format} to {target_format}")
                
                try:
                    # Remove the format subkey (e.g., 'toMP3')
                    reg.DeleteKey(hkey, sub_key_path)
                except FileNotFoundError:
                    print(f"No sub key to remove for {format} to {target_format}")

            try:
                # Remove the 'shell' subkey under the 'Convert' key
                shell_key_path = f"{convert_key_path}\\shell"
                reg.DeleteKey(hkey, shell_key_path)
            except FileNotFoundError:
                print(f"No shell key to remove under {convert_key_path}")
                
            try:
                # Finally, remove the 'Convert' key itself
                reg.DeleteKey(hkey, convert_key_path)
            except FileNotFoundError:
                print(f"No Convert key to remove for {format}")

def add_to_registry():
    add_conversion_options(audio_formats)
    # add_conversion_options(video_formats)
    # add_conversion_options(image_formats)
    print("Registry updated successfully.")

def remove_from_registry():
    remove_conversion_options(audio_formats)
    # remove_conversion_options(video_formats)
    # remove_conversion_options(image_formats)
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

# Main Execution Logic
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
        add_to_registry()  # Run this to setup or remove_from_registry() to clear old entries
