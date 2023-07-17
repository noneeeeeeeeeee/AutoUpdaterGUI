# AutoUpdaterGUI
Update your app from latest release. Works by deleting all your files in that one folder then pulling the .zip and extracting it
# Downloading v1.0
Since you cannot configure using a file you have to modify the code and build the app using this command to build below

```pyinstaller --noconfirm --onedir --windowed --add-data "<CustomTkinter Location>/customtkinter;customtkinter/"  "getupdate.py"```
