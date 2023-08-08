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


config.read("config.ini")
try:

    USERNAME = config["DEFAULT"]["USERNAME"]
    REPO = config["DEFAULT"]["REPO"]
    API_KEY = config["DEFAULT"]["API_KEY"]
    VERSION_FILE = config["DEFAULT"]["VERSION_FILE"]
    APP_FILE = config["DEFAULT"]["APP_FILE"]
except KeyError as e:

    print(f"{e} is missing in the config file, Filling it with default values")
    USERNAME = "YOUR_USERNAME_HERE"
    REPO = "YOUR_REPOSITORY_HERE"
    API_KEY = "YOUR_API_KEY_HERE"
    VERSION_FILE = "version.txt"
    APP_FILE = "getupdate.exe"

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



s.headers["User-Agent"] = "Custom"


def update():
    updatebtn.configure(state=ctk.DISABLED)
    checkforupdates.configure(state=ctk.DISABLED)
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, __file__, None, 1
        )


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

    url = f"https://api.github.com/repos/{USERNAME}/{REPO}/releases/latest"
    headers = {
        "Authorization": f"token {API_KEY}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Custom",
    }
    with requests.get(url, headers=headers) as response:
        response.raise_for_status()

        asset_url = None
        for asset in response.json()["assets"]:
            if asset["name"].endswith(".zip"):
                asset_url = asset["url"]
                break

        headers = {
            "Authorization": f"token {API_KEY}",
            "Accept": "application/octet-stream",
            "User-Agent": "Custom",
        }
    with requests.get(asset_url, headers=headers, stream=True) as response:
        response.raise_for_status()

        with open("update.zip", "wb") as f:

            total_size = int(response.headers["Content-Length"])
            label.configure(text="Downloading File...")
            time.sleep(1)
            downloaded_size = 0
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)

                downloaded_size += len(chunk)
                progress.set(downloaded_size / total_size)
                downloadsizeshow = round(downloaded_size / total_size * 100, 8)
                percentageshow.configure(text = f"{downloadsizeshow}%")
                root.update()

    with zipfile.ZipFile(file="update.zip") as zip_file:

        uncompress_size = sum((file.file_size for file in zip_file.infolist()))

        label.configure(text="Extracting File...")
        time.sleep(0.5)
        extracted_size = 0
        percentageshow.configure("0%")
        progress.set(0)

        for file in zip_file.infolist():

            zip_file.extract(member=file)

            extracted_size += file.file_size

            progressextract = extracted_size / uncompress_size

            progress.set(progressextract)
            progressextractshow = round(progressextract * 100, 8)
            percentageshow.configure(text = f"{progressextractshow}%")

            root.update_idletasks()
            time.sleep(0.01)
    os.remove("update.zip")

    updatebtn.configure(state=ctk.DISABLED)
    updatebtn.configure(fg_color="gray")
    checkforupdates.configure(state=ctk.NORMAL)

    output = open(VERSION_FILE, "r").read().strip()
    label.configure(text=f"Update Completed! Now on Version: {output}")


resultcheck = check_version()



root = ctk.CTk()
root.title("Updater v2.0.2")
root.geometry("320x400")

root.resizable(False, False)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


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
    label.configure(text="Checking for Updates...")
    time.sleep(2)
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


checkforupdates = ctk.CTkButton(
    root,
    text="Check for Updates",
    command=lambda: threading.Thread(target=check_updatemanual).start(),
    fg_color="#00a1d8",
    hover_color="#005E7D",
) 
checkforupdates.grid(row=2, column=1, sticky='nsew', padx=10, pady=5)




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



changeloglabel = ctk.CTkLabel(root, text="Changelog")
changeloglabel.grid(row=3, column=0, sticky=ctk.W, padx=15, pady=5)


textbox = ctk.CTkTextbox(root, width=300, height=250)
textbox.grid(row=4, column=0, columnspan=2, pady=5)


url = f"https://api.github.com/repos/{USERNAME}/{REPO}/releases/latest"

headers = {"Authorization": f"token {API_KEY}"}
response = requests.get(url, headers=headers)

checkchangelog = check_version()
if checkchangelog == False:
    if response.status_code == 200:
        data = response.json()
        changelog = data["body"]
        textbox.insert(ctk.END, changelog)
    else:
        print(f"Error: {response.status_code}")
else: 
    textbox.insert(ctk.END, "Your Up To Date! Nothing to See Here..")


textbox.configure(state="disabled")

root.mainloop()
