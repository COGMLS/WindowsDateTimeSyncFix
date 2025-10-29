# Windows Date Time Sync Fix

Windows Date Time Synchronization Fix is a solution created to fix the Windows 10 and Windows 11 clock (time and date) sync. This solution fixes the date and time based on local time zone configuration, getting from an open server (worldtimeapi.org) the UTC date. Using the local time zone, it calculates the difference and applies the correct values into Windows clock, fixing the outdated Windows clock.

To force a date and time sync on your Windows, execute your Windows PowerShell (version 5.0 or higher) or PowerShell with **administrator rights**. Otherwise, it will enter in test mode, and no change will be applied.

> [!IMPORTANT]
> This script does not send any personal data to the server and does not save any data from the internet.

> [!NOTE]
> The connection with the server may need multiple tries.

> [!INFO]
> Originally this solution was designed to use a Python 3 script and was recreated to work directly with PowerShell features, bringing more performance and less chances to make a significant delta time between the acquired time from server and processed time to apply on Windows Clock. The original Python script has deprecated and is archived [here](/Scripts/Archived).

## Using the script:

To use the script is just necessary to execute it with **Windows PowerShell** or the **PowerShell** console and have an internet connection to be able to communicate with the server. With you want to test the script without applying any modification, use the `-Test` on command line.

Example to synchronize and apply the correct date and time (Note: The captured console output is in Brazilian Portuguese format. The output will depend on your system regional settings):

```
C:\Users\admin\Scripts> & .\WinDateTimeSync.ps1

Windows Date Time Sync - 1.0.2
-----------------------------------------------------------------
Trying connection... (1/10)
Status: 0 Description: OK

quarta-feira, 29 de outubro de 2025 15:36:25
System's clock defined to 10/29/2025 15:36:25 with success!
```

### Script commands:

The script has a help command line that can be accessed with the cmdlet `Get-Help`:
```PowerShell
# Assuming the current working directory has the script:
Get-Help .\WinDateTimeSync.ps1
```

| Command(s) | Description | Notes |
| ---------- | ----------- | ----- |
| Test | Use the script without applying modification on your system | If the script is not execute with Administrator Rights, the TestMode will be applied automatically. |
| DebugScript | Enable the script debug mode, showing processed data and status code |  |
| Tries <value> | Set a custom number of tries to connect with server (Default is 10) | Any value set value below then one will return error 8 |
| Experimental | Enable the script experimental features | Using this parameter may lead to unexpected behavior |
| Info | Show extra information about the script procedures | Using this parameter will enable some verbose information output, but not all. To see all detailed information, use `-Verbose` and/or `-DebugScript` parameters |

## Documentation:

| Documentation | Description |
| ------------- | ----------- |
| [ProjectInfo.md](./Docs/ProjectInfo.md) | General project development information, including known bugs, deprecated or removed features. It also contains the recent and future features planned to be implemented |
| [ProjectReleases.md](./Docs/ProjectReleases.md) | Contains all project releases and modifications. |

## Releases:

<!-- Windows Date Time Fix Releases Table: -->

<head>
    <link rel="stylesheet" href="Docs/CSS/ReleaseNotes.css">
    <link rel="stylesheet" href="./CSS/ReleaseNotes.css">
</head>
<dl>
    <!-- 1.0.2 (2025/10/29) -->
    <dt><version-data>1.0.2</version-data> | Release Date: 2025/10/29</dt>
    <dd><fix-alert>Fixed </fix-alert> incompatibility with <strong>Windows PowerShell</strong> when reaching the variable <code>IsWindows</code>, which is available only on PowerShell</dd>
    <dd>Added experimental parameter <code>Wait</code>. <strong>NOTE: This feature is under development</strong></dd>
    <dd><bug-alert>[BUG]</bug-alert> Executing the script on <strong>Windows PowerShell</strong> will not work as expected. The </dd>
    <dd><strong>Updated minimum PowerShell version requirement to 5.0</strong> This fixes a minimum requirement for use classes on PowerShell.</dd>
    <!-- 1.0.1 (2025/10/03) -->
    <dt><version-data>1.0.1</version-data> | Release Date: 2025/10/03</dt>
    <dd><fix-alert>Fixed </fix-alert>parameter <code>Tries</code> not working on Windows PowerShell</dd>
    <dd><fix-alert>Fixed </fix-alert>parameter <code>Tries</code> not working as expected on PowerShell</dd>
    <dd>Changed <code>uint</code> datatype variables to <code>Int32</code> avoiding incompatibility with Windows PowerShell</dd>
    <!-- 1.0.0 (2025/09/10) -->
    <dt><version-data>1.0.0</version-data> | Release Date: 2025/09/10</dt>
    <dd>Added new comments and documentation for the PowerShell script</dd>
    <dd>Added new help examples inside the script's help</dd>
    <dd>Added <code>Info</code> parameter to print some information about the operations. (This parameter brings less information output than <code>Verbose</code> parameter)</dd>
    <dd>Promoted custom connection tries to stable features</dd>
    <dd>Small changes on cli check</dd>
    <!-- 0.9.0 (2025/09/05) -->
    <dt><version-data>0.9.0</version-data> | Release Date: 2025/09/05</dt>
    <dd>Added generic description for <code>HTTPResponseData</code></dd>
    <dd>Minor changes on console output, while gathering server information</dd>
    <dd><fix-alert>Fixed </fix-alert><code>IsElevated</code> method</dd>
    <dd><fix-alert>Fixed </fix-alert> <code>HTTPResponseData</code> status description</dd>
    <!-- 0.8.0 (2025/07/24) -->
    <dt><version-data>0.8.0</version-data> | Release Date: 2025/07/24</dt>
    <dd>Added experimental custom number of connection tries</dd>
    <dd>Added test mode on PowerShell script</dd>
    <dd>Added debug information output</dd>
    <dd>Added platform test</dd>
    <dd>Added main entry</dd>
    <dd>Added script presentation</dd>
    <dd>Added exit with error codes</dd>
    <dd>Added variable controls</dd>
    <dd>Added help command line</dd>
    <dd>Added cli test for debug and experimental options</dd>
    <dd>Added date and time extraction in UTC format from json content</dd>
    <dd>Added local date and time getter information</dd>
    <dd>Added local timezone configuration extraction</dd>
    <dd>Added delta date and time between UTC server and local information</dd>
    <dd>Added sum of delta time with local time</dd>
    <dd>Added <code>HttpResponseData</code> class</dd>
    <dd>Added <code>getDateTimeInfo</code> method</dd>
    <dd>Added loop to try and get the date time information</dd>
    <dd><strong>This version is based on all implementations made in deprecated Python script</strong></dd>
</dl>

# License

A copy of the license file is available [here](./LICENSE.txt)

MIT License

Copyright (c) 2025 Matheus Lopes Silvati

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.