# Windows Date Time Fix: Project Information

## Recent Implementations:

- Server communication and get date and time information
- Treat UTC date and time format to local time
- Main entry for python script
- Test python version before start the script
- Command line options
- Script return codes
- Test Windows version before start script
- Test PowerShell version before start script
- Experimental feature control
- PowerShell command to change the system date and time
- `DEBUG_MODE` and `DEV_MODE` variables are disabled and allows the script to apply the date and time (To test the script, use parameter `-test`)
- Add comments and documentation

## Implementations under development:


## Future Implementations:

- Test for administrator rights

## Known Bugs:

| Bug ID | Details | Notes/Workaround | Status |
| :----- | :-----: | :--------------: | -----: |
| 1 | Print help get stuck on loop | N/A | **FIXED** |
| 2 | Using `-test` parameter result in undeclared variable | N/A | **FIXED** |
| 3 | On Windows platform the timezone information is not receiving the offset, but it's location or name. | **NOTE:** This part of the code was created and tested on Linux first and the information return is a string value of UTC offset | **FIXED** |
| 4 | PowerShell is called without admin privileges | **NOTE:** Calling with `os.system()` does not keep the privileges. | **FIXED** |
| 5 | PowerShell can't open temporary script |  | **FIXED** |
| 6 | Calling PowerShell may throw an exception that leads to ***error 7***, with description: *FileNotFoundError: [Errno 2] No such file or directory: 'powershell -File "...\tmp353q0dm6.ps1"'* | **NOTE:** In the previous version **0.6.0** no exception was detected **NOTE 2:** This behavior is only affects PowerShell when try to run the script on *Linux* platforms. **TO WINDOWS USERS (WHICH IS SCRIPT FOCUS) NO WORKAROUND IS NECESSARY** | **FIXED** |
| 7 | After complete the PowerShell script execution, Python 3.13 show a `http.client` module exception. <details><summary><strong>Exception details</strong></summary><br>Exception ignored in: <http.client.HTTPResponse object at 0x000001658F2A91B0><br>Traceback (most recent call last):<br>  File "...\Lib\http\client.py", line 432, in close<br>  File "...\Lib\http\client.py", line 445, in flush<br>ValueError: I/O operation on closed file.</details> | This behavior does not prevent the script to work and apply the correct date and time on Windows | Not fixed |

## Deprecated Features:

| Feature | Details | Workaround | Notes |
| :------ | :-----: | :--------: | ----: |

## Removed Features:

| Feature | Details | Workaround | Notes |
| :------ | :-----: | :--------: | ----: |