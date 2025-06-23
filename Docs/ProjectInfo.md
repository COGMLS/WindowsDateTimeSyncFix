# Windows Date Time Fix: Project Information

## Recent Implementations:

- Server communication and get date and time information
- Treat UTC date and time format to local time
- Main entry for python script
- Test python version before start the script
- Command line options
- Script return codes
- Test Windows version before start script

## Implementations under development:

- PowerShell command to change the system date and time
- Add comments and documentation
- Test PowerShell version before start script
- Experimental feature control

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

## Deprecated Features:

| Feature | Details | Workaround | Notes |
| :------ | :-----: | :--------: | ----: |

## Removed Features:

| Feature | Details | Workaround | Notes |
| :------ | :-----: | :--------: | ----: |