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
import configparser
from tendo import singleton

s = requests.Session()

# Create only 1 Instance
me = singleton.SingleInstance()


config = configparser.ConfigParser()

# Try to read the config file

# If the file exists, load the values
config.read("config.ini")
try:
    # Try to get the values from the config file
    USERNAME = config["DEFAULT"]["USERNAME"]
    REPO = config["DEFAULT"]["REPO"]
    API_KEY = config["DEFAULT"]["API_KEY"]
    VERSION_FILE = config["DEFAULT"]["VERSION_FILE"]
    APP_FILE = config["DEFAULT"]["APP_FILE"]
except KeyError as e:
    # If a key is missing, use a default value or ask the user for input
    print(f"{e} is missing in the config file, Filling it with default values")
    USERNAME = "YOUR_USERNAME_HERE"
    REPO = "YOUR_REPOSITORY_HERE"
    API_KEY = "YOUR_API_KEY_HERE"
    VERSION_FILE = "version.txt"
    APP_FILE = "getupdate.exe"
    # Write the values to the config file
    config["DEFAULT"] = {
        "USERNAME": USERNAME,
        "REPO": REPO,
        "API_KEY": API_KEY,
        "VERSION_FILE": VERSION_FILE,
        "APP_FILE": APP_FILE,
    }
    with open("config.ini", "w") as f:
        config.write(f)
    sys.exit()


def check_version():
    print("check version called!")
    try:
        output = open(VERSION_FILE, "r").read().strip()
    except FileNotFoundError:
        print("Version.txt file not found, creating a new one")
        output = "0.0.0"
        open(VERSION_FILE, "w").write(output)

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
                downloadsizeshow = round(downloaded_size / total_size * 100, 8)
                percentageshow.configure(text = f"{downloadsizeshow}%")
                root.update()
                time.sleep(0.1)

    # Extract the zip file and delete it using a context manager and os.remove
    with zipfile.ZipFile(file="update.zip") as zip_file:
        # Get the total size of the zip file
        uncompress_size = sum((file.file_size for file in zip_file.infolist()))
        # Initialize the extracted size
        label.configure(text="Extracting File...")
        time.sleep(0.5)
        extracted_size = 0
        percentageshow.configure("0%")
        progress.set(0)
        # Loop over each file
        for file in zip_file.infolist():
            # Extract each file
            zip_file.extract(member=file)
            # Update the extracted size
            extracted_size += file.file_size
            # Calculate the percentage of completion
            progressextract = extracted_size / uncompress_size
            # Update the progress bar value
            progress.set(progressextract)
            progressextractshow = round(progressextract * 100, 8)
            percentageshow.configure(text = f"{progressextractshow}%")
            # Update the app window
            root.update_idletasks()
            time.sleep(0.9)
    os.remove("update.zip")
    # Show a success message using message["text"]
    updatebtn.configure(state=ctk.DISABLED)
    updatebtn.configure(fg_color="gray")
    checkforupdates.configure(state=ctk.NORMAL)

    output = open(VERSION_FILE, "r").read().strip()
    label.configure(text=f"Update Completed! Now on Version: {output}")


resultcheck = check_version()


# Create the GUI using ctk.CTk and ctk.geometry
root = ctk.CTk()
root.title("Updater v2.0")
root.geometry("320x400")
root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(root.winfo_id()))
root.resizable(False, False)
# Set the appearance mode and color theme using ctk.set_appearance_mode and ctk.set_color_theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# Create the widgets using ctk.Label, ctk.Button, ctk.Progressbar, and ctk.pack
label = ctk.CTkLabel(root, text="Checking for Updates...")
label.grid(row=0, column=0, sticky=ctk.N, columnspan=2)

progress = ctk.CTkProgressBar(root, orientation="horizontal", mode="determinate", width=200) 
progress.grid(row=1, column=0, columnspan=2, sticky=ctk.W, padx=10)
progress.set(0)

percentageshow = ctk.CTkLabel(root, text="00.00000000%") 
percentageshow.grid(row=1, column=1, sticky=ctk.E, padx=10)

updatebtn = ctk.CTkButton(
    root,
    text="Update",
    state=ctk.DISABLED,
    command=lambda: threading.Thread(target=update).start(),
)
updatebtn.grid(row=2, column=0, sticky='nsew', padx=10, pady=5)

def check_updatemanual():
    resultcheck = check_version()
    print(resultcheck)
    label.configure(text="Checking for Updates...")
    time.sleep(2)
    if resultcheck == True:
        label.configure(text="You are up to date!")
        updatebtn.configure(state=ctk.DISABLED)
        updatebtn.configure(fg_color="gray")


checkforupdates = ctk.CTkButton(
    root,
    text="Check for Updates",
    command=lambda: threading.Thread(target=check_updatemanual).start(),
    fg_color="#00a1d8",
    hover_color="#005E7D",
) 
checkforupdates.grid(row=2, column=1, sticky='nsew', padx=10, pady=5)


# Check for updates and enable the button if needed using an if-else statement and button["state"]

if resultcheck == True:
    label.configure(text="You are up to date!")
    updatebtn.configure(state=ctk.DISABLED)
    updatebtn.configure(fg_color="gray")
else:
    with requests.get(
        f"https://api.github.com/repos/{USERNAME}/{REPO}/releases/latest",
        auth=(USERNAME, API_KEY),
    ) as response:
        response.raise_for_status()
        latest_tag = response.json()["tag_name"]
        label.configure(text=f"There is an update available! ({latest_tag})")
    updatebtn.configure(state=ctk.NORMAL)
    updatebtn.configure(fg_color="green")


#Changelog Show here
changeloglabel = ctk.CTkLabel(root, text="Changelog")
changeloglabel.grid(row=3, column=0, sticky=ctk.W, padx=15, pady=5)

# Create a CTk textbox
textbox = ctk.CTkTextbox(root, width=300, height=250)
textbox.grid(row=4, column=0, columnspan=2, pady=5)


url = f"https://api.github.com/repos/{USERNAME}/{REPO}/releases/latest"
# Define a function to display the latest release
headers = {"Authorization": f"token {API_KEY}"}
response = requests.get(url, headers=headers)

if check_version == False:
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract the information you need
        tag_name = data["tag_name"]
        release_name = data["name"]
        release_date = data["published_at"]
        changelog = data["body"]

        # Set the text of the textbox widget to the changelog
        textbox.insert(ctk.END, changelog)

        # Start the main loop of the window
    else:
        # Handle the error
        print(f"Error: {response.status_code}")
else: 
    textbox.insert(ctk.END, "Your Up To Date! Nothing to See Here..")
textbox.configure(state="disabled")

# Start the main loop using root.mainloop
root.mainloop()
