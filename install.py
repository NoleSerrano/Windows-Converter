#!/usr/bin/env python -B

from pydub import AudioSegment
from moviepy.editor import VideoFileClip
from PIL import Image
import os
import sys
import winreg as reg
from tkinter import Tk, Label, Button, OptionMenu, StringVar
import tkinter as tk
from converter import audio_formats, video_formats, image_formats

# Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Classes\SystemFileAssociations\.mp3

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

add_to_registry()