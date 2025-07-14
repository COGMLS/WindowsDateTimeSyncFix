import http.client
import json
import datetime
import os
import sys
import copy
import time
import tempfile
import platform
import subprocess

# Version info:
__ScriptVersionNumber__ = {
        "Major"     :   0,
        "Minor"     :   7,
        "Revision"  :   1
    }

# Constants:
DEBUG_SCRIPT = False # Debug Mode
DEV_MODE = True
DEFAULT_CONNECTION_TRIES = 10

# Control Variables:
bDebugScript = DEBUG_SCRIPT
bExperimentalMode = False
bIsHelpCli = False
bIsTestScript = False
bIsUnknownCli = False
bIgnoreMinWinVer = False
bUsingCustomTries = False
iPwshType = 0   # 0: Windows PowerShell, 1: PowerShell

# Other variables:
nSrvTries = DEFAULT_CONNECTION_TRIES

# Help command line:
helpCmd = ["-help","-h","-?"]

# Help CLI info:
help_cli = [
    "\t-help -h -?          Access the command line help",
    "\t-test                Use the script without apply modification on your system",
    "\t-debug               Enable the script debug mode, showing processed data and status code",
    "\t-tries=<value>       Set a custom number of tries to connect with server (Default is 10)",
    "\t                         NOTE: Any value set value below than one will return an error 8.",
    "\t-pwsh                Force to use PowerShell and not Windows PowerShell",
    "\t--experimental       Enable the script experimental features",
    "\t--bypass-win-ver     Bypass Windows minimum version to execute the script",
    "\t                         NOTE: This may lead to unexpected behavior!"
]

# Help arrays index:
help_arrays = [helpCmd, help_cli]

# Check for debug, experimental and test parameters:
for arg in sys.argv:
    if arg.lower() == "--debugscript" or arg.lower() == "-debug":
        bDebugScript = True
        pass
    if arg.lower() == "--experimental":
        bExperimentalMode = True
        pass
    if arg.lower() == helpCmd[0] or arg.lower() == helpCmd[1] or arg.lower() == helpCmd[2]:
        bIsHelpCli = True
        pass
    if arg.lower() == "-test":
        bIsTestScript = True
        pass
    if arg.lower() == "--bypass-win-ver":
        bIgnoreMinWinVer = True
        pass
    pass

# Experimental CLI options:
if bExperimentalMode:
    for arg in sys.argv:
        # Check if custom connection tries are enabled:
        if arg.lower().startswith("-tries="):
            argVal = arg.removeprefix("-tries=")
            if len(argVal) > 0:
                try:
                    nSrvTries = int(argVal)
                except:
                    sys.exit(8) # Invalid argument value on CLI
                pass
            pass
        # Check for PowerShell type argument:
        if arg.lower() == "-pwsh":
            iPwshType = 1
            pass
        pass
    pass

# Verify Python version:
if (sys.version_info.major < 3) or (sys.version_info.major >= 3 and sys.version_info.minor < 6):
    print("This script can only work on Python 3.6 or more recently")
    sys.exit(1) # Incompatible version
    pass

# Verify platform:
if sys.platform != 'win32' and not bIsTestScript and not DEV_MODE:
    print("Current platform is not supported!\nTo test this script in other systems, use -test parameter.")
    sys.exit(5) # Incompatible platform
    pass

# Verify Windows version:
if sys.platform == 'win32':
    win32Ver = platform.win32_ver()
    win_build = int(win32Ver[1].split('.')[2])
    if win_build < 10240 and not bIgnoreMinWinVer:
        sys.exit(6) # Minimum Windows version is Windows 10 (10.0.10240)
        pass
    pass

#
# Script global variables:
#

WorldTimeApiUrl = "worldtimeapi.org"
UtcUrlPart = "/api/timezone/Etc/UTC"

#
# Script classes:
#

class HttpResponseData:
    """
    Http Response Data class
    ---------------

    The HttpResponseData provide multiple information about
    the internal method 'getDateTimeInfo' including the HttpResponse,
    but not limit to, offering additional information about
    internal method behavior and the internal HttpResponse data
    and Http status code.
    """
    _status: int
    _response: http.client.HTTPResponse
    _hasResponse: bool
    _response_data: bytes
    _http_code: int

    def __init__(self):
        self._status = -2
        self._http_code = 0
        self._response_data = 0x0
        self._hasResponse = False
        pass

    def setStatus(self, status: int) -> None:
        self._status = copy.copy(status)
        pass

    def setResponse(self, response: http.client.HTTPResponse) -> None:
        self._hasResponse = True
        self._response = copy.copy(response)
        self._http_code = response.status
        self._response_data = response.read()   # During the response copy the response data is lost. Read it and save inside a separated variable
        pass

    def getStatus(self) -> int:
        return self._status
    
    def getReason(self) -> str:
        if self._hasResponse:
            return self.getResponse().reason
        else:
            return "Unknown"
    
    def getResponse(self) -> int | http.client.HTTPResponse:
        if self._hasResponse:
            return self._response
        else:
            return 0
    
    def getHttpStatus(self) -> int:
        return self._http_code
        
    def getResponseData(self) -> bytes:
        return self._response_data

