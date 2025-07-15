# Windows Date Time Sync Fix

Windows Date Time Synchronization Fix is a solution created to fix the Windows 10 and Windows 11 clock (time and date) sync. This solution fixes the date and time based on local timezone configuration, acquiring from an open server (worldtimeapi.org) the UTC date. Using the local timezone, it calculates the difference and applies the correct values into Windows clock, fixing the outdated Windows clock.

To force a date and time sync on your Windows, execute your Python with **administrator rights**, otherwise it will fail.

> [!IMPORTANT]
> This script does not send any personal data to the server and does not save any data from the internet.

> [!NOTE]
> The connection with the server may need multiple tries.

## Using the script:

To use the script is just necessary to execute with Python 3 and have an internet connection to be able to communicate with the server. With you want to test the script before applying any modification use the `-test` command line.

Example to sync and apply the correct date and time (Note: The captured console output is in Brazilian Portuguese format. The output will depend on your system regional settings):

```
python3 WinDateTimeSync.py

Windows Date Time Sync - 0.7.1
-----------------------------------------------------------------
Retrying... (1/10)
Status: 0 Reason: OK

Setting correct date and time on Windows Clock...


segunda-feira, 14 de julho de 2025 18:49:54
Windows clock set to:
segunda-feira, 14 de julho de 2025 18:49:54
```

### Script commands:

The script has a help command line that can be accessed with parameters: `-?`, `-h` or `-help`. All commands are case-insensitive.

| Command(s) | Description | Notes |
| ---------- | ----------- | ----- |
| -help -h -? | Access the command line help |  |
| -test | Use the script without applying modification on your system |  |
| -debug | Enable the script debug mode, showing processed data and status code |  |
| -tries=<value> | Set a custom number of tries to connect with server (Default is 10) | Any value set value below then one will return error 8. **This is an experimental parameter** |
| -pwsh | Force to use PowerShell and not Windows PowerShell | Windows only came with Windows PowerShell. Using this parameter when your computer does not have the PowerShell installed, will result in an error |
| --experimental | Enable the script experimental features | Using this parameter may lead to unexpected behavior |
| --bypass-win-ver | Bypass Windows minimum version to execute the script | This may lead to unexpected behavior |

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
    <!-- 0.7.1 (2025/07/14) -->
    <dt><version-data>0.7.1</version-data> | Release Date: 2025/07/14</dt>
    <dd>Changed PowerShell script to use exit by default. Now PowerShell script will only show to return value when DebugMode is True</dd>
    <dd>Disabled <code>DEV_MODE</code></dd>
    <dd>Added remove temporary PowerShell script file</dd>
    <dd><strong>The script passed in all tests to change and update the Windows date and time correctly</strong></dd>
    <!-- 0.7.0 (2025/06/26) -->
    <dt><version-data>0.7.0</version-data> | Release Date: 2025/06/26</dt>
    <dd>Added experimental custom number of connection tries</dd>
    <dd>Added experimental force PowerShell and not Windows PowerShell</dd>
    <dd>Added test mode on PowerShell script</dd>
    <dd>Enabled <code>Set-Date</code> on PowerShell script</dd>
    <dd>Added <code>try-except</code> blocks on calling PowerShell</dd>
    <dd><fix-alert>Fixed</fix-alert> testing Windows build value</dd>
    <dd><fix-alert>Fixed</fix-alert> PowerShell script require minimum version</dd>
    <!-- 0.6.0 (2025/06/23) -->
    <dt><version-data>0.6.0</version-data> | Release Date: 2025/06/23</dt>
    <dd>Added more precise debug information</dd>
    <dd>Added new command line option</dd>
    <dd>Added DEV_MODE constant</dd>
    <dd>Added platform test</dd>
    <dd>Added Windows version test</dd>
    <dd>Changed way to call PowerShell</dd>
    <dd><fix-alert>Fixed</fix-alert> timezone information on Windows platforms</dd>
    <dd><fix-alert>Fixed</fix-alert> applying corrected time</dd>
    <dd><fix-alert>Fixed</fix-alert> minimum PowerShell version</dd>
    <dd><fix-alert>Fixed</fix-alert> missing admin rights check on PowerShell script</dd>
    <dd><fix-alert>Fixed</fix-alert> keep admin privileges when calling PowerShell</dd>
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