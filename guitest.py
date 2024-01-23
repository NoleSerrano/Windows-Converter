import tkinter as tk
from tkinter import Label, Button, OptionMenu, StringVar

def on_convert():
    chosen_format = selected_format.get()
    label.config(text=f"Selected format: {chosen_format}")
    print(f"Converting to {chosen_format}")
    # Here, add the logic to perform the conversion.
    
    # Close the window after conversion
    root.destroy()

# Supported formats for conversion
conversion_formats = ['mp3', 'wav', 'flac']

# Create the main window
root = tk.Tk()
root.title("Conversion Test")

# Create a label
label = tk.Label(root, text="Choose format to convert to:")
label.pack()

# StringVar to hold the selected format
selected_format = StringVar(root)
selected_format.set(conversion_formats[0])  # default value

# Dropdown menu for format selection
format_menu = OptionMenu(root, selected_format, *conversion_formats)
format_menu.pack()

# Create a button
convert_button = tk.Button(root, text="Convert", command=on_convert)
convert_button.pack()

# Start the event loop
root.mainloop()