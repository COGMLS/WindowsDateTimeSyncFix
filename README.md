# Windows Date Time Sync Fix

Windows Date Time Synchronization Fix is a solution created to fix the Windows 10 and Windows 11 clock (time and date) sync. This solution fix the date and time based on local timezone configuration, acquiring from a open server (worldtimeapi.org) the UTC date. Using the local timezone, it calculates the difference and apply the correct values into Windows clock.

> [!NOTE]
> This project is under development and documentations and project's script may not be available or ready to be used.

## Documentation:

This repository contain a [Docs](./Docs/) directory where the documentation is keep it.

| Documentation | Description |
| ------------- | ----------- |
| [ProjectInfo.md](./Docs/ProjectInfo.md) | General project development information, including known bugs, deprecated or removed features. It also contain the recent and future features planned to be implemented |
| [ProjectReleases.md](./Docs/ProjectReleases.md) | Contain all project releases and modifications. |

## Releases:

<!-- Windows Date Time Fix Releases Table: -->

<head>
    <link rel="stylesheet" href="Docs/CSS/ReleaseNotes.css">
    <link rel="stylesheet" href="./CSS/ReleaseNotes.css">
</head>
<dl>
    <!-- 0.5.1 (2025/06/21) -->
    <dt><version-data>0.5.1</version-data> | Release Date: 2025/06/21</dt>
    <dd>Fix <code>bIsTestScript</code> name</dd>
    <dd>Fix print help array</dd>
    <dd>Fix show help correctly</dd>
    <dd>Fix test script mode</dd>
    <!-- 0.5.0 (2025/06/21) -->
    <dt><version-data>0.5.0</version-data> | Release Date: 2025/06/21</dt>
    <dd>Added main entry</dd>
    <dd>Added script presentation</dd>
    <dd>Move previous script data processing into main entry</dd>
    <dd>Added exit with error codes</dd>
    <dd>Added new comments</dd>
    <dd>Added to execute PowerShell script only when is not in test mode</dd>
    <dd>Added new methods</dd>
    <dd>Added variable controls</dd>
    <dd>Added help command line</dd>
    <dd>Added cli test for debug and experimental options</dd>
    <dd>Removed unused code</dd>
    <!-- 0.4.0 (2025/06/20) -->
    <dt><version-data>0.4.0</version-data> | Release Date: 2025/06/20</dt>
    <dd>Added PowerShell script generation from Python processed data</dd>
    <dd>Added PowerShell script calling from Python</dd>
    <dd>Added python version test</dd>
    <dd><strong>The script is not ready to be used yet.</strong> It only process the data and return to the console window</dd>
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