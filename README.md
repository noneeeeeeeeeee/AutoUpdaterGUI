# AutoUpdaterGUI
Update your app from latest release. Works by deleting all your files in that one folder then pulling the .zip and extracting it

# Downloading v1.0(depricated)
Since you cannot configure using a file you have to modify the code and build the app using this command to build below and make sure to create a version.txt file or it will not launch. An empty one would suffice

```pyinstaller --noconfirm --onedir --windowed --add-data "<CustomTkinter Location>/customtkinter;customtkinter/"  "getupdate.py"```

# Downloading v1.5 and above
- Launch the .exe and wait for it to generate a **config.ini** file
- Set the config.ini file with your ```API_KEY``` checking the scopes of managing private repositories
- Now when you launch it again it will create a **version.txt** file. That file will be used to compare the latest release with the current one.

## How it works
It will get the latest release from the assets(not the source code) and extract that zip into the same directory as the application
