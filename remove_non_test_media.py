import os
import glob
from converter import audio_formats, video_formats, image_formats
from test import test_files

# Directory of the script
media_directory = os.path.dirname(os.path.abspath(__file__))

# Convert the test_files dictionary to a list of filenames
test_file_list = list(test_files.values())

# Create a list of patterns to match files against
patterns = ['*.{}'.format(ext) for ext in audio_formats + video_formats + image_formats]

# Remove files that are not in test_file_list
for pattern in patterns:
    for file_path in glob.glob(os.path.join(media_directory, pattern)):
        if os.path.basename(file_path) not in test_file_list:
            os.remove(file_path)
            print(f"Removed file: {file_path}")
