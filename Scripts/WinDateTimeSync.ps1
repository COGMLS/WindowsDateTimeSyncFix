<##########################################################
 # Windows Date and Time Sync script for PowerShell
 # ---------------------------------------------------
 # Author: Matheus Lopes Silvati
 # Date: 2025/10/29
 # ------------------------------------
 # Version: 1.0.2
 # ------------------------------------
 # Obs: N/A
##########################################################>

<#
.SYNOPSIS
    Windows Date and Time Synchronization Fix - Fixes the wrong date and time sync 
.DESCRIPTION
    The Windows Date and Time Synchronization Fix is focus on mitigate the wrong date and time
    on Windows, when the operation system fail to sync with the internet the correct time.

    To fix the Windows Clock, the script try the connection with a open server (worldtimeapi.org)
    and converts the UTC time to your system's local time, using the local timezone and applying
    the date and time offsets.
    
    This behavior has been observed on Windows 10 and 11, and can make the applications those
    need a synced date and time with server fail. This script helps to avoid this situation.
.INPUTS
    The script does not receive any inputs
.OUTPUTS
    The script can exit with error codes:

    0: Successful. No exception or fail was detected
    1: <Error Code Deprecated/Removed>
    2: Script reached maximum of tries to get the server information, but no response was sent
    3: PowerShell script failed to set the date
    4: Fail to get server info, but successfully processed the getDateTimeInfo method
    5: Platform incompatible
    6: <Error Code Deprecated/Removed>
    7: <Error Code Deprecated/Removed>
    8: Invalid argument value

.NOTES
    To make possible the Windows Clock fixed, you must execute the script as Administrator.
    Otherwise, it will only show the correct date and time from internet.

    The connection with the server may need multiple tries.

    This script does not send any data to the internet. Only receive the correct date and time
    information.

    This script was not designed to work on Linux.
.LINK
    Repository link: https://github.com/COGMLS/WindowsDateTimeSyncFix
    README file: https://github.com/COGMLS/WindowsDateTimeSyncFix/blob/master/README.md
.EXAMPLE
    WinDateTimeSync.ps1 -Test
    Test the Windows Date and Time Synchronization Fix script, without changing your system's settings.
.EXAMPLE
    WinDateTimeSync.ps1
    Fix the Windows Clock synchronization contacting a time server and apply the correct local date and time to your system.

    NOTE: It it necessary to execute as administrator to apply the correct date and time. Otherwise, it will have the same effect as using -Test parameter.
.EXAMPLE
    WinDateTimeSync.ps1 -Tries 5
    Make a maximum of 5 tries to contact the server.

    NOTE: The server connection may be more difficult to be stablish depending your network stability.
#>

#Requires -Version 4.0

[CmdletBinding()]
param
(
    # Use the script without apply modification on your system.
    # If the script is not execute with Administrator Rights, the TestMode will be applied automatically.
    [Parameter(
                Position = 0,
                Mandatory = $false
                )]
    [switch]
    $Test,

    # Enable the script debug mode, showing processed data and status code
    [Parameter(
                Position = 1,
                Mandatory = $false
                )]
    [switch]
    $DebugScript,

    # Set a custom number of tries to connect with server (Default is 10)
    # NOTE: Any value set value below than one will return an error.
    [Parameter(
                Position = 2,
                Mandatory = $false
                )]
    [int]
    $Tries = 10,

    # Enable the script experimental features
    [Parameter(
                Position = 3,
                Mandatory = $false
                )]
    [switch]
    $Experimental,

    # Show extra information about the script procedures
    # NOTE: Using this parameter will enable some verbose information output, but not all. To see all detailed information, use -Verbose and/or -DebugScript parameters.
    [Parameter(
                Position = 4,
                Mandatory = $false
                )]
    [switch]
    $Info,

    # Make a custom wait after server response. The default is to wait for 3 seconds.
    # WARNING: This is an experimental feature, thi may be not fully implemented or not stable. To use this feature, use with '-Experimental' parameter.
    [Parameter(
                Position = 5,
                Mandatory = $false
                )]
    [int]
    $Wait = 3
)

# Version info:
$__ScriptVersionNumber__ = @{
    "Major"     = 1;
    "Minor"     = 0;
    "Revision"  = 2
}

#
# Constants:
#
[bool]$DEBUG_SCRIPT = $false
[bool]$DEV_MODE = $false
[int]$DEFAULT_CONNECTIONS_TRIES = 10