#
# Script functions:
#

# Script Presentation:
# Function to present script's information to user, including version, release date.
# Parameters:
#   addLine: If TRUE, will add a line after the presentation
def PrintScriptPresentation(addLine: bool = False) -> None:
    global bExperimentalMode
    presentation = f"Windows Date Time Sync - {__ScriptVersionNumber__['Major']}.{__ScriptVersionNumber__['Minor']}.{__ScriptVersionNumber__['Revision']}"
    if bExperimentalMode:
        presentation += " | EXPERIMENTAL MODE"
        pass
    print(presentation)
    if addLine:
        terminal_columns = os.get_terminal_size().columns
        line = ""
        i = 0
        while i < terminal_columns:
            line += '-'
            i = i + 1
            pass
        print(line)
        pass
    pass

# Print the help command, based on help array index:
# Parameters:
#   printHelpArr: Select the detailed help array information
def PrintHelp(printHelpArr: int) -> None:
    global help_arrays
    if printHelpArr < 0 or printHelpArr >= len(help_arrays):
        print(f"[ERROR]::PrintHelp method received an unrecognizable help array! | Argument value: {printHelpArr}")
        pass
    if printHelpArr == 0:
        PrintScriptPresentation(True)
        i = 0
        iMax = len(helpCmd)
        help_str = ""
        while i < iMax:
            if i + 1 < iMax:
                help_str += f"{helpCmd[i]} "
                pass
            else:
                help_str += f"{helpCmd[i]}"
                pass
            i = i + 1
            pass
        help_str += "\tPrint the help information"
        print(help_str)
        pass
    i = 0
    iMax = len(help_arrays[printHelpArr])
    while i < iMax:
        print(help_arrays[printHelpArr][i])
        i = i + 1
        pass
    pass

def strncpy (string: str, start: int = 0, count: int = -1) -> str:
    """
    String N copy
    ===============

    Based on C strncpy method, this function copies the n elements.
    This function also has support to start from a specific index.

    Parameters
    ---------------
    
    string: The source string to make your copy

    start: Index start position. Must be zero or less than string source length

    count: Number of elements you want to copy. If the count is less or greater
    than zero, all elements will be copied

    Exceptions
    ---------------
    
    An exception is raised when start is greater than zero, resulting in
    a message 'Start index out of string limits'

    An exception is raised when start is less than zero, resulting in a
    message 'Start index can not be less than zero'
    """
    
    tmp = ""
    STR_SIZE = len(string)

    if start > STR_SIZE:
        raise Exception("Start index out of string limits")
    if start < 0:
        raise Exception("Start index can not be less than zero")

    if count < 0:
        count = len(string)
        pass
    if count > STR_SIZE:
        count = STR_SIZE
        pass

    i = start
    iMax = start + count - 1

    while i <= iMax and i <= STR_SIZE:
        tmp += string[i]
        i = i + 1
        pass

    return tmp

def getDateTimeInfo(srvUrl: str, localUrl: str) -> HttpResponseData:
    """
    Get the date and time information from server
    =============================================

    This method offer a https connection to a server
    and return the response (if not fail the server connection)
    and the internal method behavior, like if an exception
    occurred.

    Parameters
    ---------------------------------------------

    srvUrl: Server base URL

    localUrl: relative URL to use based on server URL

    Return
    ---------------------------------------------

    This method return an object of 'HttpResponseData',
    that includes the internal method status and, if not
    fail to acquire, the HttpResponse and it's internal
    content and status code.
    """
    status = -1
    respInfo = HttpResponseData()
    try:
        client = http.client.HTTPSConnection(srvUrl, timeout=30)
        client.request("GET", localUrl)
        resp = client.getresponse()
        respInfo.setResponse(resp)

        if resp.status == 200:
            status = 0
            pass
        elif resp.status > 200 and resp.status < 300:
            status = 1
            pass
        elif resp.status >= 300 and resp.status < 400:
            status = 2
            pass
        elif resp.status >= 400 and resp.status < 500:
            status = 3
            pass
        else:
            status = 4
            pass

    except:
        status = 5
    finally:
        client.close()

    respInfo.setStatus(status)
    
    return respInfo

#
# Script main entry:
#

