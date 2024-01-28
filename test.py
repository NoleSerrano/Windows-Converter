import os
import converter  # Import your converter module

# Import format lists from converter.py
from converter import audio_formats, video_formats, image_formats

# Define your test files
test_files = {
    'audio': 'test.mp3',
    'video': 'test.mp4',
    'image': 'test.png'
}

# All target formats for each type
all_formats = {
    'audio': audio_formats,
    'video': video_formats,
    'image': image_formats
}

def get_target_formats(source_file, source_type):
    _, ext = os.path.splitext(source_file)
    ext = ext[1:].lower()  # Remove the dot from extension and convert to lower case
    return [fmt for fmt in all_formats[source_type] if fmt.lower() != ext]

def test_conversion(source_file, source_type):
    for format in get_target_formats(source_file, source_type):
        output_file = converter.get_output_filename(source_file, format)
        print(f"Converting {source_file} to {format}... ", end="")

        # Perform the conversion
        if source_type == 'audio':
            converter.convert_audio(source_file, format, output_file)
        elif source_type == 'video':
            converter.convert_video(source_file, output_file)
        else:
            converter.convert_image(source_file, output_file)

        # Check if the conversion was successful
        if os.path.exists(output_file):
            print("Success")
        else:
            print("Failed")

def main():
    for media_type, file in test_files.items():
        test_conversion(file, media_type)

if __name__ == "__main__":
    main()
