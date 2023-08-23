# AutoUpdaterGUI

Update your app to the latest release by a click of a button!

#### Table of Contents

- [How to Configure the Auto Updater](#how-to-configure-the-auto-updaterlatest)
- [How to Configure the Auto Updater(Before v2.5)](#how-to-configure-the-auto-updaterbefore-v25)
- [Portable Version](#Portable)
- [How it Works](#Howitworks)

<hr>

## How to configure the auto updater(Latest)

`TBD..` `Currently just ignore this since 2.5 hasnt been released yet and is unstable`



## How to configure the auto updater(Before V2.5)

- Launch the .exe and wait for it to generate a **config.ini** file
- The `USERNAME` Should be your github username
- The `REPO` Should be your repository you want to pull the updates from
- Set the config.ini file with your `API_KEY` checking the scopes of managing private repositories
- The `VERSION_FILE` should be where your version number is. It should only be your current version. Because this file is used to compare your current version with the latest release (I recommend to not change the file name in the config.ini)
  - After you fill in the config.ini file launch the program again and it create a version.txt file. There should be an example if the point below this one isn't clear enough
  - For example `v1.0`. It should not be filled in with anything else

**It should look like this when its filled in**

![Untitled](https://github.com/noneeeeeeeeeee/AutoUpdaterGUI/assets/64634725/21abae9d-4233-48f8-9d95-5da691a2348b)

<hr>
<a name="Portable"></a>

### Need a portable version?

Instructions and download provided [here](https://github.com/noneeeeeeeeeee/AutoUpdaterGUI/releases/tag/1.x-Legacy)

<a name="Howitworks"></a>

## How it works

It will delete all the files in the folder that the app is in then it gets the latest release from the assets(not the source code) and extract that zip into the same directory as the application. It will not delete the file thats in `APP_FILE`. That is also not an array so it can only do 1 file(I will implement arrays in the next version).
