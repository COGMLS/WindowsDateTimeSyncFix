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

## Implementations under development:

- Add comments and documentation

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
| 6 | Calling PowerShell may throw an exception that leads to ***error 7***, with description: *FileNotFoundError: [Errno 2] No such file or directory: 'powershell -File "...\tmp353q0dm6.ps1"'* | In the previous version **0.6.0** no exception was detected | Not fixed |

## Deprecated Features:

| Feature | Details | Workaround | Notes |
| :------ | :-----: | :--------: | ----: |

## Removed Features:

| Feature | Details | Workaround | Notes |
| :------ | :-----: | :--------: | ----: |