if __name__ == "__main__":
    # Check for help command:
    if bIsHelpCli:
        PrintScriptPresentation(True)
        PrintHelp(1)
        sys.exit(0)
        pass

    # Show the script presentation and start the script components:

    PrintScriptPresentation(True)

    i = 1
    iMax = DEFAULT_CONNECTION_TRIES
    successOp = False
    sleepTimer = 3

    if bUsingCustomTries and bExperimentalMode:
        iMax = nSrvTries
        pass

    # The server has a difficulty to make the connection, probably will need multiple tries:
    while i <= iMax and successOp != True:
        # Use the response data object to get the method's status and the server http code and response:
        respData = getDateTimeInfo(WorldTimeApiUrl, UtcUrlPart)
        if respData.getStatus() == 0:
            print(f"Response at trying ({i}/{iMax})\nStatus: {respData.getStatus()} Reason: {respData.getReason()}")
            successOp = True
            data = respData.getResponseData()
            if bDebugScript:
                print(data)
                pass
            break
            pass
        else:
            print(f"Retrying... ({i}/{iMax})\nStatus: {respData.getStatus()} Reason: {respData.getReason()}")
            pass
        i = i + 1
        # Wait before another trying
        time.sleep(sleepTimer)
        pass

    # Report the not successful operation:
    if not successOp and respData.getStatus() != 5:
        print("Fail to get the time information from server!")
        print(f"Error: {respData.getHttpStatus()} | Reason: {respData.getReason()}")
        sys.exit(4) # Fail to get server info, but successful processed the getDateTimeInfo method
        pass

    # On successful operation, proceed to response data conversion and time fix:
    if successOp:
        # Create a JSON object from server response
        dtJson = json.loads(respData.getResponseData())

        if bDebugScript:
            print(dtJson)
            pass

        utcDt = str(dtJson["utc_datetime"])

        # Get (converting from str) the ISO format of datetime from UTC json data
        # Use the timezone info from local configuration to get the numeric difference
        # Use the timezone to create the delta that will be used to calculate the correct local time

        dt = datetime.datetime.fromisoformat(utcDt)
        now = datetime.datetime.now()
        now_localtime = time.localtime()
        local_tzinfo = now_localtime.tm_gmtoff / 3600 # Convert seconds to hours
        tzDiff = int(local_tzinfo) # Convert the float values to integers
        delta = datetime.timedelta(0, 0, 0, 0, 0, tzDiff, 0)

        if bDebugScript:
            print(f"UTC server time: {dt}")
            print(f"Local time: {now}")
            print(f"System timezone configuration: UTC{tzDiff}:00")
            pass

        # Sum the datetime with delta to find the correct local time
        dtFix = str(dt + delta)

        if bDebugScript:
            print(f"Setting new system date and time to {dtFix}")
            pass

        # Copy only the date and time and replace it's separators to comma to use as parameters:
        dateInfo = strncpy(dtFix, 0, 10).replace('-', ',')
        timeInfo = strncpy(dtFix, 11, 8).replace(':', ',')

        if bDebugScript:
            print(dateInfo)
            print(timeInfo)
            pass

        # PowerShell Script lines to write into a temporary file and execute
        if DEV_MODE:
            bIsTestScript = True
            pass

        pwshScript = [
            "#Requires -Version 4.0",
            "#Requires -RunAsAdministrator",
            f"[bool]$DebugMode = ${bDebugScript}",
            f"[bool]$TestScript = ${bIsTestScript}",
            "Write-Host -Object \"`nSetting correct date and time on Windows Clock...`n\"",
            f"$datetime = [System.DateTime]::new({dateInfo},{timeInfo})",
            "try",
            "{",
            "    if ($TestScript)",
            "    {",
            "        Write-Warning -Message \"Script is in Test Mode. No modification will be applied!\"",
            "    }",
            "    else",
            "    {",
            "        Set-Date -Date $datetime",
            "    }",
            "    Write-Host -Object \"Windows clock set to:\"",
            "    Write-Output $datetime",
            "   if ($DebugMode)",
            "   {",
            "       Write-Host -Object \"[DEBUG]::PowerShell error code: \" -NoNewLine",
            "       return 0",
            "   }",
            "    exit 0",
            "}",
            "catch",
            "{",
            "    Write-Host -Object \"Fail to set the Windows Clock\" -Foreground Red",
            "    Write-Host -Object \"No modification was made into your system\"",
            "   if ($DebugMode)",
            "   {",
            "       Write-Host -Object \"[DEBUG]::PowerShell error code: \" -NoNewLine",
            "       return 1",
            "   }",
            "    exit 1",
            "}",
        ]

        # Write the temporary file and generate a PowerShell script:
        with tempfile.NamedTemporaryFile("w", suffix=".ps1", delete=False) as tmpScript:
            for l in pwshScript:
                tmpScript.write(f"{l}\n")
                pass
        
        tmpScript.close()

        # PowerShell command:
        pwshExec = "powershell"

        if iPwshType == 1:
            pwshExec = "pwsh"
            pass

        pwshCmd = f"{pwshExec} -File \"{tmpScript.name}\""

        if not os.path.exists(tmpScript.name):
            sys.exit(9) # Fail to save script file
            pass

        if bDebugScript:
            print(pwshCmd)
            pass
        
        try:
            scriptReturn = subprocess.run(pwshCmd)
            if bDebugScript:
                print(f"PowerShell Return: {scriptReturn.returncode}")
                pass
            if scriptReturn.returncode == 1:
                sys.exit(3) # PowerShell script failed to set the date
                pass
        except:
            sys.exit(7) # Exception on calling PowerShell

        sys.exit(0) # No exception or fail was detected
        pass
    else:
        sys.exit(2) # Script reached maximum of tries to get the server information, but no response was send
        pass
    pass