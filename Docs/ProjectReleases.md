# Windows Date Time Fix Releases

<!-- Windows Date Time Fix Releases Table: -->
<head>
    <link rel="stylesheet" href="Docs/CSS/ReleaseNotes.css">
    <link rel="stylesheet" href="./CSS/ReleaseNotes.css">
</head>
<dl>
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
    <!-- 0.3.0 (2025/06/18) -->
    <dt><version-data>0.3.0</version-data> | Release Date: 2025/06/18</dt>
    <dd>Added date and time extraction in UTC format from json content</dd>
    <dd>Added local date and time getter information</dd>
    <dd>Added local timezone configuration extraction</dd>
    <dd>Added delta date and time between UTC server and local information</dd>
    <dd>Added sum of delta time with local time</dd>
    <dd>Added <code>srtncpy</code> method</dd>
    <dd>Added only date extraction from string converted <code>dtFix</code></dd>
    <dd>Added only time extraction from string converted <code>dtFix</code></dd>
    <dd>Added Windows PowerShell command</dd>
    <!-- 0.2.0 (2025/06/17) -->
    <dt><version-data>0.2.0</version-data> | Release Date: 2025/06/17</dt>
    <dd>Added if statement for successful date and time acquisition from server</dd>
    <dd>Added json treatment to extract date time from server response</dd>
    <!-- 0.1.0 (2025/06/16) -->
    <dt><version-data>0.1.0</version-data> | Release Date: 2025/06/16</dt>
    <dd>Added <code>HttpResponseData</code> class</dd>
    <dd>Added <code>getDateTimeInfo</code> method</dd>
    <dd>Added loop to try and get the date time information</dd>
</dl>