#
# Control Variables:
#

[bool]$hasAdminRights = $false
[bool]$isTestMode = $false
[bool]$isDebugMode = $false
[bool]$isExperimentalMode = $false

#
# Script Global Variables:
#

$WorldTimeApiUrl = "worldtimeapi.org"
$UtcUrlPart = "/api/timezone/Etc/UTC"

#
# Script Classes:
#

class HttpResponseData
{
    [int]$status
    [bool]$hasDatetime
    [System.DateTime]$dt
    [int]$httpCode
    [string]$httpDescription
    [string]$jsonContent

    HttpResponseData()
    {
        $this.status = -2
        $this.hasDatetime = $false
        $this.httpCode = 0
        $this.httpDescription = ""
    }

    [void]setStatus ([int]$status)
    {
        $this.status = $status
    }

    [void]setHttpStatusCode ([int]$code)
    {
        $this.httpCode = $code
    }

    [void]setHttpStatusDescription ([string]$description)
    {
        $this.httpDescription = $description
    }

    [void]setDatetime ([System.DateTime]$dt)
    {
        $this.dt = $dt
        $this.hasDatetime = $true
    }

    [void]setResponseContent ([string]$content)
    {
        $this.jsonContent = $content
    }
}

#
# Script Methods:
#

function IsElevated()
{
    $winUsrId = [System.Security.Principal.WindowsIdentity]::GetCurrent()
    $winPrincipal = [System.Security.Principal.WindowsPrincipal]::new($winUsrId)
    return $winPrincipal.IsInRole([System.Security.Principal.WindowsBuiltInRole]::Administrator)
}

function getDateTimeInfo
{
    param
    (
        [Parameter(Position = 0, Mandatory = $true)]
        [string]
        $srvUrl,
        
        [Parameter(Position = 1, Mandatory = $true)]
        [string]
        $localUrl
    )

    $finalUrl = $srvUrl+$localUrl
    $status = -1
    $description = ""
    $resp = [HttpResponseData]::new()

    try
    {
        $request = Invoke-WebRequest -Uri $finalUrl -ConnectionTimeoutSeconds 30
        $convertedJson = ConvertFrom-Json $request

        $utcDt = ($convertedJson.utc_datetime).ToUniversalTime()

        if ($request.StatusCode -eq 200)
        {
            $status = 0
            $description = "Ok"
        }
        elseif ($request.StatusCode -ge 100 -and $request.StatusCode -lt 200)
        {
            $status = 1
            $description = "Info"
        }
        elseif ($request.StatusCode -gt 200 -and $request.StatusCode -lt 300)
        {
            $status = 2
            $description = "Success"
        }
        elseif ($request.StatusCode -ge 300 -and $request.StatusCode -lt 400)
        {
            $status = 3
            $description = "Redirected"
        }
        elseif ($request.StatusCode -ge 400 -and $request.StatusCode -lt 500)
        {
            $status = 4
            $description = "Client Error"
        }
        else
        {
            $status = 5
            $description = "Server Error"
        }
        
        $resp.setDatetime($utcDt)
        $resp.setHttpStatusCode($request.StatusCode)
        #$resp.setHttpStatusDescription($request.StatusDescription)
        $resp.setResponseContent($request.Content)
    }
    catch
    {
        $status = 6
        $description = "Unknown"
    }
    finally
    {
        $resp.setStatus($status)
        $resp.setHttpStatusDescription($description)
    }

    return $resp
}

function PrintPresentation([bool]$addLine = $false)
{
    $presentation = "Windows Date Time Sync - $($__ScriptVersionNumber__["Major"]).$($__ScriptVersionNumber__["Minor"]).$($__ScriptVersionNumber__["Revision"])"
    if ($isExperimentalMode)
    {
        $presentation += " | EXPERIMENTAL MODE"
    }
    Write-Host -Object $presentation
    if ($addLine)
    {
        $terminal_columns = [System.Console]::BufferWidth
        $line = ""
        for ($i = 0; $i -lt $terminal_columns; $i++)
        {
            $line += '-'
        }
        Write-Host -Object $line
    }
}

#
# Script start here:
#

# Check the cli and apply the control variables:

$hasAdminRights = IsElevated

if ($Test -or $DEV_MODE)
{
    $isTestMode = $true
}

