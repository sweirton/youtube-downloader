import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from pytube import YouTube
import threading
import requests

# ------------------------------------ FILE NAME CLEANING -------------------------------------- #
# Function to clean up filename
def clean_filename(name):
    # returns a cleaned version of the filename. The function replaces any forbidden characters in the name with "#" and removes any leading or trailing spaces. If the resulting filename is longer than 176 characters, it truncates it to 170 characters and adds "..." at the end.

    forbidden_chars = "\"*\\/'|.?:<>"
    filename = (
        ("".join([x if x not in forbidden_chars else "#" for x in name]))
        .replace("  ", " ")
        .strip()
    )
    if len(filename) >= 176:
        filename = f"{filename[:170]} '...'"
    return filename


# -------------------------------------- VIDEO DOWNLOAD --------------------------------------- #
# Function to download the video
def download_video():
    # Video's downloaded at 720p based off of link provided by user. The progress bar appears when a valid entry is submitted. As the video downloads, the progess bar updates. The user is prompted that the update has been completed. If there's a problem with the download then the user is prompted with a messagebox.

    url = url_entry.get()

    # Checks to ensure user input something ->
    if not url:
        messagebox.showerror("Error", "Please enter a valid URL")
        return
    
    # Show the progress bar ->
    download_progress.grid(row=5, column=1, columnspan=3, pady=(10, 20))

    def download():
        try:
            yt = YouTube(url)
            stream = yt.streams.filter(res="720p", progressive=True, file_extension='mp4').first()
            total_size = stream.filesize
            download_progress['maximum'] = total_size

            # Clean up filename using clean_filename function ->
            cleaned_filename = clean_filename(yt.title)

            # Download the video using requests ->
            response = requests.get(stream.url, stream=True)
            with open(os.path.join(downloads_folder, f"{cleaned_filename}.mp4"), 'wb') as f:
                downloaded_bytes = 0
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        downloaded_bytes += len(chunk)
                        download_progress['value'] = downloaded_bytes

            messagebox.showinfo("Success", "Download complete")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # Prevents program freezing ->
    threading.Thread(target=download).start()


# -------------------------------- UI ----------------------------------- @
# Create the main window ->
root = tk.Tk()
root.title("YouTube Downloader")
root.configure(padx=20, pady=10)

# Get the path to the Downloads folder ->
downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')

# Title label ->
title_label = ttk.Label(root, text="YOUTUBE DOWNLOADER", font=("Roboto", 14, "bold"))
title_label.grid(row=0, column=1, columnspan=3, pady=20, padx=(10, 0))

# URL entry ->
url_label = ttk.Label(root, text="Enter YouTube URL:")
url_label.grid(row=1, column=1, columnspan=2, sticky="w")
url_entry = ttk.Entry(root, width=50)
url_entry.grid(row=3, column=1, columnspan=3, sticky="w")

# Download button ->
download_button = ttk.Button(root, text="Download", command=download_video)
download_button.grid(row=4, column=2, columnspan=3, pady=(5, 10), sticky="e")

# Download progress bar (initially hidden) ->
download_progress = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate')

root.mainloop()
