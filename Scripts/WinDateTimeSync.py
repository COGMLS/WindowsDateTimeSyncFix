import http.client
import json
import datetime
import os
import sys
import copy
import time
import tempfile

# Version info:
__ScriptVersionNumber__ = {
        "Major"     :   0,
        "Minor"     :   4,
        "Revision"  :   0
    }

DEBUG_SCRIPT = True

# Verify Python version:
if (sys.version_info.major < 3) or (sys.version_info.major >= 3 and sys.version_info.minor < 6):
    print("This script can only work on Python 3.6 or more recently")
    sys.exit(1) # Incompatible version
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
        client.close()

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

    respInfo.setStatus(status)
    
    return respInfo

i = 1
iMax = 10
successOp = False
sleepTimer = 3

# The server has a difficulty to make the connection, probably will need multiple tries:
while i <= iMax and successOp != True:
    # Use the response data object to get the method's status and the server http code and response:
    respData = getDateTimeInfo(WorldTimeApiUrl, UtcUrlPart)
    if respData.getStatus() == 0:
        print(f"Response at trying ({i}/{iMax})\nStatus: {respData.getStatus()} Reason: {respData.getReason()}")
        successOp = True
        data = respData.getResponseData()
        if DEBUG_SCRIPT:
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

if successOp:
    # Create a JSON object from server response
    dtJson = json.loads(respData.getResponseData())

    if DEBUG_SCRIPT:
        print(dtJson)
        pass

    utcDt = str(dtJson["utc_datetime"])

    # Get (converting from str) the ISO format of datetime from UTC json data
    # Use the timezone info from local configuration to get the numeric difference
    # Use the timezone to create the delta that will be used to calculate the correct local time

    dt = datetime.datetime.fromisoformat(utcDt)
    now = datetime.datetime.now().astimezone()
    tzDiff = int(str(now.timetz().tzinfo))
    delta = datetime.timedelta(0, 0, 0, 0, 0, tzDiff, 0)

    if DEBUG_SCRIPT:
        print(dt)
        print(now)
        print(tzDiff)
        pass

    # Sum the datetime with delta to find the correct local time
    dtFix = str(dt + delta)

    if DEBUG_SCRIPT:
        print(str(dtFix))
        pass

    # Copy only the date and time and replace it's separators to comma to use as parameters:
    dateInfo = strncpy(dtFix, 0, 10).replace('-', ',')
    timeInfo = strncpy(dtFix, 11, 8).replace(':', ',')

    if DEBUG_SCRIPT:
        print(dateInfo)
        print(timeInfo)
        pass

    # PowerShell Script lines to write into a temporary file and execute
    pwshScript = [
        "#Require -Version 5.0",
        "Write-Host -Object \"`nSetting correct date and time on Windows Clock...`n\"",
        f"$datetime = [System.DateTime]::new({dateInfo},{timeInfo})",
        "try",
        "{",
        "    #Set-Date -Date $datetime",
        "    Write-Host -Object \"Windows clock set to:\"",
        "    Write-Output $datetime",
        "    return 0",
        "}",
        "catch",
        "{",
        "    Write-Host -Object \"Fail to set the Windows Clock\" -Foreground Red",
        "    Write-Host -Object \"No modification was made into your system\"",
        "    return 1",
        "}",
    ]

    # Write the temporary file and generate a PowerShell script:
    with tempfile.NamedTemporaryFile("w", suffix=".tmp", delete=False) as tmpScript:
        for l in pwshScript:
            tmpScript.write(f"{l}\n")
            pass
    
    tmpScript.close()

    # PowerShell command:
    pwshCmd = f"powershell -File \"{tmpScript.name}\""

    if DEBUG_SCRIPT:
        print(pwshCmd)
        pass
    
    scriptReturn = os.system(pwshCmd)

    if DEBUG_SCRIPT:
        print(f"PowerShell Return: {scriptReturn}")
        pass
    pass