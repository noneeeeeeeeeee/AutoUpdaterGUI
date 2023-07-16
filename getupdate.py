# Import the modules
import requests
import zipfile
import os
import customtkinter as ctk
import ctypes
import sys
import shutil
import threading
import time

s = requests.Session()

# Define the constants
USERNAME = "noneeeeeeeeeee"
REPO = "InstructionsDatabase"
API_KEY = "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"
VERSION_FILE = "version.txt"  # This is where I changed get-update.js to version.txt
APP_FILE = "getupdate.exe"


def check_version():
    print("check version called!")
    output = open(VERSION_FILE, "r").read().strip()

    with requests.get(
        f"https://api.github.com/repos/{USERNAME}/{REPO}/releases/latest",
        auth=(USERNAME, API_KEY),
    ) as response:
        response.raise_for_status()
        latest_tag = response.json()["tag_name"]
        print("response called!")
    print("Return Called!", output, latest_tag)
    return output == latest_tag


# Add a user agent header to your requests
s.headers["User-Agent"] = "Custom"


def update():
    updatebtn.configure(state=ctk.DISABLED)
    checkforupdates.configure(state=ctk.DISABLED)
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, __file__, None, 1
        )

    # Delete all files and folders except the app file using a list comprehension and shutil.rmtree
    [
        os.remove(file)
        for file in os.listdir()
        if file != APP_FILE and os.path.exists(file) and not os.path.isdir(file)
    ]
    [
        shutil.rmtree(file)
        for file in os.listdir()
        if file != APP_FILE and os.path.exists(file) and os.path.isdir(file)
    ]
    # Download the zip file from GitHub using requests.get and a context manager
    url = f"https://api.github.com/repos/{USERNAME}/{REPO}/releases/latest"
    headers = {
        "Authorization": f"token {API_KEY}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Custom",
    }
    with requests.get(url, headers=headers) as response:
        response.raise_for_status()
        # Get the asset URL from the response JSON data using a for loop and a break statement
        asset_url = None
        for asset in response.json()["assets"]:
            if asset["name"].endswith(".zip"):
                asset_url = asset["url"]
                break
        # Download the asset file using requests.get and a context manager
        headers = {
            "Authorization": f"token {API_KEY}",
            "Accept": "application/octet-stream",
            "User-Agent": "Custom",
        }
    with requests.get(asset_url, headers=headers, stream=True) as response:
        response.raise_for_status()
        # Write the zip file using a context manager and a generator expression
        with open("update.zip", "wb") as f:
            # Get the total size of the file from the response headers
            total_size = int(response.headers["Content-Length"])
            label.configure(text="Downloading File...")
            time.sleep(1)
            downloaded_size = 0
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
                # Update the downloaded size by adding the chunk size
                downloaded_size += len(chunk)
                progress.set(downloaded_size / total_size)
                root.update()
                time.sleep(0.01)






        
    # Extract the zip file and delete it using a context manager and os.remove
    with zipfile.ZipFile("update.zip", "r") as f:
        f.extractall()
        label.configure(text="Extracting File...")
    os.remove("update.zip")
    # Show a success message using message["text"]
    updatebtn.configure(state=ctk.DISABLED)
    updatebtn.configure(fg_color="gray")
    checkforupdates.configure(state=ctk.NORMAL)

    output = open(VERSION_FILE, "r").read().strip()
    label.configure(text= f"Update Completed! Now on Version: {output}")


resultcheck = check_version()


# Create the GUI using ctk.CTk and ctk.geometry
root = ctk.CTk()  
root.title("Updater v1.0")
root.geometry("320x100")

# Set the appearance mode and color theme using ctk.set_appearance_mode and ctk.set_color_theme
ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("green")  

# Create the widgets using ctk.Label, ctk.Button, ctk.Progressbar, and ctk.pack
label = ctk.CTkLabel(
    root, text="Checking for Updates..."
)  
label.pack()

progress = ctk.CTkProgressBar(
    root, orientation="horizontal", mode="determinate"
)  
progress.pack()
progress.set(0) 

updatebtn = ctk.CTkButton(
    root, text="Update", state=ctk.DISABLED, command=lambda: threading.Thread(target=update).start()
)


def check_updatemanual():
    resultcheck = check_version()
    print(resultcheck)
    label.configure(text="Checking for Updates...")
    time.sleep(2)
    if resultcheck == True:
        label.configure(text="You are up to date!")
        updatebtn.configure(state=ctk.DISABLED)
        updatebtn.configure(fg_color="gray")

    else:
        label.configure(text="There is an update available!")
        updatebtn.configure(state=ctk.NORMAL)
        updatebtn.configure(fg_color="green")



checkforupdates = ctk.CTkButton(
    root,
    text="Check for Updates",
    command=lambda: threading.Thread(target=check_updatemanual).start(),
    fg_color="#00a1d8",
    hover_color="#005E7D",
)  # This is where I changed tk to ctk and added root as an argument


updatebtn.pack(
    side=ctk.LEFT, padx=10, pady=10
)  # This is where I packed the update button on the left with some margin
checkforupdates.pack(
    side=ctk.RIGHT, padx=10, pady=10
)  # This is where I packed the check for updates button on the right with some margin

message = ctk.CTkLabel(
    root, text=""
)  # This is where I changed tk to ctk and added root as an argument
message.pack()

# Check for updates and enable the button if needed using an if-else statement and button["state"]

if resultcheck == True:
    label.configure(text="You are up to date!")
    updatebtn.configure(state=ctk.DISABLED)
    updatebtn.configure(fg_color="gray")
else:
    label.configure(text="There is an update available!")
    updatebtn.configure(state=ctk.NORMAL)
    updatebtn.configure(fg_color="green")

# Start the main loop using root.mainloop
root.mainloop()
