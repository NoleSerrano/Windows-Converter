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

def remove_from_registry():
    for media_type in (audio_formats + video_formats + image_formats):
        try:
            with reg.ConnectRegistry(None, reg.HKEY_LOCAL_MACHINE) as hkey:
                reg.DeleteKey(hkey, rf"SOFTWARE\Classes\SystemFileAssociations\.{media_type}\shell\Convert\command")
                reg.DeleteKey(hkey, rf"SOFTWARE\Classes\SystemFileAssociations\.{media_type}\shell\Convert")
            print(f"Registry entries removed for .{media_type}")
        except FileNotFoundError:
            print(f"No registry entries found for .{media_type}")

remove_from_registry()