if ($DebugScript -or $DEBUG_SCRIPT -or $DEV_MODE)
{
    $isDebugMode = $true
}

if (-not $hasAdminRights -and -not $Test)
{
    $isTestMode = $true
}

if ($Experimental)
{
    if ($DEV_MODE)
    {
        $isDebugMode = $true    # Force the debug mode when the script is in DevMode
    }
    $isExperimentalMode = $true
}

# Check if custom connection tries uses a compatible value:
if ($Tries -lt 1)
{
    if ($Info -or $VerbosePreference)
    {
        Write-Host -Object "Invalid argument value on `"Tries`" parameter." -ForegroundColor Red
        if ($Tries -lt 0)
        {
            Write-Host -Object "Parameter `"Tries`" must receive a positive value! Using default value." -ForegroundColor White -BackgroundColor Red
        }
    }
    exit 8 # Invalid argument value in CLI
}

# Check for experimental features:
if ($isExperimentalMode)
{
}

# Verify platform:
# Check the PSVersionTable first, to avoid incompatibility with $IsWindows variable:
if ($PSVersionTable.PSVersion.Major -gt 5)
{
    if (-not $IsWindows -and -not $isDebugMode)
    {
        Write-Error -Message "Current platform is not supported!`nTo test this script in other systems, use -test parameter."
        exit 5 # Platform incompatible
    }
}

#
# Main Script:
#

PrintPresentation($true)

[int]$i = 1
[int]$iMax = $DEFAULT_CONNECTIONS_TRIES
[bool]$successOp = $false
[int]$sleepTimer = 3

if ($Tries -ne $DEFAULT_CONNECTIONS_TRIES)
{
    $iMax = $Tries
}

while ($i -le $iMax -and -not $successOp)
{
    # Get the response data from the server and convert it to HttpResponseData object:
    [HttpResponseData]$respData = getDateTimeInfo -srvUrl $WorldTimeApiUrl -localUrl $UtcUrlPart
    if ($respData.status -eq 0)
    {
        Write-Host -Object "Response at trying ($($i)/$($iMax))`nStatus: $($respData.status) Description: $($respData.httpDescription)"
        $successOp = $true
        if ($isDebugMode)
        {
            Write-Output $respData.jsonContent
        }
    }
    else
    {
        if ($i -eq 1)
        {
            Write-Host -Object "Trying connection... ($($i)/$($iMax))`nStatus: $($respData.status) Description: $($respData.httpDescription)"
        }
        else
        {
            Write-Host -Object "Retrying connection... ($($i)/$($iMax))`nStatus: $($respData.status) Description: $($respData.httpDescription)"
        }
    }
    $i++
    Wait-Event -Timeout $sleepTimer
}

# Report the not successful operation:
if (-not $successOp -and $respData.status -ne 6)
{
    Write-Host -Object "Fail to get the time information from server!"
    if ($info -or $VerbosePreference)
    {
        Write-Host -Object "Error: $($respData.status) | Description: $($respData.httpDescription)"
    }
    exit 4 # Fail to get server info, but successfully processed the getDateTimeInfo method
}

# On successful operation, apply the correct date and time:
if ($successOp -and $respData.hasDatetime)
{
    # Get the local timezone:
    $localTz = [System.TimeZoneInfo]::Local

    if ($isDebugMode -or $VerbosePreference)
    {
        Write-Host -Object "UTC server time: $($respData.dt)"
        Write-Host -Object "Local time: $(Get-Date)"
        Write-Host -Object "System timezone configuration: UTC$($localTz.BaseUtcOffset.Hours):$($localTz.BaseUtcOffset.Minutes)"
    }

    $dtFix = $respData.dt + $localTz.BaseUtcOffset

    if ($isDebugMode -or $Info)
    {
        Write-Host -Object "Setting new system date and time to $($dtFix)"
    }

    if (-not $isTestMode -and $hasAdminRights)
    {
        try
        {
            Set-Date $dtFix
            Write-Host -Object "System's clock defined to $($dtFix) with success!" -ForegroundColor Green
        }
        catch
        {
            Write-Host -Object "Fail to define the system's clock" -ForegroundColor Red
            exit 3 # PowerShell script failed to set the date
        }
    }

    exit 0 # No exception or fail was detected
}

exit 2 # Script reached maximum of tries to get the server information, but no response was sent