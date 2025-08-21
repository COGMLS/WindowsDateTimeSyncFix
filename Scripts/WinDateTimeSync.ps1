<##########################################################
 # Windows Date and Time Sync script for PowerShell
 # ---------------------------------------------------
 # Author: Matheus Lopes Silvati
 # Date: 2025/07/24
 # ------------------------------------
 # Version: 0.8.0
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
.NOTES
    To make possible the Windows Clock fixed, you must execute the script as Administrator.
    Otherwise it only will show the correct date and time from internet.

    The connection with the server may need multiple tries.

    This script does not send any data to the internet. Only receive the correct date and time
    information.

    This script was not supported in Linux.
.LINK
    Repository link: https://github.com/COGMLS/WindowsDateTimeSyncFix
.EXAMPLE
    Test-MyTestFunction -Verbose
    Explanation of the function or its result. You can include multiple examples with additional .EXAMPLE lines
#>

#Requires -Version 4.0

[CmdletBinding()]
param
(
    # Use the script without apply modification on your system.
    # If the script is not been execute with Administrator Rights, the TestMode will be applied automatically.
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
    [uint]
    $tries = 10,

    # Enable the script experimental features
    [Parameter(
                Position = 3,
                Mandatory = $false
                )]
    [switch]
    $experimental
)

# Version info:
$__ScriptVersionNumber__ = @{
    "Major"     = 0;
    "Minor"     = 8;
    "Revision"  = 0
}

#
# Constants:
#
[bool]$DEBUG_SCRIPT = $true
[bool]$DEV_MODE = $true
[uint]$DEFAULT_CONNECTIONS_TRIES = 10

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
    $winUsrId = [System.Security.WindowsIdentity]::GetCurrent()
    $winPrincipal = [System.Security.WindowsPrincipal]::new($winUsrId)
    return $winPrincipal.IsInRole([System.Security.WindowsBuiltInRole]::Administrator)
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
    $resp = [HttpResponseData]::new()

    try
    {
        $request = Invoke-WebRequest -Uri $finalUrl -ConnectionTimeoutSeconds 30
        $convertedJson = ConvertFrom-Json $request

        $utcDt = ($convertedJson.utc_datetime).ToUniversalTime()

        if ($request.StatusCode -eq 200)
        {
            $status = 0
        }
        elseif ($request.StatusCode -gt 200 -and $request.StatusCode -lt 300)
        {
            $status = 1
        }
        elseif ($request.StatusCode -ge 300 -and $request.StatusCode -lt 400)
        {
            $status = 2
        }
        elseif ($request.StatusCode -ge 400 -and $request.StatusCode -lt 500)
        {
            $status = 3
        }
        else
        {
            $status = 4
        }
        
        $resp.setDatetime($utcDt)
        $resp.setHttpStatusCode($request.StatusCode)
        $resp.setHttpStatusDescription($request.StatusDescription)
        $resp.setResponseContent($request.Content)
    }
    catch
    {
        $status = 5
        $resp.setHttpStatusDescription("Unknown")
    }
    finally
    {
        $resp.setStatus($status)
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

if ($experimental -and $isDebugMode -and $DEV_MODE)
{
    $isExperimentalMode = $true
}

# Check for experimental features:
if ($isExperimentalMode)
{
    # Check if custom connection tries are enabled:
    if ($tries -lt 1)
    {
        exit 8 # Invalid argument value in CLI
    }
}

# Verify platform:
if (-not $IsWindows -and -not $isDebugMode)
{
    Write-Error -Message "Current platform is not supported!`nTo test this script in other systems, use -test parameter."
    exit 5
}

# Verify Windows version:
if ($IsWindows)
{

}

#
# Main Script:
#

PrintPresentation($true)

[uint]$i = 1
[uint]$iMax = $DEFAULT_CONNECTIONS_TRIES
[bool]$successOp = $false
[int]$sleepTimer = 3

if ($isExperimentalMode)
{
    $iMax = $tries
}

while ($i -le $iMax -and -not $successOp)
{
    # Get the response data from the server and convert it to HttpResponseData object:
    [HttpResponseData]$respData = getDateTimeInfo -srvUrl $WorldTimeApiUrl -localUrl $UtcUrlPart
    if ($respData.status -eq 0)
    {
        Write-Host -Object "Response at trying ($($i)/$($iMax))`nStatus: $($respData.status) Description: $($resp.httpDescription)"
        $successOp = $true
        if ($isDebugMode)
        {
            Write-Output $respData.jsonContent
        }
    }
    else
    {
        Write-Host -Object "Retrying... ($($i)/$($iMax))`nStatus: $($respData.status) Description: $($resp.httpDescription)"
    }
    $i++
    Wait-Event -Timeout $sleepTimer
}

# Report the not successful operation:
if (-not $successOp -and $respData.status -ne 5)
{
    Write-Host -Object "Fail to get the time information from server!"
    Write-Host -Object "Error: $($respData.status) | Description: $($respData.httpDescription)"
    exit 4 # Fail to get server info, but successful processed the getDateTimeInfo method
}

# On successful operation, apply the correct date and time:
if ($successOp -and $respData.hasDatetime)
{
    # Get the local timezone:
    $localTz = [System.TimeZoneInfo]::Local

    if ($isDebugMode)
    {
        Write-Host -Object "UTC server time: $($respData.dt)"
        Write-Host -Object "Local time: $(Get-Date)"
        Write-Host -Object "System timezone configuration: UTC$($localTz.BaseUtcOffset.Hours):$($localTz.BaseUtcOffset.Minutes)"
    }

    $dtFix = $respData.dt + $localTz.BaseUtcOffset

    if ($isDebugMode)
    {
        Write-Host -Object "Setting new system date and time to $($dtFix)"
    }

    if (-not $isTestMode -and $hasAdminRights)
    {
        try
        {
            Set-Date $dtFix
            Write-Host -Object "System's clock defined to $($dtFix) with successful!" -ForegroundColor Green
        }
        catch
        {
            Write-Host -Object "Fail to define the system's clock" -ForegroundColor Red
            exit 3 # PowerShell script failed to set the date
        }
    }

    exit 0 # No exception or fail was detected
}

exit 2 # Script reached maximum of tries to get the server information, but no response was send