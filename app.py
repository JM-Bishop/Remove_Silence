import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import sys
import webbrowser
import os

# Check if FFmpeg is installed
def is_ffmpeg_installed():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        return True
    except FileNotFoundError:
        return False

# Prompt the user to install FFmpeg if not found
def install_ffmpeg():
    print("FFmpeg is not installed.")
    if sys.platform.startswith('linux'):
        print("On Linux, you can typically install FFmpeg via your package manager.\nFor example, on Ubuntu: sudo apt-get install ffmpeg")
    elif sys.platform == "win32":
        print("On Windows, you can download FFmpeg from https://ffmpeg.org/download.html")
        webbrowser.open("https://ffmpeg.org/download.html")
    print("Please install FFmpeg and rerun the script.")
    sys.exit(1)

# GUI Application
class SilenceRemoverApp:
    def __init__(self, master):
        self.master = master
        master.title("Silence Remover")

        # Variables to store file paths
        self.input_file_path = tk.StringVar()
        self.output_file_path = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Input file selection
        tk.Label(self.master, text="Input File:").grid(row=0, column=0, sticky=tk.W)
        tk.Entry(self.master, textvariable=self.input_file_path, width=50).grid(row=0, column=1)
        tk.Button(self.master, text="Browse...", command=self.select_input_file).grid(row=0, column=2)

        # Output file selection
        tk.Label(self.master, text="Output File:").grid(row=1, column=0, sticky=tk.W)
        tk.Entry(self.master, textvariable=self.output_file_path, width=50).grid(row=1, column=1)
        tk.Button(self.master, text="Browse...", command=self.select_output_file).grid(row=1, column=2)

        # Process button
        tk.Button(self.master, text="Remove Silence", command=self.process_files).grid(row=2, column=1, pady=10)

    def select_input_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.input_file_path.set(file_path)

    def select_output_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".mp3")
        if file_path:
            self.output_file_path.set(file_path)

    def process_files(self):
        input_file = self.input_file_path.get()
        output_file = self.output_file_path.get()
        message = self.remove_silence(input_file, output_file)
        messagebox.showinfo("Process Completed", message)


    def remove_silence(self, input_file, output_file):
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # Construct the full path to the FFmpeg executable
    ffmpeg_path = os.path.join(current_dir, "ffmpeg")  # Adjust the executable name if necessary (e.g., "ffmpeg.exe" on Windows)

    # Modify the command to use the full path to FFmpeg
    command = [
        ffmpeg_path,  # Use the full path for FFmpeg
        '-i', input_file,
        '-af', 'silenceremove=1:0:-50dB',
        output_file
    ]

    try:
        # Execute the FFmpeg command
        subprocess.run(command, check=True)
        return "Silence removed from " + input_file + ". Output saved to " + output_file + "."
    except subprocess.CalledProcessError as e:
        return "Error processing file " + input_file + ": " + str(e)
    except Exception as e:
        return "An error occurred: " + str(e)



# Main script execution
def main():
    if not is_ffmpeg_installed():
        install_ffmpeg()
    else:
        root = tk.Tk()
        app = SilenceRemoverApp(root)
        root.mainloop()

if __name__ == "__main__":
    main()
